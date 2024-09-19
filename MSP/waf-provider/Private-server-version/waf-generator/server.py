from quart import Quart, jsonify, request
import os
from datetime import datetime
import re
import terraform_generator
import s3_handler
from tf_deploy import terraform_deploy
import asyncio
from typing import Dict, Any
from CommandResult import CommandResult
# import logger

user_command_results = dict()
server = Quart(__name__)
deploy_result, status_code = -1, -1

ip_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
rules_data = None
blocked_ips = []
reasons = []
last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


def handle_customer_request(customer_id):
    global user_command_results
    result = CommandResult(customer_id)
    # Process the command...
    result.set_output(f"Command processed for customer {customer_id}")
    result.set_result("Success")
    user_command_results[customer_id] = result
    return result


def match_regex(string, pattern):
    return bool(re.match(pattern, string))

# for health check
@server.route('/', methods=['GET'])
def health_check():
    return jsonify({"message": "healthy", "status": "success"}), 200

# PUT
@server.route('/v1/waf/rules', methods=['PUT'])
def update_rules():
    if not request.data:
        return jsonify({"message": "No data received", "status": "error"}), 400
    try:
        recv_data = request.get_json()
    except:
        return jsonify({"message": "Error parsing JSON", "status": "error"}), 401

    for key, val in recv_data.items():
        print(key, val)
        if key == 'accountId' and not match_regex(str(val), r'\d{12}') :
            return jsonify({"message": "Error parsing accountid", "status": "error"}), 402
        elif key == 'rulesToUpdate':
            for rules in val:
                if  not all(rule_key in rules for rule_key in ('id', 'action')) or\
                    not match_regex(str(rules['id']), r'0|[1-9]\d*') or\
                    not match_regex(str(rules['action']), r'allow|block|count'):
                        return jsonify({"message": "Error parsing rules", "status": "error"}), 403
    success_responce = {
        "status": "success",

        "data": {
          **recv_data,
          "UpdatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    }

    return jsonify(success_responce), 200

# GET, POST, DELETE(use method POST)
@server.route('/v1/waf/rules', methods=['GET', 'POST'])
async def rule_ip():
    global user_command_results
    global last_updated
    global rules_data
    global task_statuses    

    new_data = None
    task_statuses = {"data": "None", "status": "inprocess"} # initialize task status

    if request.method == 'POST':
        if not await request.get_data():
            return jsonify({"message": "No data received", "status": "error"}), 409
        try:
            new_data = await request.get_json()
        except Exception as e:
            return jsonify({"message": "Error parsing JSON", "error": str(e), "status": "error"}), 410
        
        if new_data:
            try:
                rules_data, user_id = terraform_generator.generate_terraform(new_data)
                sys_status = handle_customer_request(user_id)
                directory = f"/home/ec2-user/customers/{user_id}"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                asyncio.create_task(s3_handler.upload_to_s3_with_content_async("kg-for-test", f"user_data/{user_id}", "generated_json.json", new_data))

                with open(f"{directory}/main.tf", 'w') as file:
                    file.write(rules_data)
                await s3_handler.upload_to_s3_with_content_async("kg-for-test", f"user_data/{user_id}", "main.tf", rules_data)
                
                task = asyncio.create_task(terraform_deploy(user_id, sys_status))

                return jsonify({"message": "server got data", "status": "success"}), 200
            except Exception as e:
                return jsonify({"message": "Error in processing", "error": str(e), "status": "error"}), 416
    elif request.method == 'GET':
        print("rules_data", rules_data)
        return jsonify({"data": rules_data})

@server.route('/v1/waf/rules/response', methods=['GET','POST'])
async def send_response():
    # global sys_status
    global user_command_results
    data = await request.get_json()

    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({
            "success": False,
            "message": "Invalid or missing user_id",
            "data": None,
        }), 400

    try:
        sys_status = user_command_results[user_id]
    except KeyError:
        return jsonify({
            "success": False,
            "message": "User not found",
            "data": None,
        }), 400
    try:
        return jsonify({
            "success": True,
            "message": "Status retrieved successfully",
            "system_status": sys_status.get_output()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to retrieve status: {str(e)}",
            "data": None,
        }), 500


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
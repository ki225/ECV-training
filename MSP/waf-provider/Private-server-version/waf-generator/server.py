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

task_statuses: Dict[str, Any] = {}
status = None
server = Quart(__name__)
deploy_result, status_code = -1, -1


ip_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
rules_data = None
blocked_ips = []
reasons = []
last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

class SystemStatus:
    def __init__(self):
        self.status = None # success or error
        self.message = ""
        self.last_updated = last_updated
    def update_status(self, status, message):
        self.status = status
        self.message = message
    def get_latest_status(self):
        return self.status
    
sys_status = SystemStatus()

# A callback function that updates the task status when the deployment completes or fails.
def update_status(future: asyncio.Future) -> None:
    global task_statuses
    global sys_status
    try:
        print("all the result:", future.result())
        sys_status.update_status("success", future.result()[len(future.result()) - 1])
        result = future.result()[len(future.result()) - 1]
        task_statuses = {"message": result, "status": "success"}
    except Exception as e:
        task_statuses = {"error message": str(e), "status": "error"}
        sys_status.update_status("error", str(e))

# Retrieves the current status of a deployment task.
async def check_deployment_status():
    global task_statuses
    print("checking deployment status", task_statuses)
    return task_statuses

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
    global last_updated
    global rules_data
    global task_statuses
    sys_status1 = CommandResult() # create a new object of CommandResult

    new_data = None
    task_statuses = {"data": "None", "status": "inprocess"} # initialize task status

    if request.method == 'POST':
        if not await request.get_data():
            sys_status1.set_result("No data received")
            return jsonify({"message": "No data received", "status": "error"}), 409
        try:
            new_data = await request.get_json()
        except Exception as e:
            return jsonify({"message": "Error parsing JSON", "error": str(e), "status": "error"}), 410
        
        if new_data:
            try:
                rules_data, user_id = terraform_generator.generate_terraform(new_data)
                directory = f"/home/ec2-user/customers/{user_id}"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                asyncio.create_task(s3_handler.upload_to_s3_with_content_async("kg-for-test", f"user_data/{user_id}", "generated_json.json", new_data))

                with open(f"{directory}/main.tf", 'w') as file:
                    file.write(rules_data)
                await s3_handler.upload_to_s3_with_content_async("kg-for-test", f"user_data/{user_id}", "main.tf", rules_data)
                
                task = asyncio.create_task(terraform_deploy(user_id))
                task.add_done_callback(lambda t: update_status(t))

                return jsonify({"message": "server got data", "status": "success"}), 200
                # return jsonify(deploy_result), status_code
            except Exception as e:
                return jsonify({"message": "Error in processing", "error": str(e), "status": "error"}), 416
    elif request.method == 'GET':
        return jsonify({"data": rules_data})

@server.route('/v1/waf/rules/response', methods=['GET'])
async def send_response():
    try:
        status = await check_deployment_status()
        print(status)
        print(type(status))
        if status.get("status") == "success" or status.get("status") == "inprocess":
            return jsonify({
                "success": True,
                "message": "Status retrieved successfully",
                "data": status
            }), 200
        else:
            return jsonify({
                "success": True,
                "message": "Status retrieved successfully",
                "data": status
            }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to retrieve status: {str(e)}",
            "data": None
        }), 500


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
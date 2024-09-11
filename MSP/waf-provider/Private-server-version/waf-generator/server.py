from quart import Quart, jsonify, request
import os
from datetime import datetime
import re
import terraform_generator
import s3_handler
import tf_deploy
import asyncio


# server = Flask(__name__)
server = Quart(__name__)


ip_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
rules_data = None
blocked_ips = []
reasons = []
last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


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

    # ========================  Validate the data =============================
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
    new_data = None

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
                directory = f"/home/ec2-user/customers/{user_id}"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                await s3_handler.upload_to_s3_with_content_async("kg-for-test", f"user_data/{user_id}", "generated_json.json", new_data)
                
                with open(f"{directory}/main.tf", 'w') as file:
                    file.write(rules_data)
                await s3_handler.upload_to_s3_with_content_async("kg-for-test", f"user_data/{user_id}", "main.tf", rules_data)
                
                deploy_result, status_code = await tf_deploy.run_terraform_deploy(user_id)
                return jsonify(deploy_result), status_code
            except Exception as e:
                return jsonify({"message": "Error in processing", "error": str(e), "status": "error"}), 416
    elif request.method == 'GET':
        return jsonify({"data": rules_data})

# @server.after_serving
# async def shutdown():
#     server.background_task.cancel()
#     try:
#         await server.background_task
#     except asyncio.CancelledError:
#         pass


# @server.after_request
# def add_header(response):
#     response.headers['Access-Control-Allow-Origin'] = 'http://kg-for-test.s3.amazonaws.com'
#     return response

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
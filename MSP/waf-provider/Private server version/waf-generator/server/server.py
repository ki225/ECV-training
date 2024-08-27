from flask import Flask, request, jsonify
import os
from datetime import datetime
import re
import terraform_generator

# =================================== global data ==============================================================
server = Flask(__name__)
ip_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
rules_data = None
blocked_ips = []
reasons = []
last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

# =================================== global function =============================================================
def match_regex(string, pattern):
    return bool(re.match(pattern, string))

# =========================================== REST API handling =====================================================
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
        return jsonify({"message": "Error parsing JSON", "status": "error"}), 400

    # ========================  Validate the data =============================
    
    for key, val in recv_data.items():
        print(key, val)
        if key == 'accountId' and not match_regex(str(val), r'\d{12}') :
            return jsonify({"message": "Error parsing accountid", "status": "error"}), 400

        elif key == 'rulesToUpdate':
            for rules in val:
                if  not all(rule_key in rules for rule_key in ('id', 'action')) or\
                    not match_regex(str(rules['id']), r'0|[1-9]\d*') or\
                    not match_regex(str(rules['action']), r'allow|block|count'):
                        return jsonify({"message": "Error parsing rules", "status": "error"}), 400

    # Successful process
    success_responce = {
        "status": "success",

        "data": {
          **recv_data,
          "UpdatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    }

    return jsonify(success_responce), 200

@server.route('/v1/waf/ip-blocks', methods=['PUT'])
def update_ip():
    # Get the JSON data from the request
    if not request.data:
        return jsonify({"message": "No data received", "status": "error"}), 400

    try:
        recv_data = request.get_json()
    except:
        return jsonify({"message": "Error parsing JSON", "status": "error"}), 400

    # Validate the data
    if not all(key in recv_data for key in ('original', 'ip')):
        return jsonify({"message": "Error parsing data", "status": "error"}), 400

    if not match_regex(str(recv_data['original']), ip_regex):
        return jsonify({"message": "Error parsing original ip", "status": "error"}), 400

    if not match_regex(str(recv_data['ip']), ip_regex):
        return jsonify({"message": "Error parsing updated ip", "status": "error"}), 400

    # Successful process
    success_responce = {
        "status": "success",
        "message": "IP in block list is successfully updated",
        "data": {
          **recv_data,
          "UpdatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    }
    return jsonify(success_responce), 200

# GET, POST, DELETE(use method POST)
@server.route('/v1/waf/rules', methods=['GET', 'POST'])
def rule_ip():
    global last_updated
    global rules_data

    if request.method == 'POST':
        if not request.data:
            return jsonify({"message": "No data received", "status": "error"}), 400
        try:
            new_data = request.get_json()
        except:
            return jsonify({"message": "Error parsing JSON", "status": "error"}), 400

        if new_data:
            #try:
            terraform_generator.generate_terraform(new_data)
            rules_data = new_data
            return jsonify({
                                "status": "success",
                                "data": {
                                    "deployedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                                    }
                                }), 200
            #except:
            #    return jsonify({"message": "Invalid rule format", "status": "error"}), 400

    elif request.method == 'GET':
        return jsonify({"data": rules_data}) # output all we have


@server.route('/v1/waf/ip-blocks', methods=['GET', 'POST'])
def block_ip():
    global last_updated
    if request.method == 'POST':
        # Get the JSON data from the request
        if not request.data:
            return jsonify({"message": "No data received", "status": "error"}), 400

        try:
            new_data = request.get_json()
        except:
            return jsonify({"message": "Error parsing JSON", "status": "error"}), 400

        if 'action' in new_data and 'delete' == new_data['action']:
            # Validate the data
            if 'ip' not in new_data.keys():
                return jsonify({"message": "Missing ip", "status": "error"}), 400

            if not match_regex(str(new_data['ip']), ip_regex):
                return jsonify({"message": "Error parsing ip", "status": "error"}), 400

            # Successful process
            success_responce = {
                "status": "success",
                "message": "IP successfully removed from block list",
                "data": {
                  **new_data,
                  "RemovedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            }

            return jsonify(success_responce), 200

        else:
            if new_data and "ip" in new_data and "reason" in new_data:
                last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                blocked_ips.append(new_data["ip"])
                reasons.append(new_data["reason"])
                return jsonify({
                                "status": "success",
                                "message": "IP successfully added to block list",
                                "data": {
                                        "ip": new_data["ip"],
                                        "reason": new_data["reason"],
                                        "addedAt": last_updated
                                    }
                                }), 200
            elif new_data and "ip" in new_data:
                last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                blocked_ips.append(new_data["ip"])
                return jsonify({
                                "status": "success",
                                "message": "IP successfully added to block list",
                                "data": {
                                        "ip": new_data["ip"],
                                        "addedAt": last_updated
                                    }
                                }), 200
            else:
                return jsonify({"message": "Invalid IP address format", "status": "error"}), 500

    elif request.method == 'GET':
        if reasons:
            return jsonify({
                "status": "success",
                "data": {
                    "blockedIPs": blocked_ips,
                    "reasons": reasons,
                    "lastUpdated": last_updated
                }
            }), 200
        elif blocked_ips: # HTTP methods POST and DELETE should includes ip
            return jsonify({
                "status": "success",
                "data": {
                    "blockedIPs": blocked_ips,
                    "lastUpdated": last_updated
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "data": {
                    "messages": "Failed to retrieve IP block list"
                }
            }), 500

@server.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://kg-bucket.s3-website-us-east-1.amazonaws.com'
    return response

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
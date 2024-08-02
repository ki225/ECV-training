from flask import Flask, request, jsonify
from datetime import datetime


app = Flask(__name__)

data_store = []
blocked_ips = []
reasons = []
last_updated = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


@app.route('/v1/waf/rules', methods=['GET', 'POST'])
def rule_ip():
    global last_updated
    if request.method == 'POST':
        new_data = request.json
        if new_data:
            data_store.append(new_data)
            return jsonify({
                            "status": "success",
                            "data": {
                                "accountId": new_data["accountId"],
                                "rulesToDeploy": new_data["rulesToDeploy"],
                                "deployedAt": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                                }
                            }), 200
        else:
            return jsonify({"message": "Invalid rule format", "status": "error"}), 400

    elif request.method == 'GET':
        return jsonify({"data": data_store})


@app.route('/v1/waf/ip-blocks', methods=['GET', 'POST'])
def block_ip():
    if request.method == 'POST':
        new_data = request.json
        if new_data and "ip" in new_data and "reason" in new_data:
            last_updated = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
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
            last_updated = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

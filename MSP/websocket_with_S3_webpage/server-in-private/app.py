# app.py

from flask import Flask, request
import boto3
import json

app = Flask(__name__)

# Initialize AWS SDK client
apigatewaymanagementapi = None

@app.route('/')
def hello():
    return "Hello, this is your Flask server running on EC2!"

@app.route('/websocket', methods=['POST'])
def handle_websocket():
    global apigatewaymanagementapi
    event = request.json
    
    if apigatewaymanagementapi is None:
        apigatewaymanagementapi = boto3.client('apigatewaymanagementapi',
            endpoint_url = f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}"
        )
    
    connection_id = event['requestContext']['connectionId']
    
    if event['requestContext']['eventType'] == 'CONNECT':
        # Handle new connection
        return {'statusCode': 200, 'body': 'Connected'}
    
    elif event['requestContext']['eventType'] == 'DISCONNECT':
        # Handle disconnection
        return {'statusCode': 200, 'body': 'Disconnected'}
    
    elif event['requestContext']['eventType'] == 'MESSAGE':
        # Handle incoming message
        message = json.loads(event['body'])
        response = f"Server received: {message}"
        
        # Send response back to the client
        apigatewaymanagementapi.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(response)
        )
        
        return {'statusCode': 200, 'body': 'Message sent'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
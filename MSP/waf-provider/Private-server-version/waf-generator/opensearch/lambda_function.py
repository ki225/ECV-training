import json
import os
import re
import uuid
from model import call
from aws_lambda_powertools import Logger, Tracer
from langchain.memory import DynamoDBChatMessageHistory

tracer = Tracer()

def get_session_id():
    return str(uuid.uuid4())  # Generate a new UUID for each invocation


def get_chat_history(session_id):
    return DynamoDBChatMessageHistory(
        table_name="YourDynamoDBTableName",  # Replace with your actual DynamoDB table name
        session_id=session_id
    )

@tracer.capture_lambda_handler 
def lambda_handler(event, context):
    user_id = event.get('user_id', 'default_user')
    session_id = get_session_id()
    chat_history = get_chat_history(session_id)
    user_input = event['input']

    try:
        response = call(chat_history)  
    except Exception as e:
        return {
        "statusCode": 500,
        "body": json.dumps({'response': str(e)}),
        "headers": {
            "Content-Type": "application/json"
        }
    }

    
    return {
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }
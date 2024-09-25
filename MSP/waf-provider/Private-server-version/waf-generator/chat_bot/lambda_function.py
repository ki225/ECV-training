import json
import os
import re

from model import generate_response_from_openai
from ConversationHistoryDB import ConversationHistoryDB
from model import generate_response_from_openai

from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()

fixed_responses = {
    '1': "This is the response for input 1.",
    '2': "This is the response for input 2.",
    '3': "This is the response for input 3.",
    '4': "This is the response for input 4."
}

db = ConversationHistoryDB()

@tracer.capture_lambda_handler 
def lambda_handler(event, context):
    user_id = event.get('user_id', 'default_user')
    history = db.get_conversation_history(user_id)

    user_input = event['input']

    if user_input in fixed_responses:
        response = fixed_responses[user_input]
    else:
        try:
            response = generate_response_from_openai(user_input, "professionalism", None, history)            
        except Exception as e:
            return {
            "statusCode": 500,
            "body": json.dumps({'response': str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    
    db.store_message(user_id, "user", user_input)
    db.store_message(user_id, "assistant", response)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }
    
    
    
    
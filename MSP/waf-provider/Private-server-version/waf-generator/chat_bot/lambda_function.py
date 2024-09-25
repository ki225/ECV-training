import json
import os
import re

from model import generate_response_from_openai
from rule_retriever import rule_retriever
from ConversationHistoryDB import ConversationHistoryDB
from cve_retriever import searchCVE
from model import generate_response_from_openai
from cve_query import parse_user_input, searchCVE


fixed_responses = {
    '1': "This is the response for input 1.",
    '2': "This is the response for input 2.",
    '3': "This is the response for input 3.",
    '4': "This is the response for input 4."
}

db = ConversationHistoryDB()

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
            response = f"An error occurred while processing your request: {str(e)}"
            
        except Exception as e:
            return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e),'response': "cannot get info"}),
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
    
    
    
    
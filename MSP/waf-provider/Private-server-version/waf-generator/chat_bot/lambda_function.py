import json
import os
from model import generate_response_from_openai

fixed_responses = {
    '1': "This is the response for input 1.",
    '2': "This is the response for input 2.",
    '3': "This is the response for input 3.",
    '4': "This is the response for input 4."
}
    


def lambda_handler(event, context):
    body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
    
    # Extract the input
    user_input = body.get('input', '')

    if user_input in fixed_responses:
        response = fixed_responses[user_input]
    else:
        try:
            response = generate_response_from_openai(user_input)
        except Exception as e:
            response = f"An error occurred while processing your request: {str(e)}"
    
    return {
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }
    
    
    
    
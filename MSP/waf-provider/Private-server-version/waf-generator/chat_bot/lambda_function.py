import json
import os
import re
from cve_retriever import searchCVE
from model import generate_response_from_openai
from cve_query import parse_user_input, search_cve, parse_cve_results
from cve_retriever import searchCVE

fixed_responses = {
    '1': "This is the response for input 1.",
    '2': "This is the response for input 2.",
    '3': "This is the response for input 3.",
    '4': "This is the response for input 4."
}

def lambda_handler(event, context):
    user_input = event['input']

    if user_input in fixed_responses:
        response = fixed_responses[user_input]
    elif 'cve' in user_input.lower():
        # try:
        if True:
            params = parse_user_input(user_input)
            results = str(searchCVE(params['cve_id']))
            # results = search_cve(**params)
            # parsed_results = parse_cve_results(results)
            # response = str(results)
            response = generate_response_from_openai(user_input, "cve", results)
            
        # except Exception as e:
        #     return {
        #     "statusCode": 500,
        #     "body": json.dumps({"error": str(e),'response': "cannot get info"}),
        #     "headers": {
        #         "Content-Type": "application/json"
        #     }
        # }
    else:
        try:
            response = generate_response_from_openai(user_input, "professionalism")
        except Exception as e:
            response = f"An error occurred while processing your request: {str(e)}"
    
    
    return {
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }
    
    
    
    
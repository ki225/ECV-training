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
    '4': "This is the response for input 4.",
    'I want to build a waf on alb': "Ok, I get it. Can you please provide the ARN of your resource? This unique identifier is crucial for correctly configuring your WAF. You can find it in the AWS Console under your resource's details. Once you share the ARN, we can proceed with the specific WAF setup.",
    'arn:aws:elasticloadbalancing:us-east-1:533267425888:loadbalancer/app/alb/a7576322d443f617': 
        "Thank you. We can talk about what service you want to protect. Understanding your specific needs will help us tailor the WAF configuration. Are you looking to secure a website, API, or another type of application? Each service may require different WAF rules and settings for optimal protection.",
    'mysql': "For MySQL you just mentioned, I recommend you to use sql-r3. This rule is specifically designed to protect against SQL injection attacks targeting MySQL databases.",
    'generate':"""{
  "Resource": {
    "Type": "alb",
    "Region": "us-east-1",
    "Resource_Arn": "arn:aws:elasticloadbalancing:us-east-1:533267425888:loadbalancer/app/alb/202d1cbeb597f90b",
    "Resource_Id": "",
    "Resource_Name": ""
  },
  "Waf": {
    "Name": "Emergency-WAF",
    "Description": "WAF created for emergency purpose",
    "Inspection": "16KB"
  },
  "Monitor_Settings": {
    "CW_Metric_Name": "Emergency-WAF",
    "Option": "true"
  },
  "Rules": {
    "Rule_Package": {
      "SQLi": {
        "Mode": "default",
        "Set": [
          {
            "Rule_Id": "SQLi-r1",
            "Chosen": false,
            "Action": "Block",
            "Priority": 0
          },
          {
            "Rule_Id": "SQLi-r2",
            "Chosen": false,
            "Action": "Block",
            "Priority": 1
          },
          {
            "Rule_Id": "SQLi-r3",
            "Chosen": true,
            "Action": "Block",
            "Priority": 2
          }
        ]
      },
      "XSS": {
        "Mode": "default",
        "Set": [
          {
            "Rule_Id": "XSS-r1",
            "Chosen": false,
            "Action": "Block",
            "Priority": 3
          },
          {
            "Rule_Id": "XSS-r2",
            "Chosen": false,
            "Action": "Block",
            "Priority": 4
          },
          {
            "Rule_Id": "XSS-r3",
            "Chosen": false,
            "Action": "Block",
            "Priority": 5
          }
        ]
      }
    },
    "Rule_Created": []
  },
  "IP": []
}"""
}


@tracer.capture_lambda_handler 
def lambda_handler(event, context):
    user_id = event.get('user_id', 'default_user')

    user_input = event['input']

    if user_input in fixed_responses:
        response = fixed_responses[user_input]
    else:
        try:
            response = generate_response_from_openai(user_input, "professionalism", None)            
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
    
    
    
    
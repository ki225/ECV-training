import boto3
import json

def rule_retriever(cve_id):
    bucket_name = 'kg-for-test'
    cve_year = cve_id[4:8]
    object_key = f'EmergencyPackage/CVE-{cve_year}.json'
    
    
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)  
        rules = response['Body'].read() 
        decode_str = rules.decode('utf-8')  
        rules = json.loads(decode_str)   
        for rule in rules:
            if rule["Rule_Id"] == cve_id:
                config_str = rule["Rule_Configuration"]
                config_list = config_str.split("\\n")
                return "\n".join(config_list)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

import boto3
import json

s3 = boto3.client('s3')

# pull object from s3
def get_s3_object(bucket_name, object_key):
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    return response['Body'].read()

# Upload variable value to S3 directly
def upload_to_s3_with_content(bucket_name, folder_name, file_name, content):
    if isinstance(content, dict):
        content = json.dumps(content)
    elif isinstance(content, str):
        content = content.encode('utf-8')
    key = f"{folder_name}/{file_name}"
    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=content)
        print(f"Stored {file_name} in s3://{bucket_name}/{key} successfully")
    except Exception as e:
        print(f"An error occurred while storing {file_name} in s3: {str(e)}")

# Upload a file to S3
def upload_to_s3_with_path(file_path, bucket_name, s3_key):
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload to S3: {str(e)}")
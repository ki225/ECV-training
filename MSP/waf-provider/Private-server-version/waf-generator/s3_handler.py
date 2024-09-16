import boto3
import json
import asyncio
import aioboto3
from botocore.exceptions import ClientError
from tf_deploy import check_waf_acl_id

s3 = boto3.client('s3')

# pull object from s3
def get_s3_object(bucket_name, object_key):
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    return response['Body'].read()

# Upload variable value to S3 directly
async def upload_to_s3_with_content_async(bucket_name, folder_name, file_name, content):
    if isinstance(content, dict):
        content = json.dumps(content)
    elif isinstance(content, str):
        content = content.encode('utf-8')
    key = f"{folder_name}/{file_name}"

    async with aioboto3.Session().client('s3') as s3:
        try:
            await s3.put_object(Bucket=bucket_name, Key=key, Body=content)
            print(f"Stored {file_name} in s3://{bucket_name}/{key} successfully")
        except Exception as e:
            print(f"An error occurred while storing {file_name} in s3: {str(e)}")


# Upload a file to S3
async def upload_to_s3_with_path_async(local_file_path, bucket_name, s3_key, timeout=60):
    session = aioboto3.Session()
    async with session.client('s3') as s3:
        try:
            await s3.upload_file(local_file_path, bucket_name, s3_key)
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            raise
    
async def periodic_s3_upload(terraform_dir: str, local_file_path: str, bucket_name: str, s3_key: str, stop_event: asyncio.Event) -> None:
    while True:
        try:
            await upload_to_s3_with_path_async(local_file_path, bucket_name, s3_key)
            print("Uploaded to S3 successfully")
        except Exception as e:
            print(f"Error during periodic S3 upload: {e}")
        waf_created_result = await check_waf_acl_id(terraform_dir, stop_event)
        if waf_created_result:
            stop_event.set()
            break
        await asyncio.sleep(10)
    print("Periodic S3 upload completed")
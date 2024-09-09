import threading
import subprocess
import os
import time
import s3_handler
from datetime import datetime
from flask import jsonify
from tf_output import filter_terraform_output
import re
import sys

def upload_if_changed(output_file, bucket_name, s3_key, last_modified):
    try:
        current_modified = os.path.getmtime(output_file)
        if current_modified != last_modified[0]:
            s3_handler.upload_to_s3_with_path(output_file, bucket_name, s3_key)
            last_modified[0] = current_modified
            print(f"Uploaded {output_file} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error during upload: {str(e)}")

def periodic_upload(output_file, bucket_name, s3_key, stop_event):
    last_modified = [0]  # Using a list to make it mutable within the function
    while not stop_event.is_set():
        if os.path.exists(output_file):
            upload_if_changed(output_file, bucket_name, s3_key, last_modified)
        time.sleep(1)  # Check every second for changes

def run_terraform_deploy(account_id):
    output_file = f"terraform_output_{account_id}.txt"
    filtered_output_file = f"filtered_terraform_output_{account_id}.txt"
    bucket_name = "kg-for-test"
    s3_key = f"user_data/{account_id}/{filtered_output_file}"

    stop_upload = threading.Event()
    upload_thread = threading.Thread(
        target=periodic_upload,
        args=(filtered_output_file, bucket_name, s3_key, stop_upload)
    )
    upload_thread.start()

    try:
        workspace_name = f"customer_{account_id}"
        terraform_dir = f"/home/ec2-user/customers/{account_id}"

        if not os.path.exists(terraform_dir):
            raise FileNotFoundError(f"Terraform directory not found: {terraform_dir}")

        if not os.path.exists(os.path.join(terraform_dir, 'main.tf')):
            raise FileNotFoundError(f"main.tf not found in: {terraform_dir}")

        subprocess.run(["terraform", "-chdir=" + terraform_dir, "workspace", "new", workspace_name], check=False, capture_output=True)
        subprocess.run(["terraform", "-chdir=" + terraform_dir, "workspace", "select", workspace_name], check=True)
        subprocess.run(["terraform", "-chdir=" + terraform_dir, "init"], check=True)

        os.chdir(terraform_dir)
        with open(output_file, 'w') as f, open(filtered_output_file, 'w') as filtered_f:
            process = subprocess.Popen(
                ["terraform", "-chdir=" + terraform_dir, "apply", "-auto-approve", "-verbose"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            output_buffer = ""
            for line in process.stdout:   
                sys.stdout.flush()             
                if account_id in line or not re.search(r'\d{12}', line):
                    f.write(line)
                    f.flush()
                    output_buffer += line
                    current_filtered_output = filter_terraform_output(output_buffer)
                    if current_filtered_output != last_filtered_output:
                        filtered_f.write(current_filtered_output[len(last_filtered_output):])
                        filtered_f.flush()
                        last_filtered_output = current_filtered_output

                    print(f"[Account {account_id}] {line}", end='')
                
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, process.args)
            
        print(f"Terraform apply completed successfully for account {account_id} in workspace: {workspace_name}")

        stop_upload.set()
        upload_thread.join()

        s3_handler.upload_to_s3_with_path(filtered_output_file, bucket_name, s3_key)
        print(f"Filtered Terraform output for account {account_id} uploaded to s3://{bucket_name}/{s3_key}")

        return jsonify({
            "status": "success",
            "data": {
                "deployedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "outputLocation": f"s3://{bucket_name}/{s3_key}"
            }
        }), 200

    except subprocess.CalledProcessError as e:
        stop_upload.set()
        upload_thread.join()
        return jsonify({
            "status": "error",
            "message": f"Terraform command failed for account {account_id}: {str(e)}"
        }), 500
    except Exception as e:
        stop_upload.set()
        upload_thread.join()
        return jsonify({
            "status": "error",
            "message": f"An error occurred for account {account_id}: {str(e)}"
        }), 500
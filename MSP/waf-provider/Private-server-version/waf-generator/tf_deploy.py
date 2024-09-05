import threading
import subprocess
import os
import time
import s3_handler
from datetime import datetime
from flask import jsonify

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

def run_terraform_deploy(user_id):
    output_file = "terraform_output.txt"
    bucket_name = "kg-for-test"
    s3_key = f"user_data/{user_id}/{output_file}"

    stop_upload = threading.Event()
    upload_thread = threading.Thread(
        target=periodic_upload,
        args=(output_file, bucket_name, s3_key, stop_upload)
    )
    upload_thread.start()

    try:
        workspace_name = f"customer_{user_id}"
        terraform_dir = f"/home/ec2-user/customers/{user_id}"

        # Ensure the terraform_dir exists
        if not os.path.exists(terraform_dir):
            raise FileNotFoundError(f"Terraform directory not found: {terraform_dir}")

        # Check if main.tf exists in the specified directory
        if not os.path.exists(os.path.join(terraform_dir, 'main.tf')):
            raise FileNotFoundError(f"main.tf not found in: {terraform_dir}")

        # Create and select workspace
        subprocess.run(["terraform", "-chdir=" + terraform_dir, "workspace", "new", workspace_name], check=False, capture_output=True)
        subprocess.run(["terraform", "-chdir=" + terraform_dir, "workspace", "select", workspace_name], check=True)

        # Initialize Terraform
        subprocess.run(["terraform", "-chdir=" + terraform_dir, "init"], check=True)

        # Apply Terraform configuration
        os.chdir(terraform_dir)
        with open(output_file, 'w') as f:
            process = subprocess.Popen(
                ["terraform", "-chdir=" + terraform_dir, "apply", "-auto-approve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            for line in process.stdout:
                print(line, end='')  # Print to console
                f.write(line)        # Write to file
                f.flush()            # Ensure it's written immediately
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, process.args)
            
        print(f"Terraform apply completed successfully in workspace: {workspace_name}")

        # Stop the upload thread
        stop_upload.set()
        upload_thread.join()

        # Final upload after completion
        s3_handler.upload_to_s3_with_path(output_file, bucket_name, s3_key)
        print(f"Final Terraform output uploaded to s3://{bucket_name}/{s3_key}")

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
            "message": f"Terraform command failed: {str(e)}"
        }), 500
    except Exception as e:
        stop_upload.set()
        upload_thread.join()
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500
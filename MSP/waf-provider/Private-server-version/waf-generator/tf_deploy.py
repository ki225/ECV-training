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
        subprocess.run(["terraform", "init"], check=True)
        with open(output_file, 'w') as f:
            process = subprocess.Popen(
                ["terraform", "apply", "-auto-approve"],
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
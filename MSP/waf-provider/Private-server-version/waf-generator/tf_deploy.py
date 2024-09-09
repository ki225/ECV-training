import subprocess
import os
from flask import jsonify
from datetime import datetime

def run_terraform_command(cmd, output_file, account_id):
    with open(output_file, 'a') as f:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        output = []
        for line in iter(process.stdout.readline, ''):
            f.write(line)
            f.flush()
            output.append(line)
            print(f"[Account {account_id}] {line}", end='', flush=True)
        
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd, ''.join(output))
        return ''.join(output)

def delete_workspace(terraform_dir, workspace_name, output_file, account_id):
    try:
        # 首先切換到默認工作區
        run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "select", "default"],
            output_file,
            account_id
        )
        
        # 然後刪除指定的工作區
        delete_output = run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "delete", workspace_name],
            output_file,
            account_id
        )
        print(f"Workspace deletion output: {delete_output}")
        if f"Deleted workspace \"{workspace_name}\"" in delete_output:
            print(f"Successfully deleted workspace '{workspace_name}'")
            return True
        else:
            print(f"Failed to delete workspace '{workspace_name}'")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error deleting workspace: {e}")
        return False

def ensure_workspace(terraform_dir, workspace_name, output_file, account_id):
    try:
        # 檢查工作區是否存在
        list_output = run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "list"],
            output_file,
            account_id
        )
        if workspace_name in list_output:
            print(f"Workspace '{workspace_name}' exists. Deleting it.")
            if not delete_workspace(terraform_dir, workspace_name, output_file, account_id):
                raise Exception(f"Failed to delete existing workspace '{workspace_name}'")
        
        # 創建新的工作區
        create_output = run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "new", workspace_name],
            output_file,
            account_id
        )
        print(f"Workspace creation output: {create_output}")
        if "Created and switched to workspace" in create_output:
            print(f"Successfully created new workspace '{workspace_name}'")
            return True
        else:
            print(f"Failed to create workspace '{workspace_name}'")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error managing workspace: {e}")
        return False

def run_terraform_deploy(account_id):
    output_file = f"terraform_output_{account_id}.txt"
    bucket_name = "kg-for-test"
    s3_key = f"user_data/{account_id}/{output_file}"

    try:
        workspace_name = f"customer_{account_id}"
        terraform_dir = f"/home/ec2-user/customers/{account_id}"

        if not os.path.exists(terraform_dir):
            raise FileNotFoundError(f"Terraform directory not found: {terraform_dir}")

        if not os.path.exists(os.path.join(terraform_dir, 'main.tf')):
            raise FileNotFoundError(f"main.tf not found in: {terraform_dir}")

        # 確保工作區存在（如果已存在則刪除並重新創建）
        if not ensure_workspace(terraform_dir, workspace_name, output_file, account_id):
            raise Exception("Failed to create workspace")

        # 執行 Terraform 命令
        commands = [
            ["terraform", "-chdir=" + terraform_dir, "init"],
            ["terraform", "-chdir=" + terraform_dir, "apply", "-auto-approve", "-verbose"]
        ]

        for cmd in commands:
            run_terraform_command(cmd, output_file, account_id)

        print(f"Terraform apply completed successfully for account {account_id} in workspace: {workspace_name}")

        # 這裡可以添加 S3 上傳邏輯

        return jsonify({
            "status": "success",
            "data": {
                "deployedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "outputLocation": f"s3://{bucket_name}/{s3_key}"
            }
        }), 200

    except subprocess.CalledProcessError as e:
        error_message = f"Terraform command failed for account {account_id}: {str(e)}"
        print(error_message)
        return jsonify({"status": "error", "message": error_message}), 500
    except Exception as e:
        error_message = f"An error occurred for account {account_id}: {str(e)}"
        print(error_message)
        return jsonify({"status": "error", "message": error_message}), 500
import subprocess
import os
from quart import jsonify
from datetime import datetime
import asyncio
import json
from stopEvent import stopEvent
from checker import check_waf_acl_id
from tf_output import filter_terraform_output
from s3_handler import periodic_s3_upload

stop_event = stopEvent()

async def destroy_resources_in_workspace(terraform_dir, workspace_name, output_file, account_id):
    try:
        await run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "select", workspace_name],
            output_file,
            account_id
        )
        print(f"Attempting to destroy resources in workspace {workspace_name}...")
        await run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "destroy", "-auto-approve"],
            output_file,
            account_id
        )
        print(f"Successfully destroyed all resources in workspace {workspace_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to destroy resources in workspace {workspace_name}")
        print("Terraform output:")
        print(e.output)
        return False
    finally:
        await run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "select", "default"],
            output_file,
            account_id
        )

async def delete_workspace(terraform_dir, workspace_name, output_file, account_id):
    try:
        await run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "select", "default"],
            output_file,
            account_id
        )
        destroy_success = await destroy_resources_in_workspace(terraform_dir, workspace_name, output_file, account_id)
        if not destroy_success:
            print("Failed to destroy resources in workspace. Proceeding with deletion anyway.")
        
        delete_output = await run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "delete", "-force", workspace_name],
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
        print(f"Command output: {e.output}")
        return False

async def run_terraform_command(cmd, output_file, account_id):
    with open(output_file, 'a') as f:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        output = []
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            line = line.decode().strip()
            f.write(filter_terraform_output(line) + '\n')
            f.flush()
            output.append(line)
            print(f"[Account {account_id}] {line}", flush=True)
        
        await process.wait()
        if process.returncode != 0:
            await asyncio.sleep(10)
            raise subprocess.CalledProcessError(process.returncode, cmd, '\n'.join(output))
        return '\n'.join(output)

# ensure whether the workspace exist 
async def ensure_workspace(terraform_dir, workspace_name, output_file, account_id):
    try:
        list_output = await run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "list"],
            output_file,
            account_id
        )
        if workspace_name in list_output:
            print(f"Workspace '{workspace_name}' exists.")
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error managing workspace: {e}")
        return False

async def create_new_workspace(terraform_dir, workspace_name, output_file, account_id):
    try:
        create_output = await run_terraform_command(
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
        print(f"Error creating workspace: {e}")
        return False

# deploying the tf code and returning the msg for rendering
async def run_terraform_deploy(account_id):
    output_file = f"terraform_output_{account_id}.txt"
    bucket_name = "kg-for-test"
    s3_key = f"user_data/{account_id}/{output_file}"
    workspace_name = f"customer_{account_id}"
    terraform_dir = f"/home/ec2-user/customers/{account_id}"
    try:
        if not os.path.exists(terraform_dir):
            raise FileNotFoundError(f"Terraform directory not found: {terraform_dir}")
        if not os.path.exists(os.path.join(terraform_dir, 'main.tf')):
            raise FileNotFoundError(f"main.tf not found in: {terraform_dir}")
        try:
            if await ensure_workspace(terraform_dir, workspace_name, output_file, account_id):
                await delete_workspace(terraform_dir, workspace_name, output_file, account_id)
            try:
                await create_new_workspace(terraform_dir, workspace_name, output_file, account_id)
            except subprocess.CalledProcessError as e:
                print(f"Error for creating new workspace: {e}")

        except subprocess.CalledProcessError as e:
            print(f"Error for workspace preprocessing: {e}")
        try:
            select_result = await run_terraform_command(
                ["terraform", "-chdir=" + terraform_dir, "workspace", "select", workspace_name],
                output_file,
                account_id
            )
            print(f"Selected workspace: {select_result}")
        except subprocess.CalledProcessError as e:
            print(f"Error selecting workspace: {e}")

        commands = [
            ["terraform", "-chdir=" + terraform_dir, "init"],
            ["terraform", "-chdir=" + terraform_dir, "apply", "-auto-approve"]
        ]

        global stop_event
        upload_task = asyncio.create_task(
            periodic_s3_upload(terraform_dir, output_file, bucket_name, s3_key, stop_event)
        )

        for cmd in commands:
            await run_terraform_command(cmd, output_file, account_id)

        stop_event.set()
        upload_task.cancel()
        try:
            await upload_task
        except asyncio.CancelledError:
            pass
        print(f"Terraform apply completed successfully for account {account_id} in workspace: {workspace_name}")
        return {
            "status": "success",
            "data": {
                "deployedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "outputLocation": f"s3://{bucket_name}/{s3_key}"
            }
        }, 200
    except subprocess.CalledProcessError as e:
        error_message = f"Terraform command failed for account {account_id}: {str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}, 500
    except Exception as e:
        error_message = f"An error occurred for account {account_id}: {str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}, 500
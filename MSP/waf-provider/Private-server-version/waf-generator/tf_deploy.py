import subprocess
import os
from quart import jsonify
from datetime import datetime
from s3_handler import upload_to_s3_with_path_async
import asyncio
import json

async def check_waf_acl_id(terraform_dir, timeout=60):
    start_time = asyncio.get_event_loop().time()
    
    while True:
        print(3333)
        try:
            result = await asyncio.create_subprocess_exec(
                "terraform", "-chdir=" + terraform_dir, "show", "-json",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = await result.communicate()
            
            if result.returncode != 0:
                print(f"Error running terraform show: {stderr.decode('utf-8')}")
                raise subprocess.CalledProcessError(result.returncode, "terraform show")
            
            state = json.loads(stdout.decode('utf-8'))
            print(f"state: {state}")
            waf_acl_id = state.get('values', {}).get('outputs', {}).get('waf_acl_id', {}).get('value')
            print(f"waf_acl_id: {waf_acl_id}")
            
            if waf_acl_id:
                return waf_acl_id
            
        except Exception as e:
            print(f"Error running terraform show: {e}")
        
        current_time = asyncio.get_event_loop().time()
        if current_time - start_time > timeout:
            raise TimeoutError("Timed out waiting for waf_acl_id")

        await asyncio.sleep(10)

async def check_deployment_status(process):
    completed = False
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        try:
            data = json.loads(line)
            if data.get('type') == 'apply_complete':
                completed = True
                changes = data.get('changes', {})
                print(f"Deployment completed. Add: {changes.get('add', 0)}, Change: {changes.get('change', 0)}, Destroy: {changes.get('destroy', 0)}")
                break
            elif data.get('type') == 'diagnostic' and data.get('severity') == 'error':
                print(f"Error: {data.get('summary', 'Unknown error occurred')}")
                completed = False
                break
        except json.JSONDecodeError:
            print(f"Could not parse line: {line.decode().strip()}")

    await process.wait()
    return completed and process.returncode == 0


async def periodic_s3_upload(local_file_path: str, bucket_name: str, s3_key: str, stop_event: asyncio.Event) -> None:
    while True:
        print("stop event: ", stop_event.is_set())
        if stop_event.is_set():
            break
        try:
            await upload_to_s3_with_path_async(local_file_path, bucket_name, s3_key)
            print("Uploaded to S3 successfully")
        except Exception as e:
            print(f"Error during periodic S3 upload: {e}")
        await asyncio.sleep(10)


async def destroy_resources_in_workspace(terraform_dir, workspace_name, output_file, account_id):
    try:
        select_result = await run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "select", workspace_name],
            output_file,
            account_id
        )
        
        print(f"Attempting to destroy resources in workspace {workspace_name}...")
        destroy_result = await run_terraform_command(
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
            f.write(line + '\n')
            f.flush()
            output.append(line)
            print(f"[Account {account_id}] {line}", flush=True)
        
        await process.wait()
        if process.returncode != 0:
            await asyncio.sleep(10)
            raise subprocess.CalledProcessError(process.returncode, cmd, '\n'.join(output))
        return '\n'.join(output)

async def ensure_workspace(terraform_dir, workspace_name, output_file, account_id):
    try:
        list_output = await run_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "list"],
            output_file,
            account_id
        )
        if workspace_name in list_output:
            print(f"Workspace '{workspace_name}' exists. Deleting it.")
            if not await delete_workspace(terraform_dir, workspace_name, output_file, account_id):
                raise Exception(f"Failed to delete existing workspace '{workspace_name}'")
        else:
            create_output = await run_terraform_command(
                ["terraform", "-chdir=" + terraform_dir, "workspace", "new", workspace_name],
                output_file,
                account_id
            )
            print("create output: ", create_output)

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


async def run_terraform_deploy(account_id):
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

        if not await ensure_workspace(terraform_dir, workspace_name, output_file, account_id):
            raise Exception("Failed to create workspace")

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

        stop_event = asyncio.Event()
        upload_task = asyncio.create_task(
            periodic_s3_upload(output_file, bucket_name, s3_key, stop_event)
        )

        for cmd in commands:
            await run_terraform_command(cmd, output_file, account_id)
            if "apply" in cmd:
                print(222222)
                try:
                    waf_acl_id = await check_waf_acl_id(terraform_dir)
                    print(f"Found waf_acl_id: {waf_acl_id}")
                    # Generate stopped signal
                    stop_event.set()
                    print("Set stop event")
                except TimeoutError:
                    print("Timed out waiting for waf_acl_id")
                    stop_event.set()  # Ensure the upload task is stopped
                except Exception as e:
                    print(f"Error checking waf_acl_id: {e}")
                    stop_event.set()  # Ensure the upload task is stopped



        upload_task.cancel()
        try:
            await upload_task
        except asyncio.CancelledError:
            pass

        # await asyncio.sleep(60)

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
import subprocess
import asyncio
import json
import stopEvent

async def check_waf_acl_id(terraform_dir, stop_event):
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
            waf_acl_id = state.get('values', {}).get('outputs', {}).get('waf_acl_id', {}).get('value')
            print(f"waf_acl_id: {waf_acl_id}")
                
            if waf_acl_id:
                stop_event.set()
                return True
    except Exception as e:
        print(f"Error running terraform show: {e}")
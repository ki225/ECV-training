# Execute Terraform with the generated content.
import subprocess
import tempfile
import os

def execute_terraform(tmpdir): 
    
    subprocess.run(["terraform", "init"], cwd=tmpdir, check=True)
           
    result = subprocess.run(["terraform", "apply", "-auto-approve"], 
                                cwd=tmpdir, capture_output=True, text=True, check=True) 
        
        # Extract the output
    output = subprocess.run(["terraform", "output"], 
                                cwd=tmpdir, capture_output=True, text=True, check=True)
        
    return result.stdout, output.stdout


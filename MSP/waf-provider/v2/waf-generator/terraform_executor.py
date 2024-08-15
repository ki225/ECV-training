# Execute Terraform with the generated content.
import subprocess
import tempfile
import os

def execute_terraform(tf_content):
    with tempfile.TemporaryDirectory() as tmpdir:
        tf_file = os.path.join(tmpdir, "main.tf")
        with open(tf_file, "w") as f:
            f.write(tf_content)
        
        # Initialize Terraform
        subprocess.run(["terraform", "init"], cwd=tmpdir, check=True)
        
        # Apply Terraform configuration
        result = subprocess.run(["terraform", "apply", "-auto-approve"], 
                                cwd=tmpdir, capture_output=True, text=True, check=True)
        
        # Extract the output
        output = subprocess.run(["terraform", "output"], 
                                cwd=tmpdir, capture_output=True, text=True, check=True)
        
        return result.stdout, output.stdout


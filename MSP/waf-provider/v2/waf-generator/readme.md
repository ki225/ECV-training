In file `terraform_executor`, it will execute the terraform file in this folder. 

## How it works?
With `subprocess` in python, we can run the files through shell commands. For example, if we want to run the `hello.py` file automatically with code, we can do like the following:

```py
# hello.py
print("hello")
```

```py
import subprocess

file_to_run = "hello.py"
result = subprocess.run(["python", file_to_run], capture_output=True, text=True)

print("Output from hello.py:")
print(result.stdout)

if result.stderr:
    print("Errors:")
    print(result.stderr)
```


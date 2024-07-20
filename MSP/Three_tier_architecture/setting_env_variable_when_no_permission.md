# setting env. variable when no permission
Because the laptop is given to us by the company, we do not have the permission to edit environment path file. Therefore, we use the following ways to solve this problem.

## First step. Downloading PowerShell 
In Microsoft Store, find it and download it if you have not downloaded it yet.

![image](https://hackmd.io/_uploads/H17sbzMdR.png)

## Second step. set the path into the file for PowerShell

```=
code $PROFILE
```
Type the following code in the file open in vscode. Remember to save the file.
```tf=
# Functions
function restart-pwsh {
    clear
    Invoke-Command { & "pwsh.exe" } -NoNewScope
}

# Alias
Set-Alias psd pushd
Set-Alias ppd popd
Set-Alias clr clear
Set-Alias restart restart-pwsh
Set-Alias terraform "D:\terraform.exe"
Set-Alias tf "D:\terraform.exe"
```
![image](https://hackmd.io/_uploads/Sk_bXffuR.png)

Restart the PowerShell so that it can understand the setting.

```=
. $PROFILE
```
Then we can run the command.

![image](https://hackmd.io/_uploads/ryV2GfMuR.png)


---
The original commands that Markus gave to us is like below, but this one cannot recognize the parameters. So the result is like the following one. 
```tf=
function terraform-cli{
    Invoke-Command { & "D:\terraform.exe" }
}
 
# $env:terraform = "D:\terraform.exe"

Set-Alias terraform terraform-cli
Set-Alias tf terraform-cli
```
![image](https://hackmd.io/_uploads/Bk3CeffdA.png)


Then the correct one should be like this:

```tf=
# Functions
function restart-pwsh {
    clear
    Invoke-Command { & "pwsh.exe" } -NoNewScope
}

# Alias
Set-Alias psd pushd
Set-Alias ppd popd
Set-Alias clr clear
Set-Alias restart restart-pwsh
Set-Alias terraform "D:\terraform.exe"
Set-Alias tf "D:\terraform.exe"
```

---
# deploy your resources
First, install the plugin `AWS_tool`. Enter your access key and secret access key into it, then click `view` > `command palette...(ctrl+shift+P)` > `AWS: create credential profile`

You will get credential file in path like `%USERPROFILE%/.aws/credentials`.

Write the terraform file then do the following three steps: `terraform init`, `terraform plan`, `terraform apply`. Enter `yes` when the system ask you to enter a value.

The path of credential should be right, or you will get error when you are doing the second step. Error might like the statement below:
```=
Planning failed. Terraform encountered an error while generating this plan.

╷
│ Error: failed to get shared config profile, default
│
│   with provider["registry.terraform.io/hashicorp/aws"],
│   on main.tf line 2, in provider "aws":
│    2: provider "aws" {
│
╵
```
![image](https://hackmd.io/_uploads/HyS3I4MOA.png)

If you set the path by default, the correct path might like this `%USERPROFILE%/.aws/credentials`

---
# other commands
- watch the status of all resources we just created.
    ```sh=
    terraform state list
    ```
- delete the particular resources instead of all
    ```sh=
    terraform state rm <resource_to_be_deleted>
    ```
-  destroy the whole stack except above excluded resource(s)
    ```sh=
    terraform destroy
    ```
- check that your configuration has no syntax error
    ```sh=
    terraform validate
    ```
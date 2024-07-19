> just for practicing and it's still not completed yet.
# level 1 
## goal
- [ ] Can see the Instance's private ip by access CloudFront's domain url
- [ ] Open multiple website to confirm that the ELB has a diversion (the web pages will show a different ip)
- [ ] Website can still be accessed normally after terminate one of EC2
- [ ] Can use SSM get into instance
- [ ] Can connect to RDS from EC2

![image](https://hackmd.io/_uploads/SyHiPQAvR.png)

## create VPC and subnets
- [How to Create an AWS VPC with Public and Private Subnets](https://www.youtube.com/watch?v=ApGz8tpNLgo)
- [Introduction to AWS Networking](https://www.youtube.com/watch?v=XZbvQWkpJTI)

## create ALB 
- since webserver is in private subnet, we choose the Internal option.
![image](https://hackmd.io/_uploads/H1mcDXADA.png)
- because our auto-scaling-group will be across 2 AZs, we have to choose both AZs
![image](https://hackmd.io/_uploads/S13Nd7CPR.png)
- the document mentions that ALB listens 80 port
![image](https://hackmd.io/_uploads/SyEsOQCPA.png)
- ?
![image](https://hackmd.io/_uploads/ryTVK70vA.png)
- need to add it to the target group(bottom of the pic)
![image](https://hackmd.io/_uploads/SyC4CVCv0.png)
- create EC2 image for the template later
![image](https://hackmd.io/_uploads/Sk8gc4APA.png)
- creating
![image](https://hackmd.io/_uploads/Bk_v5VAw0.png)
- select the AMI we created
![image](https://hackmd.io/_uploads/rJEcsVRw0.png)
![image](https://hackmd.io/_uploads/Hyjsj40w0.png)
- select subnets to let EC2 Auto Scaling balance your instances across these zones. 
![image](https://hackmd.io/_uploads/SyUIgHCDC.png)
- Attach to an existing load balancer
![image](https://hackmd.io/_uploads/BkkRgrCPC.png)
- setting ASG and selecting scaling policy
    - Min: 1
    - Desired: 1
    - Max: 3
![image](https://hackmd.io/_uploads/r1jdZr0D0.png)
> Target tracking scaling policy
> Choose a CloudWatch metric and target value and let the scaling policy adjust the desired capacity in proportion to the metric's value.

[AWS Tutorial to create Application Load Balancer and Auto Scaling Group](https://youtu.be/fZuxp_pOzgI?si=mhXtA2kTcyG37es6)

## build a RDS
- Under Connectivity, for Compute resource, choose Don't connect to an EC2 compute resource because we'll connect the EC2 instance and the RDS database later.
![image](https://hackmd.io/_uploads/H1-8BH0wR.png)
- set VPC and do not assign public IP
![image](https://hackmd.io/_uploads/ry_EBB0PR.png)
- manage secret by ourselves, we do not use the secret manager
![image](https://hackmd.io/_uploads/BJnKKSRwA.png)

## To automatically connect an EC2 instance to an RDS database using the EC2 console
- [official document link](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/option1-task3-connect-ec2-instance-to-rds-database.html)
- connect to RDS 
![image](https://hackmd.io/_uploads/HkG62rRPA.png)
- because our database is cluster db, we choose cluster
![image](https://hackmd.io/_uploads/Sydm0H0vA.png)

### Verify the connection configuration
- [how to verify](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/option1-task4-verify-connection-configuration.html#option1-task4-verify-connection-configuration-animation)

## create cloudfront
- [ref video: CloudFront with AWS Application Load balancer by AWS Avinash Reddy](https://www.youtube.com/watch?v=8sUJFkXtzXY)
- choose alb(load balance we just created) as an AWS origin
![image](https://hackmd.io/_uploads/BkYYvLAPC.png)


# 刪除資源

![image](https://hackmd.io/_uploads/H1zihD0PR.png)
![image](https://hackmd.io/_uploads/BJJ3nPCwR.png)

可以記下網卡的編號，去ec2找，會看到相關的說明(e.g. 誰創的資源)

## network interface

## probem: Network interface is currently in use and is of type "interface".
https://stackoverflow.com/questions/37232965/issue-when-trying-to-delete-vpc-and-network-interface

# Terraform
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

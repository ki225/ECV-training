# 2024/7/1-7
I got the offer on 7/1. HR send me a link of training courses after checking electronic self documents I had sent. The records of learning from the online resources provided by ECV are placed in "2024_Internship_Hand-on_practice" folder.

Learning how to build cloud architectures sometimes will be unaffordable for student like us. However, there is no need to pay in all the workshops I take. Really appreciate.

# 2024/7/8
Today is Onboard day. I was assigned into MSP team with two international students. For me, it is a huge challenge because I'm not good at English speaking. However, in fact, I found that my English speaking skill has been improved a little after a whole day.

All the interns had a test in the afternoon, and it seems as hard as SAA for me. I'll keep studying hard for understanding the usage of AWS services! Hope every things will be great in the coming three months!

# 2024/7/9
Tasks:
- Hand-on lab: Get Started with Amazon ElastiCache for Redis
- Hand-on lab: Get Started with AWS WAF
- AWS Cloud Essentials & taking notes

Lessons Learned:
- AWS CP 考試內容
- understand how to protect resources with WAF
- understand how to reduce the latency with AWS CloudFront and cache hierachy

Unresolved Challenges:
- review the exam taken yesterday
- find the problem that cause me cannot complete the lab "How to Setup Site-to-Site VPN Connection"

# 2024/7/10
Tasks:
- Pass the AWS CP exam and get the certificate
- Hand-on lab: Get Started with CloudFormation

Lessons Learned:
- understand the lesson about security

Unresolved Challenges:
- review the remain problems from exam taken on 7/8
- find out the problem with hand-on lab: Get Started with CloudFormation

# 2024/7/11
Tasks:
- Hand-on lab: Deploy an Event triggered automatic workload subroutine
- Hand-on lab: Get Started with CloudFormation
- Hand-on lab: How to Setup Site-to-Site VPN Connection
- AWS Cloud Essentials & taking notes

Lessons Learned:
- Serverless Architecture
- VPN connection: route table, gateway, ...

# 2024/7/12
Tasks:
- AWS Basic Infra and CloudWatch Monitoring Practice
- delete all the resources (it took so much time)

Lessons Learned:
- build an architecture from a diagram
- how to delete RDS(have to uncheck one selection)
- propose of using bastion and ec2 in private subnet
- setting autoscaling group
- EC2 connect to RDS

Unresolved Challenges:
- build by using CloudFormation
- understand session system manager and network interface

> For the first week in internship, I feel really excited and have so many expectation for the following days. The environment and atmosphere here are excellent and my team members and mentors are pretty nice. Besides, we finished the online courses and started to do hand-on task this week. I am looking forward to learn how to build them well.
> 
> The notes for online courses are in `onboard` folder.


# 2024/7/15
Tasks:
- build level1 AWS architecture with Terraform

Lessons Learned:
- How to set environment variable in PowerShell without permissions.
- Set the environment to run Terraform
- Use Terraform to build VPCs, subnets, EC2s

# 2024/7/17
Tasks:
- complete level1 AWS architecture through the AWS console

Lessons Learned:
- Switching role, connect ec2, building rds, ...

Unresolved Challenges:
- how to make ec2 connect to RDS
- setting SSM agent
- complete the task i do today


# 2024/7/18
Tasks:
- complete level1 AWS architecture through the AWS console

Lessons Learned:
- understanding  the reason of why changing IAM role cannot function right away
- learn about IMDSv2 and its usage
- how to use SSM without rebuilding an ec2 (restart in the ec2)
- building cloudwatch agent through CLI and generating json file by wizard
- instance connection and SSM is for replacing  
- remember to close the cookie when refreshing the website, so we can get the diff. ip
- many commands

Unresolved Challenges:
- to organize all the knowledge I have learned
- learn how to use ECS

# 2024/7/19

Tasks:
- complete level2 AWS architecture through the AWS console
- fix the problem of webpage not found (just reboot)

Lessons Learned:
- Using CloudFront to connect EC2 instance
- building docker with ECS AMI
- docker commands
- SQL injections

Unresolved Challenges:
- complete task 5 and task 6

# 2024/7/22
Tasks:
- complete level2 AWS architecture through the AWS console

Lessons Learned:
- Concept of CSRF
- SQL injections commands and some database knowledge

Unresolved Challenges:
- learn some security knowledge like CSRF, XSS
- complete level2 AWS architecture with Terraform
- modify data in database
- learn setting custom WAF by using regex

# 2024/7/23
Tasks:
- write a document for understanding the differences between Git Flow, GitHub Flow, GitLab Flow.
- try to build level 2 implementation by Terraform
- use Cloud9 to solve the laptop permission problems

Lessons Learned:
- Terraform

Unresolved Challenges:
- complete level 2 implementation by Terraform

# 2024/7/29

Tasks:
- building DVWA with Terraform
- upload files to GitLab through commands
- download Git in Windows OS
- try to fix error
    ```
    Planning failed. Terraform encountered an error while generating this plan.

    ╷
    │ Error: Retrieving AWS account details: validating provider credentials: retrieving caller identity from STS: operation error STS: GetCallerIdentity, https response error StatusCode: 403, RequestID: 49e00923-f52c-443b-af3d-4a4431403a3b, api error InvalidClientTokenId: The security token included in the request is invalid.
    │ 
    │   with provider["registry.terraform.io/hashicorp/aws"],
    │   on main.tf line 1, in provider "aws":
    │    1: provider "aws" {

    │ Error: creating IAM Role (ecs_task_execution_role): operation error IAM: CreateRole, https response error StatusCode: 403, RequestID: 7102428a-8b69-45d8-8e04-51fc7b9e2f8f, api error InvalidClientTokenId: The security token included in the request is invalid
    │ 
    │   with aws_iam_role.ecs_task_execution,
    │   on main.tf line 219, in resource "aws_iam_role" "ecs_task_execution":
    │  219: resource "aws_iam_role" "ecs_task_execution" {
    │ 
    ```
- discuss the problem with our mentor
- explain how we solve to Addi and Markus

Lessons Learned:
- Terraform
- credential priority
- credential store

# 2024/7/30
Tasks:
- Build and design POST/GET RESTful API
- connect API and EC2 instance
Lessons Learned:
- RESTful API
- VPC link
Unresolved Challenges:
- 前端和後端都會放在同一台EC2嗎
- 如果放在一起的話，使用api gateway 的意義為何
- 找讓架構更安全的方法
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-aws-waf.html
    https://docs.aws.amazon.com/zh_tw/apigateway/latest/developerguide/apigateway-custom-domain-tls-version.html
    https://docs.aws.amazon.com/zh_tw/network-firewall/latest/developerguide/what-is-aws-network-firewall.html


# 2024/7/31
Tasks:
- MSP Intern task 1&2
- solve many problems XD

Lessons Learned:
- API gateway
- proxy

Unresolved Challenges:
- Complete task by using Terraform

Problem solved
- [Task solving records](https://hackmd.io/@okii77/S1pHqTHKC)


# 2024/8/1
Tasks:
- Build waf-manager by using Terraform
- Build S3 by terraform 

Lessons Learned:
- How to use Terraform build api gateway

Unresolved Challenges:
- check S3 creation with CloudTrail

Problem Solve
- Q: Error "The REST API doesn't contain any methods" was found when running Terraform file.
    ```
    │ Error: creating API Gateway Deployment: operation error API Gateway: CreateDeployment, https response error StatusCode: 400, RequestID: 2315e9cf-2586-4b17-abd6-a85fd3b67aaf, BadRequestException: The REST API doesn't contain any methods
    │ 
    │   with aws_api_gateway_deployment.deployment,
    │   on main.tf line 134, in resource "aws_api_gateway_deployment" "deployment":
    │  134: resource "aws_api_gateway_deployment" "deployment" {
    │ 

    ╷
    │ Error: putting API Gateway Integration Response: operation error API Gateway: PutIntegrationResponse, https response error StatusCode: 404, RequestID: 6c0e1d05-7bb8-4427-ba88-6abe9236599e, NotFoundException: Invalid Integration identifier specified
    │ 
    │   with aws_api_gateway_integration_response.get_ip_blocks_integration_response,
    │   on main.tf line 128, in resource "aws_api_gateway_integration_response" "get_ip_blocks_integration_response":
    │  128: resource "aws_api_gateway_integration_response" "get_ip_blocks_integration_response" {
    │ 
    ╵

    ╷
    │ Error: creating API Gateway Deployment: operation error API Gateway: CreateDeployment, https response error StatusCode: 400, RequestID: aa659100-a6f0-4441-b889-47354c7e0b67, BadRequestException: No integration defined for method
    │ 
    │   with aws_api_gateway_deployment.deployment2,
    │   on main.tf line 268, in resource "aws_api_gateway_deployment" "deployment2":
    │  268: resource "aws_api_gateway_deployment" "deployment2" {
    │ 
    ```
    - A: We should add parameter depends_on, so that the resource will be executed after the target resources are built. (Like topo sort ?_?)
    - REF:
        - https://stackoverflow.com/questions/61027229/error-creating-api-gateway-integration-response-notfoundexception-invalid-inte
        - https://github.com/hashicorp/terraform-provider-aws/issues/4001


# 2024/8/2
Tasks:
- task3: check S3 creation with CloudTrail
- get credential by usingiam role 
- assume role for creating bucket

Lessons Learned:
- API key
- how important writing document is

Unresolved Challenges:
- write document
- find credential

# 2024/8/5
Tasks:
- finish [task3 notes](https://hackmd.io/@okii77/S1CFb3_YA)
- complete API document for task1&2
- design final project architecture
- find CVE payload
    - [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CVE%20Exploits)

Lessons Learned:
- IAM role & trust policy
- how important writing document is
Unresolved Challenges:

# 2024/8/6
Tasks:
- ACloudGURU LAB
- Using Secrets Manager to Authenticate with an RDS Database Using Lambda
- Triggering AWS Lambda from Amazon SQS
- Standing Up an Amazon Aurora Database with an Automatically Rotated Password Using AWS Secrets Manager
- Build webpage for testing 

Lessons Learned:
- secret manager

Unresolved Challenges:
- use regex for blocking the remain attacks
- Nginx website
- sqlmap

# 2024/8/7
Tasks:
- Find Nginx vulnerabilities
- Design the whole architecture of  fp

Unresolved Challenges:
- Design the architecture
- Test REGEX for some NGINX vulnerabilities 

# 2024/8/8
Tasks:
- Design FP architecture and diagram
- find nginx vulnerability
    - https://reversebrain.github.io/2021/03/29/The-story-of-Nginx-and-uri-variable/

Unresolved Challenges:
- Test REGEX for some NGINX vulnerabilities 

# 2024/8/9
Tasks:
- find nginx vulnerability
    - note: https://hackmd.io/@okii77/rJxhuIeQ9C

Unresolved Challenges:
- Test REGEX for some NGINX vulnerabilities 


# 2024/8/12
Tasks:
- nginx vulnerability PoC
- finding other vulnerabilities

Lessons Learned:
- Nginx-ingress
- K3S

Unresolved Challenges:
- Test REGEX for some NGINX vulnerabilities 

To-do list
- waf architecture in private subnet
- keep notes

# 2024/8/13
Tasks:
- Build architecture: S3 website send API request into server in private subnet
- Build in console

Lessons Learned:
- VPC endpoint
- NLB
- VPC link
- presentation

Unresolved Challenges:
- Build with Terraform

To-do list
- design in/output format in .json file
- make connection between front-end and back-end

# 2024/8/14
Tasks:
- Build architecture: S3 website send API request into server in private subnet with Terraform
- design in/output format in .json file
- front-end diagram
- Terraform file for building customize waf for customer

Unresolved Challenges:
- Terraform file for building customize waf for customer
- make connection between front-end and back-end

# 2024/8/15
Tasks:
- design in/output format in .json file
- Terraform file for building customize waf across different account
- take notes https://hackmd.io/@okii77/S1talricA


Unresolved Challenges:
- python files for generating terraform files
- make connection between front-end and back-end

# 2024/8/19
Tasks:
- build terraform_generator.py for building terraform file with .json input from front-end

Lessons Learned:
- Pydantic

Unresolved Challenges:
- modify the original code with Pydantic to make code clear and easy to be managed 

# 2024/8/20
Tasks:
- Create terraform_generator.py to generate Terraform configuration files using .json input from the front-end.

Unresolved Challenges:
- complete the original code with Pydantic

# 2024/8/21
Tasks:
- build terraform_generator.py for building terraform file with .json input from front-end
- re-design the json file

Unresolved Challenges:
- modify the original code with Pydantic to make code clear and easy to be managed 
# 2024/8/22
Tasks:
- build terraform_generator.py for building terraform file with .json input from front-end
- document for service usage
- document for request body with Pydantic

Unresolved Challenges:
- modify the original code with Pydantic to make code clear and easy to be managed 

To-Do
- Find rules samples for demo

# 2024/8/26

Tasks:
- find regex rules for WAF protection
    - https://github.com/nasbench/sigma/tree/master/rules/web/webserver_generic
    - SQLi for each database
    - XSS
- make connection between API gateway and terraform generator 
- complete the terraform generator's environment
    - use python version later than 3.8
        - https://repost.aws/questions/QUtA3qNBaLSvWPfD5kFwI0_w/python-3-10-on-ec2-running-amazon-linux-2-and-the-openssl-upgrade-requirement

To-Do:
- modify the json test and send it from API gateway to server 
- find more regex
- modify the server.py
- modify the user data for terraform generator's environment

# 2024/8/27
Tasks:
- make front-end send API request to back-end server and build file successfully 

To-Do:
- find more regex
- test whether the terraform file can execute successfully
- add priority part


# 2024/8/28
Tasks:
- make the process that front-end send API request to back-end server and build file fluently
- add priority to the rule
- find bugs
- combine both customized rules and package rules

To-Do:
- test whether the terraform file works
- make the rule package file for generating detail of the package rule 
- modify Pydantic document
- automatic deployment python file

# 2024/8/29
Tasks:
- test whether the terraform file works
- make the rule package file for generating detail of the package rule 
- modify Pydantic document
- make terraform be executed automatically

Learn:
- Browser Caching

To-Do:
- cross account
- rule priority
- complete Web request body inspection

# 2024/8/30
Tasks:
- make function work cross account
- finish first version
- clean the code
- write document and notes

To-Do:
- clean the code
- add more functions and fix the bug

# 2024/9/2
Tasks:
- Design a new architecture for waf-manager 

goal: 
- achieve reliability, availability and security
- 3-tier framework
- Real time rendered web page
- asynchronized
- Distinguish each user's credential and information
- handle multiple users' request?
- Dynamic Workspace Creation: Create a separate workspace (directory) for each customer's Terraform project.

Learn
- TTL
- websocket
- package manager

# 2024/9/3
Tasks:
- use websocket api gateway for rendering front-end
- modify the terraform file

To-Do:
- find the solution to fix the problem today
- make front-end be rendered 
- handle with different client credential

# 2024/9/4
Tasks:
- handle with different client credential
- update data to s3 with polling method 
- document

To-Do:
- make front-end and back-end work together
- document
- priority

# 2024/9/5
Tasks:
- make terraform file execute in terraform workspace to prevent "state lock" problem
- test for credential switching
- use WSGI for making tasks running concurrently
- document writing

Learn 
- WSGI
    - propose: make execute concurrently
    - Gunicorn

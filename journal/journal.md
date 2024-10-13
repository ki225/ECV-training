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

# 2024/9/9

Tasks:
- modify the service terraform file
- adding api gateway and lambda function
- upgrade the ec2 level
- debug and solve the tf workspace conflict problem
- modify the json/pydantic format setting
- add python file for filtering the console output from different account and the status content for rendering front-end

To-do
- fix the bug and let the modified content send to s3 bucket
- add model into our service

# 2024/9/11
Tasks:
- build asynchronous and concurrency server with quart and hypercorn
- fix bugs

Learn
- quart
- hypercorn

To-do
- fix "Failed to create workspace"
- possible way1: code for validate whether customer's account have one
- possible way 2: use terraform show to get output value for waf 
- because the terraform cannot show the status successfully
- fix "terraform workspace deletion & creation "


Error
```
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started parent process [4539]
INFO:     Started server process [4544]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Started server process [4543]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Started server process [4542]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Started server process [4541]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.

```
https://stackoverflow.com/questions/64512286/asgi-lifespan-protocol-appears-unsupported

```
myenv) [root@ip-10-0-3-125 ec2-user]# uvicorn server:asgi_app --host 0.0.0.0 --port 5000 --workers 4 --lifespan on
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started parent process [4555]
INFO:     Started server process [4559]
INFO:     Started server process [4560]
INFO:     Waiting for application startup.
INFO:     Waiting for application startup.
ERROR:    Exception in 'lifespan' protocol
Traceback (most recent call last):
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/uvicorn/lifespan/on.py", line 86, in main
    await app(scope, self.receive, self.send)
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
    return await self.app(scope, receive, send)
```

[Flask : RuntimeError: Working outside of request context](https://stackoverflow.com/questions/68710021/flask-runtimeerror-working-outside-of-request-context)


```
Traceback (most recent call last):
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/quart/app.py", line 1403, in handle_request
    return await self.full_dispatch_request(request_context)
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/quart/app.py", line 1441, in full_dispatch_request
    result = await self.handle_user_exception(error)
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/quart/app.py", line 1029, in handle_user_exception
    raise error
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/quart/app.py", line 1439, in full_dispatch_request
    result = await self.dispatch_request(request_context)
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/quart/app.py", line 1535, in dispatch_request
    return await self.ensure_async(handler)(**request_.view_args)  # type: ignore
  File "/home/ec2-user/server.py", line 70, in rule_ip
    if request.method == 'POST':
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/werkzeug/local.py", line 318, in __get__
    obj = instance._get_current_object()
  File "/home/ec2-user/myenv/lib64/python3.8/site-packages/werkzeug/local.py", line 519, in _get_current_object
    raise RuntimeError(unbound_message) from None
RuntimeError: Working outside of request context.

This typically means that you attempted to use functionality that needed
an active HTTP request. Consult the documentation on testing for
information about how to avoid this problem.
```
after I found this solution https://stackoverflow.com/questions/68710021/flask-runtimeerror-working-outside-of-request-context

i change my code from

```
from flask import Flask, request, jsonify
from quart import Quart, jsonify
```
to
```
from quart import Quart, request, jsonify
```

# 2024/9/13
Tasks:
- solve server timeout problem (504)
- asynchronous return value
- make js keep calling api for rendering instead of getting data from s3
    - https://claude.ai/chat/431b81b3-86b4-4da8-80b6-4a134978b21f
- fix bugs
- add more api gw resources

Learn
- Future
- asynchronous: await vs asyncio.create_task
- webhook
- gather
    - description: uber & bus
    - https://claude.ai/chat/ad3531e4-06cc-4c51-b233-dea4b1b0134c
```
async def function1(task_id, iterations):
    print(f"Function 1 (Task ID: {task_id}) started")
    for i in range(iterations):
        print(f"Function 1 (Task ID: {task_id}) iteration {i+1}")
        await asyncio.sleep(0.5)  # Simulating some work
    print(f"Function 1 (Task ID: {task_id}) finished")
    return f"Result from Function 1 (Task ID: {task_id})"

async def function2(task_id, iterations):
    print(f"Function 2 (Task ID: {task_id}) started")
    for i in range(iterations):
        print(f"Function 2 (Task ID: {task_id}) iteration {i+1}")
        await asyncio.sleep(0.3)  # Simulating some work
    print(f"Function 2 (Task ID: {task_id}) finished")
    return f"Result from Function 2 (Task ID: {task_id})"

async def main():
    # Create two tasks with different functions, IDs, and iteration counts
    task1 = asyncio.create_task(function1(1, 5))
    task2 = asyncio.create_task(function2(2, 7))

    # Wait for both tasks to complete and get their results
    results = await asyncio.gather(task1, task2)

    print("Both tasks have finished execution")
    print("Results:", results)

# Run the main coroutine
asyncio.run(main())
```


To-do
- PPT
- clean code
- webhook manage several task status

# 2024/9/18
Tasks:
- add lambda to connect OpenAI as assistant
- use Api to get deployment process
- clean code and fix bugs
- ppt

Learn
- lambda layers 
- OpenAI

```
[ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': No module named 'pydantic_core._pydantic_core'
Traceback (most recent call last):INIT_REPORT Init Duration: 165.44 ms    Phase: init    Status: error    Error Type: Runtime.Unknown
[ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': No module named 'pydantic_core._pydantic_core'
Traceback (most recent call last):INIT_REPORT Init Duration: 2428.59 ms    Phase: invoke    Status: error    Error Type: Runtime.Unknown
START RequestId: a46809e1-8e11-4177-a86d-2a605ccf1a30 Version: $LATEST
Unknown application error occurred
Runtime.Unknown
END RequestId: a46809e1-8e11-4177-a86d-2a605ccf1a30
REPORT RequestId: a46809e1-8e11-4177-a86d-2a605ccf1a30    Duration: 2469.43 ms    Billed Duration: 2470 ms    Memory Size: 128 MB    Max Memory Used: 14 MB
```

```
{
  "errorMessage": "Unable to import module 'lambda_function': urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168",
  "errorType": "Runtime.ImportModuleError",
  "stackTrace": []
}
```

# 2024/9/20

Tasks:
- clean code and fix bugs
- ppt

# 2024/9/23
Tasks:
- make chat-bot read history
  - DynamoDB
  - IAM role should be attached to lambda
- fix rendering bug
  - API for lambda should use "post" method for showing on webpage 
- improve prompt for asking information
- ppt

To-do
- document
- bedrock

# 2024/9/24
Tasks:
- 1-on-1 meeting
- documentation

# 2024/9/25
Tasks:
- build bedrock
- documentation
- debug
- runnable for chat history

Learn
- Langchain
- RAG, embedding
- bedrock

To-do
- fix LLM response error
- bedrock


# 2024/9/27
Tasks:
- modify the prompt
- bedrock
- SOW 
- ppt
- PoC
- CVE regex finding

Learn
- temperature
  - near 1 : 即興發揮炒飯
  - near 0 : 照食譜做的炒飯
  - The temperature is a parameter that controls the randomness of the LLM's output. A higher temperature will result in more creative and imaginative text, while a lower temperature will result in more accurate and factual text.

# 2024/9/30
Tasks:
- ppt
- presentation
- fix prompt
# Building WAF Manager Across Different Account With Credential

## Scenario
![image](https://hackmd.io/_uploads/HyXdiSs5R.png)



In this scenario, we have to create WAF resource for customer in our company's account. Here are the steps for complete this.

## Decide what we need
In order to let programmer complete this task without getting into customer's account, we need to make a tunnel from company's account to customer's. Therefore, we need 2 `IAM-roles's arn` in this task. Besides, we need to know which resource that should be protected by WAF. Therefore, All we need are:

-  2 `IAM-roles's arn`
    -  company's account for programmer
    -  customer's assume-role
- which resource will be associated with WAF

## Set IAM Role
### Create role for working env.
Let's continue with the IAM roles we need. The first one is in company's acc. Since the working environment is in ec2, let's make it with following requirements:

- Trusted entity type: Trusted entity type
- Use case: EC2 (so that we can attach it into the ec2 instance)

![image](https://hackmd.io/_uploads/BymmNBo5A.png)

The IAM role in company account will be like the one below:

```json=
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```


### Get credential from customer & Make trust relationship
The other one is in customer's acc. This role should have enough permission to build target resource, and it usually should be AdminRole. 

Before we start to make the Terraform file, we need to make the trust relationship first. With trust relationship, it represents that your customers allow you to do something in their acc.

> It might be dangeourous if no check with trust relationship. In other word, it means that everyone can create resource in your account without authentication.

For example, here is the trust relationship policy from customer's role. 

```json=
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com",
                "AWS": "arn:aws:iam::<COMPANY_ACC_ID>:role/<COMPANY_IAM_ROLE>"
            },
            "Action": "sts:AssumeRole",
            "Condition": {}
        }
    ]
}
```
Let's break the "Statement" part down:
- Effect
    - Specifies whether the statement allows or denies access. "Allow" means the specified actions are permitted.
- Principal
    - specifies the entity (user, service, or account) that is allowed or denied access to a resource.
    - In this example, it allows the EC2 service and particular IAM role to assume this role.
- Action
    - Specifies the action that is allowed or denied. In this case, it allows the assumption of this role.
- Condition
    - Specifies conditions for when this policy is in effect. An empty object means no additional conditions are applied.

## Assume role during deployment
We complete this task with terraform file in ec2 environment. Actually what programmer's role will do depends on the code in terraform file. Therefore, we have to defined customer's information in the file.

In order to manage resources across multiple accounts/regions in a single Terraform configuration, Terraform provide "provider" to achieve this it. First, let's define a provider:

```tf=
# Provider configuration
provider "aws" {
      alias  = "customer"
      region = "us-east-1"
      assume_role {
            role_arn = "arn:aws:iam::<CUSTOMER_ACC_ID>:role/<CUSTOMER_ROLE_NAME>"
      }
}
```
In this way, we can get the existing resource in customer's account:
```tf=
data "aws_lb" "target_alb" {
  provider = aws.waf
  name     = var.alb_name
}
```

Besides, if there are resources that will be created in customer's account instead of company's, we should define it like the example below first.

```tf=
# example: use company account to build waf in customer's account 
resource "aws_wafv2_web_acl" "customer_waf_acl" {
  # provider: define the destination of this resource
  provider = aws.customer 
  name        = ...
  description = ...
  scope       = ...

  # detailed setting
}
```
:::danger
Problem might occur if user want to create resources on different account without setting provider well:

```
│ Error: creating WAFv2 WebACL Association (arn:aws:wafv2:us-east-1:<COMPANY_ACC_ID>:regional/webacl/test_waf/...,arn:aws:elasticloadbalancing:us-east-1:<CUSTOMER_ACC_ID>:loadbalancer/app/cutomer-alb/...): operation error WAFV2: AssociateWebACL, https response error StatusCode: 400, RequestID: ..., api error AccessDeniedException: User: arn:aws:sts::<CUSTOMER_ACC_ID>:assumed-role/customer-role/aws-go-sdk-... is not authorized to perform: wafv2:AssociateWebACL on resource: arn:aws:wafv2:us-east-1:<COMPANY_ACC_ID>:regional/webacl/test_waf/... because noresource-based policy allows the wafv2:AssociateWebACL action
│
```
This problem occurs because the system thinks that the WAFv2 resource should be built in company account. Therefore, permissions aren't enough during associattion.
:::


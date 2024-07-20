# building a three-tier architecture 

## Goal
In this practice, there is a need for building an three tier architecture website with AWS. In order to implement reliability, we have to build ec2 in AZs and auto scaling group. In this article, I will keep notes for the problems I met. 

## Architecture
![截圖 2024-07-19 清晨6.34.14](https://hackmd.io/_uploads/HkcdOMDuA.png)

## function
* Can see the Instance's private ip by access CloudFront's domain url
* Open multiple website to confirm that the ELB has a diversion (the web pages will show a different ip) 
* Website can still be accessed normally after terminate one of EC2
* Can use SSM get into instance
* Can connect to RDS from EC2
* Can see the metric about memory utilization on CloudWatch Dashboard 
* Can see the log which be pushed from Instance in CloudWatch Log Groups 
* If Instance's CPU usage over 100% will received the notify email

## Can use SSM get into instance
### background
In AWS, the use for SSM(system session manager, the second choice for connection) and Instance connection(based on SSH, the first choice for connection) is to replace the use of bastion due to the security issue. In other words, if we create the SSM successfully, there is no need for bastion anymore.

### steps

- create IAM role 
- attach it to EC2 instance


### problem: SSM Agent is not online The SSM Agent was unable to connect to a Systems Manager endpoint to register itself with the service.

if you attach the iam role to the ec2 but still cannot connect by SSM, you have to do the following commands.
```
systemctl restart amazon-ssm
```

https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent-status-and-restart.html


if you cannot deal with it by commands, you can just create a new one and edit the iam role in advanced detail before you create it completely.




### install Apache into instances by user data 
user data is the part in `launch template > advanced details`

```sh=
#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo yum install -y httpd php
sudo systemctl start httpd
sudo systemctl enable httpd
```

### use bastion to connect the instances in private subnets
For using SSH, we need to use the key pair. Because we got the key pairs information in Windows host locally, we need to send these data into instance's host through commands.

In Windows, the steps for it is more complicated:
1. set variable `$PATH` as your key pair path or your key-pair name.
    ```sh=
    $PATH = "\<YOUR_KEY_PAIR_PATH>"
    ```
2. reset the access control lists (ACLs) of a file or directory to the default values(e.g. permissions) inherited from its parent directory
    ```sh=
    icacls.exe $PATH /reset
    ```
3. modify the access control list (ACL) of a file or directory specified by `$PATH` in Windows.
    ```sh=
    icacls.exe $PATH /GRANT:R "$($env:USERNAME):(R)"
    ```
4. manage the inheritance settings of the access control list
    ```sh=
    icacls.exe $PATH /inheritance
    ```



Then send key pairs through SSH copy. The first AWS host is bastion. The second one is instance in private subnet. Replace the `TARGETSENDING_FILE` with your key pair for ec2 in private subnet.
```bash=
scp -i <BASTION_KEY_PAIR> <TARGETSENDING_FILE> ec2-user@<BASTION_PUBLIC_IP>:/home/ec2-user
```


### update the permission of the key
problem:
![截圖 2024-07-20 上午10.22.18](https://hackmd.io/_uploads/B1OYyiu_0.png)



## Open multiple website to confirm that the ELB has a diversion (the web pages will show a different ip)


### Use ALB(app load balancer)
Though ALB seems to connect to private EC2 in the architecture diagram from the beginning of the article, ALB should be mapping to public part(internet-facing). The following picture distinguish the difference between ALB and other LB.

![1*YuG-jq-PGFfiHlsI7daA2w](https://hackmd.io/_uploads/Hy7aofPdR.png)



### Use auto scaling group and launch template
By using auto scaling group, instances will be generated automatically depends on the launch template. Remember to change the template version in auto scaling group after updating the template. 

![截圖 2024-07-20 上午10.08.11](https://hackmd.io/_uploads/Hyom39_dR.png)



## send log files into log group
From the information bekow, we can know that the log file for Apache is in the same path as `HTTPD_ROOT+DEFAULT_ERRORLOG`
```sh=
httpd -V
```

The outpus:
```
Server version: Apache/2.4.59 ()
Server built:   Apr 22 2024 13:07:26
Server's Module Magic Number: 20120211:131
Server loaded:  APR 1.7.2, APR-UTIL 1.6.3, PCRE 8.32 2012-11-30
Compiled using: APR 1.7.2, APR-UTIL 1.6.3, PCRE 8.32 2012-11-30
Architecture:   64-bit
Server MPM:     prefork
  threaded:     no
    forked:     yes (variable process count)
Server compiled with....
 -D APR_HAS_SENDFILE
 -D APR_HAS_MMAP
 -D APR_HAVE_IPV6 (IPv4-mapped addresses enabled)
 -D APR_USE_PROC_PTHREAD_SERIALIZE
 -D APR_USE_PTHREAD_SERIALIZE
 -D SINGLE_LISTEN_UNSERIALIZED_ACCEPT
 -D APR_HAS_OTHER_CHILD
 -D AP_HAVE_RELIABLE_PIPED_LOGS
 -D DYNAMIC_MODULE_LIMIT=256
 -D HTTPD_ROOT="/etc/httpd"
 -D SUEXEC_BIN="/usr/sbin/suexec"
 -D DEFAULT_PIDLOG="/run/httpd/httpd.pid"
 -D DEFAULT_SCOREBOARD="logs/apache_runtime_status"
 -D DEFAULT_ERRORLOG="logs/error_log"
 -D AP_TYPES_CONFIG_FILE="conf/mime.types"
 -D SERVER_CONFIG_FILE="conf/httpd.conf"
 ```
 
 https://unix.stackexchange.com/questions/115972/how-do-i-find-where-apache-keeps-the-log-files
 
 

## Can see the log which be pushed from Instance in CloudWatch Log Groups
 
### cloudwatch agent
 ```
[root@ip-10-0-5-9 logs]# cd /opt/aws/
[root@ip-10-0-5-9 aws]# ls
amazon-cloudwatch-agent  apitools  bin
```

- We need to get logs from path `/var/log/access_log`, but our log file is actually at `/etc/httpd/logs/access_log`. Use the following command to make a file which point to the original one.
    ```sh=
    sudo ln -s /etc/httpd/logs/access_log /var/log/access_log
    ```
- Edit the json file for setting cloudwatch-agent. We need cloudwatch-agent to send logs.
    ```sh=
    nano /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
    ```
- Paste the following:
    ```json=
    {
      "agent": {
        "run_as_user": "root"
      },
      "metrics": {
        "metrics_collected": {
          "mem": {
            "measurement": [
              "mem_used_percent"
            ],
            "metrics_collection_interval": 60
          }
        }
      },
      "logs": {
        "logs_collected": {
          "files": {
            "collect_list": [
              {
                "file_path": "/var/log/access_log",
                "log_group_name": "kiki-log-group",
                "log_stream_name": "{instance_id}"
              }
            ]
          }
        }
      }
    }
    ```
- Execute 
    ```sh=
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
    ```

### user data

```sh=
#!/bin/bash

sudo ln -s /etc/httpd/logs/access_log /var/log/access_log

cat << 'EOF' > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
{
  "agent": {
    "run_as_user": "root"
  },
  "metrics": {
    "metrics_collected": {
      "mem": {
        "measurement": [
          "mem_used_percent"
        ],
        "metrics_collection_interval": 60
      }
    }
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/access_log",
            "log_group_name": "kiki-log-group",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOF

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```
![截圖 2024-07-20 上午10.28.32](https://hackmd.io/_uploads/HJHbZjdOA.png)

```sh=
# Optionally, set appropriate permissions
chmod 644 /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json

# Optionally, restart the CloudWatch agent if it's already running
systemctl restart amazon-cloudwatch-agent
```

  
- For using the cloudwatch agent to create cloudwatch logs and send to group, we have to add more policies:
    ```json=
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "cloudwatch:PutMetricData",
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "logs:DescribeLogStreams"
          ],
          "Resource": "*"
        }
      ]
    }
    ```
---
## final user data
```sh=
#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo yum install -y httpd php
sudo systemctl start httpd
sudo systemctl enable httpd
sudo yum install -y mysql
sudo yum install amazon-cloudwatch-agent -y
sudo yum install aws-cli -y


HOST_IP1=$(ip addr show enX0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)
HOST_IP2=$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)
echo -e "$HOST_IP1\n$HOST_IP2" > /var/www/html/index.html

sudo ln -s /etc/httpd/logs/access_log /var/log/access_log

cat << 'EOF' > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
{
  "agent": {
    "run_as_user": "root"
  },
  "metrics": {
    "metrics_collected": {
      "mem": {
        "measurement": [
          "mem_used_percent"
        ],
        "metrics_collection_interval": 60
      }
    }
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/access_log",
            "log_group_name": "kiki-log-group",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOF

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```
![image](https://hackmd.io/_uploads/Hkkh13EdC.png)
---
## If Instance's CPU usage over 100% will received the notify email

- command for testing
    ``` sh=
    $(for i in `seq 1 $(cat /proc/cpuinfo |grep "physical id" |wc -l)`;do dd if=/dev/zero of=/dev/null & done)
    ```
    - this command is running in background. 
        - ctrl+z  (暫停當前的某項工作)
    ![截圖 2024-07-20 上午10.33.19](https://hackmd.io/_uploads/S1ofMiO_C.png)



# result
- [x] After refreshing the web page, the ip will be different.

> - remember to turn off the cookie
> - set the lower requirement for auto generating instances might be clear
> - should wait for a while due to the ec2 deployment 
- [x] The website will still be worked after 1~2 instance(s) be terminated.

![image](https://hackmd.io/_uploads/Sy32TI8O0.png)

![image](https://hackmd.io/_uploads/BkbX08UuR.png)
![image](https://hackmd.io/_uploads/S1mdCIIu0.png)


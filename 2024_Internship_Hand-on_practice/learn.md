# Hosting a Static Website on Amazon S3

## learn
- Create a static website hosting through S3
- How to use Amazon S3

# Connect to EC2 Linux Instance
EC2 Instance can be different types of servers such as a web server, database server, authentication server... For using EC2 as a server, sometimes user might upload packages and software required to it before development. Therefore, user will access EC2 through different ways, SSH connection is mostly used among these ways. 

In this practice, I learned access EC2 through SSH with EC2-key-pair and commands.

More information about EC2 connection could be found in [連線至 EC2 的三種方法與比較 – SSH、EC2 Instance Connect、System Manager](https://www.ecloudture.com/連線至ec2的三種方法與比較-ssh，ec2實例連接，系統管理/) written by ECV.


```
chmod 400 <yourKeyPair.pem>
```
Due to the setting of Linux2 or Amazon Linux AMI, the user name is ec2-user.
```
ssh -i <yourKeyPair.pem> ec2-user@<EC2_INSTANCE_IP>
```
## learn
- Launch an EC2 instance
- Create a key pair
- Connect your EC2 Instance by using terminal or putty.exe


# Implement an LAMP structure
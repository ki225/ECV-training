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
> LAMP is known for its free and open-source approach to back end development. It contains Linux OS, Apache web server, MySQL database, and PHP. Besides PHP, developers can also use Python and Perl as an alternative.

The article above is a short description about LAMP structure from learning materials. Users use LAMP for building a web page due to its inexpensive cost, efficiency, high maintenance and support, flexibility. After first practice, we learned how to build a static, simple website with Amazon S3, and now we can build both static and dynamic website with LAMP structure.

![](img/img1.png)

More information could be found in [What is a LAMP stack?](https://aws.amazon.com/what-is/lamp-stack/?nc1=h_ls) written by AWS team.

In this practice, I use EC2 instance as a web server to connect RDS database. With the public IP assigned by EC2 automatically, we can do CRUD operations through the web page below.

![](img/img2.png)


## learn 
- Deploy a RDS database and web server
- Connect your web server to your database

![](img/img7.png)

# Create Your EC2 Instance in Your Custom Network Environment

![](img/img3.png)

In this workshop, we let the EC2 instance, which called ForTestNAT in the private subnet, could connect to the Internet by setting route table and session manager. 

After attaching Internet gateway and NAT gateway, the EC2 can get the resources outside or ping to the websites.

![](img/img4.png)

![](img/img5.png)

We can also browse this website through its public IP.

![](img/img6.png)

## learn
- Configure VPC and Subnet to your own internet environment
- Edit your Route Table to the accurate path
- Knowing the difference between network in and out and how we could use NAT Gateway to route our private network to public
# Create virtual environment for running Python 3.8
![image](https://hackmd.io/_uploads/SyOmlz12A.png)

## Background
Some package can only be used in target version, however, I found that the default python version in EC2 instance is fixed. Therefore, I try to use virtual environment to run Python file in other version.

The reason that causes this situation is due to the AMI we choose. AMIs are pre-configured templates for EC2 instances that contain the necessary information to launch an instance. Each AMI is essentially a snapshot of a configured server. This snapshot includes:

* The operating system
* Pre-installed software packages
* Any custom configurations

From the [official document](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html), it is clear that python is one of the pre-installed packages in the AMI.

## Solution
In order to use different python version, we can create a python virtual environment with the following commands.

Install version 3.8:
```sh=
sudo yum remove python3 
sudo amazon-linux-extras install python3.8 
sudo ln -s /usr/bin/python3.8 /usr/bin/python3
sudo ln -s /usr/bin/pydoc3.8 /usr/bin/pydoc
```
Create environment:
```sh=
python3.8 -m venv myenv
```
Get into that environment:
```sh=
source myenv/bin/activate
```

## REF
- [Python 3.10+ on EC2 running Amazon Linux 2, and the openssl upgrade requirement.](https://repost.aws/questions/QUtA3qNBaLSvWPfD5kFwI0_w/python-3-10-on-ec2-running-amazon-linux-2-and-the-openssl-upgrade-requirement)
- [Amazon Machine Images in Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
- [Find an AMI that meets the requirements for your EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html)


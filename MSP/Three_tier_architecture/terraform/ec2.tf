resource "aws_instance" "web_server" {
    ami           = "ami-013a28d7c2ea10269"   # Find AMIs with the SSM Agent preinstalled (https://docs.aws.amazon.com/systems-manager/latest/userguide/ami-preinstalled-agent.html)
    instance_type = "t3.micro"
    key_name      = aws_key_pair.deployer.key_name
    security_groups = [aws_security_group.ec2_sg.id]
    # vpc_security_group_ids = [ aws_security_group.ec2_sg.name ]
    iam_instance_profile = aws_iam_instance_profile.dev-resources-iam-profile.id
    subnet_id = aws_subnet.private1.id
    # download and install ssm-agent
    /*
    https://oxla.io/how-to-configure-aws-systems-manager-agent-with-terraform-in-7-steps/

    but some ami have already installed

    https://docs.aws.amazon.com/systems-manager/latest/userguide/ami-preinstalled-agent.html

    */
    user_data = <<-EOF
                #!/bin/bash
                sudo mkdir /tmp/ssm
                cd /tmp/ssm
                wget https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb
                sudo dpkg -i amazon-ssm-agent.deb
                sudo systemctl enable amazon-ssm-agent
                rm amazon-ssm-agent.deb
                
                cd ~/home
                sudo yum update -y
                sudo yum install -y httpd
                sudo systemctl start httpd
                sudo systemctl enable httpd
                private_ip=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
                echo "<html><body><h1>Private IP: $private_ip</h1></body></html>" > /var/www/html/index.html
                EOF
    tags = {
        Name = "web-server"
    }
}

# security group
resource "aws_security_group" "ec2_sg" {
    name        = "ec2-sg"
    description = "Allow traffic from ALB"
    vpc_id      = aws_vpc.main.id

    # #allow http
    ingress {
        from_port       = 80
        to_port         = 80
        protocol        = "tcp"
        cidr_blocks = [ "0.0.0.0/0" ]
        # security_groups = [aws_security_group.alb_sg.id]
    }

    # allow SSH
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # #all outbound
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        stack = "test"
    }
}
data "aws_iam_role" "existing_role" {
  name = "kg-terraform-role"  # Replace with the name of your existing IAM role
}

# main.tf

provider "aws" {
  region = "us-east-1"  # Change this to your preferred region
}

# S3 Bucket
resource "aws_s3_bucket" "web_bucket" {
  bucket = "my-web-bucket-${random_string.suffix.result}"
}

resource "aws_s3_bucket_public_access_block" "web_bucket" {
  bucket = aws_s3_bucket.web_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "web_bucket" {
  bucket = aws_s3_bucket.web_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "web_bucket" {
  bucket = aws_s3_bucket.web_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.web_bucket.arn}/*"
      },
    ]
  })
}

# Upload index.html to S3
resource "aws_s3_object" "index_html" {
  bucket       = aws_s3_bucket.web_bucket.id
  key          = "index.html"
  source       = "index.html"  # Make sure this file exists in your local directory
  content_type = "text/html"
}

# IAM Role for EC2 instance
resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach policies to the IAM role
resource "aws_iam_role_policy_attachment" "ssm_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  role       = aws_iam_role.ec2_role.name
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2-flask-server-instance-profile"
  role = data.aws_iam_role.existing_role.name
}

# EC2 Instance
resource "aws_instance" "flask_server" {
  ami           = "ami-03972092c42e8c0ca"  # Amazon Linux 2 AMI (adjust for your region)
  instance_type = "t2.micro"
  
  vpc_security_group_ids = [aws_security_group.flask_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_instance_profile.name

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 python3-pip
              pip3 install flask flask-socketio
              
              cat <<EOT > /home/ec2-user/app.py
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_terraform')
def handle_terraform():
    process = subprocess.Popen(['terraform', 'apply', '-auto-approve'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               universal_newlines=True)
    
    for stdout_line in iter(process.stdout.readline, ""):
        emit('terraform_output', {'data': stdout_line.strip()})
    
    process.stdout.close()
    return_code = process.wait()
    if return_code == 0:
        emit('terraform_complete', {'status': 'success'})
    else:
        emit('terraform_complete', {'status': 'error'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
EOT

              sudo -u ec2-user python3 /home/ec2-user/app.py
              EOF

  tags = {
    Name = "Flask Server"
  }
}

# Security Group for EC2
resource "aws_security_group" "flask_sg" {
  name        = "flask_sg"
  description = "Allow inbound traffic for Flask server"

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Flask server port"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Random string for unique S3 bucket name
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Output
output "website_url" {
  value = "http://${aws_s3_bucket_website_configuration.web_bucket.website_endpoint}"
}

output "ec2_public_ip" {
  value = aws_instance.flask_server.public_ip
}
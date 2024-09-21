# main.tf

resource "aws_vpc" "kg_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "kg-vpc"
  }
}

resource "aws_subnet" "pub_subnet_1a" {
  vpc_id     = aws_vpc.kg_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "kg-subnet-public1-us-east-1a"
  }
}

resource "aws_subnet" "pub_subnet_1b" {
  vpc_id     = aws_vpc.kg_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "kg-subnet-public1-us-east-1b"
  }
}

resource "aws_subnet" "pri_subnet_1a" {
  vpc_id     = aws_vpc.kg_vpc.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "kg-subnet-private1-us-east-1a"
  }
}

resource "aws_subnet" "pri_subnet_1b" {
  vpc_id     = aws_vpc.kg_vpc.id
  cidr_block = "10.0.4.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "kg-subnet-private-us-east-1b"
  }
}


resource "aws_internet_gateway" "kg_igw" {
  vpc_id = aws_vpc.kg_vpc.id

  tags = {
    Name = "kg_igw"
  }
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat_eip" {
  domain = "vpc"
  depends_on = [aws_internet_gateway.kg_igw]
}

resource "aws_nat_gateway" "kg_nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.pub_subnet_1a.id  

  tags = {
    Name = "kg_nat"
  }

  depends_on = [aws_internet_gateway.kg_igw]
}

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.kg_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.kg_igw.id
  }

  tags = {
    Name = "Public Route Table"
  }
}

# Private Route Table
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.kg_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.kg_nat.id
  }

  tags = {
    Name = "Private Route Table"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public_1a" {
  subnet_id      = aws_subnet.pub_subnet_1a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_1b" {
  subnet_id      = aws_subnet.pub_subnet_1b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_1a" {
  subnet_id      = aws_subnet.pri_subnet_1a.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_1b" {
  subnet_id      = aws_subnet.pri_subnet_1b.id
  route_table_id = aws_route_table.private.id
}

# EC2 Instance
resource "aws_instance" "flask_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.pri_subnet_1a.id
  key_name               = var.key_pair_name

  vpc_security_group_ids = [aws_security_group.app_sg.id]
  iam_instance_profile = data.aws_iam_role.existing_ssm_role.name

  tags = {
    Name = "App Server"
  }
  user_data = <<-EOF
      #!/bin/bash

      sudo yum update -y
      sudo yum remove python3 -y
      sudo amazon-linux-extras install python3.8
      sudo ln -s /usr/bin/python3.8 /usr/bin/python3
      sudo ln -s /usr/bin/pydoc3.8 /usr/bin/pydoc
      sudo yum install -y python3 python3-pip
      sudo yum install -y yum-utils
      sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
      sudo yum -y install terraform

      pip3 install flask
      pip3 install pydantic

      cat <<EOT > /home/ec2-user/server.py
          
      EOT

      cat <<EOT > /home/ec2-user/terraform_generator.py
          
      EOT

      # python3 /home/ec2-user/server.py
    EOF
}

# Security Group
resource "aws_security_group" "app_sg" {
  name        = "app-sg"
  description = "Security group for the application server"
  vpc_id      = aws_vpc.kg_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
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

  tags = {
    Name = "App Security Group"
  }
}

# Target Group
resource "aws_lb_target_group" "kg_tg" {
  name        = "app-tg"
  port        = 5000
  protocol    = "TCP"
  vpc_id      = aws_vpc.kg_vpc.id
  target_type = "instance"

  health_check {
    port     = 5000
    protocol = "TCP"
  }
}

resource "aws_lb_target_group_attachment" "kg_tg_attachment" {
  target_group_arn = aws_lb_target_group.kg_tg.arn
  target_id        = aws_instance.flask_server.id
  port             = 5000
}

# Network Load Balancer
resource "aws_lb" "app_nlb" {
  name               = "app-nlb"
  internal           = true
  load_balancer_type = "network"
  subnets            = [
    aws_subnet.pub_subnet_1a.id,
    aws_subnet.pub_subnet_1b.id
  ]

  enable_deletion_protection = false

  tags = {
    Name = "App NLB"
  }
}

# NLB Listener
resource "aws_lb_listener" "app_nlb_listener" {
  load_balancer_arn = aws_lb.app_nlb.arn
  port              = 5000
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.kg_tg.arn
  }
}

# VPC Link
resource "aws_api_gateway_vpc_link" "app_vpc_link" {
  name        = "app-vpc-link"
  description = "VPC Link for the application"
  target_arns = [aws_lb.app_nlb.arn]
  tags = {
    Name = "App VPC Link"
  }
}

# API Gateway
resource "aws_api_gateway_rest_api" "api" {
  name        = "WAF-Rules-Management "
  description = "API Gateway connected to EC2 instance"

  tags = {
    Name = "WAF-Rules-Management"
  }
}

# -------------------------------- resources ---------------------------------------
resource "aws_api_gateway_resource" "v1" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "v1"
  depends_on = [ aws_api_gateway_rest_api.api ]
}

resource "aws_api_gateway_resource" "waf" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "waf"
  depends_on = [ aws_api_gateway_resource.v1 ]
}

resource "aws_api_gateway_resource" "ip_blocks" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.waf.id
  path_part   = "ip-blocks"
  depends_on = [ aws_api_gateway_resource.waf ]
}

resource "aws_api_gateway_resource" "rules" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.waf.id
  path_part   = "rules"
  depends_on = [ aws_api_gateway_resource.waf ]
}

resource "aws_api_gateway_resource" "response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.rules.id
  path_part   = "response"
  depends_on = [ aws_api_gateway_resource.rules ]
}

# ------------------------------------- response  ---------------------------------
resource "aws_api_gateway_method" "post_response" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.response.id
  http_method   = "POST"
  authorization = "NONE"
  depends_on = [ aws_api_gateway_resource.response ]
}

resource "aws_api_gateway_method" "cors_options-response" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.response.id
  http_method   = "OPTIONS"
  authorization = "NONE"
  depends_on = [ aws_api_gateway_resource.response ]
}

resource "aws_api_gateway_integration" "post_response_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.response.id
  http_method             = aws_api_gateway_method.post_response.http_method
  integration_http_method = "POST"
  type                     = "HTTP"
  uri                      = "http://${aws_lb.app_nlb.dns_name}:5000/v1/waf/rules/response"
  connection_type         = "VPC_LINK"
  connection_id           = aws_api_gateway_vpc_link.app_vpc_link.id
  depends_on = [ aws_api_gateway_method.post_response ]
}

# ------------------------------------- ip-blocks ---------------------------------

resource "aws_api_gateway_method" "get_ip_blocks" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.ip_blocks.id
  http_method   = "GET"
  authorization = "NONE"
  depends_on = [ aws_api_gateway_resource.ip_blocks ]
}

resource "aws_api_gateway_method" "post_ip_blocks" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.ip_blocks.id
  http_method   = "POST"
  authorization = "NONE"
  depends_on = [ aws_api_gateway_resource.ip_blocks ]
}

resource "aws_api_gateway_method" "cors_options-ipblocks" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.ip_blocks.id
  http_method   = "OPTIONS"
  authorization = "NONE"
  depends_on = [ aws_api_gateway_resource.ip_blocks ]
}

resource "aws_api_gateway_integration" "get_ip_blocks_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.ip_blocks.id
  http_method             = aws_api_gateway_method.get_ip_blocks.http_method
  integration_http_method = "GET"
  type                    = "HTTP"
  uri                     = "http://${aws_lb.app_nlb.dns_name}:5000/v1/waf/ip-blocks"
  connection_type         = "VPC_LINK"
  connection_id           = aws_api_gateway_vpc_link.app_vpc_link.id
  depends_on = [ aws_api_gateway_method.get_ip_blocks ]
}

resource "aws_api_gateway_integration" "post_ip_blocks_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.ip_blocks.id
  http_method             = aws_api_gateway_method.post_ip_blocks.http_method
  integration_http_method = "POST"
  type                     = "HTTP"
  uri                      = "http://${aws_lb.app_nlb.dns_name}:5000/v1/waf/ip-blocks"
  connection_type         = "VPC_LINK"
  connection_id           = aws_api_gateway_vpc_link.app_vpc_link.id
  depends_on = [ aws_api_gateway_method.post_ip_blocks ]
}

resource "aws_api_gateway_integration" "cors_integration-ipblocks" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.ip_blocks.id
  http_method = aws_api_gateway_method.cors_options-ipblocks.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
  depends_on = [ aws_api_gateway_method.cors_options-ipblocks ]
}

resource "aws_api_gateway_method_response" "get_ip_blocks_response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.ip_blocks.id
  http_method = aws_api_gateway_method.get_ip_blocks.http_method
  status_code = "200"
  depends_on = [ aws_api_gateway_integration.get_ip_blocks_integration ]
}

resource "aws_api_gateway_method_response" "post_ip_blocks_response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.ip_blocks.id
  http_method = aws_api_gateway_method.post_ip_blocks.http_method
  status_code = "200"
  depends_on = [ aws_api_gateway_integration.post_ip_blocks_integration ]
}


resource "aws_api_gateway_method_response" "cors_method_response-ipblocks" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.ip_blocks.id
  http_method = aws_api_gateway_method.cors_options-ipblocks.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }

  depends_on = [ aws_api_gateway_integration.cors_integration-ipblocks ]
}

resource "aws_api_gateway_integration_response" "get_ip_blocks_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.ip_blocks.id
  http_method = aws_api_gateway_method.get_ip_blocks.http_method
  status_code = aws_api_gateway_method_response.get_ip_blocks_response.status_code
  
  depends_on = [ 
    aws_api_gateway_method_response.get_ip_blocks_response 
  ]
}

resource "aws_api_gateway_integration_response" "post_ip_blocks_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.ip_blocks.id
  http_method = aws_api_gateway_method.post_ip_blocks.http_method
  status_code = aws_api_gateway_method_response.post_ip_blocks_response.status_code
  depends_on = [ 
    aws_api_gateway_method_response.post_ip_blocks_response 
  ]
}


resource "aws_api_gateway_integration_response" "cors_integration_response-ipblocks" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.ip_blocks.id
  http_method = aws_api_gateway_method.cors_options-ipblocks.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
  depends_on = [ aws_api_gateway_method_response.cors_method_response-ipblocks ]
}

# -------------------------------------- rules ---------------------------------------------

resource "aws_api_gateway_method" "get_rules" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.rules.id
  http_method   = "GET"
  authorization = "NONE"
  depends_on = [ aws_api_gateway_resource.rules ]
}

resource "aws_api_gateway_method" "post_rules" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.rules.id
  http_method   = "POST"
  authorization = "NONE"
  depends_on = [ aws_api_gateway_resource.rules ]
}

resource "aws_api_gateway_method" "cors_options-rules" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.rules.id
  http_method   = "OPTIONS"
  authorization = "NONE"
  depends_on = [ aws_api_gateway_resource.rules ]
}


resource "aws_api_gateway_integration" "get_rules_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.rules.id
  http_method             = aws_api_gateway_method.get_rules.http_method
  integration_http_method = "GET"
  type                    = "HTTP"
  uri                     = "http://${aws_lb.app_nlb.dns_name}:5000/v1/waf/rules"

  connection_type         = "VPC_LINK"
  connection_id           = aws_api_gateway_vpc_link.app_vpc_link.id
  depends_on = [ aws_api_gateway_method.get_rules ]
}

resource "aws_api_gateway_integration" "post_rules_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.rules.id
  http_method             = aws_api_gateway_method.post_rules.http_method
  integration_http_method = "POST"
  type                    = "HTTP"
  uri                     = "http://${aws_lb.app_nlb.dns_name}:5000/v1/waf/rules"

  connection_type         = "VPC_LINK"
  connection_id           = aws_api_gateway_vpc_link.app_vpc_link.id
  depends_on = [ aws_api_gateway_method.post_rules ]    
}

resource "aws_api_gateway_integration" "cors_integration-rules" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.cors_options-ipblocks.http_method
  type        = "MOCK"


  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
  depends_on = [ aws_api_gateway_method.cors_options-rules ]
}



resource "aws_api_gateway_method_response" "get_rules_response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.get_rules.http_method
  status_code = "200"
  depends_on = [ aws_api_gateway_integration.get_rules_integration ]
}

resource "aws_api_gateway_method_response" "post_rules_response_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.post_rules.http_method
  status_code = "200"
  depends_on = [ aws_api_gateway_integration.post_rules_integration ]
}

resource "aws_api_gateway_method_response" "post_rules_response_400" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.post_rules.http_method
  status_code = "400"
  response_models = {
    "application/json" = "Error"
  }
  depends_on = [ aws_api_gateway_integration.post_rules_integration ]
}

resource "aws_api_gateway_method_response" "cors_method_response-rules" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.cors_options-rules.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
  depends_on = [ aws_api_gateway_integration.cors_integration-rules ]
}

resource "aws_api_gateway_integration_response" "get_rules_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.get_rules.http_method
  status_code = aws_api_gateway_method_response.get_rules_response.status_code
  depends_on = [  aws_api_gateway_method_response.get_rules_response ]
}

resource "aws_api_gateway_integration_response" "post_rules_integration_response_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.post_rules.http_method
  selection_pattern = "2\\d{2}"
  status_code = aws_api_gateway_method_response.post_rules_response_200.status_code
  depends_on = [ aws_api_gateway_method_response.post_rules_response_200 ]
}

resource "aws_api_gateway_integration_response" "post_rules_integration_response_400" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.post_rules.http_method
  selection_pattern = "4\\d{2}"
  status_code = aws_api_gateway_method_response.post_rules_response_400.status_code
  depends_on = [ aws_api_gateway_method_response.post_rules_response_400 ]
}

resource "aws_api_gateway_integration_response" "cors_integration_response-rules" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.cors_options-rules.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
  depends_on = [ aws_api_gateway_method_response.cors_method_response-rules ]
}


# deployment
# resource "aws_api_gateway_deployment" "deployment" {
#   rest_api_id = aws_api_gateway_rest_api.api.id
#   stage_name  = "waf-stage"
#   triggers = {
#     redeployment = sha1(jsonencode(aws_api_gateway_rest_api.api.id))
#   }
#   lifecycle {
#     create_before_destroy = true
#   }
#   depends_on = [
#       aws_api_gateway_integration.get_ip_blocks_integration, 
#       aws_api_gateway_integration.post_ip_blocks_integration,
#       aws_api_gateway_integration.cors_integration-ipblocks
#       ]
# }

resource "aws_api_gateway_deployment" "deployment2" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "waf-stage"
  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.api.id))
  }
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [
      aws_api_gateway_integration_response.get_rules_integration_response,
      aws_api_gateway_integration_response.post_rules_integration_response_200,
      aws_api_gateway_integration_response.post_rules_integration_response_400,
      aws_api_gateway_integration.cors_integration-rules
  ]
}

# ======================== S3 ==================================================

resource "aws_s3_bucket" "kg_frontend_bucket" {
  bucket = "waf-manager-storing-user-data"  

  tags = {
    Name        = "kg-s3"
    Environment = "Dev"
  }
}

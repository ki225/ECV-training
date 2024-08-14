# main.tf
provider "aws" {
  region = var.region
}

resource "aws_internet_gateway" "kg_igw" {
  vpc_id = data.aws_vpc.kg_vpc.id

  tags = {
    Name = "kg_igw"
  }
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat_eip" {
  domain = "vpc"
  depends_on = [aws_internet_gateway.kg_igw]
}

# NAT Gateway Resource
resource "aws_nat_gateway" "kg_nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = data.aws_subnet.pub_subnet_1a.id  # Assuming we want to place it in the first public subnet

  tags = {
    Name = "kg_nat"
  }

  depends_on = [aws_internet_gateway.kg_igw]
}

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = data.aws_vpc.kg_vpc.id

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
  vpc_id = data.aws_vpc.kg_vpc.id

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
  subnet_id      = data.aws_subnet.pub_subnet_1a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_1b" {
  subnet_id      = data.aws_subnet.pub_subnet_1b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_1a" {
  subnet_id      = data.aws_subnet.pri_subnet_1a.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_1b" {
  subnet_id      = data.aws_subnet.pri_subnet_1b.id
  route_table_id = aws_route_table.private.id
}

# EC2 Instance
resource "aws_instance" "flask_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = data.aws_subnet.pri_subnet_1a

  vpc_security_group_ids = [aws_security_group.app_sg.id]

  tags = {
    Name = "App Server"
  }
}

# Security Group
resource "aws_security_group" "app_sg" {
  name        = "app-sg"
  description = "Security group for the application server"
  vpc_id      = data.aws_vpc.kg_vpc.id

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
resource "aws_lb_target_group" "app_tg" {
  name        = "app-tg"
  port        = 5000
  protocol    = "TCP"
  vpc_id      = data.aws_vpc.kg_vpc.id
  target_type = "ip"

  health_check {
    port     = 5000
    protocol = "TCP"
  }
}

# Target Group Attachment
resource "aws_lb_target_group_attachment" "app_tg_attachment" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = aws_instance.flask_server.private_ip
  port             = 5000
}

# Network Load Balancer
resource "aws_lb" "app_nlb" {
  name               = "app-nlb"
  internal           = true
  load_balancer_type = "network"
  subnets            = [data.aws_subnet.pub_subnet_1a, data.aws_subnet.pub_subnet_1b]

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
    target_group_arn = aws_lb_target_group.app_tg.arn
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
resource "aws_api_gateway_resource" "v2" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "v2"
  depends_on = [ aws_api_gateway_rest_api.api ]
}

resource "aws_api_gateway_resource" "waf" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.v2.id
  path_part   = "waf"
  depends_on = [ aws_api_gateway_resource.v2 ]
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
  type                     = "HTTP_PROXY"
  uri                      = "http://${data.aws_instance.flask-server.public_ip}:5000/v2/waf/ip-blocks"
  depends_on = [ aws_api_gateway_method.get_ip_blocks ]
}

resource "aws_api_gateway_integration" "post_ip_blocks_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.ip_blocks.id
  http_method             = aws_api_gateway_method.post_ip_blocks.http_method
  integration_http_method = "POST"
  type                     = "HTTP_PROXY"
  uri                      = "http://${data.aws_instance.flask-server.public_ip}:5000/v2/waf/ip-blocks"
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
  type                     = "HTTP_PROXY"
  uri                      = "http://${data.aws_instance.flask-server.public_ip}:5000/v2/waf/rules"
  depends_on = [ aws_api_gateway_method.get_rules ]
}

resource "aws_api_gateway_integration" "post_rules_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.rules.id
  http_method             = aws_api_gateway_method.post_rules.http_method
  integration_http_method = "POST"
  type                     = "HTTP_PROXY"
  uri                      = "http://${data.aws_instance.flask-server.public_ip}:5000/v2/waf/rules"
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

resource "aws_api_gateway_method_response" "post_rules_response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.post_rules.http_method
  status_code = "200"
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

resource "aws_api_gateway_integration_response" "post_rules_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.rules.id
  http_method = aws_api_gateway_method.post_rules.http_method
  status_code = aws_api_gateway_method_response.post_rules_response.status_code
  depends_on = [ aws_api_gateway_method_response.post_rules_response ]
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
resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "waf-stage"
  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.api.id))
  }
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [
      aws_api_gateway_integration.get_ip_blocks_integration, 
      aws_api_gateway_integration.post_ip_blocks_integration,
      aws_api_gateway_integration.cors_integration-ipblocks
      ]
}

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
      aws_api_gateway_integration_response.post_rules_integration_response,
      aws_api_gateway_integration.cors_integration-rules
  ]
}
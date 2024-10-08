provider "aws" {
  region = "us-east-1"  
}

# --------------------------------- vpc ----------------------------------------------

data "aws_vpc" "selected_vpc" {
  filter {
    name   = "tag:Name"
    values = ["<VPC_NAME>"]  
  }
}

data "aws_subnet" "selected_subnet" {
  filter {
    name   = "tag:Name"
    values = ["<SUBNET_NAME>"] 
  }
}

# ------------------------------- ec2 -------------------------------------------------

data "aws_instance" "flask-server" {
  filter {
    name   = "instance-id"
    values = ["<INSTANCE_ID>"] 
  }
}

data "aws_security_group" "selected_security_group" {
  id = "<SG_ID>"
}

# --------------------------------- apigw ------------------------------------------------

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

resource "aws_api_gateway_integration" "get_ip_blocks_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.ip_blocks.id
  http_method             = aws_api_gateway_method.get_ip_blocks.http_method
  integration_http_method = "GET"
  type                     = "HTTP_PROXY"
  uri                      = "http://${data.aws_instance.flask-server.public_ip}:5000/v1/waf/ip-blocks"
  depends_on = [ aws_api_gateway_method.get_ip_blocks ]
}

resource "aws_api_gateway_integration" "post_ip_blocks_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.ip_blocks.id
  http_method             = aws_api_gateway_method.post_ip_blocks.http_method
  integration_http_method = "POST"
  type                     = "HTTP_PROXY"
  uri                      = "http://${data.aws_instance.flask-server.public_ip}:5000/v1/waf/ip-blocks"
  depends_on = [ aws_api_gateway_method.post_ip_blocks ]
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
      aws_api_gateway_integration.post_ip_blocks_integration
      ]
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


resource "aws_api_gateway_integration" "get_rules_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.rules.id
  http_method             = aws_api_gateway_method.get_rules.http_method
  integration_http_method = "GET"
  type                     = "HTTP_PROXY"
  uri                      = "http://${data.aws_instance.flask-server.public_ip}:5000/v1/waf/rules"
  depends_on = [ aws_api_gateway_method.get_rules ]
}

resource "aws_api_gateway_integration" "post_rules_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.rules.id
  http_method             = aws_api_gateway_method.post_rules.http_method
  integration_http_method = "POST"
  type                     = "HTTP_PROXY"
  uri                      = "http://${data.aws_instance.flask-server.public_ip}:5000/v1/waf/rules"
  depends_on = [ aws_api_gateway_method.post_rules ]    
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
      aws_api_gateway_integration_response.post_rules_integration_response
  ]
}
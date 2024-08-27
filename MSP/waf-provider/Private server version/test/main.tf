# main.tf
provider "aws" {
  region = var.region
}

resource "aws_iam_role" "ec2_ssm_role" {
  name = "ec2_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ec2_ssm_policy_attachment" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn  = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}


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

# NAT Gateway Resource
resource "aws_nat_gateway" "kg_nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.pub_subnet_1a.id  # Assuming we want to place it in the first public subnet

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

resource "aws_iam_instance_profile" "ec2_ssm_instance_profile" {
  name = "ec2_ssm_instance_profile"
  role = aws_iam_role.ec2_ssm_role.name
}

# EC2 Instance
resource "aws_instance" "flask_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.pri_subnet_1a.id

  iam_instance_profile = aws_iam_instance_profile.ec2_ssm_instance_profile.name
  key_name      = var.key_pair

  vpc_security_group_ids = [aws_security_group.app_sg.id]

  tags = {
    Name = "App Server"
  }
  // update python to be 3.8 so that we can use "from typing import List, Literal, Optional, Union, Dict, Any"
  // https://repost.aws/questions/QUtA3qNBaLSvWPfD5kFwI0_w/python-3-10-on-ec2-running-amazon-linux-2-and-the-openssl-upgrade-requirement
  user_data = <<-EOF
      #!/bin/bash

      sudo yum update -y
      sudo yum install -y python3 python3-pip
      sudo pip3 install pydantic
      sudo yum update -y
      sudo amazon-linux-extras install python3.8
      pip3 install flask

      cat <<EOT > /home/ec2-user/server.py
          from flask import Flask, request, jsonify
          from datetime import datetime
          import re

          server = Flask(__name__)
          ip_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
          rules_data = {}
          blocked_ips = []
          reasons = []
          last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

          def match_regex(string, pattern):
              return bool(re.match(pattern, string))


          @server.route('/', methods=['GET'])
          def health_check():
              return jsonify({"message": "healthy", "status": "success"}), 200



          # PUT
          @server.route('/v1/waf/rules', methods=['PUT'])
          def update_rules():
              # Get the JSON data from the request
              if not request.data:
                  return jsonify({"message": "No data received", "status": "error"}), 400

              try:
                  recv_data = request.get_json()
              except:
                  return jsonify({"message": "Error parsing JSON", "status": "error"}), 400

              # Validate the data
              if not all(key in recv_data for key in ('accountId', 'rulesToUpdate')):
                  return jsonify({"message": "Error parsing data", "status": "error"}), 400

              for key, val in recv_data.items():
                  print(key, val)
                  if key == 'accountId' and not match_regex(str(val), r'\d{12}') :
                      return jsonify({"message": "Error parsing accountid", "status": "error"}), 400

                  elif key == 'rulesToUpdate':
                      for rules in val:
                          if  not all(rule_key in rules for rule_key in ('id', 'action')) or\
                              not match_regex(str(rules['id']), r'0|[1-9]\d*') or\
                              not match_regex(str(rules['action']), r'allow|block|count'):
                                  return jsonify({"message": "Error parsing rules", "status": "error"}), 400

              # Successful process
              success_responce = {
                  "status": "success",

                  "data": {
                    **recv_data,
                    "UpdatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                  }
              }

              return jsonify(success_responce), 200

          @server.route('/v1/waf/ip-blocks', methods=['PUT'])
          def update_ip():
              # Get the JSON data from the request
              if not request.data:
                  return jsonify({"message": "No data received", "status": "error"}), 400

              try:
                  recv_data = request.get_json()
              except:
                  return jsonify({"message": "Error parsing JSON", "status": "error"}), 400

              # Validate the data
              if not all(key in recv_data for key in ('original', 'ip')):
                  return jsonify({"message": "Error parsing data", "status": "error"}), 400

              if not match_regex(str(recv_data['original']), ip_regex):
                  return jsonify({"message": "Error parsing original ip", "status": "error"}), 400

              if not match_regex(str(recv_data['ip']), ip_regex):
                  return jsonify({"message": "Error parsing updated ip", "status": "error"}), 400

              # Successful process
              success_responce = {
                  "status": "success",
                  "message": "IP in block list is successfully updated",
                  "data": {
                    **recv_data,
                    "UpdatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                  }
              }
              return jsonify(success_responce), 200

          # GET, POST, DELETE(use method POST)
          @server.route('/v1/waf/rules', methods=['GET', 'POST'])
          def rule_ip():
              global last_updated

              if request.method == 'POST':
                  if not request.data:
                      return jsonify({"message": "No data received", "status": "error"}), 400
                  try:
                      new_data = request.get_json()
                  except:
                      return jsonify({"message": "Error parsing JSON", "status": "error"}), 400

                  if new_data:
                      # Delete rules
                      if 'rulesToDelete' in new_data:
                          # Validate the data
                          if not all(key in new_data for key in ('accountId', 'rulesToDelete')):
                              return jsonify({"message": "Error parsing data", "status": "error"}), 400

                          for key, val in new_data.items():
                              print(key, val)
                              if key == 'accountId' and not match_regex(str(val), r'\d{12}') :
                                  return jsonify({"message": "Error parsing accountid", "status": "error"}), 400

                              elif key == 'rulesToDelete':
                                  for rule_id in val:
                                      if not match_regex(str(rule_id), r'0|[1-9]\d*'):
                                          return jsonify({"message": "Error parsing rule ids", "status": "error"}), 400
                                      # delete
                                      rules_dict = rules_data[new_data["accountId"]]
                                      del rules_dict[rule_id]

                          # Successful process
                          success_responce = {
                              "status": "success",

                              "data": {
                                **new_data,
                                "DeletedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                              }
                          }

                          return jsonify(success_responce), 200

                      # Deploy rules
                      elif 'rulesToDeploy' in new_data:
                          account_id = new_data["accountId"]
                          if account_id in rules_data:
                              rules_dict = rules_data[account_id]
                          else:
                              rules_dict = {}
                          for rule in new_data["rulesToDeploy"]:
                              rules_dict[rule["id"]] = rule["action"]

                          rules_data[account_id] = rules_dict

                          # output what we got
                          return jsonify({
                                          "status": "success",
                                          "data": {
                                              "accountId": new_data["accountId"],
                                              "rulesToDeploy": new_data["rulesToDeploy"],
                                              "deployedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                                              }
                                          }), 200
                      else: jsonify({"message": "Header missing", "status": "error"}), 400
                  else:
                      return jsonify({"message": "Invalid rule format", "status": "error"}), 400

              elif request.method == 'GET':
                  return jsonify({"data": rules_data}) # output all we have


          @server.route('/v1/waf/ip-blocks', methods=['GET', 'POST'])
          def block_ip():
              global last_updated
              if request.method == 'POST':
                  # Get the JSON data from the request
                  if not request.data:
                      return jsonify({"message": "No data received", "status": "error"}), 400

                  try:
                      new_data = request.get_json()
                  except:
                      return jsonify({"message": "Error parsing JSON", "status": "error"}), 400

                  if 'action' in new_data and 'delete' == new_data['action']:
                      # Validate the data
                      if 'ip' not in new_data.keys():
                          return jsonify({"message": "Missing ip", "status": "error"}), 400

                      if not match_regex(str(new_data['ip']), ip_regex):
                          return jsonify({"message": "Error parsing ip", "status": "error"}), 400

                      # Successful process
                      success_responce = {
                          "status": "success",
                          "message": "IP successfully removed from block list",
                          "data": {
                            **new_data,
                            "RemovedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                          }
                      }

                      return jsonify(success_responce), 200

                  else:
                      if new_data and "ip" in new_data and "reason" in new_data:
                          last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                          blocked_ips.append(new_data["ip"])
                          reasons.append(new_data["reason"])
                          return jsonify({
                                          "status": "success",
                                          "message": "IP successfully added to block list",
                                          "data": {
                                                  "ip": new_data["ip"],
                                                  "reason": new_data["reason"],
                                                  "addedAt": last_updated
                                              }
                                          }), 200
                      elif new_data and "ip" in new_data:
                          last_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                          blocked_ips.append(new_data["ip"])
                          return jsonify({
                                          "status": "success",
                                          "message": "IP successfully added to block list",
                                          "data": {
                                                  "ip": new_data["ip"],
                                                  "addedAt": last_updated
                                              }
                                          }), 200
                      else:
                          return jsonify({"message": "Invalid IP address format", "status": "error"}), 500

              elif request.method == 'GET':
                  if reasons:
                      return jsonify({
                          "status": "success",
                          "data": {
                              "blockedIPs": blocked_ips,
                              "reasons": reasons,
                              "lastUpdated": last_updated
                          }
                      }), 200
                  elif blocked_ips: # HTTP methods POST and DELETE should includes ip
                      return jsonify({
                          "status": "success",
                          "data": {
                              "blockedIPs": blocked_ips,
                              "lastUpdated": last_updated
                          }
                      }), 200
                  else:
                      return jsonify({
                          "status": "error",
                          "data": {
                              "messages": "Failed to retrieve IP block list"
                          }
                      }), 500

          @server.after_request
          def add_header(response):
              response.headers['Access-Control-Allow-Origin'] = 'http://kg-bucket.s3-website-us-east-1.amazonaws.com'
              return response

          if __name__ == '__main__':
              server.run(host='0.0.0.0', port=5000)
      EOT

      # Run the Flask application (this will run on startup)
      python3 /home/ec2-user/server.py
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
  uri                      = "http://${aws_lb.app_nlb.dns_name}:5000/v2/waf/ip-blocks"
  depends_on = [ aws_api_gateway_method.get_ip_blocks ]
}

resource "aws_api_gateway_integration" "post_ip_blocks_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.ip_blocks.id
  http_method             = aws_api_gateway_method.post_ip_blocks.http_method
  integration_http_method = "POST"
  type                     = "HTTP_PROXY"
  uri                      = "http://${aws_lb.app_nlb.dns_name}:5000/v2/waf/ip-blocks"
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
  type                    = "HTTP_PROXY"
  uri                     = "http://${aws_lb.app_nlb.dns_name}:5000/v2/waf/rules"
  depends_on = [ aws_api_gateway_method.get_rules ]
}

resource "aws_api_gateway_integration" "post_rules_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.rules.id
  http_method             = aws_api_gateway_method.post_rules.http_method
  integration_http_method = "POST"
  type                    = "HTTP_PROXY"
  uri                     = "http://${aws_lb.app_nlb.dns_name}:5000/v2/waf/rules"
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


# variables.tf
# terraform apply -var="region=us-west-2" -var="stage_name=dev" -var="backend_url=https://your-backend-url.com"

variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for the private subnets"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  default     = "ami-03972092c42e8c0ca"  # Replace with your desired AMI
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  default     = "t2.micro"
}

variable "stage_name" {
  description = "The name of the API Gateway stage"
  type        = string
  default     = "dev"
}

variable "flask_port" {
  description = "Port for the Flask server"
  type        = number
  default     = 5000
}

variable "key_pair" {
  description = "The name of the EC2 key pair to use for SSH access."
  type        = string
}


locals {
  api_gateway_url = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.region}.amazonaws.com/${var.stage_name}:5000/"
}

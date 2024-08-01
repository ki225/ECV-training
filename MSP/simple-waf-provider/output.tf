output "api_url_rules" {
  value = "${aws_api_gateway_rest_api.api.execution_arn}/waf-stage/v1/waf/rules"
}

output "api_url_ip-blocks" {
  value = "${aws_api_gateway_rest_api.api.execution_arn}/waf-stage/v1/waf/ip-blocks"
}

output "vpc_id" {
  value = data.aws_vpc.selected_vpc.id
}

output "subnet_id" {
  value = data.aws_subnet.selected_subnet.id
}

output "instance_id" {
  value = data.aws_instance.flask-server.id
}

output "instance_type" {
  value = data.aws_instance.flask-server.instance_type
}

output "security_group_id" {
  value = data.aws_security_group.selected_security_group.id
}

output "security_group_name" {
  value = data.aws_security_group.selected_security_group.name
}

output "instance_public_ip" {
  value = data.aws_instance.flask-server.public_ip
}

# outputs.tf

output "s3_bucket_url" {
  value ="http://${data.aws_caller_identity.kg_identity.account_id}.s3-control.${var.region}.amazonaws.com"
  description = "The URL of the S3 bucket."
}

output "ec2_private_ip" {
  value       = aws_instance.flask_server.private_ip
  description = "The private IP address of the EC2 instance"
}

output "api_gateway_url_rules" {
  value       = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.region}.amazonaws.com/${var.stage_name}:5000/v2/waf/rules"
  description = "The URL to invoke the API Gateway endpoint with rules"
}

output "api_gateway_url_ip_blocks" {
  value       = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.region}.amazonaws.com/${var.stage_name}:5000/v2/waf/ip-blocks"
  description = "The URL to invoke the API Gateway endpoint with IPs should be blocked"
}

output "api_gateway_url_check_health" {
  value       = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.region}.amazonaws.com/${var.stage_name}:5000/"
  description = "The URL that target group check for health"
}
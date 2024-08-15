provider "aws" {
  alias  = "customer"
  region = "us-east-1"
  assume_role {
    role_arn = "<CUSTOMER_ADMIN_ROLE_ARN>"
  }
}

data "aws_lb" "target_alb" {
  provider = aws.customer
  name     = var.alb_name
}

variable "alb_name" {
  type        = string
  description = "Name of the ALB in Account B"
}

variable "region" {
  description = "AWS region for regional resources (ignored for CLOUDFRONT scope)"
  type        = string
  default     = null
}

# Variables
variable "customer_name" {
  description = "customer's name"
  type        = string
}

variable "scope" {
  description = "WAF's scope (CLOUDFRONT or REGIONAL)"
  type        = string
  validation {
    condition     = contains(["CLOUDFRONT", "REGIONAL"], var.scope)
    error_message = "Scope must be either CLOUDFRONT or REGIONAL."
  }
}

variable "waf_description" {
  description = "waf's desciption"
  type        = string
  validation {
    condition     = can(regex("^[\\w+=:#@/\\-,.][\\w+=:#@/\\-,.\\s]+[\\w+=:#@/\\-,.]$", var.waf_description))
    error_message = "The WAF description must start and end with a letter or number, and can contain only alphanumeric characters, hyphens (-), periods (.), and spaces. It must be between 1 and 256 characters."
  }
}

# AWS WAF WebACL
resource "aws_wafv2_web_acl" "customer_waf_acl" {
  provider = aws.customer
  name        = "${var.customer_name}-waf-acl"
  description = "${var.waf_description}"
  scope       = "${var.scope}"

  default_action {
    allow {}
  }

  # Example rule to block requests from a specific IP set
  rule {
    name     = "block-ip-set"
    priority = 1

    action {
      block {}
    }

    statement {
      ip_set_reference_statement {
        arn = aws_wafv2_ip_set.customer_waf_ipset.arn
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "BlockIPSetRule"
      sampled_requests_enabled   = true
    }
  }
  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.customer_name}WAFACL"
    sampled_requests_enabled   = true
  }
}

# Example IP Set (you can modify this as needed)
resource "aws_wafv2_ip_set" "customer_waf_ipset" {
    provider = aws.customer
  name               = "${var.customer_name}-ip-set"
  description        = "${var.customer_name} IP set"
  scope              = "${var.scope}"
  ip_address_version = "IPV4"
  addresses          = ["192.0.2.0/24", "198.51.100.0/24"]  # Example IP ranges
}

resource "aws_wafv2_web_acl_association" "waf_association" {
  provider = aws.customer
  resource_arn = data.aws_lb.target_alb.arn
  web_acl_arn  = aws_wafv2_web_acl.customer_waf_acl.arn
}

# Output the WebACL ID
output "web_acl_id" {
  value = aws_wafv2_web_acl.customer_waf_acl.id
}

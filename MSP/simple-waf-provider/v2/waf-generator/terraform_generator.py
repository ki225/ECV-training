# Generate a Terraform file based on the received data.
import subprocess
import tempfile
import uuid

def generate_terraform_file(data):
    """Generate a Terraform file for WAF rules based on the received data."""
    resource_type = data.get('resource_type', 'cloudfront')
    resource_arn = data.get('resource_arn', '')
    regex_patterns = data.get('regex_patterns', [])
    
    # Generate a unique name for the WAF resources
    waf_name = f"waf-{uuid.uuid4().hex[:8]}"
    
    tf_content = f"""
    resource "aws_wafv2_web_acl" "{waf_name}" {{
      name  = "{waf_name}"
      scope = "{resource_type}"

      default_action {{
        allow {{}}
      }}

      rule {{
        name     = "{waf_name}-rule"
        priority = 1

        action {{
          block {{}}
        }}

        statement {{
          regex_pattern_set_reference_statement {{
            arn = aws_wafv2_regex_pattern_set.{waf_name}.arn
            field_to_match {{
              uri_path {{}}
            }}
            text_transformation {{
              priority = 1
              type     = "NONE"
            }}
          }}
        }}

        visibility_config {{
          cloudwatch_metrics_enabled = true
          metric_name                = "{waf_name}-rule-metric"
          sampled_requests_enabled   = true
        }}
      }}

      visibility_config {{
        cloudwatch_metrics_enabled = true
        metric_name                = "{waf_name}-metric"
        sampled_requests_enabled   = true
      }}
    }}

    resource "aws_wafv2_regex_pattern_set" "{waf_name}" {{
      name  = "{waf_name}-pattern-set"
      scope = "{resource_type}"

      regular_expression {{
        regex_string = "${' | '.join(regex_patterns)}"
      }}
    }}

    resource "aws_wafv2_web_acl_association" "{waf_name}" {{
      resource_arn = "{resource_arn}"
      web_acl_arn  = aws_wafv2_web_acl.{waf_name}.arn
    }}

    output "web_acl_id" {{
      value = aws_wafv2_web_acl.{waf_name}.id
    }}
    """
    return tf_content
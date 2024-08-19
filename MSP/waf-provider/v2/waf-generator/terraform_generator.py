# Generate a Terraform file based on the received data.
import json
import os

def generate_terraform(config):
    config = json.loads(config)
    customer_credential = ""
    terraform_config = f"""

    # AWS Provider

provider "aws" {{
  alias  = "customer"
  region = "us-east-1"
  assume_role {{
    role_arn = "{customer_credential}"
  }}
}}


resource "aws_wafv2_web_acl" "{config['name']}" {{
  name        = "{config['name']}"
  description = "{config['description']}"
  scope       = "{config['scope']}"

  default_action {{
    {config['default_action']} {{}}
  }}

  visibility_config {{
    cloudwatch_metrics_enabled = true
    metric_name                = "{config['name']}-metric"
    sampled_requests_enabled   = true
  }}

  {generate_rules(config['rules'])}
}}
"""
    return terraform_config

def generate_rules(rules):
    rule_configs = []
    for rule in rules:
        if rule['type'] == 'managed':
            rule_configs.append(generate_managed_rule(rule))
        elif rule['type'] == 'custom':
            rule_configs.append(generate_custom_rule(rule))
    return "\n".join(rule_configs)

def generate_managed_rule(rule):
    return f"""
  rule {{
    name     = "{rule['name']}"
    priority = {rule['priority']}

    override_action {{
      {rule['override_action']} {{}}
    }}

    statement {{
      managed_rule_group_statement {{
        name        = "{rule['rule_group_name']}"
        vendor_name = "{rule['vendor_name']}"
      }}
    }}

    visibility_config {{
      cloudwatch_metrics_enabled = true
      metric_name                = "{rule['name']}-metric"
      sampled_requests_enabled   = true
    }}
  }}
"""

def generate_custom_rule(rule):
    return f"""
  rule {{
    name     = "{rule['name']}"
    priority = {rule['priority']}

    action {{
      {rule['action']} {{}}
    }}

    visibility_config {{
      cloudwatch_metrics_enabled = true
      metric_name                = "{rule['metric_name']}"
      sampled_requests_enabled   = true
    }}

    statement {{
      {generate_statement(rule['statement'])}
    }}

    {generate_rule_labels(rule.get('labels', []))}
  }}
"""

def generate_rule_labels(labels):
    if not labels:
        return ""
    label_strings = [f'{{key = "{label["key"]}"}}' for label in labels]
    return f"""
    rule_labels {{
      {" ".join(label_strings)}
    }}
"""

# ========================================================================

def generate_statement(statement): # config['rules']['rule_created']['Statement']['Statement_type']
    if statement['Statement_type'] == "Match":
        return 
    elif statement['Statement_type'] == "Or":
        return f"""
        "OrStatement" :{
        "Statements": [
          {
            ${normal_statement} or ${not_statement} 
          },
          {
          }        
        ]
      }

        
        """
    elif statement['Statement_type'] == "And":
        return f"""
        "AndStatement" :{
        "Statements": [
          {
            ${normal_statement} or ${not_statement} 
          },
          {
          }        
        ]
      }
        """
    elif statement['Statement_type'] == "Not":
        return f"""
        "NotStatement": {
          "Statement": {
            {generate_matchType(statement['MatchType'])}
          }
        }
        
        """
    elif statement['Statement_type'] == "RateBased":
        return f"""
        "RateBasedStatement": {{
            "Limit": {statement["RateBased"]["Limit"]}, 
            "EvaluationWindowSec": {statement["RateBased"]["EvaluationWindowSec"]}, 
            "AggregateKeyType": "FORWARDED_IP", 
            ${rate_type}
        }}
        """
        
def generate_matchType(MatchType): # config['rules']['rule_created']['Statement']['Statement_type']['MatchType']['Match_type']
    if MatchType['Match_type'] == "originCountry-sourceIp":
        return f"""
        "GeoMatchStatement": {
            "CountryCodes": [ 
                {MatchType["originCountry-sourceIp"]["CountryCodes"] }
            ]
        }
        """
    elif MatchType['Match_type'] == "originCountry-ipHeader":
        return f"""
        "GeoMatchStatement": {
            "CountryCodes": [ 
                {MatchType["originCountry-ipHeader"]["CountryCodes"]}
            ],
            "ForwardedIPConfig": {
                "HeaderName": "X-Forwarded-For",
                "FallbackBehavior": {MatchType["originCountry-ipHeader"]["FallbackBehavior"]}
            }
        }
        """
    elif MatchType['Match_type'] == "originIp-sourceIp":
        return f"""
        "IPSetReferenceStatement": { 
            "ARN": {MatchType["originIp-sourceIp"]["IPSetReferenceStatement"]} 
        }
        """
    elif MatchType['Match_type'] == "originIp-ipHeader":
        return f"""
        "IPSetReferenceStatement": {{ 
            "ARN": {MatchType["originIp-ipHeader"]["ARN"]}
            "IPSetForwardedIPConfig": {{
                "HeaderName": "X-Forwarded-For",
                "FallbackBehavior": {MatchType["originIp-ipHeader"]["ARN"]["IPSetForwardedIPConfig"]["FallbackBehavior"]},
                "Position": {MatchType["originIp-ipHeader"]["ARN"]["IPSetForwardedIPConfig"]["Position"]}
            }}
        }}

        """
    elif MatchType['Match_type'] == "label-label":
        return f"""
        "LabelMatchStatement": {
            "Scope": "LABEL",
            "Key":  {MatchType["label-label"]["LabelMatchStatement"]["Key"]}
        }
        """
    elif MatchType['Match_type'] == "label-nameSpace":
        return f"""
        "LabelMatchStatement": {
            "Scope": "NAMESPACE",
            "Key": {MatchType["label-label"]["label-nameSpace"]["Key"]}
        }
        """
    elif MatchType['Match_type'] == "String-match-condition":
        return f"""
        "ByteMatchStatement": {{
          "FieldToMatch": {
              {generate_inspect()}
          },
          "PositionalConstraint":  {MatchType["String-match-condition"]["PositionalConstraint"]}
          "SearchString": {MatchType["String-match-condition"]["PositionalConstraint"]},
          "TextTransformations": [ 
              {
                  "Type": "COMPRESS_WHITE_SPACE", //NONE/COMPRESS_WHITE_SPACE/HTML_ENTITY_DECODE/LOWERCASE/CMD_LINE/URL_DECODE          //BASE64_DECODE/HEX_DECODE/MD5/REPLACE_COMMENTS/ESCAPE_SEQ_DECODE/           //SQL_HEX_DECODE/CSS_DECODE/JS_DECODE/NORMALIZE_PATH/NORMALIZE_PATH_WIN/            //REMOVE_NULLS/REPLACE_NULLS/BASE64_DECODE_EXT/URL_DECODE_UNI/UTF8_TO_UNICODE
                  "Priority": 0
              }
          ]
      }}
        """
    elif MatchType['Match_type'] == "regexSet":
        return f"""
        "RegexPatternSetReferenceStatement": {{
            "FieldToMatch": {
                {generate_inspect()}
            },
            "ARN": {MatchType["regexSet"]["ARN"]}
            "TextTransformations": [
                {
                    "Type": "NONE",
                    "Priority": 0
                }
            ]
        }}

        """
    elif MatchType['Match_type'] == "regex":
        return f"""
        "RegexMatchStatement": {{
            "FieldToMatch": {
                {generate_inspect()}
            },
            "TextTransformations": [ 
                {
                    "Type": "NONE",
                    "Priority": 0
                }
            ],
            "RegexString": "string" // self defined
        }}

        """
    
    elif MatchType['Match_type'] == "Size-match-condition":
        return f"""
        "SizeConstraintStatement": {{
          "FieldToMatch": {
              {generate_inspect()}
          },
          "ComparisonOperator": {MatchType["sqli"]["ComparisonOperator"]}
          "Size": {MatchType["sqli"]["Size"]},
          "TextTransformations": [ // multiple up to 10
              {
                  "Type": "NONE",
                  "Priority": 0
              }
          ]
      }}
        """
    elif MatchType['Match_type'] == "sqli":
        return f"""
        "SqliMatchStatement": {{
          "FieldToMatch": {
              {generate_inspect()}
          },
          "TextTransformations": [ // multiple up to 10
              {
                  "Type": "NONE",
                  "Priority": 0
              }
          ],
          "SensitivityLevel":  {MatchType["sqli"]["SensitivityLevel"]}
      }}
        """
    elif MatchType['Match_type'] == "xss":
        return f"""
        "XssMatchStatement": {{
          "FieldToMatch": {
              {generate_inspect()}
          },
          "TextTransformations": [ // multiple up to 10
              {
                  "Type": "NONE",
                  "Priority": 0
              }
          ]
      }}
        """

def generate_inspect(Inspect): # config['rules']['rule_created']['Statement']['Statement_type']['MatchType']['Match_type']['Inspect']
    if Inspect['Inspect_type'] == "SingleHeader":
        return f"""       
        "SingleHeader": {
            "Name": {Inspect['SingleHeader'] ['name']}
        }
        """
    elif Inspect['Inspect_type'] == "Headers":
        return f"""
        "Headers": {{
            "MatchScope": "{Inspect["Headers"]['MatchScope']}",
            "MatchPattern": {Inspect["Headers"]['MatchPattern']},
            "OversizeHandling": "{Inspect["Headers"]['OversizeHandling']}"
        }}
        """
    elif Inspect['Inspect_type'] == "Cookies":
        return f"""
        "Cookies": {{
            "MatchScope": "{Inspect["Cookies"]['MatchScope']}",
            "MatchPattern": {Inspect["Cookies"]['MatchPattern']},
            "OversizeHandling": "{Inspect["Cookies"]['OversizeHandling']}"
        }}
        """
    elif Inspect['Inspect_type'] == "SingleQueryArgument":
        return f"""
        "SingleQueryArgument": {{
            "Name": "{Inspect["SingleQueryArgument"]['Name']}"
        }}
        """
    elif Inspect['Inspect_type'] == "AllQueryArguments":
        return '"AllQueryArguments": {}'
    elif Inspect['Inspect_type'] == "UriPath":
        return '"UriPath": {}'
    elif Inspect['Inspect_type'] == "QueryString":
        return '"QueryString": {}'
    elif Inspect['Inspect_type'] == "Body":
        return f"""
        "Body": {{
            "OversizeHandling": "{Inspect["Body"]['OversizeHandling']}"
        }}
        """
    elif Inspect['Inspect_type'] == "JsonBody":
        invalid_fallback = f'"InvalidFallbackBehavior": "{Inspect["JsonBody"]["InvalidFallbackBehavior"]}",' if 'InvalidFallbackBehavior' in Inspect else ""
        return f"""
        "JsonBody": {{
            "MatchScope": "{Inspect["JsonBody"]['MatchScope']}",
            {invalid_fallback}
            "MatchPattern": {Inspect["JsonBody"]['MatchPattern']},
            "OversizeHandling": "{Inspect["JsonBody"]['OversizeHandling']}"
        }}
        """
    elif Inspect['Inspect_type'] == "JA3Fingerprint":
        return f"""
        "JA3Fingerprint": {{
            "FallbackBehavior": "{Inspect["JA3Fingerprint"]['FallbackBehavior']}"
        }}
        """
    elif Inspect['Inspect_type'] == "HeaderOrder":
        return f"""
        "HeaderOrder": {{
            "OversizeHandling": "{Inspect["HeaderOrder"]['OversizeHandling']}"
        }}
        """
    elif Inspect['Inspect_type'] == "Http":
        return '"Method": {}'
    else:
        return f"// Unsupported inspect type"
        



if __name__ == '__main__':
    config = """

    {
        "resource": {
            "type": "load balancer",
            "region": "global",
            "resource-id": "",
            "resource-arn": "",
            "resource-name": "kg-alb"
        },
        "waf": {
            "name": "name",
            "discribtion": "string",
            "inspection": "16KB"
        },
        "monitor_settings": {
            "cw_metric_name": "string",
            "option": ""
        },
        "ip": [
            {
                "action": "block",
                "cidr": "10.0.0.0/24"
            }
        ],
        "rules": {
            "rule_package": {
                "SQLi": {
                    "mode": "",
                    "SQLi-set": [
                        {
                            "rule_id": "",
                            "rule": "",
                            "chosen": ""
                        }
                    ]
                },
                "XSS": {
                    "mode": "",
                    "SQLi-set": [
                        {
                            "rule_id": "",
                            "rule": "",
                            "chosen": ""
                        }
                    ]
                }
            },
            "rule_created": [
                {

                },
                {

                }
            ]
        },
        "rule_prioritization": {
            "description": "",
            "order": []
        }
    }
    """
    
    tf = generate_terraform(config)
    output_file_path = os.path.join("terraform", "main.tf")
    with open(output_file_path, 'w') as f:
        f.write(tf)

    print(f"Terraform code has been written to {output_file_path}")

    


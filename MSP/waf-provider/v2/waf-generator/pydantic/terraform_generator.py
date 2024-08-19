from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union
from typing import List, Optional, Literal, Dict, Any
import json

# ================================== Base Models ==================================

class ResourceConfig(BaseModel):
    type: Literal["cloudfront"]
    region: Literal["global"]
    resource_arn: str = Field(..., alias="resource-arn")

class WAFConfig(BaseModel):
    name: str
    description: str
    inspection: Literal["16KB"]

class MonitorSettings(BaseModel):
    cw_metric_name: str
    option: str

class IPRule(BaseModel):
    action: Literal["block"]
    cidr: str

class RulePrioritization(BaseModel):
    description: str
    order: List[str]


# ------------------------- action -------------------------
class Header(BaseModel):
    Name: str
    Value: str

class CustomRequest(BaseModel):
    CustomRequestHandling: Dict[str, List[Header]]

class CustomResponse(BaseModel):
    ResponseHeaders: List[Header]
    ResponseCode: str
    CustomResponseBodyKey: str

class ImmunityTimeProperty(BaseModel):
    ImmunityTime: str

class CaptchaConfig(BaseModel):
    ImmunityTimeProperty: Optional[ImmunityTimeProperty]

class BlockAction(BaseModel):
    Block: Dict[str, Any]
    CustomResponse: Optional[CustomResponse] = None
    CaptchaConfig: Optional[CaptchaConfig] = None

class AllowAction(BaseModel):
    Allow: Dict[str, Any]
    CustomRequestHandling: Optional[CustomRequest] = None

class CountAction(BaseModel):
    Count: Dict[str, Any]
    CustomRequestHandling: Optional[CustomRequest] = None
    CaptchaConfig: Optional[CaptchaConfig] = None

class CaptchaAction(BaseModel):
    Captcha: Dict[str, Any]
    CustomRequestHandling: Optional[CustomRequest] = None
    CaptchaConfig: Optional[CaptchaConfig] = None

class ChallengeAction(BaseModel):
    Challenge: Dict[str, Any]
    CaptchaConfig: Optional[CaptchaConfig] = None

class CaptchaConfig(BaseModel):
    ImmunityTimeProperty: Optional[ImmunityTimeProperty]

class BlockAction(BaseModel):
    Block: Dict[str, Any]
    custom_response: Optional[CustomResponse] = None
    CaptchaConfig: Optional[CaptchaConfig] = None

class AllowAction(BaseModel):
    Allow: Dict[str, Any]
    custom_request: Optional[CustomRequest] = None

class CountAction(BaseModel):
    Count: Dict[str, Any]
    custom_request: Optional[CustomRequest] = None
    CaptchaConfig: Optional[CaptchaConfig] = None

class CaptchaAction(BaseModel):
    Captcha: Dict[str, Any]
    custom_request: Optional[CustomRequest] = None
    CaptchaConfig: Optional[CaptchaConfig] = None

class ChallengeAction(BaseModel):
    Challenge: Dict[str, Any]
    CaptchaConfig: Optional[CaptchaConfig] = None

# ======================================= IP Rule =======================================

class RulePackage(BaseModel):
    name: str
    version: str
    # Add other fields as necessary

class CreatedRule(BaseModel):
    class CreatedRule(BaseModel):
        Name: str
        Priority: int
        Action: Union[BlockAction, AllowAction, CountAction, CaptchaAction, ChallengeAction]
        VisibilityConfig: VisibilityConfig
        Statement: Statement
        RuleLabels: Optional[List[RuleLabel]]

# ======================================= Rule Package =======================================

# ======================================= Created Rule (customized rules) =======================================
class VisibilityConfig(BaseModel):
    SampledRequestsEnabled: bool
    CloudWatchMetricsEnabled: bool
    MetricName: str

class Statement(BaseModel):
    Statement_type: str
    statement: Dict[str, Any]

class RuleLabel(BaseModel):
    key: str

# =========================================== functions ============================================
def generate_terraform(config: str) -> str:
    waf_config = WAFConfig(**json.loads(config))
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

    resource "aws_wafv2_web_acl" "{waf_config.name}" {{
      name        = "{waf_config.name}"
      description = "{waf_config.description}"
      scope       = "{waf_config.scope}"

      default_action {{
        {waf_config.default_action} {{}}
      }}

      visibility_config {{
        cloudwatch_metrics_enabled = true
        metric_name                = "{waf_config.name}-metric"
        sampled_requests_enabled   = true
      }}

      {generate_rules(waf_config.rules)}
    }}
    """
    return terraform_config

def generate_rules(rules: List[Rule]) -> str:
    return "\n".join(generate_rule(rule) for rule in rules)

def generate_rule(rule: Rule) -> str:
    rule_config = f"""
  rule {{
    name     = "{rule.name}"
    priority = {rule.priority}

    {generate_action(rule)}

    visibility_config {{
      cloudwatch_metrics_enabled = {rule.visibility_config.cloudwatch_metrics_enabled}
      metric_name                = "{rule.visibility_config.metric_name}"
      sampled_requests_enabled   = {rule.visibility_config.sampled_requests_enabled}
    }}

    statement {{
      {generate_statement(rule.statement)}
    }}

    {generate_rule_labels(rule.labels)}
  }}
"""
    return rule_config

def generate_action(rule: Rule) -> str:
    if rule.override_action:
        return f"override_action {{\n      {rule.override_action} {{}}\n    }}"
    elif rule.action:
        return f"action {{\n      {rule.action} {{}}\n    }}"
    else:
        raise ValueError("Rule must have either override_action or action")

def generate_statement(statement: Statement) -> str:
    if statement.managed_rule_group_statement:
        return f"""managed_rule_group_statement {{
        name        = "{statement.managed_rule_group_statement.name}"
        vendor_name = "{statement.managed_rule_group_statement.vendor_name}"
      }}"""
    else:
        raise ValueError("Unsupported statement type")

def generate_rule_labels(labels: Optional[List[RuleLabel]]) -> str:
    if not labels:
        return ""
    label_strings = [f'{{key = "{label.key}"}}' for label in labels]
    return f"""
    rule_labels {{
      {" ".join(label_strings)}
    }}
"""
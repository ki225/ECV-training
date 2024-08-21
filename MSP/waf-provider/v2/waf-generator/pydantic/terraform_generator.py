# BaseModel is for some functions like validation, it is optional in every class
from pydantic import BaseModel, Field 
from typing import List, Literal, Optional, Union, Dict, Any
import json
import os

# ================================== Base ==================================

class ResourceConfig(BaseModel):
    type: Literal[
        "cloudfront",
        "alb",
        "apigateway",
        "apprunner",
        "appsync",
        "cognito",
        "verifiedaccess"
    ]
    region: str
    resource_arn: str = Field(..., alias="resource-arn")

class Waf(BaseModel):
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

class WAFConfig(BaseModel):
    resource: ResourceConfig
    waf: Waf
    monitor_settings: MonitorSettings
    ip_rules: List[IPRule]
    rule_prioritization: RulePrioritization

# ------------------------- AggregateKeyType -------------------------
class TextTransformation(BaseModel):
    Type: Literal["NONE", "COMPRESS_WHITE_SPACE", "HTML_ENTITY_DECODE", "LOWERCASE", "CMD_LINE", "URL_DECODE",
                  "BASE64_DECODE", "HEX_DECODE", "MD5", "REPLACE_COMMENTS", "ESCAPE_SEQ_DECODE",
                  "SQL_HEX_DECODE", "CSS_DECODE", "JS_DECODE", "NORMALIZE_PATH", "NORMALIZE_PATH_WIN",
                  "REMOVE_NULLS", "REPLACE_NULLS", "BASE64_DECODE_EXT", "URL_DECODE_UNI", "UTF8_TO_UNICODE"]
    Priority: int

class QueryStringKey(BaseModel):
    QueryString: Dict[Literal["TextTransformations"], List[TextTransformation]]

class QueryArgumentKey(BaseModel):
    QueryArgument: Dict[Literal["Name", "TextTransformations"], Union[str, List[TextTransformation]]]

class LabelNamespaceKey(BaseModel):
    LabelNamespace: Dict[Literal["Namespace"], str]

class HeaderKey(BaseModel):
    Header: Dict[Literal["Name", "TextTransformations"], Union[str, List[TextTransformation]]]

class HTTPMethodKey(BaseModel):
    HTTPMethod: Dict

class UriPathKey(BaseModel):
    UriPath: Dict[Literal["TextTransformations"], List[TextTransformation]]

class CookieKey(BaseModel):
    Cookie: Dict[Literal["Name", "TextTransformations"], Union[str, List[TextTransformation]]]

AggregationKey = Union[
    QueryStringKey,
    QueryArgumentKey,
    LabelNamespaceKey,
    HeaderKey,
    HTTPMethodKey,
    UriPathKey,
    CookieKey
]

# ------------------------- inspect type -------------------------

class SingleHeader(BaseModel):
    SingleHeader: Dict[Literal["Name"], str]

class MatchPattern(BaseModel):
    All: Optional[Dict] = None
    IncludedHeaders: Optional[List[str]] = None
    ExcludedHeaders: Optional[List[str]] = None
    IncludedCookies: Optional[List[str]] = None
    ExcludedCookies: Optional[List[str]] = None
    IncludedPaths: Optional[List[str]] = None

class Headers(BaseModel):
    MatchScope: Literal["ALL", "KEY", "VALUE"]
    MatchPattern: MatchPattern
    OversizeHandling: Literal["CONTINUE", "MATCH", "NO_MATCH"]

class Cookies(BaseModel):
    MatchScope: Literal["VALUE"]
    MatchPattern: MatchPattern
    OversizeHandling: Literal["CONTINUE", "MATCH", "NO_MATCH"]

class SingleQueryArgument(BaseModel):
    SingleQueryArgument: Dict[Literal["Name"], str]

class AllQueryArguments(BaseModel):
    AllQueryArguments: Dict

class UriPath(BaseModel):
    UriPath: Dict

class QueryString(BaseModel):
    QueryString: Dict

class Body(BaseModel):
    Body: Dict[Literal["OversizeHandling"], Literal["CONTINUE", "MATCH", "NO_MATCH"]]

class JsonBody(BaseModel):
    MatchScope: Literal["ALL", "KEY", "VALUE"]
    InvalidFallbackBehavior: Optional[Literal["EVALUATE_AS_STRING", "MATCH", "NO_MATCH"]]
    MatchPattern: MatchPattern
    OversizeHandling: Literal["CONTINUE", "MATCH", "NO_MATCH"]

class JA3Fingerprint(BaseModel):
    JA3Fingerprint: Dict[Literal["FallbackBehavior"], Literal["MATCH"]]

class HeaderOrder(BaseModel):
    HeaderOrder: Dict[Literal["OversizeHandling"], Literal["CONTINUE"]]

class Method(BaseModel):
    Method: Dict


# ------------------------- match type -------------------------

class ForwardedIPConfig(BaseModel):
    HeaderName: str
    FallbackBehavior: Literal["MATCH", "NO_MATCH"]

class IPSetForwardedIPConfig(BaseModel):
    HeaderName: str
    FallbackBehavior: Literal["MATCH", "NO_MATCH"]
    Position: Literal["FIRST", "LAST", "ANY"]

class TextTransformation(BaseModel):
    Type: Literal["NONE", "COMPRESS_WHITE_SPACE", "HTML_ENTITY_DECODE", "LOWERCASE", "CMD_LINE", "URL_DECODE", 
                  "BASE64_DECODE", "HEX_DECODE", "MD5", "REPLACE_COMMENTS", "ESCAPE_SEQ_DECODE", 
                  "SQL_HEX_DECODE", "CSS_DECODE", "JS_DECODE", "NORMALIZE_PATH", "NORMALIZE_PATH_WIN", 
                  "REMOVE_NULLS", "REPLACE_NULLS", "BASE64_DECODE_EXT", "URL_DECODE_UNI", "UTF8_TO_UNICODE"]
    Priority: int

class FieldToMatch(BaseModel):
    field: Union[
        SingleHeader,
        Headers,
        Cookies,
        SingleQueryArgument,
        AllQueryArguments,
        UriPath,
        QueryString,
        Body,
        JsonBody,
        JA3Fingerprint,
        HeaderOrder,
        Method
    ]

class GeoMatchStatement(BaseModel):
    CountryCodes: List[str]
    Forwarded_IP_config: Optional[ForwardedIPConfig] = None

class IPSetReferenceStatement(BaseModel):
    ARN: str
    IPSet_forwarded_IP_config: Optional[IPSetForwardedIPConfig] = None

class LabelMatchStatement(BaseModel):
    Scope: Literal["LABEL", "NAMESPACE"]
    Key: str

class ByteMatchStatement(BaseModel):
    FieldToMatch: FieldToMatch
    PositionalConstraint: Literal["EXACTLY", "STARTS_WITH", "ENDS_WITH", "CONTAINS", "CONTAINS_WORD"]
    SearchString: str
    TextTransformations: List[TextTransformation]

class RegexPatternSetReferenceStatement(BaseModel):
    FieldToMatch: FieldToMatch
    ARN: str
    TextTransformations: List[TextTransformation]

class RegexMatchStatement(BaseModel):
    FieldToMatch: FieldToMatch
    TextTransformations: List[TextTransformation]
    RegexString: str

class SizeConstraintStatement(BaseModel):
    FieldToMatch: FieldToMatch
    ComparisonOperator: Literal["EQ", "NE", "LE", "LT", "GE", "GT"]
    Size: str
    TextTransformations: List[TextTransformation]

class SqliMatchStatement(BaseModel):
    FieldToMatch: FieldToMatch
    TextTransformations: List[TextTransformation]
    SensitivityLevel: Literal["LOW", "HIGH"]

class XssMatchStatement(BaseModel):
    FieldToMatch: FieldToMatch
    TextTransformations: List[TextTransformation]



# ------------------------- statement -------------------------
class MatchStatement(BaseModel):
    __root__: Union[
        GeoMatchStatement,
        IPSetReferenceStatement,
        LabelMatchStatement,
        ByteMatchStatement,
        RegexPatternSetReferenceStatement,
        RegexMatchStatement,
        SizeConstraintStatement,
        SqliMatchStatement,
        XssMatchStatement
    ]

class NotStatement(BaseModel):
    NotStatement: MatchStatement

class OrStatement(BaseModel):
    OrStatement: Dict[Literal["Statements"], List[Union[MatchStatement, NotStatement]]]

class AndStatement(BaseModel):
    AndStatement: Dict[Literal["Statements"], List[Union[MatchStatement, NotStatement]]]

class ForwardedIPConfig(BaseModel):
    HeaderName: str
    FallbackBehavior: Literal["MATCH", "NO_MATCH"]

class ScopeDownStatement(BaseModel):
    statement: Union[MatchStatement, NotStatement, OrStatement, AndStatement]


# ------------------------- rate_type -------------------------
class ForwardedIPConfig(BaseModel):
    HeaderName: str
    FallbackBehavior: Literal["MATCH", "NO_MATCH"]

class ScopeDownStatement(BaseModel):
    statement: Union[MatchStatement, NotStatement, OrStatement, AndStatement]


class ForwardedIPRateType(BaseModel):
    ForwardedIPConfig: ForwardedIPConfig
    Scope_down_statement: Optional[ScopeDownStatement] = None

class IPRateType(BaseModel):
    Scope_down_statement: Optional[ScopeDownStatement] = None

class CustomKeysRateType(BaseModel):
    CustomKeys: List[AggregationKey]
    Scope_down_statement: Optional[ScopeDownStatement] = None

class ConstantRateType(BaseModel):
    Scope_down_statement: ScopeDownStatement

class RateBasedStatement(BaseModel):
    Limit: int = Field(..., ge=100, le=2000000000)
    AggregateKeyType: Literal["FORWARDED_IP", "IP", "CUSTOM_KEYS", "CONSTANT"]
    Forwarded_IP_config: Optional[ForwardedIPConfig] = None
    Scope_down_statement: Optional[ScopeDownStatement] = None
    CustomKeys: Optional[List[AggregationKey]] = None

    @property
    def rate_type(self) -> Union[ForwardedIPRateType, IPRateType, CustomKeysRateType, ConstantRateType]:
        if self.AggregateKeyType == "FORWARDED_IP":
            return ForwardedIPRateType(
                ForwardedIPConfig=self.ForwardedIPConfig,
                ScopeDownStatement=self.ScopeDownStatement
            )
        elif self.AggregateKeyType == "IP":
            return IPRateType(ScopeDownStatement=self.ScopeDownStatement)
        elif self.AggregateKeyType == "CUSTOM_KEYS":
            return CustomKeysRateType(
                CustomKeys=self.CustomKeys,
                ScopeDownStatement=self.ScopeDownStatement
            )
        elif self.AggregateKeyType == "CONSTANT":
            return ConstantRateType(ScopeDownStatement=self.ScopeDownStatement)
        else:
            raise ValueError(f"Invalid AggregateKeyType: {self.AggregateKeyType}")

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

class CaptchaConfig(BaseModel):
    ImmunityTime: int = Field(..., description="Immunity time in seconds")

# Action Models
class BlockAction(BaseModel):
    custom_response: Optional[CustomResponse] = None

class AllowAction(BaseModel):
    custom_request: Optional[CustomRequest] = None

class CountAction(BaseModel):
    custom_request: Optional[CustomRequest] = None

class CaptchaAction(BaseModel):
    custom_request: Optional[CustomRequest] = None
    Captcha_config: Optional[CaptchaConfig] = None

class ChallengeAction(BaseModel):
    Captcha_config: Optional[CaptchaConfig] = None


# ======================================= IP Rule =======================================

class RulePackage(BaseModel):
    name: str
    version: str
    # Add other fields as necessary

class CreatedRule(BaseModel):
    Name: str
    Priority: int
    Action: Union[BlockAction, AllowAction, CountAction, CaptchaAction, ChallengeAction]
    VisibilityConfig: VisibilityConfig
    Statement: Statement

class Rule(BaseModel):
    Rule_created: CreatedRule
    Rule_package: RulePackage
# ======================================= Rule Package =======================================

# ======================================= Created Rule (customized rules) =======================================
class VisibilityConfig(BaseModel):
    SampledRequestsEnabled: bool
    CloudWatchMetricsEnabled: bool
    MetricName: str

class Statement(BaseModel):
    Statement_type: str
    statement: Union[MatchStatement, NotStatement, OrStatement, AndStatement, RateBasedStatement]

class RuleLabel(BaseModel):
    key: str

# =========================================== functions ============================================

def generate_terraform(config: str) -> str:
    waf_config = WAFConfig(**json.loads(config))
    customer_credential = ""   # IAM role ARN
    
    terraform_config = f"""
    # AWS Provider
    provider "aws" {{
      alias  = "customer"
      region = "{waf_config.resource.region}"
      assume_role {{
        role_arn = "{customer_credential}"
      }}
    }}

    resource "aws_wafv2_web_acl" "{waf_config.waf.name}" {{
      name        = "{waf_config.waf.name}"
      description = "{waf_config.waf.description}"
      scope       = "{'CLOUDFRONT' if waf_config.resource.type.upper() == 'CLOUDFRONT' else 'REGIONAL'}"

      default_action {{
        {waf_config.waf.default_action} {{}}
      }}

      visibility_config {{
        cloudwatch_metrics_enabled = true
        metric_name                = "{waf_config.monitor_settings.cw_metric_name}"
        sampled_requests_enabled   = true
      }}

      {generate_rules(waf_config.rule_created)}
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

# =================================================== test ================================================


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
            "description": "string",
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



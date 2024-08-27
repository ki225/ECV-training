# BaseModel is for some functions like validation, it is optional in every class
from pydantic import BaseModel, Field, RootModel 
from typing import List, Literal, Optional, Union, Dict, Any
import json
import os
from pydantic import TypeAdapter
# from terraform_executor import execute_terraform

# ------------------------- AggregateKeyType -------------------------
class TextTransformation(BaseModel):
    Type: Literal["NONE", "COMPRESS_WHITE_SPACE", "HTML_ENTITY_DECODE", "LOWERCASE", "CMD_LINE", "URL_DECODE",
                  "BASE64_DECODE", "HEX_DECODE", "MD5", "REPLACE_COMMENTS", "ESCAPE_SEQ_DECODE",
                  "SQL_HEX_DECODE", "CSS_DECODE", "JS_DECODE", "NORMALIZE_PATH", "NORMALIZE_PATH_WIN",
                  "REMOVE_NULLS", "REPLACE_NULLS", "BASE64_DECODE_EXT", "URL_DECODE_UNI", "UTF8_TO_UNICODE"]
    Priority: int

class QueryStringKey(BaseModel):
    Query_String: Dict[Literal["TextTransformations"], List[TextTransformation]]

class QueryArgumentKey(BaseModel):
    Query_Argument: Dict[Literal["Name", "TextTransformations"], Union[str, List[TextTransformation]]]

class LabelNamespaceKey(BaseModel):
    Label_Namespace: Dict[Literal["Namespace"], str]

class HeaderKey(BaseModel):
    Header: Dict[Literal["Name", "TextTransformations"], Union[str, List[TextTransformation]]]

class HTTPMethodKey(BaseModel):
    HTTP_Method: Dict

class UriPathKey(BaseModel):
    Uri_Path: Dict[Literal["TextTransformations"], List[TextTransformation]]

class CookieKey(BaseModel):
    Cookie: Dict[Literal["Name", "TextTransformations"], Union[str, List[TextTransformation]]]

Aggregation_Key = Union[
    QueryStringKey,
    QueryArgumentKey,
    LabelNamespaceKey,
    HeaderKey,
    HTTPMethodKey,
    UriPathKey,
    CookieKey
]

# ------------------------------------------ Inspect module ------------------------------------
class SingleHeader(BaseModel):
    Name : str
    # Single_Header: Dict[Literal["Name"], str]

class MatchPattern(BaseModel):
    All: Optional[Dict] = None
    Included_Headers: Optional[List[str]] = None
    Excluded_Headers: Optional[List[str]] = None
    Included_Cookies: Optional[List[str]] = None
    Excluded_Cookies: Optional[List[str]] = None
    Included_Paths: Optional[List[str]] = None

class Headers(BaseModel):
    Match_Scope: Literal["ALL", "KEY", "VALUE"]
    Match_Pattern: MatchPattern
    Oversize_Handling: Literal["CONTINUE", "MATCH", "NO_MATCH"]

class Cookies(BaseModel):
    Match_Scope: Literal["VALUE"]
    Match_Pattern: MatchPattern
    Oversize_Handling: Literal["CONTINUE", "MATCH", "NO_MATCH"]

class SingleQueryArgument(BaseModel):
    Name: str
    # Single_Query_Argument: Dict[Literal["Name"], str]

class AllQueryArguments(BaseModel):
    pass
    # All_Query_Arguments: Dict

class UriPath(BaseModel):
    pass
    # UriPath: Dict

class QueryString(BaseModel):
    pass
    # Query_String: Dict

class Body(BaseModel):
    Oversize_Handling: Literal["CONTINUE", "MATCH", "NO_MATCH"]

class JsonBody(BaseModel):
    Match_Scope: Literal["ALL", "KEY", "VALUE"]
    Invalid_Fallback_Behavior: Optional[Literal["EVALUATE_AS_STRING", "MATCH", "NO_MATCH"]]
    Match_Pattern: MatchPattern
    Oversize_Handling: Literal["CONTINUE", "MATCH", "NO_MATCH"]

class JA3Fingerprint(BaseModel):
    Fallback_Behavior: Literal["MATCH"]

class HeaderOrder(BaseModel):
    Oversize_Handling: Literal["CONTINUE"]

class Http(BaseModel):
    Method: Dict

# ------------------------------------------- matchType module --------------------------------------------

class ForwardedIPConfig(BaseModel):
    Header_Name: str
    Fallback_Behavior: Literal["MATCH", "NO_MATCH"]

class GeoMatchStatement(BaseModel):
    Country_Codes: List[Literal[
        "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ",
        "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS",
        "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN",
        "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE",
        "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF",
        "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM",
        "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM",
        "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC",
        "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK",
        "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA",
        "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG",
        "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW",
        "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS",
        "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO",
        "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI",
        "VN", "VU", "WF", "WS", "XK", "YE", "YT", "ZA", "ZM", "ZW"
    ]]
    Forwarded_IP_Config: Optional[ForwardedIPConfig] = None

class IPSetForwardedIPConfig(BaseModel):
    Header_Name: str
    Fallback_Behavior: Literal["MATCH", "NO_MATCH"]
    Position: Literal["FIRST", "LAST", "ANY"]

# inspect
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
        Http
    ]

class IPSetReferenceStatement(BaseModel):
    ARN: str
    IPSet_forwarded_IP_config: Optional[IPSetForwardedIPConfig] = None #  originIp-ipHeader needs

class LabelMatchStatement(BaseModel):
    Scope: Literal["LABEL", "NAMESPACE"]
    Key: str

class ByteMatchStatement(BaseModel):
    Field_To_Match: FieldToMatch # inspect
    Positional_Constraint: Literal["EXACTLY", "STARTS_WITH", "ENDS_WITH", "CONTAINS", "CONTAINS_WORD"]
    Search_String: str
    Text_Transformations: List[TextTransformation] = Field(..., max_items=10) # multiple up to 10

class RegexPatternSetReferenceStatement(BaseModel):
    Field_To_Match: FieldToMatch
    ARN: str
    Text_Transformations: List[TextTransformation] = Field(..., max_items=10)

class RegexMatchStatement(BaseModel):
    Field_To_Match: FieldToMatch
    Text_Transformations: List[TextTransformation] = Field(..., max_items=10)
    Regex_String: str # self defined

class SizeConstraintStatement(BaseModel):
    Field_To_Match: FieldToMatch
    Comparison_Operator: Literal["EQ", "NE", "LE", "LT", "GE", "GT"]
    Size: str
    Text_Transformations: List[TextTransformation] = Field(..., max_items=10)

class SqliMatchStatement(BaseModel):
    Field_To_Match: FieldToMatch
    Text_Transformations: List[TextTransformation] = Field(..., max_items=10)
    Sensitivity_Level: Literal["LOW", "HIGH"]

class XssMatchStatement(BaseModel):
    Field_To_Match: FieldToMatch
    Text_Transformations: List[TextTransformation] = Field(..., max_items=10)

# ------------------------- statement -------------------------

class SelectedStatements(BaseModel):
    Match_type: str
    GeoMatch_Statement: Optional[GeoMatchStatement] = None
    IPSetReference_Statement: Optional[IPSetReferenceStatement] = None
    LabelMatch_Statement: Optional[LabelMatchStatement] = None
    ByteMatch_Statement: Optional[ByteMatchStatement] = None
    RegexPatternSetReference_Statement: Optional[RegexPatternSetReferenceStatement]=None
    RegexMatch_Statement: Optional[RegexMatchStatement] = None
    SizeConstraint_Statement: Optional[SizeConstraintStatement] = None
    SqliMatch_Statement: Optional[SqliMatchStatement] = None
    XssMatch_Statement: Optional[XssMatchStatement] = None
    
class MatchStatement(BaseModel):
    Selected_statement: SelectedStatements

StatementType = Union[
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

class OrStatement(BaseModel):
    Statement_amount: str
    Selected_statement1: SelectedStatements
    Selected_statement2: SelectedStatements
    Selected_statement3: Optional[SelectedStatements] = None
    Selected_statement4: Optional[SelectedStatements] = None
    Selected_statement5: Optional[SelectedStatements] = None

class AndStatement(BaseModel):
    Statement_amount: str
    # Selected_statement: List[Selected_statements]
    Selected_statement1: SelectedStatements
    Selected_statement2: SelectedStatements
    Selected_statement3: Optional[SelectedStatements] = None
    Selected_statement4: Optional[SelectedStatements] = None
    Selected_statement5: Optional[SelectedStatements] = None

class NotStatement(BaseModel):
    # Selected_statement: SelectedStatements
    Selected_statement: List[SelectedStatements] = Field(..., min_items=1)

# ------------------------- rate_type -------------------------

class ScopeDownStatement(BaseModel):
    statement: Union[MatchStatement, NotStatement, OrStatement, AndStatement]

class ForwardedIPRateType(BaseModel):
    Forwarded_IP_Config: ForwardedIPConfig
    Scope_down_statement: Optional[ScopeDownStatement] = None

class IPRateType(BaseModel):
    Scope_down_statement: Optional[ScopeDownStatement] = None

class CustomKeysRateType(BaseModel):
    Custom_Keys: List[Aggregation_Key]
    Scope_down_statement: Optional[ScopeDownStatement] = None

class ConstantRateType(BaseModel):
    Scope_down_statement: ScopeDownStatement

class RateBasedStatement(BaseModel):
    Limit: int = Field(..., ge=100, le=2000000000)
    Aggregate_Key_Type: Literal["FORWARDED_IP", "IP", "CUSTOM_KEYS", "CONSTANT"]
    Forwarded_IP_config: Optional[ForwardedIPConfig] = None
    Scope_down_statement: Optional[ScopeDownStatement] = None
    Custom_Keys: Optional[List[Aggregation_Key]] = None

    @property
    def rate_type(self) -> Union[ForwardedIPRateType, IPRateType, CustomKeysRateType, ConstantRateType]:
        if self.Aggregate_Key_Type == "FORWARDED_IP":
            return ForwardedIPRateType(
                Forwarded_IP_Config=self.Forwarded_IP_Config,
                Scope_Down_Statement=self.Scope_Down_Statement
            )
        elif self.Aggregate_Key_Type == "IP":
            return IPRateType(Scope_Down_Statement=self.Scope_Down_Statement)
        elif self.Aggregate_Key_Type == "CUSTOM_KEYS":
            return CustomKeysRateType(
                Custom_Keys=self.CustomKeys,
                Scope_Down_Statement=self.Scope_Down_Statement
            )
        elif self.Aggregate_Key_Type == "CONSTANT":
            return ConstantRateType(ScopeDownStatement=self.Scope_Down_Statement)
        else:
            raise ValueError(f"Invalid AggregateKeyType: {self.Aggregate_Key_Type}")

# ------------------------- action -------------------------
class Header(BaseModel):
    Name: str
    Value: str

class CustomRequest(BaseModel):
    Custom_Request_Handling: Dict[str, List[Header]]

class CustomResponse(BaseModel):
    Response_Headers: List[Header]
    Response_Code: str
    Custom_Response_Body_Key: str

class CaptchaConfig(BaseModel):
    Immunity_Time: int = Field(..., description="Immunity time in seconds")

# Action Models
class BlockAction(BaseModel):
    Custom_Response: Optional[CustomResponse] = None

class AllowAction(BaseModel):
    Custom_Request: Optional[CustomRequest] = None

class CountAction(BaseModel):
    Custom_Request: Optional[CustomRequest] = None

class CaptchaAction(BaseModel):
    Custom_Request: Optional[CustomRequest] = None
    Captcha_Config: Optional[CaptchaConfig] = None

class ChallengeAction(BaseModel):
    Captcha_Config: Optional[CaptchaConfig] = None

class Action(BaseModel):
    Block: Optional[BlockAction] = None
    Allow: Optional[AllowAction] = None
    Count: Optional[CountAction] = None
    Captcha: Optional[CaptchaAction] = None
    Challenge: Optional[ChallengeAction] = None


# ======================================= Rule Package =======================================

# ======================================= Created Rule (customized rules) =======================================
class VisibilityConfig(BaseModel):
    Sampled_Requests_Enabled: bool = Field(default=True)
    CloudWatch_Metrics_Enabled: bool = Field(default=True)
    Metric_Name: str = Field(..., description="The name created in monitor field of the form")

class StatementContent(BaseModel):
    Match_Statement: Union[MatchStatement, None] = None
    Not_Statement: Union[NotStatement, None] = None
    Or_Statement: Union[OrStatement, None] = None
    And_Statement: Union[AndStatement, None] = None

class Statements(BaseModel):
    Statement_type: Literal["MatchStatement","NotStatement","OrStatement","AndStatement"]
    Statement_Content: StatementContent

class RuleLabel(BaseModel):
    Key: str

# ======================================= IP Rule =======================================

class RulePackage(BaseModel):
    Name: str
    Version: str
    # Add other fields as necessary

# class CreatedRule(BaseModel):
#     Name: str
#     Priority: int
#     Action: Union[BlockAction, AllowAction, CountAction, CaptchaAction, ChallengeAction]
#     Visibility_config: VisibilityConfig
#     Statement: Statements

class Rule(BaseModel):
    Name: str
    Priority: int
    Action: Action
    Visibility_config: VisibilityConfig
    Statement: Statements

class Rules(BaseModel):
    Rule_Package: List = []
    Rule_Created: List[Rule]

# ================================== Base ==================================

class Resource(BaseModel):
    Type: Literal[
        "cloudfront",
        "alb",
        "apigateway",
        "apprunner",
        "appsync",
        "cognito",
        "verifiedaccess"
    ]
    Region: str
    Resource_id: str = Field(alias="Resource-id")
    Resource_arn: str = Field(alias="Resource-arn")
    Resource_name: str = Field(alias="Resource-name")

class WAF(BaseModel):
    Name: str
    Description: str
    Inspection: str

class MonitorSettings(BaseModel):
    CW_Metric_Name: str
    Option: str

class IPRule(BaseModel):
    Action: str
    CIDR: str

class RulePrioritization(BaseModel):
    pass

class WAFConfig(BaseModel):
    Resource: Resource
    Waf: WAF
    Monitor_Settings: MonitorSettings
    IP: List[IPRule]
    Rules: Rules
    Rule_Prioritization: RulePrioritization

# =========================================== functions ============================================

def generate_terraform(config: str) -> str:
    config_data = json.loads(config)
    waf_config = TypeAdapter(WAFConfig).validate_python(config_data)

    customer_credential = "arn:aws:iam::812428033092:role/kg-terraform-role"   # IAM role ARN

    terraform_config = f"""
    # AWS Provider
    provider "aws" {{
      alias  = "customer"
      region = "us-east-1"
      assume_role {{
        role_arn = "{customer_credential}"
      }}
    }}

    resource "aws_wafv2_web_acl" "{waf_config.Waf.Name}" {{
      name        = "{waf_config.Waf.Name}"
      description = "{waf_config.Waf.Description}"
      scope       = "{'CLOUDFRONT' if waf_config.Resource.Type.upper() == 'CLOUDFRONT' else 'REGIONAL'}"


    default_action {{
        allow {{}}
    }}

      {generate_rules(waf_config.Rules)}
    }}
    """
    return terraform_config

def generate_rules(rules: Dict[str, List[Rule]]) -> str:
    all_rules = []
    for rule in rules.Rule_Created:
        all_rules.append(generate_rule(rule))
        # all_rules.extend(generate_rule(rule) for rule in rule_list)
    return "\n".join(all_rules)

def generate_rule(rule: Rule) -> str:

    rule_config = f"""
      rule {{
        name     = "{rule.Name}"
        priority = {rule.Priority}
        {generate_action(rule.Action)}
        visibility_config {{
          cloudwatch_metrics_enabled = {str(rule.Visibility_config.CloudWatch_Metrics_Enabled).lower()}
          metric_name                = "{rule.Visibility_config.Metric_Name}"
          sampled_requests_enabled   = {str(rule.Visibility_config.Sampled_Requests_Enabled).lower()}
        }}
        statement {{
          {generate_statement(rule.Statement)}
        }}
      }}
    """

    return rule_config


def generate_action(action: Action) -> str:
    if action.Block:
        return "action { block {} }"
    elif action.Allow:
        return "action { allow {} }"
    elif action.Count:
        return "action { count {} }"
    elif action.Captcha:
        return "action { captcha {} }"
    elif action.Challenge:
        return "action { challenge {} }"
    else:
        return "# Unknown action type"

# ---------------------------------- statement ----------------------------------------------------
def generate_geo(geo_statement):
    return f"geo_match_statement {{ country_codes = { geo_statement.Country_Codes} }}"

def generate_rate_based_statement(rate_based_statement):
    return f"""
        rate_based_statement {{
            limit              = {rate_based_statement.Limit}
            aggregate_key_type = "{rate_based_statement.AggregateKeyType}"
        }}
    """


def generate_ip_set_reference(ip_set_statement):
    return f'ip_set_reference_statement {{ arn = "{ip_set_statement.ARN}" }}'

def generate_label_match(label_match_statement):
    return f'label_match_statement {{ key = "{label_match_statement.Key}", scope = "{label_match_statement.Scope}" }}'

def generate_byte_match(byte_match_statement):
    return f"""
        byte_match_statement {{
            search_string         = "{byte_match_statement.SearchString}"
            positional_constraint = "{byte_match_statement.PositionalConstraint}"
            field_to_match {{
                {generate_field_to_match(byte_match_statement.FieldToMatch)}
            }}
            text_transformation {{
                {generate_text_transformation(byte_match_statement.TextTransformations[0])}
            }}
        }}
    """

def generate_regex_pattern_set_reference(regex_pattern_set_statement):
    return f'regex_pattern_set_reference_statement {{ arn = "{regex_pattern_set_statement.ARN}" }}'

def generate_size_constraint(size_constraint_statement):
    return f"""
        size_constraint_statement {{
            comparison_operator = "{size_constraint_statement.ComparisonOperator}"
            size                = {size_constraint_statement.Size}
            field_to_match {{
                {generate_field_to_match(size_constraint_statement.FieldToMatch)}
            }}
            text_transformation {{
                {generate_text_transformation(size_constraint_statement.TextTransformations[0])}
            }}
        }}
    """

def generate_sqli_match(sqli_match_statement):
    return f"""
        sqli_match_statement {{
            field_to_match {{
                {generate_field_to_match(sqli_match_statement.FieldToMatch)}
            }}
            text_transformation {{
                {generate_text_transformation(sqli_match_statement.TextTransformations[0])}
            }}
        }}
    """

def generate_xss_match(xss_match_statement):
    return f"""
        xss_match_statement {{
            field_to_match {{
                {generate_field_to_match(xss_match_statement.FieldToMatch)}
            }}
            text_transformation {{
                {generate_text_transformation(xss_match_statement.TextTransformations[0])}
            }}
        }}
    """

def generate_field_to_match(field_to_match):
    if 'SingleHeader' in field_to_match:
        return f'single_header {{ name = "{field_to_match.SingleHeader.Name}" }}'

def generate_text_transformation(text_transformation):
    return f"""
        priority = {text_transformation.Priority}
        type     = "{text_transformation.Type}"
    """

def generate_match_statement(statement):
    config = ""
    if statement.Match_type == "GeoMatchStatement":
        config += f"""
                    statement {{
                        {generate_geo(statement.GeoMatch_Statement)}
                    }}
                """
    elif statement.Match_type == "LabelMatchStatement":
        config += f"""
            statement {{
                {generate_label_match(statement.LabelMatch_Statement)}
            }}
        """
        
    return config

def generate_not_statement(statement):
    not_statement_config = f"""
        not_statement {{
            {generate_match_statement(statement.Not_Statement.Selected_statement)}
        }}
    """
    return not_statement_config

def generate_or_statement(statement) :
    or_statement_config = f"""
        or_statement {{
            {generate_match_statement(statement.Or_Statement.Selected_statement)}
        }}
    """
    return or_statement_config

def generate_and_statement(statement) :
    statement_num = int(statement.And_Statement.Statement_amount)
    statement1 = statement.And_Statement.Selected_statement1
    statement2 = statement.And_Statement.Selected_statement2
    statement3 = statement.And_Statement.Selected_statement3
    statement4 = statement.And_Statement.Selected_statement4
    statement5 = statement.And_Statement.Selected_statement5
    statement_list = [statement1, statement2, statement3, statement4, statement5] 
    config = ""
    for i in range(statement_num):
        config += f"{generate_match_statement(statement_list[i])}\n"
    and_statement_config = f"""
        and_statement {{
            {config}
        }}
    """
    return and_statement_config

def generate_statement(statement_input):
    statementType= statement_input.Statement_type
    statement = statement_input.Statement_Content


    if statementType == "MatchStatement":
        config = generate_match_statement(statement)
    elif statementType == "NotStatement":
        config = generate_not_statement(statement)
    elif statementType == "OrStatement":
        config = generate_or_statement(statement)
    elif statementType == "AndStatement":
        config = generate_and_statement(statement)
    elif statementType == "RateBasedStatement":
        config = generate_rate_based_statement(statement)
    else:
        config = f"# Unsupported statement type: {statementType}"

    return config


# =================================================== test ================================================


if __name__ == '__main__':
    config = """
    {
    "Resource": {
        "Type": "alb",
        "Region": "global",
        "Resource-id": "",
        "Resource-arn": "",
        "Resource-name": "kg-alb"
    },
    "Waf": {
        "Name": "name",
        "Description": "string",
        "Inspection": "16KB"
    },
    "Monitor_Settings": {
        "CW_Metric_Name": "string",
        "Option": ""
    },
    "IP": [
        {
            "Action": "block",
            "CIDR": "10.0.0.0/24"
        }
    ],
    "Rules": {
        "Rule_Package": [],
        "Rule_Created": [
            {
                "Name": "rule1",
                "Priority": 0,
                "Action": {
                    "Block": {
                        "Custom_Response": {
                            "Response_Headers": [
                                {
                                    "Name": "sd",
                                    "Value": "ff"
                                }
                            ],
                            "Response_Code": "501",
                            "Custom_Response_Body_Key": "ddd"
                        }
                    }
                },
                "Visibility_config": {
                    "Sampled_Requests_Enabled": true,
                    "CloudWatch_Metrics_Enabled": true,
                    "Metric_Name": "matrice"
                },
                "Statement": {
                    "Statement_type": "AndStatement",
                    "Statement_Content": {
                        "And_Statement": {
                            "Statement_amount": "2",
                            "Selected_statement1": {
                                
                                    "Match_type": "GeoMatchStatement",
                                    "GeoMatch_Statement": {
                                        "Country_Codes": [
                                            "TW"
                                        ]
                                    }
                                
                                
                            },
                            "Selected_statement2": {
                                "Match_type": "LabelMatchStatement",
                                "LabelMatch_Statement": {
                                    "Scope": "NAMESPACE",
                                    "Key": "awswaf:111122223333:rulegroup:testRules:namespace1:namespace2:"
                                }      
                            }
                        }
                    }
                }
            }
        ]
    },
    "Rule_Prioritization": {
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
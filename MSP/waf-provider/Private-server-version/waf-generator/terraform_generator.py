# BaseModel is for some functions like validation, it is optional in every class
from pydantic import BaseModel, Field, RootModel, TypeAdapter
from typing import List, Literal, Optional, Union, Dict, Any
import json
import s3_handler

# ------------------------- AggregateKeyType -------------------------
class TextTransformation(BaseModel):
    Type: Literal["NONE", "COMPRESS_WHITE_SPACE", "HTML_ENTITY_DECODE", "LOWERCASE", "CMD_LINE", "URL_DECODE",
                  "BASE64_DECODE", "HEX_DECODE", "MD5", "REPLACE_COMMENTS", "ESCAPE_SEQ_DECODE",
                  "SQL_HEX_DECODE", "CSS_DECODE", "JS_DECODE", "NORMALIZE_PATH", "NORMALIZE_PATH_WIN",
                  "REMOVE_NULLS", "REPLACE_NULLS", "BASE64_DECODE_EXT", "URL_DECODE_UNI", "UTF8_TO_UNICODE"]
    Priority: int

class QueryStringKey(BaseModel):
    Text_Transformations: List[TextTransformation]

class QueryArgumentKey(BaseModel):
    Name: str
    Text_Transformations: List[TextTransformation]

class LabelNamespaceKey(BaseModel):
    Label_Namespace: Dict[Literal["Namespace"], str]

class HeaderKey(BaseModel):
    Name: str
    Text_Transformations: List[TextTransformation]

class HTTPMethodKey(BaseModel):
    HTTP_Method: Dict

class UriPathKey(BaseModel):
    Name: str
    Text_Transformations: List[TextTransformation]

class CookieKey(BaseModel):
    Name: str
    Text_Transformations: List[TextTransformation]

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
    Match_Scope: Literal["ALL", "KEY", "VALUE"]
    Match_Pattern: MatchPattern
    Oversize_Handling: Literal["CONTINUE", "MATCH", "NO_MATCH"]

class SingleQueryArgument(BaseModel):
    Name: str

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
    Fallback_Behavior: Literal["MATCH", "NO_MATCH"]

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
    Single_Header: Optional[SingleHeader] = None
    Headers_: Optional[Headers] = None
    Cookies_: Optional[Cookies] = None
    Single_Query_Argument: Optional[SingleQueryArgument] = None
    All_Query_Arguments: Optional[AllQueryArguments] = None
    Uri_Path: Optional[UriPath] = None
    Query_String: Optional[QueryString] = None
    Body_: Optional[Body] = None
    Json_Body: Optional[JsonBody] = None
    JA3_Fingerprint: Optional[JA3Fingerprint] = None
    Header_Order: Optional[HeaderOrder] = None
    Http_: Optional[Http] = None

class IPSetReferenceStatement(BaseModel):
    ARN: str
    IPSet_forwarded_IP_Config: Optional[IPSetForwardedIPConfig] = None #  originIp-ipHeader needs

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
    Regex_String: str 

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
    Match_Type: str
    Not: Optional[bool] = None
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
    Selected_Statement: SelectedStatements

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
    Statement_Amount: int
    Selected_Statement1: SelectedStatements
    Selected_Statement2: SelectedStatements
    Selected_Statement3: Optional[SelectedStatements] = None
    Selected_Statement4: Optional[SelectedStatements] = None
    Selected_Statement5: Optional[SelectedStatements] = None

class AndStatement(BaseModel):
    Statement_Amount: int
    Selected_Statement1: SelectedStatements
    Selected_Statement2: SelectedStatements
    Selected_Statement3: Optional[SelectedStatements] = None
    Selected_Statement4: Optional[SelectedStatements] = None
    Selected_Statement5: Optional[SelectedStatements] = None

class NotStatement(BaseModel):
    Selected_Statement: SelectedStatements

# ------------------------- rate_type -------------------------

class ScopeDownStatement(BaseModel):
    Statement: Union[MatchStatement, NotStatement, OrStatement, AndStatement]

class ForwardedIPRateType(BaseModel):
    Forwarded_IP_Config: ForwardedIPConfig
    Scope_Down_Statement: Optional[ScopeDownStatement] = None

class IPRateType(BaseModel):
    Scope_Down_Statement: Optional[ScopeDownStatement] = None

class CustomKeysRateType(BaseModel):
    Custom_Keys: List[Aggregation_Key]
    Scope_Down_Statement: Optional[ScopeDownStatement] = None

class ConstantRateType(BaseModel):
    Scope_Down_Statement: ScopeDownStatement

class RateBasedStatement(BaseModel):
    Limit: int = Field(..., ge=100, le=2000000000)
    Aggregate_Key_Type: Literal["FORWARDED_IP", "IP", "CUSTOM_KEYS", "CONSTANT"]
    Forwarded_IP_Config: Optional[ForwardedIPConfig] = None
    Scope_Down_Statement: Optional[ScopeDownStatement] = None
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

# -------------------------------------------------------
class InsertHeaders(BaseModel):
    Name: str
    Value: str
# ------------------------- action -------------------------
class Header(BaseModel):
    Name: str
    Value: str

class CustomRequest(BaseModel):
    Custom_Request_Handling: Optional[List[InsertHeaders]] = Field(default_factory=list)

class CustomResponse(BaseModel):
    Response_Headers: List[Header]
    Response_Code: str
    Custom_Response_Body_Key: str

class ImmunityTimeProperty(BaseModel):
    Immunity_Time: str

class CaptchaConfig(BaseModel):
    Immunity_Time_Property: ImmunityTimeProperty

# ================================================= Action Models =====================================
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
class xssRule(BaseModel):
    Rule_Id: str
    Chosen: bool
    Action: Optional[Literal["Block", "Allow", "Count", "Captcha", "Challenge"]]
    Priority: int

class sqliRule(BaseModel):
    Rule_Id: str
    Chosen: bool
    Action: Optional[Literal["Block", "Allow", "Count", "Captcha", "Challenge"]]
    Priority: int

class cveRule(BaseModel):
    Rule_Id: str
    Chosen: bool
    Action: Optional[Literal["Block", "Allow", "Count", "Captcha", "Challenge"]]
    Priority: int

class XSS_rule(BaseModel):
    Mode: Optional[Literal["disable", "default", "test", "advanced"]]
    Set: List[xssRule]

class SQLi_rule(BaseModel):
    Mode: Optional[Literal["disable", "default", "test", "advanced"]]
    Set: List[sqliRule]

class CVE_rule(BaseModel):
    Mode: Optional[Literal["disable", "default", "test", "advanced"]]
    Set: List[cveRule]

class RulePackage(BaseModel):
    SQLi: Optional[SQLi_rule] = None
    XSS: Optional[XSS_rule] = None
    CVE: Optional[CVE_rule] = None

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
    Statement_Type: Literal["MatchStatement","NotStatement","OrStatement","AndStatement"]
    Statement_Content: StatementContent

class RuleLabel(BaseModel):
    Key: str

# ======================================= IP Rule =======================================
class Rule(BaseModel):
    Name: str
    Priority: int
    Action: Action
    Visibility_Config: VisibilityConfig
    Statement: Statements

class Rules(BaseModel):
    Rule_Package: Optional[RulePackage] = None
    Rule_Created: Optional[List[Rule]] = None

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
    Resource_Id: str
    Resource_Arn: str
    Resource_Name: str

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

class WAFConfig(BaseModel):
    Resource: Resource
    Waf: WAF
    Monitor_Settings: MonitorSettings
    IP: Optional[List[IPRule]] = None
    Rules: Rules
    # Rule_Prioritization: RulePrioritization

# =========================================== functions ============================================
import json

def get_iam_role_by_userid(data, target_userid):
    for item in data:
        if item["UserId"] == str(target_userid):
            return item["IAMRole"]
    return None  

def get_user_iam_role(user_id):
    all_data = s3_handler.get_s3_object('kg-for-test', 'user-credential.json')
    data = json.loads(all_data)
    iam_role = get_iam_role_by_userid(data, user_id)
    return iam_role


def generate_package_rule(target_rule):
    ruleid = str(target_rule["Rule_Id"])
    index = ruleid.find("-")
    object_key = f"packageRules/{ruleid[:index]}.json"
    try:
        rules = s3_handler.get_s3_object('kg-for-test', object_key)
        decode_str = rules.decode('utf-8')  
        rules = json.loads(decode_str)
        

        for rule in rules:
            if rule["Rule_Id"] == target_rule["Rule_Id"]:
                config_str = rule["Rule_Configuration"]
                config_list = config_str.split("\\n")
                return "\n".join(config_list)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
    


def generate_terraform(config: json) -> str:
    waf_config = TypeAdapter(WAFConfig).validate_python(config)
    accountId_start = waf_config.Resource.Resource_Arn.replace(':', 'x', 3).find(':')+1
    accountId_end = waf_config.Resource.Resource_Arn.replace(':', 'x', 4).find(':')
    user_id = waf_config.Resource.Resource_Arn[accountId_start:accountId_end ]
    customer_credential = get_user_iam_role(user_id)

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
        provider = aws.customer
        name        = "{waf_config.Waf.Name}"
        description = "{waf_config.Waf.Description}"
        scope       = "{'CLOUDFRONT' if waf_config.Resource.Type.upper() == 'CLOUDFRONT' else 'REGIONAL'}"

        default_action {{
            allow {{}}
        }}

        {generate_rules(waf_config.Rules)}

        visibility_config {{
          cloudwatch_metrics_enabled = true
          metric_name                = "{waf_config.Monitor_Settings.CW_Metric_Name}"
          sampled_requests_enabled   = {str(waf_config.Monitor_Settings.Option).lower()}
        }}
    }}

    resource "aws_wafv2_web_acl_association" "waf_association" {{
        provider = aws.customer
        resource_arn = "{waf_config.Resource.Resource_Arn}"
        web_acl_arn  = aws_wafv2_web_acl.{waf_config.Waf.Name}.arn
    }}

    output "waf_acl_id" {{
        value       = aws_wafv2_web_acl.{waf_config.Waf.Name}.id
    }}

    output "waf_acl_arn" {{
        value       = aws_wafv2_web_acl.{waf_config.Waf.Name}.arn
    }}
    """
    return terraform_config, user_id


cate_dict = {"SQLi": "Set", "XSS": "Set", "CVE": "Set"}
def generate_rules(rules) -> str:
    all_rules = []
    for rule in rules.Rule_Created:
        all_rules.append(generate_cus_rule(rule))
    for category, set_name in cate_dict.items():
        try:
            if hasattr(rules.Rule_Package, category):
                category_obj = getattr(rules.Rule_Package, category)
                category_obj = category_obj.dict()
                rule_set = category_obj["Set"]
                for rule in rule_set:
                    result = generate_package_rule(rule)
                    if result: # prevent empty result
                        all_rules.append(result)
        except:
            print(f"{category} not found in Rule_Package")
            continue
    return "\n".join(all_rules)


def generate_cus_rule(rule: Rule) -> str:
    rule_config = f"""
      rule {{
        name     = "{rule.Name}"
        priority = {rule.Priority}
        {generate_action(rule.Action)}
        visibility_config {{
          cloudwatch_metrics_enabled = {str(rule.Visibility_Config.CloudWatch_Metrics_Enabled).lower()}
          metric_name                = "{rule.Visibility_Config.Metric_Name}"
          sampled_requests_enabled   = {str(rule.Visibility_Config.Sampled_Requests_Enabled).lower()}
        }}
        statement {{
          {generate_statement(rule.Statement)}
        }}
      }}
    """

    return rule_config


def generate_action(action: Action) -> str:
    if action.Block:
        return f"""action {{
                    block {{}}
                }}"""
    elif action.Allow:
        return f"""action {{
                        allow {{}}
                    }}"""
    elif action.Count:
        return f"""action {{
                        count {{}}
                    }}"""
    elif action.Captcha:
        return f"""action {{
                        captcha {{}}
                    }}"""
    elif action.Challenge:
        return f"""action {{
                        challenge {{}}
                    }}"""
    else:
        return "# Unknown action type"

# ---------------------------------- statement ----------------------------------------------------
def generate_geo(geo_statement):
    country_codes_str = ", ".join(f'"{code}"' for code in geo_statement.Country_Codes)
    return f"""
        geo_match_statement {{ 
            country_codes = [{country_codes_str}] 
        }}
    """

def generate_rate_based_statement(rate_based_statement):
    return f"""
        rate_based_statement {{
            limit              = {rate_based_statement.Limit}
            aggregate_key_type = "{rate_based_statement.AggregateKeyType}"
        }}
    """

def generate_ip_set_reference(ip_set_statement):
    return f'''
        ip_set_reference_statement {{ 
            arn = "{ip_set_statement.ARN}" 
        }}
    '''

def generate_label_match(label_match_statement):
    return f'''label_match_statement {{ 
            key = "{label_match_statement.Key}"
            scope = "{label_match_statement.Scope}" 
        }}
    '''

def generate_byte_match(byte_match_statement):
    return f"""
        byte_match_statement {{
            search_string         = "{byte_match_statement.Search_String}"
            positional_constraint = "{byte_match_statement.Positional_Constraint}"
            field_to_match {{
                {generate_field_to_match(byte_match_statement.Field_To_Match)}
            }}
            text_transformation {{
                {generate_text_transformation(byte_match_statement.Text_Transformations[0])}
            }}
        }}
    """

def generate_regex_pattern_set_reference(regex_pattern_set_statement):
    return f'''
        regex_pattern_set_reference_statement {{ 
            arn = "{regex_pattern_set_statement.ARN}" 
        }}
    '''

def generate_regex_match(regex_match_statement):
    return f"""
        regex_match_statement {{
            regex_string = "{regex_match_statement.Regex_String}"
            field_to_match {{
                {regex_match_statement.Field_To_Match}
            }}
            text_transformation {{
                priority = {regex_match_statement.Text_Transformation.Priority}
                type     = "{regex_match_statement.Text_Transformation.Type}"
            }}
        }}
    """

def generate_size_constraint(size_constraint_statement):
    return f"""
        size_constraint_statement {{
            comparison_operator = "{size_constraint_statement.Comparison_Operator}"
            size                = {size_constraint_statement.Size}
            field_to_match {{
                {generate_field_to_match(size_constraint_statement.Field_To_Match)}
            }}
            text_transformation {{
                {generate_text_transformation(size_constraint_statement.Text_Transformations[0])}
            }}
        }}
    """

def generate_sqli_match(sqli_match_statement):
    return f"""
        sqli_match_statement {{
            field_to_match {{
                {generate_field_to_match(sqli_match_statement.Field_To_Match)}
            }}
            text_transformation {{
                {generate_text_transformation(sqli_match_statement.Text_Transformations[0])}
            }}
        }}
    """

def generate_xss_match(xss_match_statement):
    return f"""
        xss_match_statement {{
            field_to_match {{
                {generate_field_to_match(xss_match_statement.Field_To_Match)}
            }}
            text_transformation {{
                {generate_text_transformation(xss_match_statement.Text_Transformations[0])}
            }}
        }}
    """


def generate_field_to_match(field_to_match): #  object type is <...>_Statement.Field_To_Match
    if field_to_match.Single_Header is not None:
        return f'single_header {{ name = "{field_to_match.Single_Header.Name}" }}'
    elif field_to_match.Headers_ is not None:
        return 'headers {}'  # You might need to add more details here depending on the Headers structure
    elif field_to_match.Cookies_ is not None:
        return f"""
        cookies{{
            match_scope = "{field_to_match.Cookies_.Match_Scope}"
            match_pattern {{
                    all {{

                    }}
            }}
            oversize_handling = "{field_to_match.Cookies_.Oversize_Handling}"
        }}

        """
    elif field_to_match.Single_Query_Argument is not None:
        return f'single_query_argument {{ name = "{field_to_match.Single_Query_Argument.Name}" }}'
    elif field_to_match.All_Query_Arguments is not None:
        return 'all_query_arguments {}'
    elif field_to_match.Uri_Path is not None:
        return 'uri_path {}'
    elif field_to_match.Query_String is not None:
        return 'query_string {}'
    elif field_to_match.Body_ is not None:
        return 'body {}'
    elif field_to_match.Json_Body is not None:
        return 'json_body {}'  # You might need to add more details here depending on the JsonBody structure
    elif field_to_match.JA3_Fingerprint is not None:
        return 'ja3_fingerprint {}'
    elif field_to_match.Header_Order is not None:
        return f"""
        header_order {{
            oversize_handling = "{field_to_match.Header_Order.Oversize_Handling}"

        }}
        """
    elif field_to_match.Http_ is not None:
        return 'http {}'
    else:
        raise ValueError("No valid field_to_match type found")

def generate_text_transformation(text_transformation):
    return f"""
        priority = {text_transformation.Priority}
        type     = "{text_transformation.Type}"
    """

def generate_match_statement(statement): # .Match_Statement.Selected_Statement
    config = ""
    if statement.Match_Type == "GeoMatchStatement":
        config += generate_geo(statement.GeoMatch_Statement)
    elif statement.Match_Type == "IPSetReferenceStatement":
        config += generate_ip_set_reference(statement.IPSetReference_Statement)
    elif statement.Match_Type == "LabelMatchStatement":
        config += generate_label_match(statement.LabelMatch_Statement)
    elif statement.Match_Type == "ByteMatchStatement":
        config += generate_byte_match(statement.ByteMatch_Statement)
    elif statement.Match_Type == "RegexPatternSetReferenceStatement":
        config += generate_regex_pattern_set_reference(statement.RegexPatternSetReference_Statement)
    elif statement.Match_Type == "RegexMatchStatement":
        config += generate_regex_match(statement.RegexMatch_Statement)
    elif statement.Match_Type == "SizeConstraintStatement":
        config += generate_size_constraint(statement.SizeConstraint_Statement)
    elif statement.Match_Type == "SqliMatchStatement":
        config += generate_sqli_match(statement.SqliMatch_Statement)
    elif statement.Match_Type == "XssMatchStatement":
        config += generate_xss_match(statement.XssMatch_Statement)
    else:
        config += f"# Unsupported match type: {statement.Match_Type}"
    return config

def generate_not_statement(statement):
    not_statement_config = f"""
        not_statement {{
            statement {{
                {generate_match_statement(statement)}
            }}
        }}
    """
    return not_statement_config

def generate_or_statement(statement: object):  # obj type is Statement_Content.And_Statement
    statement_num = int(statement.Statement_Amount)
    statement1 = statement.Selected_Statement1
    statement2 = statement.Selected_Statement2
    statement3 = statement.Selected_Statement3
    statement4 = statement.Selected_Statement4
    statement5 = statement.Selected_Statement5
    statement_list = [statement1, statement2, statement3, statement4, statement5]
    config = ""
    for i in range(statement_num):
        if hasattr(statement_list[i], 'Not') and statement_list[i].Not == True:
            config += f"""
                statement {{
                        {generate_match_statement(statement_list[i])}
                }}\n"""
        else:
            config += f"""
                statement {{
                        {generate_match_statement(statement_list[i])}
                }}\n"""

    or_statement_config = f"""
        or_statement {{
            {config}
        }}
    """
    return or_statement_config

def generate_and_statement(statement: object):  # obj type is Statement_Content.And_Statement
    statement_num = int(statement.Statement_Amount)
    statement1 = statement.Selected_Statement1
    statement2 = statement.Selected_Statement2
    statement3 = statement.Selected_Statement3
    statement4 = statement.Selected_Statement4
    statement5 = statement.Selected_Statement5
    statement_list = [statement1, statement2, statement3, statement4, statement5]
    config = ""

    for i in range(statement_num):
        if hasattr(statement_list[i], 'Not') and statement_list[i].Not == True:
            config += f"""
                statement {{
                        {generate_match_statement(statement_list[i])}
                }}\n"""
        else:
            config += f"""
                statement {{
                        {generate_match_statement(statement_list[i])}
                }}\n"""

    and_statement_config = f"""
        and_statement {{
            {config}
        }}
    """
    return and_statement_config

def generate_statement(statement_input):
    statementType= statement_input.Statement_Type
    statement = statement_input.Statement_Content

    if statementType == "MatchStatement":
        config = generate_match_statement(statement.Match_Statement.Selected_Statement)
    elif statementType == "NotStatement":
        config = generate_not_statement(statement.Not_Statement.Selected_Statement)
    elif statementType == "OrStatement":
        config = generate_or_statement(statement.Or_Statement)
    elif statementType == "AndStatement":
        config = generate_and_statement(statement.And_Statement)
    elif statementType == "RateBasedStatement":
        config = generate_rate_based_statement(statement)
    else:
        config = f"# Unsupported statement type: {statementType}"

    return config

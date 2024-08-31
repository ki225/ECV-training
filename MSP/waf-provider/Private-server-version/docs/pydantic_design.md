# Pydantic Design

This document is based on request body defined in document [request_structure_and_format_design](https://gitlab.ecvmsp.com/ecloudvalley_kiki.huang/waf-manager/-/blob/feature_frontend/docs/request_structure_design.md). The usage of Pydantic is for validating the input. We will go through every parts from the top and get deeper.

## Overview of request body
There are 6 main part to form the whole reques, including resource, waf, monitor_settings, ip, rules and rule_prioritization.

```py
class WAFConfig(BaseModel):
    Resource: Resource
    Waf: WAF
    Monitor_Settings: MonitorSettings
    IP: List[IPRule]
    Rules: Rules
    Rule_Prioritization: RulePrioritization
```

- resource: What kind of resource the WAF to build upon.
- waf: It is the profile of the WAF, describing the WAF metadata.
- monitor_settings: Describes AWS CloudFront monitor settings.
- ip: Assign IP and give action, such as blocking an IP and allowing and IP.
- rules: WAF rules configuration. After a long period of research on each web exploit payload, we extract their main pattern to form our robust rules for customers. We also provide custom rule option for you to make your own rules! Our strong regex set will asist customer in the rule customize process.
- rule_prioritization: Which rule will be apply first. Be careful for the priority settings, a subtle change may result in distinct result. We recommand to put your own customized rule set at the higher priority, and then our prdefined robust rule set and then aws provided ruleset.

```py
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

class RulePrioritization(BaseModel):
    pass
```

## Basic structure of a rule packages data format
For rule package part, it might contain several types of rules, such as SQL injection, XSS and CSRF. The following are all the options we provide:
- SQLi
- XSS

```py
class RulePackage(BaseModel):
    SQLi: Optional[SQLi]
    XSS: Optional[XSS]
```
For each security aspect, it has the following information:
- mode: customer's level
- set: the rules we provide for preventing particular attack.

```py
class XSS(BaseModel):
    Mode: Optional[Literal["disable", "default", "test", "advanced"]]
    XSS_Set: List[xssRule]

class SQLi(BaseModel):
    Mode: Optional[Literal["disable", "default", "test", "advanced"]]
    SQLi_Set: List[sqliRule]
```


For each set, it contains multiple choices of rules for customers. For each rule, it includes the following information:
- rule id
- chosem: whether it is chosen or not
- action: the action we use for that single rule

```py
class xssRule(BaseModel):
    Rule_Id: str
    Chosen: bool
    Action: Optional[Literal["block", "allow", "count", "Captcha", "Challenge"]]

class sqliRule(BaseModel):
    Rule_Id: str
    Chosen: bool
    Action: Optional[Literal["block", "allow", "count", "Captcha", "Challenge"]]
```



## Basic structure of a custom rule data format
In this part, we use the Rules Class to get all the customized rules.

```py
class Rules(BaseModel):
    Rule_Package: Optional[RulePackage] = None
    Rule_Created: Optional[List[Rule]] = None
```

For each rule, we use the Rule Class to define.

```py
class Rule(BaseModel):
    Name: str
    Priority: int
    Action: Action
    Visibility_Config: VisibilityConfig
    Statement: Statements
```

Later, we will go through every parts in this class.

---

## action module
In this part, there are 5 actions.
```py
class Action(BaseModel):
    Block: Optional[BlockAction] = None
    Allow: Optional[AllowAction] = None
    Count: Optional[CountAction] = None
    Captcha: Optional[CaptchaAction] = None
    Challenge: Optional[ChallengeAction] = None
```
For each action, the definition is like the following content:

```py
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
```
Then we will go to the class definition below the Action module.

---

## custom_response module
```py
class CustomResponse(BaseModel):
    Response_Headers: List[Header]
    Response_Code: str
    Custom_Response_Body_Key: str
```

### custom_request module
```py
class CustomRequest(BaseModel):
    Custom_Request_Handling: Dict[str, List[Header]]
```

### CaptchaConfig module
```py
class ImmunityTimeProperty(BaseModel):
    Immunity_Time: str

class CaptchaConfig(BaseModel):
    Immunity_Time_Property: ImmunityTimeProperty
```

The Class Header is defined like the following:
```py
class Header(BaseModel):
    Name: str
    Value: str
```
---
## statement module

A statement is the main logic of the rule. A statement can be derived into normal_statement, not_statement, or_statement, and_statement and rate_statement.

- normal_statement: Action will be apply if the inspect string match the criteria.
- not_statement: Action will be apply if the inspect string doesn't match the criteria.
- or_statement: Action will be apply if the inspect string fits any criteria.
- and_statement: Action will be apply if the inspect string fits every criteria.
- rate_statement: Limitation will be apply if the request that matches the criteria send over a predefined rate.

${Statement} -> ${normal_statement} | ${not_statement} | ${or_statement} | ${and_statement} | ${rate_statement}
```py
class StatementContent(BaseModel):
    Match_Statement: Union[MatchStatement, None] = None
    Not_Statement: Union[NotStatement, None] = None
    Or_Statement: Union[OrStatement, None] = None
    And_Statement: Union[AndStatement, None] = None

class Statements(BaseModel):
    Statement_Type: Literal["MatchStatement","NotStatement","OrStatement","AndStatement"]
    Statement_Content: StatementContent
```

For each statement_type, the definitions is like the following:
```py
class MatchStatement(BaseModel):
    Selected_Statement: SelectedStatements
    
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
```
---
## matchType module
In MatchStatement, there are many types:
```py
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
   
```

Here is the definition for every class in detailed.

```py
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
```

For the parameter "Field_To_Match," the value assigned to it should be the one we define in inspect module. All the statements in this module is like the Union list below, and we will explain them later.

```py
class FieldToMatch(BaseModel):
    # inspect
    Field: Union[
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
```
## Inspect module
```py
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
```
---
## rate_type module

```py

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
```
--- 
## AggregateKeyType
Here are the key's types:
```py
Aggregation_Key = Union[
    QueryStringKey,
    QueryArgumentKey,
    LabelNamespaceKey,
    HeaderKey,
    HTTPMethodKey,
    UriPathKey,
    CookieKey
]
```
For each key, the definition is like the following:
```py
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
```
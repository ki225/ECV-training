# request_structure_and_format_design
## Overview of request body
We design the request structure according to the essential parameters required when creating a WAF. The request data will be transfered in JSON format. There are 6 main part to form the whole reques, including resource, waf, monitor_settings, ip, rules and rule_prioritization.
- resource: What kind of resource the WAF to build upon.
- waf: It is the profile of the WAF, describing the WAF metadata.
- monitor_settings: Describes AWS CloudFront monitor settings.
- ip: Assign IP and give action, such as blocking an IP and allowing and IP. 
- rules: WAF rules configuration. After a long period of research on each web exploit payload, we extract their main pattern to form our robust rules for customers. We also provide custom rule option for you to make your own rules! Our strong regex set will asist customer in the rule customize process.
- rule_prioritization: Which rule will be apply first. Be careful for the priority settings, a subtle change may result in distinct result. We recommand to put your own customized rule set at the higher priority, and then our prdefined robust rule set and then aws provided ruleset.

For resource type abbreviations:
- alb = Application Load Balancer
- api = Amazon API GaREST API
- runner = Amazon App Rservice
- graph = AWS ApGraphQL API
- cognito = Amazon Couser pool
- access = AWS VerAccess

```
{
    "resource": {
        "type": "cloudfront",
        "region": "global",
        "resource-arn": "string"
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
            "cidr": "10.0.0.0/0"
        }
    ],
    "rules": {
        "rule_package": {
            "SQLi": {
                "mode": "",
                "SQLi-set": [
                    {
                        "rule_id": "",
                        "chosen": "",
                        "action": ""
                    }
                ]
            },
            "XSS": {
                "mode": "",
                "XSS-set": [
                    {
                        "rule_id": "",
                        "chosen": "",
                        "action": ""
                    }
                ]
            }
        },
        "rule_created": [
            {
                // Will be discussed bellow
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
```

## Custom rule format design
The custom rule creation process is extremely complax. Therefor, we designed this part in a modular way to make the overall development easier.
### Basic structure of a custom rule data format
In each section wrapped by ${} is a module. A module is a function in the front-end javascript code.
```
{
    "Name": "name",
    "Priority": ${priority},
    "Action": {
        ${action}
    },
    "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "${the name created in monitor field of the form}"
    },
    "Statement": {
        "Statement_type": "",
        ${statement}
    },
    "RuleLabels": [
         ${labels}
    ]
}
```

### action module
Describes the action for specific rules, rule groups and IPs.
```
if block,
${action} =  "Block": {
    ${custom_response} //optional
 }

if allow, -----------------------------------------> doesn't exist in rate based rule
${action} =
"Allow": {
    ${custom_request} //optional
}
 
if count,
${action} = 
"Count": {
    ${custom_request} //optional
    } 

       
if CAPTCHA,
${action} =
"Captcha": {
      ${custom_request} //if chosed
    }

*** if "Set a custom immunity time for this rule" is checked, add the following to the level same as action block
"CaptchaConfig": {
    "ImmunityTimeProperty": {
      "ImmunityTime": "500"
    }
  }
      

if challange,
${action} =
"Challenge": {}

*** if "Set a custom immunity time for this rule" is checked, add the following to the level same as action block
"ChallengeConfig": {
    "ImmunityTimeProperty": {
      "ImmunityTime": "500"
    }
  }
```


### custom_response module
For the "block" action, customize the response send back to the user.
```
"CustomResponse": {
        "ResponseHeaders": [ // multiple
          {
            "Name": "sd",
            "Value": "ff"
          }
         ],
        "ResponseCode": "501",
        "CustomResponseBodyKey": "ddd"
}
```


### custom_request module
For the "allow", "count" and captcha" action, customize the response send back to the user.
```
"CustomRequestHandling": {
    "InsertHeaders": [
      {
        "Name": "r",
        "Value": "r"
      }
    ]
}
```

### statement module
A statement is the main logic of the rule. A statement can be derived into normal_statement, not_statement, or_statement, and_statement and rate_statement. 
- normal_statement: Action will be apply if the inspect string match the criteria.
- not_statement: Action will be apply if the inspect string doesn't match the criteria.
- or_statement: Action will be apply if the inspect string fits any criteria.
- and_statement: Action will be apply if the inspect string fits every criteria.
- rate_statement: Limitation will be apply if the request that matches the criteria send over a predefined rate.

${Statement} -> ${normal_statement} | ${not_statement} | ${or_statement} | ${and_statement} | ${rate_statement} 

```
${normal_statement} = ${matchType}

${not_statement}  = 
"NotStatement": {
  "Statement": {
    ${matchType}
  }
}

${or_statement} = 
"OrStatement" :{
  "Statement_Amount" = "",
  "Statements": [
    {
      ${normal_statement} or ${not_statement} 
    },
    {
    }        
  ]
}

${and_statement} =
"AndStatement" :{
    "Statement_Amount" = "",
  "Statements": [
    {
      ${normal_statement} or ${not_statement} 
    },
    {
    }        
  ]
}

${rate_statement} =
"RateBasedStatement": {
        "Limit": "200", //  100 ~ 2,000,000,000.
        "EvaluationWindowSec": 300, // 60, 120, 300, 600
        "AggregateKeyType": "FORWARDED_IP", //FORWARDED_IP/IP/CUSTOM_KEYS/CONSTANT
        ${rate_type}        
}
```

### matchType module
Match type describe the type of the criteria.
```
//originCountry-sourceIp
"GeoMatchStatement": {
    "CountryCodes": [ //multiple
        //AD, AE, AF, AG, AI, AL, AM, AO, AQ, AR, AS, AT, AU, AW, AX, AZ, BA, BB, BD, BE, BF, BG, BH, BI, BJ, BL, BM, BN, BO, BQ, BR, BS, BT, BV, BW, BY, BZ, CA, CC, CD, CF, CG, CH, CI, CK, CL, CM, CN, CO, CR, CU, CV, CW, CX, CY, CZ, DE, DJ, DK, DM, DO, DZ, EC, EE, EG, EH, ER, ES, ET, FI, FJ, FK, FM, FO, FR, GA, GB, GD, GE, GF, GG, GH, GI, GL, GM, GN, GP, GQ, GR, GS, GT, GU, GW, GY, HK, HM, HN, HR, HT, HU, ID, IE, IL, IM, IN, IO, IQ, IR, IS, IT, JE, JM, JO, JP, KE, KG, KH, KI, KM, KN, KP, KR, KW, KY, KZ, LA, LB, LC, LI, LK, LR, LS, LT, LU, LV, LY, MA, MC, MD, ME, MF, MG, MH, MK, ML, MM, MN, MO, MP, MQ, MR, MS, MT, MU, MV, MW, MX, MY, MZ, NA, NC, NE, NF, NG, NI, NL, NO, NP, NR, NU, NZ, OM, PA, PE, PF, PG, PH, PK, PL, PM, PN, PR, PS, PT, PW, PY, QA, RE, RO, RS, RU, RW, SA, SB, SC, SD, SE, SG, SH, SI, SJ, SK, SL, SM, SN, SO, SR, SS, ST, SV, SX, SY, SZ, TC, TD, TF, TG, TH, TJ, TK, TL, TM, TN, TO, TR, TT, TV, TW, TZ, UA, UG, UM, US, UY, UZ, VA, VC, VE, VG, VI, VN, VU, WF, WS, XK, YE, YT, ZA, ZM, ZW
    ]
}
//originCountry-ipHeader
"GeoMatchStatement": {
    "CountryCodes": [ // multiple
        //AD, AE, AF, AG, AI, AL, AM, AO, AQ, AR, AS, AT, AU, AW, AX, AZ, BA, BB, BD, BE, BF, BG, BH, BI, BJ, BL, BM, BN, BO, BQ, BR, BS, BT, BV, BW, BY, BZ, CA, CC, CD, CF, CG, CH, CI, CK, CL, CM, CN, CO, CR, CU, CV, CW, CX, CY, CZ, DE, DJ, DK, DM, DO, DZ, EC, EE, EG, EH, ER, ES, ET, FI, FJ, FK, FM, FO, FR, GA, GB, GD, GE, GF, GG, GH, GI, GL, GM, GN, GP, GQ, GR, GS, GT, GU, GW, GY, HK, HM, HN, HR, HT, HU, ID, IE, IL, IM, IN, IO, IQ, IR, IS, IT, JE, JM, JO, JP, KE, KG, KH, KI, KM, KN, KP, KR, KW, KY, KZ, LA, LB, LC, LI, LK, LR, LS, LT, LU, LV, LY, MA, MC, MD, ME, MF, MG, MH, MK, ML, MM, MN, MO, MP, MQ, MR, MS, MT, MU, MV, MW, MX, MY, MZ, NA, NC, NE, NF, NG, NI, NL, NO, NP, NR, NU, NZ, OM, PA, PE, PF, PG, PH, PK, PL, PM, PN, PR, PS, PT, PW, PY, QA, RE, RO, RS, RU, RW, SA, SB, SC, SD, SE, SG, SH, SI, SJ, SK, SL, SM, SN, SO, SR, SS, ST, SV, SX, SY, SZ, TC, TD, TF, TG, TH, TJ, TK, TL, TM, TN, TO, TR, TT, TV, TW, TZ, UA, UG, UM, US, UY, UZ, VA, VC, VE, VG, VI, VN, VU, WF, WS, XK, YE, YT, ZA, ZM, ZW
    ],
    "ForwardedIPConfig": {
        "HeaderName": "X-Forwarded-For",
        "FallbackBehavior": "MATCH/NO_MATCH" // MATCH/NOTMATCH
    }
}
//originIp-sourceIp
"IPSetReferenceStatement": { //existed ip set
    "ARN": "arn:aws:wafv2:us-east-1:812428033092:regional/ipset/test/ff24bb02-3ee1-4708-8b74-0de09602cf4c"
}
//originIp-ipHeader
"IPSetReferenceStatement": { //existed ip set
    "ARN": "arn:aws:wafv2:us-east-1:812428033092:regional/ipset/test/ff24bb02-3ee1-4708-8b74-0de09602cf4c",
    "IPSetForwardedIPConfig": {
        "HeaderName": "X-Forwarded-For",
        "FallbackBehavior": "NO_MATCH", // MATCH / NO_MATCH
        "Position": "FIRST" // LAST / FIRST / ANY
    }
}
//label-label
"LabelMatchStatement": {
    "Scope": "LABEL",
    "Key": "wswaf:managed:aws:managed-rule-set:namespace1:name" // no colon at the end
}
//label-nameSpace
"LabelMatchStatement": {
    "Scope": "NAMESPACE",
    "Key": "awswaf:111122223333:rulegroup:testRules:namespace1:namespace2:" // have colon at the end
}
//(inspect other than originCountry, originIp, and label)-(exactly/starts/ends/containString/containWord)
"ByteMatchStatement": {
    "FieldToMatch": {
        ${inspect}
    },
    "PositionalConstraint": "EXACTLY", // EXACTLY/STARTS_WITH/ENDS_WITH/CONTAINS/CONTAINS_WORD
    "SearchString": "asdsaaa",
    "TextTransformations": [ // multiple up to 10
        {
            "Type": "COMPRESS_WHITE_SPACE", //NONE/COMPRESS_WHITE_SPACE/HTML_ENTITY_DECODE/LOWERCASE/CMD_LINE/URL_DECODE          //BASE64_DECODE/HEX_DECODE/MD5/REPLACE_COMMENTS/ESCAPE_SEQ_DECODE/           //SQL_HEX_DECODE/CSS_DECODE/JS_DECODE/NORMALIZE_PATH/NORMALIZE_PATH_WIN/            //REMOVE_NULLS/REPLACE_NULLS/BASE64_DECODE_EXT/URL_DECODE_UNI/UTF8_TO_UNICODE
            "Priority": 0
        }
    ]
}
//(inspect other than originCountry, originIp, and label)-regexSet
"RegexPatternSetReferenceStatement": {
    "FieldToMatch": {
        ${inspect}
    },
    // exist regex pattern set
    "ARN": "arn:aws:wafv2:us-east-1:812428033092:regional/regexpatternset/test/af771c8d-4c0b-46c0-ac70-5a795f684d2f",
    "TextTransformations": [ //multiple up to 10
        {
            "Type": "NONE",
            "Priority": 0
        }
    ]
}
//(inspect other than originCountry, originIp, and label)-regex
"RegexMatchStatement": {
    "FieldToMatch": {
        ${inspect}
    },
    "TextTransformations": [ // multiple up to 10
        {
            "Type": "NONE",
            "Priority": 0
        }
    ],
    "RegexString": "string" // self defined
}
//(inspect other than originCountry, originIp, and label)-(sizeEq/sizeNotEq/sizeLessOrEq/sizeLess/sizeGrOrEq/sizeGr)
"SizeConstraintStatement": {
    "FieldToMatch": {
        ${inspect}
    },
    "ComparisonOperator": "EQ", //EQ/NE/LE/LT/GE/GT
    "Size": "1",
    "TextTransformations": [ // multiple up to 10
        {
            "Type": "NONE",
            "Priority": 0
        }
    ]
}
//(inspect other than originCountry, originIp, and label)-sqli
"SqliMatchStatement": {
    "FieldToMatch": {
        ${inspect}
    },
    "TextTransformations": [ // multiple up to 10
        {
            "Type": "NONE",
            "Priority": 0
        }
    ],
    "SensitivityLevel": "LOW" //LOW/HIGH
}
//(inspect other than originCountry, originIp, and label)-xss
"XssMatchStatement": {
    "FieldToMatch": {
        ${inspect}
    },
    "TextTransformations": [ // multiple up to 10
        {
            "Type": "NONE",
            "Priority": 0
        }
    ]
}
```

### Inspect module
Inspect area describe where to apply the criteria check.
```
//singleHeader
"SingleHeader": {
    "Name": "string"
}
//allHeader-allHeader
"Headers": {
    "MatchScope": "ALL", //ALL/KEY/VALUE
    "MatchPattern": {
        "All": {}
    },
    "OversizeHandling": "CONTINUE" //CONTINUE/MATCH/NO_MATCH
}
// allHeader-include
"Headers": {
    "MatchScope": "ALL",
    "MatchPattern": {
        "IncludedHeaders": [ // self-defined multiple
            "sdws"
        ]
    },
    "OversizeHandling": "NO_MATCH" //CONTINUE/MATCH/NO_MATCH
}
// allHeader-exclude-*
"Headers": {
    "MatchScope": "ALL",
    "MatchPattern": {
        "ExcludedHeaders": [ // self-defined multiple
            "wed"
        ]
    },
    "OversizeHandling": "NO_MATCH" //CONTINUE/MATCH/NO_MATCH
}
// cookie-allHeader-*
"Cookies": {
    "MatchScope": "VALUE",
    "MatchPattern": {
        "All": {}
    },
    "OversizeHandling": "NO_MATCH" //CONTINUE/MATCH/NO_MATCH
}
// cookie-include-*
"Cookies": {
    "MatchScope": "VALUE",
    "MatchPattern": {
        "IncludedCookies": [
            "asdf"
        ]
    },
    "OversizeHandling": "NO_MATCH" //CONTINUE/MATCH/NO_MATCH
}
// cookie-exclude-*
"Cookies": {
    "MatchScope": "VALUE",
    "MatchPattern": {
        "ExcludedCookies": [
            "sdfg"
        ]
    },
    "OversizeHandling": "NO_MATCH" //CONTINUE/MATCH/NO_MATCH
}
// singleQuery-*
"SingleQueryArgument": {
    "Name": "aaaa"
}
// allQuery-*
"AllQueryArguments": {}
// uri-*
"UriPath": {}
// queryString-*
"QueryString": {}
// body-plainText-*
"Body": {
    "OversizeHandling": "CONTINUE" //CONTINUE/MATCH/NO_MATCH
}
// body-json-full-*
"JsonBody": {
    "MatchScope": "KEY", //ALL/KEY/VALUE
    "InvalidFallbackBehavior": "MATCH", //EVALUATE_AS_STRING/MATCH/NO_MATCH -> if None is chosen, 
    // this field will not exist
    "MatchPattern": {
        "All": {}
    },
    "OversizeHandling": "CONTINUE" //CONTINUE/MATCH/NO_MATCH
}
// body-json-element-*
"JsonBody": {
    "MatchScope": "ALL",
    "InvalidFallbackBehavior": "EVALUATE_AS_STRING", //EVALUATE_AS_STRING/MATCH/NO_MATCH
    // -> if None is chosen, this field will not exist
    "MatchPattern": {
        "IncludedPaths": [
            "/a/s/d"
        ]
    },
    "OversizeHandling": "CONTINUE" //CONTINUE/MATCH/NO_MATCH
}
// JA3Fingerprint
"JA3Fingerprint": {
    "FallbackBehavior": "MATCH"
}
// header order
"HeaderOrder": {
    "OversizeHandling": "CONTINUE"
}
// http
"Method": {}
```


### rate_type module
Describe the aggreation type of requests.
```
if "AggregateKeyType": "FORWARDED_IP"
then ${rate_type} =
"ForwardedIPConfig": {
    "HeaderName": "X-Forwarded-For",
    "FallbackBehavior": "MATCH" // "No_MATCH"
},
// only shown when choose "Only consider requests that match the criteria in a rule statement"      
"ScopeDownStatement": {
    ${matchType}
}



"AggregateKeyType": "IP"
then ${rate_type} =
// only shown when choose "Only consider requests that match the criteria in a rule statement"      
"ScopeDownStatement": {
    ${matchType}
}



"AggregateKeyType": "CUSTOM_KEYS",
then ${rate_type} =
"CustomKeys": [
    {
        ${aggregation_key}
    }
],
// only shown when choose "Only consider requests that match the criteria in a rule statement"      
"ScopeDownStatement": {
    ${matchType}
}



"AggregateKeyType": "CONSTANT"
then ${rate_type} =
"ScopeDownStatement": {
    ${matchType}
}
```


### aggregation_key module
Describe the custom aggregation key.
```
if "QueryString" checked,
then ${aggregation_key} =
// Query String
"QueryString": {
    "TextTransformations": [
        {
            "Type": "NONE",
//NONE/COMPRESS_WHITE_SPACE/HTML_ENTITY_DECODE/LOWERCASE/CMD_LINE/URL_DECODE          //BASE64_DECODE/HEX_DECODE/MD5/REPLACE_COMMENTS/ESCAPE_SEQ_DECODE/           //SQL_HEX_DECODE/CSS_DECODE/JS_DECODE/NORMALIZE_PATH/NORMALIZE_PATH_WIN/            //REMOVE_NULLS/REPLACE_NULLS/BASE64_DECODE_EXT/URL_DECODE_UNI/UTF8_TO_UNICODE            
            "Priority": 0
        }
    ]
}

if "QueryArgument" checked,
then ${aggregation_key} =
// Query Argument
"QueryArgument": {
    "Name": "ghiuhihi",
    "TextTransformations": [
        {
            "Type": "NONE",
//NONE/COMPRESS_WHITE_SPACE/HTML_ENTITY_DECODE/LOWERCASE/CMD_LINE/URL_DECODE          //BASE64_DECODE/HEX_DECODE/MD5/REPLACE_COMMENTS/ESCAPE_SEQ_DECODE/           //SQL_HEX_DECODE/CSS_DECODE/JS_DECODE/NORMALIZE_PATH/NORMALIZE_PATH_WIN/            //REMOVE_NULLS/REPLACE_NULLS/BASE64_DECODE_EXT/URL_DECODE_UNI/UTF8_TO_UNICODE            
            "Priority": 0
        }
    ]
}

if "LabelNamespace" checked,
then ${aggregation_key} =
// label namespace
{
    "LabelNamespace": {
        "Namespace": "xxxxx" // Valid characters should follow:  A-Z, a-z, 0-9, colon (:), - (hyphen), and _ (underscore).
    }
},

if "Header" checked,
then ${aggregation_key} =
// Header
{
    "Header": {
        "Name": "test",
        "TextTransformations": [
            {
                "Type": "COMPRESS_WHITE_SPACE", //NONE/COMPRESS_WHITE_SPACE/HTML_ENTITY_DECODE/LOWERCASE/CMD_LINE/URL_DECODE          //BASE64_DECODE/HEX_DECODE/MD5/REPLACE_COMMENTS/ESCAPE_SEQ_DECODE/           //SQL_HEX_DECODE/CSS_DECODE/JS_DECODE/NORMALIZE_PATH/NORMALIZE_PATH_WIN/            //REMOVE_NULLS/REPLACE_NULLS/BASE64_DECODE_EXT/URL_DECODE_UNI/UTF8_TO_UNICODE
                "Priority": 0
            }
        ]
    }
},

if "HTTPMethod" checked,
then ${aggregation_key} =
// HTTP method
{
    "HTTPMethod": {}
}

if "UriPath" checked,
then ${aggregation_key} =
// URI path 
{
    "UriPath": {
        "TextTransformations": [
            {
                "Type": "UTF8_TO_UNICODE",
//NONE/COMPRESS_WHITE_SPACE/HTML_ENTITY_DECODE/LOWERCASE/CMD_LINE/URL_DECODE          //BASE64_DECODE/HEX_DECODE/MD5/REPLACE_COMMENTS/ESCAPE_SEQ_DECODE/           //SQL_HEX_DECODE/CSS_DECODE/JS_DECODE/NORMALIZE_PATH/NORMALIZE_PATH_WIN/            //REMOVE_NULLS/REPLACE_NULLS/BASE64_DECODE_EXT/URL_DECODE_UNI/UTF8_TO_UNICODE                
                "Priority": 0
            }
        ]
    }
}

if "Cookie" checked,
then ${aggregation_key} =
// cookie
{
    "Cookie": {
        "Name": "cookie_name",
        "TextTransformations": [
            {
                "Type": "URL_DECODE", //NONE/COMPRESS_WHITE_SPACE/HTML_ENTITY_DECODE/LOWERCASE/CMD_LINE/URL_DECODE          //BASE64_DECODE/HEX_DECODE/MD5/REPLACE_COMMENTS/ESCAPE_SEQ_DECODE/           //SQL_HEX_DECODE/CSS_DECODE/JS_DECODE/NORMALIZE_PATH/NORMALIZE_PATH_WIN/            //REMOVE_NULLS/REPLACE_NULLS/BASE64_DECODE_EXT/URL_DECODE_UNI/UTF8_TO_UNICODE
                "Priority": 0
            }
        ]
    }
}
```




### labels module
Add labels to the request matching the rule.
```
{
      "Name": "aaaaa:ddddd"
},
{
}
```

 

variable "resource" {
  description = "Details of the resource to which the WAF will be applied"
  type = object({
    type         = string
    region       = string
    resource_arn = string
  })
  validation {
    condition     = contains(["cloudfront", "alb", "apigw"], var.resource.type)
    error_message = "Resource type must be one of: cloudfront, alb, or apigw."
  }
}

variable "waf" {
  description = "WAF configuration details"
  type = object({
    name         = string
    description  = string
    inspection   = string
  })
  validation {
    condition     = var.waf.inspection == "16KB" || var.waf.inspection == "50KB"
    error_message = "Inspection size must be either 16KB or 50KB."
  }
}

variable "monitor_settings" {
  description = "Monitoring settings for the WAF"
  type = object({
    cw_metric_name = string
    option         = string
  })
}

variable "ip_rules" {
  description = "List of IP rules for the WAF"
  type = list(object({
    action = string
    cidr   = string
  }))
  validation {
    condition     = alltrue([for rule in var.ip_rules : contains(["block", "allow"], rule.action)])
    error_message = "IP rule action must be either 'block' or 'allow'."
  }
}

variable "managed_rule_groups" {
  description = "Managed rule groups configuration"
  type = object({
    SQLi = object({
      mode     = string
      rule_set = list(object({
        rule_id = string
        rule    = string
        chosen  = bool
      }))
    })
    XSS = object({
      mode     = string
      rule_set = list(object({
        rule_id = string
        rule    = string
        chosen  = bool
      }))
    })
  })
}

variable "custom_rules" {
  description = "List of custom rules for the WAF"
  type = list(object({
    action      = string
    description = string
    rule        = string
  }))
}

variable "rule_prioritization" {
  description = "Rule prioritization configuration"
  type = object({
    description = string
    order       = list(string)
  })
}
variable "project" {
  type        = string
  default     = "boy-v2-dev"
  description = "Boy project version (prod/dev)"
}

variable "run_version" {
  type    = string
  default = "-dev"
}

variable "region" {
  type    = string
  default = "europe-west3"
}

variable "credentials" {
  type    = string
  default = "../../credentials/terraform.json"
}

variable "name" {
  type        = string
  default     = ""
  description = "Resource name"
}

variable "enabled" {
  type        = bool
  default     = true
  description = "Set to false to prevent the module from creating any resources"
}

variable "attributes" {
  type        = list(string)
  default     = []
  description = "Additional attributes"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Additional tags"
}

variable "context" {
  type = object({
    project    = string
    stage      = string
    name       = string
    enabled    = bool
    attributes = list(string)
    tags       = map(string)
  })
  default = {
    project    = "boy-v2-dev"
    stage      = ""
    name       = ""
    enabled    = true
    attributes = []
    tags       = {}
  }
  description = "Default context to use for passing state between label invocations"
}
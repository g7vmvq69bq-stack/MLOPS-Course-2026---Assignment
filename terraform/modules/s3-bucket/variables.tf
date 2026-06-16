variable "key" {
  description = "Base name for the bucket (environment suffix is added by locals)"
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev, tst, prd)"
  type        = string
}

variable "delimiter" {
  description = "Delimiter between name parts"
  type        = string
  default     = "-"
}

variable "tags" {
  description = "Map of tags to attach to the bucket"
  type        = map(string)
  default     = {}
}

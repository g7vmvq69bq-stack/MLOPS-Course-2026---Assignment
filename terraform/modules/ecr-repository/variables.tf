variable "key" {
  description = "Base name for the ECR repository"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "delimiter" {
  description = "Delimiter between name parts"
  type        = string
  default     = "-"
}

variable "image_tag_mutability" {
  description = "MUTABLE allows overwriting tags (e.g. 'latest'); IMMUTABLE prevents it"
  type        = string
  default     = "MUTABLE"
}

variable "scan_on_push" {
  description = "Scan images for vulnerabilities when pushed"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to attach to the repository"
  type        = map(string)
  default     = {}
}

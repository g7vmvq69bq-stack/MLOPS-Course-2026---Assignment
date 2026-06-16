variable "aws_region" {
  description = "AWS region where resources are deployed"
  type        = string
  default     = "eu-west-3"
}

variable "environment" {
  description = "Deployment environment (dev, tst, prd)"
  type        = string
  default     = "dev"
}

variable "delimiter" {
  description = "Delimiter used between resource name parts"
  type        = string
  default     = "-"
}

variable "s3_buckets" {
  description = "List of S3 buckets to create via the s3-bucket module"
  type        = list(any)
  default     = []
}

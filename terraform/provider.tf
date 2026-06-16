terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=5.97"
    }
  }

  # Remote backend: state is stored in a shared S3 bucket instead of locally.
  # The actual bucket/key/region values come from backends/dev.conf at init time.
  # This solves the "state file on one laptop" problem from Phase 1.
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

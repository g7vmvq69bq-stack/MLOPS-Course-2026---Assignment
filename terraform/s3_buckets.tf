# This file calls the s3-bucket module once for every entry in var.s3_buckets.
# for_each turns the list into a map keyed by bucket name, then Terraform
# creates one module instance (= one S3 bucket) per entry.
#
# To add a new bucket, just add one line to environments/dev.tfvars — no
# copy-pasting of resource blocks needed.

module "s3_bucket" {
  for_each = { for s3 in var.s3_buckets : s3.key => s3 }
  source   = "./modules/s3-bucket"

  key         = each.value.key
  environment = var.environment
  delimiter   = var.delimiter
  tags        = merge(try(each.value.tags, {}), { environment = var.environment })
}

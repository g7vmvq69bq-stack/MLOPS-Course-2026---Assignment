# Reusable S3 bucket module.
# Instead of copy-pasting the same resource block for every bucket,
# we define it once here and call it with different variables each time.
# This is the DRY (Don't Repeat Yourself) principle applied to infrastructure.

resource "aws_s3_bucket" "s3" {
  bucket = local.name
  tags   = var.tags
}

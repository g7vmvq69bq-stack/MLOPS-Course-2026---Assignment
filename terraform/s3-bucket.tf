resource "aws_s3_bucket" "my_bucket" {
  # Bucket names are globally unique across ALL of AWS.
  # This name includes the AWS account ID to guarantee uniqueness.
  bucket = "mlops-course-2026-20916836"

  tags = {
    Environment = "dev"
    Project     = "mlops-course-2026"
  }
}

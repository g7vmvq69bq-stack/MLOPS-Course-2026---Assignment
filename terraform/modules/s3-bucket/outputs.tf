output "data" {
  description = "The full S3 bucket object (exposes id, arn, etc. to the caller)"
  value       = aws_s3_bucket.s3
}

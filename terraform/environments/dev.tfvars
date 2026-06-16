environment = "dev"
aws_region  = "eu-west-3"

# Each entry here creates one S3 bucket via the s3-bucket module.
# Adding a new bucket = adding one line to this list.
s3_buckets = [
  {
    key  = "mlops-course-datastore"
    tags = {}
  }
]

environment = "dev"
aws_region  = "eu-west-3"

# ── S3 Buckets ────────────────────────────────────────────────────────────────
s3_buckets = [
  {
    key  = "mlops-course-datastore"
    tags = {}
  }
]

# ── ECR Repository ────────────────────────────────────────────────────────────
# Stores the Docker images built by the application CI/CD pipeline.
ecr_repositories = [
  {
    key                  = "mlops-course-app"
    image_tag_mutability = "MUTABLE"
    scan_on_push         = true
    tags                 = {}
  }
]

# ── ECS Fargate Service ───────────────────────────────────────────────────────
# Pulls the latest image from ECR and runs it as a live web service.
# Replace YOUR_ACCOUNT_ID with: 274020916836
ecs_services = [
  {
    key            = "mlops-course-app"
    image_url      = "274020916836.dkr.ecr.eu-west-3.amazonaws.com/mlops-course-app-dev"
    image_tag      = "latest"
    container_name = "app"
    container_port = 80
    cpu            = 256
    memory         = 512
    desired_count  = 1
    tags           = {}
  }
]

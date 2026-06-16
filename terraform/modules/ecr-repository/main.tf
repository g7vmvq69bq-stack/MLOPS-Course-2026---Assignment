# WHY ECR:
# We build a Docker image locally (or in CI), but where does it live so
# that AWS ECS can pull it? ECR (Elastic Container Registry) is AWS's
# private Docker image storage. It's like Docker Hub but inside your AWS
# account — images are versioned and only your services can access them.

resource "aws_ecr_repository" "ecr" {
  name                 = local.name
  image_tag_mutability = var.image_tag_mutability

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }

  tags = var.tags
}

# Lifecycle policy: keep only the last 10 images to control storage costs
resource "aws_ecr_lifecycle_policy" "ecr" {
  repository = aws_ecr_repository.ecr.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 10 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 10
      }
      action = { type = "expire" }
    }]
  })
}

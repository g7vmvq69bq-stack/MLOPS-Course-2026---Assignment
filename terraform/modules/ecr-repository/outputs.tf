output "repository_url" {
  description = "Full ECR URL — used by docker push and ECS task definition"
  value       = aws_ecr_repository.ecr.repository_url
}

output "repository_name" {
  description = "Repository name"
  value       = aws_ecr_repository.ecr.name
}

output "data" {
  description = "Full ECR repository object"
  value       = aws_ecr_repository.ecr
}

variable "key" {
  description = "Base name for the ECS cluster and service"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "delimiter" {
  description = "Delimiter between name parts"
  type        = string
  default     = "-"
}

variable "image_url" {
  description = "ECR repository URL (without tag)"
  type        = string
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "container_name" {
  description = "Name of the container inside the task definition"
  type        = string
  default     = "app"
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 80
}

variable "cpu" {
  description = "CPU units for the Fargate task (256 = 0.25 vCPU)"
  type        = number
  default     = 256
}

variable "memory" {
  description = "Memory in MB for the Fargate task"
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Number of container replicas to run"
  type        = number
  default     = 1
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

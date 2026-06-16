# WHY ECS FARGATE:
# We have a Docker image in ECR. Now we need something to actually RUN it
# 24/7 in the cloud. ECS Fargate is AWS's serverless container service —
# you say "run this image on port 80 with 256 CPU units" and AWS handles
# all the underlying servers. No EC2 instances to manage.
#
# The four pieces needed:
#   1. Cluster  — logical grouping (like a namespace)
#   2. Task Definition — blueprint: which image, how much CPU/memory, which port
#   3. Service  — keeps N copies of the task running (restarts if it crashes)
#   4. Security Group — firewall: who can reach the service and what it can reach

# ── IAM Role so ECS can pull the image from ECR ───────────────────────────────
data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution" {
  name               = "${local.name}-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
  tags               = var.tags
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ── 1. Cluster ────────────────────────────────────────────────────────────────
resource "aws_ecs_cluster" "cluster" {
  name = local.name
  tags = var.tags
}

# ── 2. Task Definition (blueprint for the container) ─────────────────────────
resource "aws_ecs_task_definition" "task" {
  family                   = local.name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([{
    name      = var.container_name
    image     = "${var.image_url}:${var.image_tag}"
    essential = true
    portMappings = [{
      containerPort = var.container_port
      hostPort      = var.container_port
      protocol      = "tcp"
    }]
  }])

  tags = var.tags
}

# ── 3. Security Group (firewall) ──────────────────────────────────────────────
# NOTE: allowing all ingress (0.0.0.0/0) is fine for this course demo.
# In production you would restrict ingress to a load balancer only.
resource "aws_security_group" "sg" {
  name        = "${local.name}-sg"
  description = "Allow HTTP inbound and all outbound for ${local.name}"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP from anywhere (course demo only)"
    from_port   = var.container_port
    to_port     = var.container_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "All outbound (needed to pull from ECR)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# ── 4. Service (keeps the task running) ───────────────────────────────────────
resource "aws_ecs_service" "service" {
  name            = local.name
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.sg.id]
    assign_public_ip = true  # needed so we can reach it without a load balancer
  }

  tags = var.tags

  # Ignore image changes — the app CI/CD pipeline handles redeployment
  lifecycle {
    ignore_changes = [task_definition]
  }
}

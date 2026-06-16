module "ecs_fargate_service" {
  for_each = { for svc in var.ecs_services : svc.key => svc }
  source   = "./modules/ecs-fargate-service"

  key            = each.value.key
  environment    = var.environment
  delimiter      = var.delimiter
  image_url      = each.value.image_url
  image_tag      = try(each.value.image_tag, "latest")
  container_name = try(each.value.container_name, "app")
  container_port = try(each.value.container_port, 80)
  cpu            = try(each.value.cpu, 256)
  memory         = try(each.value.memory, 512)
  desired_count  = try(each.value.desired_count, 1)
  tags           = merge(try(each.value.tags, {}), { environment = var.environment })
}

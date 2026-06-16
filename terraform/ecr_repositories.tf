module "ecr_repository" {
  for_each = { for r in var.ecr_repositories : r.key => r }
  source   = "./modules/ecr-repository"

  key                  = each.value.key
  environment          = var.environment
  delimiter            = var.delimiter
  image_tag_mutability = try(each.value.image_tag_mutability, "MUTABLE")
  scan_on_push         = try(each.value.scan_on_push, true)
  tags                 = merge(try(each.value.tags, {}), { environment = var.environment })
}

locals {
  name = join(var.delimiter, [var.key, var.environment])
}

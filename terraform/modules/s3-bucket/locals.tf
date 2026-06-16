# locals.tf computes derived values so main.tf stays clean.
# The bucket name is built by joining key + environment with the delimiter,
# e.g. "mlops-course-datastore" + "-" + "dev" = "mlops-course-datastore-dev"

locals {
  name = join(var.delimiter, [var.key, var.environment])
}

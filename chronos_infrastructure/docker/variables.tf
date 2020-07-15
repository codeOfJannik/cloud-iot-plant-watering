// template, to pass optional dependencies from root main.tf
// actual used to pass output from iot_core main.tf "docker_dependencies": wait for all "Thing depended" resources
variable "dependencies" {
  type    = list(any)
  default = []
}

locals {
  files = fileset(path.cwd, "/iot_core/devices/*/config.yaml")
}

variable "aws_endpoint" {
  type = string
  default = ""
}
// template, to pass optional dependencies from root main.tf
// actual used to pass output from iot_core main.tf "docker_dependencies": wait for all "Thing depended" resources
variable "dependencies" {
  type    = list(any)
  default = []
}

// needed to perform a for each file loop
locals {
  files = fileset(path.cwd, "/iot_core/devices/*/emulator_config.yaml")
}

// template to get aws endpoint from root main.tf
variable "aws_endpoint" {
  type = string
  default = ""
}
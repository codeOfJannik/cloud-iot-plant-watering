// template, to pass optional dependencies from root main.tf
// actual used to pass output from iot_core main.tf "docker_dependencies": wait for all "Thing depended" resources
variable "dependencies" {
  type    = list(any)
  default = []
}
// get path to every device policy
locals {
  files = fileset(path.cwd, "/iot_core/devices/*/settings.yaml")
}

// template variable for name ending in aws_iot_policy resource
variable "policy" {
  type = string
  default = "_policy"
}

// template variable for file ending *.cert.pem, used by creating pem files for each device
variable "cert_file_ending" {
  type = string
  default = ".cert.pem"
}

// template variable for file ending *.private.key
variable "private_key_ending" {
  type = string
  default = ".private.key"
}

// template, to pass optional dependencies from root main.tf
// actual used to pass output from iot_events main.tf "iot_core_dependencies": wait for create_event_inputs
variable "dependencies" {
  type    = list(any)
  default = []
}

// get path to every device policy
locals {
  files = fileset(path.cwd, "/iot_core/devices/*/policy.json")
}
// template variable
variable "policy" {
  type = string
  default = "_policy"
}

variable "cert_file_ending" {
  type = string
  default = ".cert.pem"
}

variable "private_key_ending" {
  type = string
  default = ".private.key"
}

variable "dependencies" {
  type    = list(any)
  default = []
}

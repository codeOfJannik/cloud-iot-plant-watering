// template, to pass optional dependencies from root main.tf
// actual not used in the module
variable "dependencies" {
  type    = list(any)
  default = []
}

// next two variables were set to have control of the CLI --profile and --region by the root main.tf file
variable "aws_profile" {
  type = string
  default = "chronos"
}

variable "aws_region" {
  type = string
  default = "us-east-1"
}
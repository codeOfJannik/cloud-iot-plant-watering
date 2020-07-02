variable "dependencies" {
  type    = list(any)
  default = []
}

variable "aws_profile" {
  type = string
  default = "chronos"
}

variable "aws_region" {
  type = string
  default = "us-east-1"
}
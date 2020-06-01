locals {
  files = fileset(path.cwd, "devices/*/policy.json")
}

provider "aws" {
  profile    = "default"
  region     = "us-east-1"
}

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

data "aws_iot_endpoint" "endpointUrl" {
  endpoint_type = "iot:Data-ATS"
}

resource "aws_iot_thing" "thing" {
  for_each = local.files
  name = basename(dirname(each.value))
}

resource "aws_iot_certificate" "thing_cert" {
  for_each = local.files
  active = true
}

data "aws_arn" "thing_instance" {
  for_each = local.files
  arn = aws_iot_thing.thing[each.key].arn
}

resource "aws_iot_policy" "thing_policy" {
  for_each = local.files
  name = "${basename(dirname(each.value))}${var.policy}"
  policy = templatefile(each.value,  {
    clientId = aws_iot_thing.thing[each.key].name,
    arn = "arn:${data.aws_arn.thing_instance[each.key].partition}:${data.aws_arn.thing_instance[each.key].service}:${data.aws_arn.thing_instance[each.key].region}:${data.aws_arn.thing_instance[each.key].account}:"
  }
  )
}

resource "aws_iot_thing_principal_attachment" "att" {
  for_each = local.files
  principal = aws_iot_certificate.thing_cert[each.key].arn
  thing     = aws_iot_thing.thing[each.key].name
}

resource "aws_iot_policy_attachment" "att" {
  for_each =  local.files
  policy = aws_iot_policy.thing_policy[each.key].name
  target = aws_iot_certificate.thing_cert[each.key].arn
}

resource "local_file" "thing_cert_pem" {
  for_each = local.files
  sensitive_content = aws_iot_certificate.thing_cert[each.key].certificate_pem
  file_permission = "0664"
  filename = "${dirname(each.value)}/${basename(dirname(each.value))}${var.cert_file_ending}"
}

resource "local_file" "thing_key_pem" {
  for_each = local.files
  sensitive_content = aws_iot_certificate.thing_cert[each.key].private_key
  file_permission = "0664"
  filename = "${dirname(each.value)}/${basename(dirname(each.value))}${var.private_key_ending}"
}

resource "local_file" "aws_endpoint" {
  filename = ".env"
  content = "AWS_ENDPOINT=${data.aws_iot_endpoint.endpointUrl.endpoint_address}"

  provisioner "local-exec" {
    command = "docker-compose up --build -d"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "docker-compose down"
  }
}

data "aws_iot_endpoint" "endpointUrl" {
  endpoint_type = "iot:Data"
}

variable "sensor_name" {
  type = string
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


provider "aws" {
  profile    = "default"
  region     = "us-east-1"
}

resource "aws_iot_thing" "thing" {
  name = var.sensor_name
}

resource "aws_iot_certificate" "thing_cert" {
  active = true
}

resource "aws_iot_policy" "thing_policy" {
  name = "${var.sensor_name}${var.policy}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["iot:*"],
      "Resource": ["*"]
    }
  ]
}
EOF
}

resource "aws_iot_thing_principal_attachment" "att" {
  principal = aws_iot_certificate.thing_cert.arn
  thing     = aws_iot_thing.thing.name
}

resource "aws_iot_policy_attachment" "att" {
  policy = aws_iot_policy.thing_policy.name
  target = aws_iot_certificate.thing_cert.arn
}

resource "local_file" "thing_cert_pem" {
  sensitive_content = aws_iot_certificate.thing_cert.certificate_pem
  file_permission = "0664"
  filename = "${var.sensor_name}${var.cert_file_ending}"
}

resource "local_file" "thing_key_pem" {
  sensitive_content = aws_iot_certificate.thing_cert.private_key
  file_permission = "0664"
  filename = "${var.sensor_name}${var.private_key_ending}"
}

resource "local_file" "aws_endpoint" {
  filename = "aws_endpoint_url"
  content = data.aws_iot_endpoint.endpointUrl.endpoint_address
}

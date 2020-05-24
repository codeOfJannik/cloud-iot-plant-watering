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
      "Action": [
        "iot:Publish",
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:us-east-1:511071744436:topic/sdk/test/java",
        "arn:aws:iot:us-east-1:511071744436:topic/sdk/test/Python",
        "arn:aws:iot:us-east-1:511071744436:topic/topic_1",
        "arn:aws:iot:us-east-1:511071744436:topic/topic_2"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:us-east-1:511071744436:topicfilter/sdk/test/java",
        "arn:aws:iot:us-east-1:511071744436:topicfilter/sdk/test/Python",
        "arn:aws:iot:us-east-1:511071744436:topicfilter/topic_1",
        "arn:aws:iot:us-east-1:511071744436:topicfilter/topic_2"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect"
      ],
      "Resource": [
        "arn:aws:iot:us-east-1:511071744436:client/sdk-java",
        "arn:aws:iot:us-east-1:511071744436:client/basicPubSub",
        "arn:aws:iot:us-east-1:511071744436:client/sdk-nodejs-*"
      ]
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

provider "aws" {
  profile    = "default"
  region     = "us-east-1"
}

resource "aws_iot_thing" "soil_moisture_2" {
  name = "soil_moisture_2"
}

resource "aws_iot_certificate" "soil_moisture_2_cert" {
  active = true
}

resource "aws_iot_policy" "soil_moisture_2_policy" {
  name = "soil_moisture_2_policy"

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
  principal = aws_iot_certificate.soil_moisture_2_cert.arn
  thing     = aws_iot_thing.soil_moisture_2.name
}

resource "aws_iot_policy_attachment" "att" {
  policy = aws_iot_policy.soil_moisture_2_policy.name
  target = aws_iot_certificate.soil_moisture_2_cert.arn
}

resource "local_file" "soil_moisture_2_cert_pem" {
  sensitive_content = aws_iot_certificate.soil_moisture_2_cert.certificate_pem
  file_permission = "0664"
  filename = "soil_moisture_2.cert.pem"
}

resource "local_file" "soil_moisture_2_key_pem" {
  sensitive_content = aws_iot_certificate.soil_moisture_2_cert.private_key
  file_permission = "0664"
  filename = "soil_moisture_2.private.key"
}

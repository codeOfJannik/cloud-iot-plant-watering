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
}


resource "aws_iot_topic_rule" "control_panel_rule" {
  depends_on = [var.dependencies]

  name        = "sendControlPanel"
  description = "send control panel data"
  enabled     = true
  sql         = "SELECT state.reported.data FROM '$aws/things/control_panel/shadow/update/accepted'"
  sql_version = "2016-03-23"

  iot_events {
    input_name = "ControlPanelInput"
    role_arn   = aws_iam_role.core_rule_role.arn
  }
}

resource "aws_iot_topic_rule" "soil_moisture_rule" {
  depends_on = [var.dependencies]

  name        = "sendSoilMoisture"
  description = "send soil moisture"
  enabled     = true
  sql         = "SELECT get((SELECT VALUE data FROM state.reported), 0) as data FROM '$aws/things/+/shadow/update/accepted' WHERE regexp_matches(topic(3), 'soilMoisture[0-9]{1,2}_sensor')"
  sql_version = "2016-03-23"

  iot_events {
    input_name = "SoilMoistureInput"
    role_arn   = aws_iam_role.core_rule_role.arn
  }
}

resource "aws_iot_topic_rule" "rain_barrel_rule" {
  depends_on = [var.dependencies]

  name        = "sendRainBarrelReadings"
  description = "send rain barrel data"
  enabled     = true
  sql         = "SELECT get((SELECT VALUE data FROM state.reported), 0) as data FROM '$aws/things/+/shadow/update/accepted' WHERE regexp_matches(topic(3), 'rain_barrel_sensor')"
  sql_version = "2016-03-23"

  iot_events {
    input_name = "RainBarrelSensorInput"
    role_arn   = aws_iam_role.core_rule_role.arn
  }
}

resource "aws_iam_policy" "core_rule_policy" {
  depends_on = [var.dependencies]

  name = "core_rule_policy"

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "iotevents:BatchPutMessage",
        "Resource": [
            "arn:aws:iotevents:us-east-1:002917872344:input/SoilMoistureInput",
            "arn:aws:iotevents:us-east-1:002917872344:input/ControlPanelInput",
            "arn:aws:iotevents:us-east-1:002917872344:input/RainBarrelSensorInput"
        ]
      },
      {
        "Effect": "Allow",
        "Action": "iot:Publish",
        "Resource": "arn:aws:iot:us-east-1:002917872344:topic/events/rules/test"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy_attachment" "attach_role_policy" {
  policy_arn = aws_iam_policy.core_rule_policy.arn
  role = aws_iam_role.core_rule_role.name
}

resource "aws_iam_role" "core_rule_role" {
  name = "core_rule_role"
  path = "/service-role/"
  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "iot.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }
  EOF
}

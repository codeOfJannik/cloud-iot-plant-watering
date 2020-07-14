data "aws_iot_endpoint" "endpointUrl" {
  endpoint_type = "iot:Data-ATS"
}

// used to get current account ID
data "aws_caller_identity" "current" {}

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

// attache each certificate and policy to the corresponding thing (for each device)
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

// create certificate and private key files for each device
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

// write endpoint to .env file, to have access in software class (for sdk connection)
resource "local_file" "aws_endpoint" {
  filename = ".env"
  content = "AWS_ENDPOINT=${data.aws_iot_endpoint.endpointUrl.endpoint_address}"
}

// create rules to pass information to AWS IoT Events (next three resources)
resource "aws_iot_topic_rule" "control_panel_rule" {
  depends_on = [var.dependencies]

  name        = "sendControlPanel"
  description = "send control panel data"
  enabled     = true
  sql         = "SELECT state.reported FROM '$aws/things/control_panel/shadow/update/accepted'"
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
  sql         = "SELECT topic(3) as sensorId, state.reported.value FROM '$aws/things/+/shadow/update/accepted' WHERE regexp_matches(topic(3), 'soilMoisture[0-9]{1,2}_sensor')"
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
  sql         = "SELECT topic(3) as sensorId, state.reported.value FROM '$aws/things/+/shadow/update/accepted' WHERE regexp_matches(topic(3), 'rain_barrel_sensor')"
  sql_version = "2016-03-23"

  iot_events {
    input_name = "RainBarrelSensorInput"
    role_arn   = aws_iam_role.core_rule_role.arn
  }
}

// set permissions in policy, allow rules sending data to IoT Events Inputs
// in addition for development: allow sending data to a "test" mqtt topic
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
            "arn:aws:iotevents:*:${data.aws_caller_identity.current.account_id}:input/SoilMoistureInput",
            "arn:aws:iotevents:*:${data.aws_caller_identity.current.account_id}:input/ControlPanelInput",
            "arn:aws:iotevents:*:${data.aws_caller_identity.current.account_id}:input/RainBarrelSensorInput"
        ]
      },
      {
        "Effect": "Allow",
        "Action": "iot:Publish",
        "Resource": "arn:aws:iot:*:${data.aws_caller_identity.current.account_id}:topic/events/rules/test"
      }
    ]
  }
  EOF
}

// attache policy to role
resource "aws_iam_role_policy_attachment" "attach_role_policy" {
  policy_arn = aws_iam_policy.core_rule_policy.arn
  role = aws_iam_role.core_rule_role.name
}

// role, containing the permissions of the event rules
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

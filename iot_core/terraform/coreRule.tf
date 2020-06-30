resource "aws_iot_topic_rule" "control_panel_rule" {
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
  name = "test_policy"

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "ec2:Describe*"
        ],
        "Effect": "Allow",
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": "iotevents:BatchPutMessage",
        "Resource": [
            "arn:aws:iotevents:us-east-1:002917872344:input/SoilMoistureInput",
            "arn:aws:iotevents:us-east-1:002917872344:input/ControlPanelInput",
            arn:aws:iotevents:us-east-1:002917872344:input/RainBarrelSensorInpu
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
  policy_arn = aws_iam_role_policy.core_rule_policy.arn
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
          "AWS": "arn:aws:iam::002917872344:role/*"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }
  EOF
}
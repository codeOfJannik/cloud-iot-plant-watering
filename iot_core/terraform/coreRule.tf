resource "aws_iot_topic_rule" "control_panel_rule" {
  name        = "sendControlPanel"
  description = "send control panel data"
  enabled     = true
  sql         = "SELECT state.reported.data FROM '$aws/things/control_panel/shadow/update/accepted'"
  sql_version = "2016-03-23"

  iot_events {
    input_name = "ControlPanelInput"
    role_arn   = "arn:aws:iam::002917872344:role/service-role/soilMoisture_core_rule_role" //aws_iam_role.controlPanel_core_rule_role_copy.arn
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
    role_arn   = "arn:aws:iam::002917872344:role/service-role/soilMoisture_core_rule_role" //aws_iam_role.controlPanel_core_rule_role_copy.arn
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
    role_arn   = "arn:aws:iam::002917872344:role/service-role/rainBarrel_core_rule_role" //aws_iam_role.controlPanel_core_rule_role_copy.arn
  }
}

//data "aws_iam_policy_document" "core_rule_permissions" {
//  statement {
//    effect = "Allow"
//    actions = [
//      "iotevents:BatchPutMessage"
//      ]
//    resources = [
//      "arn:aws:iotevents:us-east-1:002917872344:input/SoilMoistureInput"
//    ]
//  }
//  statement {
//    effect = "Allow"
//    actions = [
//      "iotevents:BatchPutMessage"
//    ]
//    resources = [
//      "arn:aws:iotevents:us-east-1:002917872344:input/ControlPanelInput"
//    ]
//  }
//  statement {
//    effect = "Allow"
//    actions = [
//      "iot:Publish"
//    ]
//    resources = [
//      "arn:aws:iot:us-east-1:002917872344:topic/events/rules/test"
//    ]
//  }
//}
//
//resource "aws_iam_role" "controlPanel_core_rule_role_copy" {
//  name               = "controlPanel_core_rule_role_copy"
//  path               = "/service-role/"
//  assume_role_policy = data.aws_iam_policy_document.core_rule_permissions.json
//}
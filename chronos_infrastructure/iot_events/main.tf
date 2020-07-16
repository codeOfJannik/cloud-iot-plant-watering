// create event inputs
resource "null_resource" "create_event_inputs" {

  // rain barrel sensor
  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://iot_events/RainBarrelSensorInput.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // control panel soil moisture thresholds
  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://iot_events/ControlPanelInput.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // control panel rain barrel thresholds
  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://iot_events/RainBarrelThresholdInput.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // soil moisture sensor
  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://iot_events/SoilMoistureInput.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

}

// create detector models after creating inputs
resource "null_resource" "create_event_models" {

  depends_on = [
    null_resource.create_event_inputs
  ]

  // water source
  provisioner "local-exec" {
    command = " aws iotevents create-detector-model --cli-input-json file://iot_events/WaterSourceDetectorModel.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // soil moisture
  provisioner "local-exec" {
    command = " aws iotevents create-detector-model --cli-input-json file://iot_events/SoilMoistureLogic.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }


}

// when terraform destroy, delete detector models before inputs
resource "null_resource" "destroy_event_models_inputs" {

  // water source detector model
  provisioner "local-exec" {
    when = destroy
    command = "aws iotevents delete-detector-model --detector-model-name WaterSourceDetectorModel --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // soil moisture detector model
  provisioner "local-exec" {
    when = destroy
    command = "aws iotevents delete-detector-model --detector-model-name SoilMoistureLogic --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // rain barrel sensor input
  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name RainBarrelSensorInput --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // control panel soil moisture thresholds
  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name ControlPanelInput --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // control panel rain barrel thresholds
  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name RainBarrelThresholdInput --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  // soil moisture sensor input
  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name SoilMoistureInput --profile ${var.aws_profile} --region ${var.aws_region}"
  }

}

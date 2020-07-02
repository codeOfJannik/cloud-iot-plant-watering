// create inputs
resource "null_resource" "create_event_inputs" {

  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://iot_events/RainBarrelSensorInput.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://iot_events/ControlPanelInput.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://iot_events/SoilMoistureInput.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

}

// create detector models after creating inputs
resource "null_resource" "create_event_models" {

  depends_on = [
    null_resource.create_event_inputs
  ]

  provisioner "local-exec" {
    command = " aws iotevents create-detector-model --cli-input-json file://iot_events/WaterSourceDetectorModel.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  provisioner "local-exec" {
    command = " aws iotevents create-detector-model --cli-input-json file://iot_events/SoilMoistureLogic.json --profile ${var.aws_profile} --region ${var.aws_region}"
  }


}

// when terraform destroy, delete detector models before inputs
resource "null_resource" "destroy_event_models_inputs" {

  provisioner "local-exec" {
    when = destroy
    command = "aws iotevents delete-detector-model --detector-model-name WaterSourceDetectorModel --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  provisioner "local-exec" {
    when = destroy
    command = "aws iotevents delete-detector-model --detector-model-name SoilMoistureLogic --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name RainBarrelSensorInput --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name ControlPanelInput --profile ${var.aws_profile} --region ${var.aws_region}"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name SoilMoistureInput --profile ${var.aws_profile} --region ${var.aws_region}"
  }

}

//resource "null_resource" "destroy_event_inputs" {
//
//  depends_on = [
//    null_resource.destroy_event_models
//  ]
//
//  provisioner "local-exec" {
//    when    = destroy
//    command = "aws iotevents delete-input --input-name RainBarrelSensorInput --profile ${var.aws_profile} --region ${var.aws_region}"
//  }
//
//  provisioner "local-exec" {
//    when    = destroy
//    command = "aws iotevents delete-input --input-name ControlPanelInput --profile ${var.aws_profile} --region ${var.aws_region}"
//  }
//
//  provisioner "local-exec" {
//    when    = destroy
//    command = "aws iotevents delete-input --input-name SoilMoistureInput --profile ${var.aws_profile} --region ${var.aws_region}"
//  }
//
//}
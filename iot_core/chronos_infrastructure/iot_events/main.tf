resource "null_resource" "create_event_inputs" {

  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://../iot_events/RainBarrelSensorInput.json --profile chronos --region us-east-1"
  }

  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://../iot_events/ControlPanelInput.json --profile chronos --region us-east-1"
  }

  provisioner "local-exec" {
    command = "aws iotevents create-input --cli-input-json file://../iot_events/SoilMoistureInput.json --profile chronos --region us-east-1"
  }

}


resource "null_resource" "create_event_models" {

  depends_on = [
    null_resource.create_event_inputs
  ]

  provisioner "local-exec" {
    command = " aws iotevents create-detector-model --cli-input-json file://../iot_events/WaterSourceDetectorModel.json --profile chronos --region us-east-1"
  }

  provisioner "local-exec" {
    command = " aws iotevents create-detector-model --cli-input-json file://../iot_events/SoilMoistureLogic.json --profile chronos --region us-east-1"
  }


}

resource "null_resource" "destroy_event_models_inputs" {

  provisioner "local-exec" {
    when = destroy
    command = "aws iotevents delete-detector-model --detector-model-name WaterSourceDetectorModel --profile chronos --region us-east-1"
  }

  provisioner "local-exec" {
    when = destroy
    command = "aws iotevents delete-detector-model --detector-model-name SoilMoistureLogic --profile chronos --region us-east-1"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name RainBarrelSensorInput --profile chronos --region us-east-1"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name ControlPanelInput --profile chronos --region us-east-1"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "aws iotevents delete-input --input-name SoilMoistureInput --profile chronos --region us-east-1"
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
//    command = "aws iotevents delete-input --input-name RainBarrelSensorInput --profile chronos --region us-east-1"
//  }
//
//  provisioner "local-exec" {
//    when    = destroy
//    command = "aws iotevents delete-input --input-name ControlPanelInput --profile chronos --region us-east-1"
//  }
//
//  provisioner "local-exec" {
//    when    = destroy
//    command = "aws iotevents delete-input --input-name SoilMoistureInput --profile chronos --region us-east-1"
//  }
//
//}
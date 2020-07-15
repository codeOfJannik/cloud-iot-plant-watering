provider "aws" {
  profile    = "chronos"
  region     = "us-east-1"
}

module "iot_events" {
  source = "./iot_events"
  aws_profile = "chronos"
  aws_region = "us-east-1"
}

module "iot_core" {
  source = "./iot_core"
  // specified in iot_events:
  // IoT Core Event-Rules need to be wait for IoT Events inputs
  dependencies = [module.iot_events.iot_core_dependencies]
}

module "docker" {
  source = "./docker"
  // specified in iot_core:
  // Docker services will be started after all AWS resources are deployed
  dependencies = [module.iot_core.docker_dependencies]
  aws_endpoint = module.iot_core.aws_endpoint
}

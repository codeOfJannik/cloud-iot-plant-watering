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

  dependencies = [module.iot_events.iot_core_dependencies]
}

module "docker" {
  source = "./docker"

  dependencies = [module.iot_core.docker_dependencies]
}

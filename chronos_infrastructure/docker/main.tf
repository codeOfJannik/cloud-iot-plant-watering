provider "docker" {}

resource "docker_network" "chronos_network" {
  name = "chronos_network"
}

// emulator container for each device
resource "docker_container" "emulator_container" {
  depends_on = [var.dependencies]
  for_each = local.files
  image = "csiot/emulator:latest"
  name  = "emulator_${basename(dirname(each.value))}"
  hostname = basename(dirname(each.value))
  networks_advanced {
    name = "chronos_network"
  }
  restart = "always"
  volumes {
    container_path = "/emulator/config.yaml"
    host_path = abspath(each.value)
  }
  ports {
    internal = "9292"
    external = 5555 + index(tolist(local.files), each.value)
  }
}

// software container for each device
resource "docker_container" "software_container" {
  depends_on = [docker_container.emulator_container]
  for_each = docker_container.emulator_container
  image = "chronos/software:latest"
  name  = "software_${each.value.hostname}"
    networks_advanced {
    name = "chronos_network"
  }
  restart = "always"
  env = [
     "HARDWARE_URL=http://${each.value.name}:9292",
     "DEVICE_NAME=${each.value.hostname}",
     "INTERVAL_TIME=30",
     "AWS_IOT_ENDPOINT=${var.aws_endpoint}",
     "PYTHONUNBUFFERED=1"
  ]
  volumes {
    container_path = "/usr/src/app/"
    host_path = abspath("iot_core/devices/${each.value.hostname}/")
  }
  volumes {
    container_path = "/usr/src/app/software_class/"
    host_path = abspath("iot_core/software_class/")
  }
}
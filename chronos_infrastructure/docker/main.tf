resource "null_resource" "manage_docker_containers" {

  depends_on = [var.dependencies]

  provisioner "local-exec" {
    command = "docker-compose -f iot_core/docker-compose.yml up --build -d"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "docker-compose -f iot_core/docker-compose.yml down"
  }
}
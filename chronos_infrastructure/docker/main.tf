resource "null_resource" "manage_docker_containers" {

  depends_on = [var.dependencies]

  provisioner "local-exec" {
    command = "docker-compose up --build -d"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "docker-compose down"
  }
}
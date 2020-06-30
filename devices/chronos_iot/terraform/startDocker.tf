resource "null_resource" "start_docker_containers" {

  depends_on = [
    aws_iot_thing.thing,
    aws_iot_policy_attachment.att,
    aws_iot_thing_principal_attachment.att,
    aws_iot_certificate.thing_cert,
    local_file.aws_endpoint,
    local_file.thing_cert_pem,
    local_file.thing_key_pem
  ]

  provisioner "local-exec" {
    command = "docker-compose up --build -d"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "docker-compose down"
  }
}
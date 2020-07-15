// need in docker module:
// wait until the iot_core module is ready, used to minimize docker container restarts due to missing connection to AWS
// IoT Things.
output "docker_dependencies" {
  value = [
    aws_iot_thing.thing,
    aws_iot_policy_attachment.att,
    aws_iot_thing_principal_attachment.att,
    aws_iot_certificate.thing_cert,
    local_file.aws_endpoint,
    local_file.thing_cert_pem,
    local_file.thing_key_pem
  ]
}

output "aws_endpoint" {
  value = data.aws_iot_endpoint.endpointUrl.endpoint_address
}
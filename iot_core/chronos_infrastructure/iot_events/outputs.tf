output "iot_core_dependencies" {
  value = [
    null_resource.create_event_inputs
  ]
}

// need in iot_core module:
// wait until inputs are deployed, to set up the iot core rules.
output "iot_core_dependencies" {
  value = [
    null_resource.create_event_inputs
  ]
}

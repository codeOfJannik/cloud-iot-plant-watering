# Terraform - Docker Devices + Software
This terraform script is deploying and destroying the devices as docker container. See [iot_core 
readme](../../iot_core/README.md) for more details about this devices.
The used ports are beginning from _'5555'_ until the count of device folders under [devices](../../iot_core/devices).
Important: Check for free ports before setting up a new device. 

Variables:
* dependencies (list)

    template, to pass optional dependencies from root main.tf, actual used to wait for the iot_core thing depended 
    resources (see iot_core [outputs.tf](../iot_events/outputs.tf) and [readme](../iot_core/README.md) for more 
    information)

* local.files (fileset)

    path to every device config.yaml

* aws_endpoint (string)

    template to get the aws endpoint from root main.tf

Outputs:
- none
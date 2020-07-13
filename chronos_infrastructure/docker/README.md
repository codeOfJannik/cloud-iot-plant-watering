# Terraform - Docker Devices + Software
This terraform script is using the CLI docker-compose commmands _"up"_ and _"down"_, to perform the instructions, defined
in the [docker-compose.yml](../../iot_core/docker-compose.yml) file: 

1. terraform apply
    * start docker images with _'docker-compose up --build -d'_
    
2. terraform destroy
    * stop docker images with _'docker-compose down'_
    
Variables:
* dependencies (list)

    template, to pass optional dependencies from root main.tf, actual used to wait for the iot_core thing depended 
    resources (see iot_core [outputs.tf](../iot_events/outputs.tf) and [readme](../iot_core/README.md) for more 
    information)

Outputs:
- none
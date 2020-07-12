# Terraform - IoT Events
This terraform script is setting up and destroying the IoT Event models using the AWS CLI, because during the development 
of the project there were no terraform scripts for AWS IoT Events resource.

1. terraform apply
    * create event inputs
    * create detector models after creating inputs (to prevent a _'declared input in detector model dose not exists'_ error)

2. terraform destroy
    * delete detector models before inputs (to prevent a _'cannot delete, because detector model depends on input'_ error)
    * delete inputs
    
The different input and detector model json structures can be found in the [iot_events](../../iot_events) directory.
See the corresponding [README](../../iot_events/README.md) to get an overview about them.

Variables:
* dependencies (list)

    template, to pass optional dependencies from root main.tf, actual not used in the iot_events module
    
* aws_profile (string)

    used to set the _--profile_ option in the CLI commands
    
* aws_region (string)

    used to set the _--region_ option in the CLI commands

Outputs:
- iot_core_dependencies (list)
 
    needed in [iot_core](../iot_core) module, to wait until the _event inputs_ are deployed, to set up the iot core 
    rules (see [iot_core README](../iot_core/README.md)).
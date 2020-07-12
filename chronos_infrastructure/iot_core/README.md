# Terraform - IoT Core
This terraform script is setting up and destroying the IoT Core resources:
- Things
- Policies
- SSH Keys
- Shadows
- Event-Rules
- Corresponding IAM Roles & Permissions
    
For each device, specified under the [iot_core](../../iot_core) directory, a thing, policy, SSH key and shadow will be 
automatically deployed in the AWS IoT Core Service. 
See for more information the corresponding [README](../../iot_core/README.md).
The Event-Rules are provided in dependency to the [iot_events](../iot_events) inputs. The dependencies specified by the 
root _main.tf_ are  used to wait for them.

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
    

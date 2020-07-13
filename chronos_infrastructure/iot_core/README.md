# Terraform - IoT Core
This terraform script is setting up and destroying the IoT Core resources:
- Things
- Certificates
- Policies
- SSH Keys
- Shadows
- Event-Rules
- Corresponding IAM Roles & Permissions
    
For each device, specified under the [iot_core](../../iot_core) directory, a thing, certificate, policy, SSH key and 
shadow will be automatically deployed in the AWS IoT Core Service. 
See for more information about devices and directories in the corresponding [README](../../iot_core/README.md).
The Event-Rules are provided in dependency to the [iot_events](../iot_events) inputs. The dependencies specified by the 
root _main.tf_ are used to wait for them. The three Event Rule resources are created not in a loop, because the SELECT 
statements are to differently. 
More details about the _iot_core_ terraform can be found in the [_main.tf_](./main.tf) file.

Variables:
* local.files (fileset)

    path to every device policy
    
* policy (string)

    template variable for name ending in aws_iot_policy resource
    
* cert_file_ending (string)

    template variable for file ending *.cert.pem, used by creating pem files for each device

* private_key_ending (string)

    template variable for file ending *.private.key, used by creating private key files for each device

* dependencies (list)
    
    template, to pass optional dependencies from root main.tf, actual used to pass output from iot_events main.tf 
    "iot_core_dependencies": wait for create_event_inputs (see iot_events [outputs.tf](../iot_events/outputs.tf))

Outputs:
- docker_dependencies (list)
 
    needed in [docker](../docker) module, to wait until the [_iot_core_](../iot_core) module is ready, used to minimize 
    docker container restarts due to missing connection to AWS IoT Things.
    

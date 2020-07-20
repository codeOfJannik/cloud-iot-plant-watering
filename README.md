# chronos

This is the project repository for the course 113455a "Cloud Services and Internet of Things".
Target was to connect IoT devices using scalable cloud services in a project setup.

## Features/functions of this project
This project implements automated plant watering for any number of beds. For each bed any number of
soil mositure sensors can be assigned. Based on the readings of the soil mositure sensors for a bed and the
threshold for the bed, set optionally on a control panel device, the related watering valve will be opend or closed.
Additional another valve is implemented which controls the water source based on the fill level of a rain barrel.
The minimum fill level of the rain barrel before it is used as the water source can also be set via the control panel device.

As cloud provider AWS was chosen and that's why most of the files are in JSON. All infrastructure setup,
both on the AWS site and on local site, is done via [Terrafrom](https://www.terraform.io/).
[AWS IoT Core](https://aws.amazon.com/iot-core/) and [AWS IoT Events](https://aws.amazon.com/iot-events/) are the services
used on server side. For more information see [IoT Core](iot_core/README.md) and [IoT Events](iot_events/README.md).
Programming of the software code for the devices was done in Python.
Due to COVID-19 there were no real devices and sensors, so emulator devices were used instead.
The emulators are based on the following project:
https://gitlab.mi.hdm-stuttgart.de/csiot-tools/emulator

## Further readme files for other important project aspects
- [Infrastructure as Code (Terraform)](chronos_infrastructure/README.md)
- [IoT Core](iot_core/README.md)
- [IoT Events](iot_events/README.md)
- [Software Class](iot_core/software_class/README.md)
- [Tests](tests/README.md)
- [CI-Runner (Info)](CI-Runner.md)

## Setup instructions

### Requirements
- AWS Account (NO AWS Educate account - does not include AWS IoT Events!)
- [AWS CLI Version > 2.0.27](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed
- [Terrafrom](https://www.terraform.io/) installed
- [Docker](https://www.docker.com/) and installed
- `git clone git@gitlab.mi.hdm-stuttgart.de:csiot/ss20/chronos.git`

### Setup steps

#### 1. Update your AWS Credentials
Put your valid AWS credentials to `$HOME/.aws/credentials` on Linux and OS X
or `%USERPROFILE%\.aws\credentials` on Windows and update the profile in chronos_infrastructure/main.tf

#### 2. Build emulator and software image
The csiot/emulator and chronos/software docker images need to be build once. Run the build script
located at the root directory with `. build`

#### 3. Initialize Terraform
`terraform init chronos_infrastructure/`

#### 4. Optional: Check terraform script
`terraform plan chronos_infrastructure/`

There should not be any errors.

#### 5. Execute terraform script (see [README](chronos_infrastructure/README.md))
`terraform apply chronos_infrastructure/`

Terraform creates the AWS IoT Events Inputs and Detector Models (see 
[iot_events module](chronos_infrastructure/iot_events/README.md)).
After that, Terraform creates an AWS IoT Thing, certificate and policy for each device declared by a
directory in devices/chronos_iot/devices, as well as rules to send data to iot events (see 
[iot_core module](chronos_infrastructure/iot_core/README.md)). 
After creating the AWS resources, Terraform deploys two docker containers (emulator & software) for 
each device (see [docker module](chronos_infrastructure/docker/README.md)). 
After building the Docker containers, the **run.py** script is started in the software container of each device (see
[Dockerfile](iot_core/Dockerfile) and [README](iot_core/README.md)).

__If changes to software or config files occured and the docker containers should be restarted, it's necessary to call__
__`terraform destroy chronots_infrastructure/`. Otherwise the AWS IoT MQTT client won't work as desired.__

#### Information terraform destroy
When `terraform destroy chronos_infrastructure/` is executed, the Docker containers are stopped and all AWS
resources are deleted in reversed order.

## New Devices
New devices can be added by creating a new folder for the device at [iot_core/devices](iot_core/devices).
More information about can be found [here](iot_core/README.md).

## Contributors
Jannik Schlemmer (js329@hdm-stuttgart.de)  
Patrick Eichhorn (pe019@hdm-stuttgart.de)  
Jan Ziemann (jz043@hdm-stuttgart.de)  

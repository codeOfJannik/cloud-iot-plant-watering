# chronos

## Function
This is the repository based on the project for the course 113455a "Cloud Services and Internet of Things".
Target was to connect IoT devices using scalable cloud services in a project setup.

## Features/functions of this project
This is an automatic watering model based on the decision of soil moisture sensors.
Therefore there are actually 2 soil moisture sensors sending data and 2 valves.
One valve is for watering itself and the other one is for the watering source.
Based on the fuel level of a rain barrel it decides to take water either of the barrel or a 
normal water pipe.
As cloud provider AWS was chosen and that's why most of the files are in JSON, programming
was mainly in Python. Due to COVID-19 there were no real sensors, so there is an emulator 
in background sending emulated data to AWS based on following project: 
https://gitlab.mi.hdm-stuttgart.de/csiot-tools/emulator

## Further readme files for other important project aspects
- [Infrastructure as Code (Terraform)](chronos_infrastructure/README.md)
- [IoT Core](iot_core/README.md)
- [IoT Events](iot_events/README.md)
- [Software Class](chronos_infrastructure/README.md)
- [Tests](tests/README.md)

## Setup instructions

### Requirements
- AWS Account
- [AWS CLI Version > 2.0.27](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed
- [Terrafrom](https://www.terraform.io/) installed
- [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/install/) installed
- `git clone git@gitlab.mi.hdm-stuttgart.de:csiot/ss20/chronos.git`

### Setup steps

#### 1. Update your AWS Credentials
Put your valid AWS credentials to `~/.aws/credentials` and update the profile in chronos_infrastructure/main.tf

#### 2. Build emulator and software image
The csiot/emulator and chronos/software docker images need to be build once. Run the build script
located at the root directory with `. build`

#### 3. Initialize Terraform
`terraform init chronos_infrastructure/`

#### 4. Optional: Check terraform script
`terraform plan chronos_infrastructure/`

There should not be any errors or warnings

#### 5. Execute terraform script (see [README](chronos_infrastructure/README.md))
`terraform apply chronos_infrastructure/`

Terraform creates the AWS IoT Events Inputs and Detector Models (see 
[iot_events module](chronos_infrastructure/iot_events/README.md)).
After that, Terraform creates an AWS IoT Thing, certificate and policy for each device declared by a
directory in devices/chronos_iot/devices, as well as rules to send data to iot events (see 
[iot_core module](chronos_infrastructure/iot_core/README.md)). 
After creating the AWS resources, Terraform deploys the docker container for 
each device to emulate them (see [docker module](chronos_infrastructure/docker/README.md)). 
After building the Docker containers, the **run.py** script is started in the container of each emulated device (see
[Dockerfile](iot_core/Dockerfile) and [README](iot_core/README.md)).

#### Information terraform destroy
When `terraform destroy chronos_infrastructure/` is executed, the Docker containers are stopped and the AWS IoT
resources are deleted in reversed order.

##Contributors
Jannik Schlemmer (js329@hdm-stuttgart.de)
Patrick Eichhorn (pe019@hdm-stuttgart.de)
Jan Ziemann (jz043@hdm-stuttgart.de)

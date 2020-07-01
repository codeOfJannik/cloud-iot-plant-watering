# chronos

## Setup instructions

### Requirements
- AWS Account
- [Terrafrom](https://www.terraform.io/) installed
- [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/install/) installed
- `git clone git@gitlab.mi.hdm-stuttgart.de:csiot/ss20/chronos.git`

### Setup steps

#### 1. Update your AWS Credentials
Put your valid AWS credentials to `~/.aws/credentials`

#### 2. Build emulator image
The csiot/emulator docker image needs to be build once. Run the build script
located at `/devices/emulator-chronos/build`

#### 3. cd into Chronos IoT folder
`cd devices/chronos_iot`

#### 4. Initialize Terraform
`terraform init chronos_infrastructure/`

#### 5. Optional: Check terraform script
`terraform plan chronos_infrastructure/`

There should not be any errors or warnings

#### 6. Execute terraform script
`terraform apply chronos_infrastructure/`

Terraform creates an AWS IoT Thing, certificate and policy for each device declared by a
directory in devices/chronos_iot/devices. After creating the AWS resources,
Terraform executes the docker-compose up command that sets up Docker container for each device
to emulate it. After building the Docker containers, the **run.py** script is started
in the container of each emulated device.

#### Information terraform destroy
When `terraform destroy chronos_infrastructure/` is executed, the Docker containers are stopped and the AWS IoT
resources are deleted.

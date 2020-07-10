# IoT Core
The _iot_core_ directory contains all devices, the according software classes, the docker file
and the docker-compose.yml.

## Devices
Contains all current devices. To setup a new device check:
https://gitlab.mi.hdm-stuttgart.de/csiot-tools/emulator/-/blob/master/README.md

## Software Class 
Check https://gitlab.mi.hdm-stuttgart.de/csiot/ss20/chronos/-/blob/master/iot_core/software_class/README.md

## docker-compose.yml
Contains emulator and software volumes for all devices. For performance reasons the option 
"restart : always" was introduced. 
Important: Check for free ports before setting up a new device. 
Following scheme was used for all devices:
https://gitlab.mi.hdm-stuttgart.de/csiot-tools/emulator/-/blob/master/example/docker-compose.yml


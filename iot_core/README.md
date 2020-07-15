# IoT Core
The _iot_core_ directory contains all devices, the according software classes and the docker file for the software docker
image.

## Devices
Contains all current devices. To setup a new device, append a new device directory to the devices folder.
In such a device directory a config.yaml (see [emulator 
setup](https://gitlab.mi.hdm-stuttgart.de/csiot-tools/emulator/-/blob/master/README.md) for more details), a policy.json 
and a run.py file need to be declared. The config.yaml describe the emulator device and the following types are possible:
- control panel (only one for all beds is necessary)
- soil moisture sensor (new once can added with a new number in directory name and config file)
- watering source valve (only one for all beds is necessary in case of only one rain barrel)
- watering valve (only one per bed)


## Software Class
Check [software readme](software_class/README.md) for details

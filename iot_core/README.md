# AWS IoT Core
Things for all devices are created in the AWS IoT Core service. The MQTT communication with the AWS IoT Core service and the device is handled from the
[Software Class](#software-class). The devices update the shadows at AWS IoT Core. In AWS IoT Core are rules defined that wait for shadow update acceptance
messages and send the values to corresponding [AWS IoT Events](../iot_events/README.md) inputs. A huge advantage of using AWS IoT Core shadows is, that
if the state of e.g. a watering valve needs to be changed, just a message with the desired state must be send to the shadow and the device which subscribed
on the shadow delta topic is informed when the states don't match.

# IoT Core
The _iot_core_ directory contains the configuration files for all devices, the according software code and the docker file for the software docker
image.

## Devices
The _devices_ directory contains a folder for each device. Based on the folders Terraform sets up the thing instances
in AWS IoT Core and starts the docker containers for emulator and software of each device.

__control_panel__, __rain_barrel_sensor__ and __watering_source_valve__ are devices that are required only once and 
no more folder of these device types should be added.

### New Device
To setup a new device (soil moisture sensor or watering valve), add a new device folder to the `./devices` directory.
The folder name must match the pattern of the existing devices (_soilMoisture\<nr\>\_sensor_ or _watering_valve\_\<bed_id\>_).
The number in the name of the watering valve must match the number of the bed to which the valve belongs.
The device folder needs two files:

#### emulator_config.yaml
The _emulator_config.yaml_ is used for the [emulator](https://gitlab.mi.hdm-stuttgart.de/csiot-tools/emulator).
Each file needs two keys _name_ and _gpios_ on root level. The name does not necessarily have to match the name
of the device folder. The key _gpios_ defines the components of the device (LED, switch, sensor). Each
component needs further configuration. If a new soil mositure sensor should be added, a emulator_config.yaml
of an existing soil moisture sensor can be copied and modified as follows:

```yaml
name: <any-sensor-name>  # UI only, duplicate names cause no problems
gpios:

  soilMoistureSensor:  # DO NOT modify, gpio name used in software class
    type: sensor  # DO NOT modify
    state:
      # the initial value can be modified
      value: 50 
      
      # the minimal value
      min: 0
      
      # the maximum value
      max: 300
      
      # the step-size if the value goes up or down
      increment: 1
      
      # the unit (UI only, empty string for unitless)
      unit: "nFk (%)"
```

For a new watering valve the emulator_config.yaml can be copied as well:
```yaml
name: <any-valve-name>  # UI only, duplicate names cause no problems
gpios:

  valve:  # DO NOT modify, gpio name used in software class
    type: switch  # DO NOT modify
    state:
      open: true  # initial state can be modified

```

#### settings.yaml
The values of the _settings.yaml_ is
1. used during the Terraform setup to attach the correct policy to the created AWS IoT Core thing.
2. read during init of the DeviceSoftware class to set some constant values.

As with _emulator_config.yaml_, _settings.yaml_ can be copied from existing devices:
```yaml
# time interval in which the sensor value is send to AWS IoT Core
#  optional value, default is set to 30 if not defined
time_interval: 30  
# device_type defines which policy is required. Possible values are: sensor, valve.
# devices of type sensor just need permission to send data to AWS
# devices of type valve need permissions for sending data and receiving shadow updates
device_type: sensor
# iot_type defines which method of the DeviceSoftware class must be executed
# possible values: soil_moisture, water_valve, control_panel, rain_barrel
iot_type: soil_moisture
# just required for devices that belong to a specific bed
# defines the bed number the device belongs to
bed: 1
```

### New bed
If devices for a new bed should be created the following steps need to be done. Make sure you dont skip a bed number when creating a new one:
1. Create any number of soil mositure sensors as [described above](#new-device). Set the bed number of the new bed in [settings.yaml](#settings.yaml) for each new soil mositure sensor.
2. Create a new watering valve as [described above](#new-device). Make sure to use the number of the new bed in the name of the watering valve (e.g. for bed 3: watering_valve_3).
3. Add a new gpio component to the control panel's [emulator_config.yaml](devices/control_panel/emulator_config.yaml). Copy and paste an existing ___bed\_#\_soilMoisture_threshold___ to the end of the file. 
    * __Change the number in the component name!__
    * __Double check for correct indentation of the pasted block!__

## Software Class
Check [software readme](software_class/README.md) for details.

## Dockerfile
The Dockerfile that is used to build the software docker image.
- the AWS root certificate is downloaded
- the AWSIoTDeviceSDK is installed via `pip install AWSIoTPythonSDK`
- the pyyaml package is installed via `pip install pyyaml`
- [run.py](./run.py) should be executed when docker container is started

## Policies
The [sensor_policy.json](./sensor_policy.json) and [valve_poilcy.json](./valve_policy.json) are template files that are used by Terraform to generate the
required AWS IoT thing policies. The template files contain variables (`${arn}` & `${clientId}`) that are filled
correctly for each device during Terraform setup.

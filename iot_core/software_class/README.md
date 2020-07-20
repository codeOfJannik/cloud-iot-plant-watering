# Software Class
The _software_class_ directory contains the software code of all Chronos-IoT devices. A main method is called in the
[___run.py___ file](../run.py), mounted by the [docker containers](../../chronos_infrastructure/docker/README.md) in 
each device folder. This method decides by a passed environment variable, which device specific method needs to be 
called. 
For every device a connection to the AWS MQTT endpoint is setup using the
AWSIoTClient class in [_aws_iot_client.py_](aws_iot_client.py). The _DeviceSoftware_ class in 
[_device_software.py_](device_software.py) contains the logic to update sensor values and perform actions of incoming 
messages.

## aws_iot_client.py
The ___AWSIotClient___ class uses the [AWS IoT Device SDK for Python](https://github.com/aws/aws-iot-device-sdk-python) to 
connect to AWS IoT through MQTT. Every device with a connection over AWSIoTClient can publish messages in MQTT topics or
subscribe to MQTT topics to receive messages, assuming they are allowed to in the device policy.

The ***\_\_init__*** method sets up the connection to the AWS ioT platform.

```python
def __init__(self, root_ca_path, certificate_path, private_key_path, device_name):
    self.mqttClient = AWSIoTMQTTClient(device_name)
    self.mqttClient.configureEndpoint(os.getenv("AWS_IOT_ENDPOINT"), 8883)
    self.mqttClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

    self.mqttClient.connect()
```

Every instance of [___AWSIoTMQTTClient___](https://github.com/aws/aws-iot-device-sdk-python/blob/master/AWSIoTPythonSDK/MQTTLib.py#L35)
requires a client ID. We use the names of our IoT device as client ID for the connection. To define to which AWS IoT
endpoint the IoT device should connect to, we pass the endpoint address to the _configureEndpoint()_ method. The 
endpoint address was stored during terraform setup in a _.env_ file, so it is assigned as environment variable when
the terraform [docker module](../../chronos_infrastructure/docker) is executed. By passing the port number 8883 the 
client uses TLS mutual authentication. With port number 443 it would use authentication via websocket.

The `subscribe_to_topic()` and `publish_message_to_topic()` methods map the equivalent methods of the AWS IoT SDK to
our class.

## device_software.py
The ___DeviceSoftware___ class is a subclass of the ___AWSIoTClient___ and is instanced for each device in the _run.py_
file. The corresponding run method is called in the _run.py_ through a method which decides which device specific function
needs to be called. This has the advantage to use the __same__ _run.py_ file for each device.  

### init
At initialization environment variables that have been set during the terraform docker module execution are assigned to 
class variables, specific device information stored in a ___settings.yaml___ file in each device folder are set (see 
[iot_core readme](../README.md) for more information), the existence of the required certificates and private key files 
is checked and if they are present,  the `super().__init__` method is called to get a MQTT connection to the AWS IoT 
platform with the the aws_iot_client  class. If a certificate or the private key is missing the code exits with a 
failure message.

### run methods
#### Update control panel
The control panel is a device that can be used to set different threshold values, e.g. soil moisture thresholds for
different beds or the minimum water level in the rain barrel.
So the ___run_update_control_panel___  method updates the AWS IoT shadow with its 'sensor' values and 'bed_id' (if it 
is a bed specific value) in an interval that was defined in the related part of the device specific _settings.yaml_ file.

A. Full GPIO output is read:
```python
url = '{url}/gpios'.format(url=self.HARDWARE_URL)
# get current state from gpio
data = get_gpio(url=url)
```

B. Iteration over keys of GPIO output and index (to get the bed_id) which correspond to the sensor names and writing 
sensor values in new JSON which is used to update the AWS IoT shadow with:
```python
for index, key in enumerate(data):
    shadow_data = {"value": data[key]["state"]["value"]}
    if index != 0:
        shadow_data["bed_id"] = index
    self.update_device_shadow(shadow_data, shadow_name=key)
```

#### Update rain barrel sensor
The ___run_update_rain_barrel_sensor___ method updates the AWS IoT shadow with the current fill level of the rain barrel
in an interval that was defined in the related part of the _docker_compose.yml_. In this project only one rain barrel for
all beds exists, therefore no bed_id value is needed.

A. The rain barrel sensor device has just 1 sensor (rain_barrel_sensor). So the GPIO value of the sensor can be read
directly:
```python
url = '{url}/gpios/rain_barrel_sensor'.format(url=self.HARDWARE_URL)
# get current state from gpio
sensor_value = get_gpio(url=url)["state"]["value"]
``` 

B. The sensor value is written to a new JSON which is used to update the device shadow:
```python
data = {"value": sensor_value}
self.update_device_shadow(data)
```

#### Update soil mositure
The ___run_update_soil_moisture___ method updates the AWS IoT shadow with the current soil moisture reading of the device
and the bed_id (got from the settings.yaml) in an interval that was defined in the related part of the 
_docker_compose.yml_.

A. The soil moisture sensor GPIO value of each soil moisture sensor device can be read directly:
```python
url = '{url}/gpios/soilMoistureSensor'.format(url=self.HARDWARE_URL)
# get current state from gpio
sensor_value = get_gpio(url=url)["state"]["value"]
```

B. The sensor value is written to a new JSON which is used to update the device shadow:
```python
data = {"value": sensor_value,
        "bed_id": self.BED_ID}
self.update_device_shadow(data)
```

#### Run water valves
The ___run_water_valve___ method handles all logic of valve devices.

A. When the software is started, the current state of the valve is read from GPIOs and reported to the shadow. In 
addition, the bed_id will be append to the Payload, if one set in the device specific settings.yaml. This is used to 
set a bed_id for devices of the type _watering_valve_. The type _watering_source_valve_ has no bed id because there is 
only one rain barrel.  
```python
print(f'Starting software')
url = f'{self.HARDWARE_URL}/gpios/valve'
# ...
sensor_value = not get_gpio(url=url)["state"]["open"]
data = {"valve_open": sensor_value}
# add bed_id if one set in the device specific settings.yaml file
if self.BED_ID is not None:
    data['bed_id'] = self.BED_ID
# update device shadow with current state
print(f'update shadow value with data: {data}')
self.update_device_shadow(data)
```
B. Afterwards the device subscribes to the delta topic of the device shadow to be informed, when the desired state is
different from the current device state.
```python
delta_topic = "$aws/things/{device}/shadow/update/delta".format(device=self.DEVICE_NAME)
print('subscribe...')

if self.subscribe_to_topic(delta_topic, custom_callback, 0):
    pass
else:
    return False
```
C. A custom callback is defined for incoming messages in the delta topic. The callback reads the desired valve state
of the shadow delta message, sets the valve of the device via GPIOs to the desired state and reports the changed valve
state back to the device shadow to match the desired state.
```python
# received message:
print('custom callback')
received_data = json.loads(message.payload)
print(f'received shadow delta: {received_data}')
desired_valve_state = received_data['state']['valve_open']
data_message = json.dumps({"open": not desired_valve_state})
set_gpio(url=url, data=data_message)

# update shadow after changed to new switch state
sensor_value = not get_gpio(url=url)["state"]["open"]
data = {"valve_open": sensor_value}
# update device shadow with current state
self.update_device_shadow(data)
print('set gpio success')
```

#### Update device shadow
The ___update_device_shadow___ method is used by all run methods. It receives the data that should be written to the
shadow as input parameter. The data is put in the correct JSON format to report a state to the device shadow and the 
JSON message is published to the related shadow update topic. If a shadow_name is passed, a sub-shadow of the device type
will be created. This is needed for the control panel device, which set thresholds of different devices.
```python
def update_device_shadow(self, data, shadow_name=None):
    message = {
        "state": {
            "reported": data
        }
    }
    json_message = json.dumps(message)
    # publish message to update device shadow with current value
    if shadow_name:
        topic = f"$aws/things/{self.DEVICE_NAME}/shadow/name/{shadow_name}/update"
    else:
        topic = f"$aws/things/{self.DEVICE_NAME}/shadow/update"
    print(self.publish_message_to_topic(json_message, topic, 0))
```

### GPIO functions
The functions ___get_gpio___ and ___set_gpio___ are helper functions to access the switches and sensors of the emulator
devices. The emulator devices use HTTP requests to set/read the switch state/sensor values. If real hardware devices would
be used e.g. the switch state could be changed by sending high/low voltage to related GPIO pins.
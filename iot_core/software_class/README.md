# Software Class
The _software_class_ directory contains the software code of all IoT devices. The specific method is called in the
___run.py___ in each device folder. For every device a connection to the AWS MQTT endpoint is setup using the
AWSIoTClient class in _aws_iot_client.py_. The _DeviceSoftware_ class in _device_software.py_ contains the logic to
update sensor values and perform actions of incoming messages.

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
requires a client Id. We use the names of our IoT device as client Id for the connection. To define to which AWS IoT
endpoint the IoT device should connect to, we pass the endpoint address to the _configureEndpoint()_ method. The 
endpoint address was stored during terraform setup in a _.env_ file, so it is assigned as environment variable when
`docker-compose up` is called. By passing the port number 8883 the client uses TLS mutual authentication. With port number
443 it would use authentication via websocket.

The `subscribe_to_topic()` and `publish_message_to_topic()` methods map the equivalent methods of the AWS IoT SDK to
our class.

## device_software.py
The ___DeviceSoftware___ class is subclass of the ___AWSIoTClient___ and is instanced for each device in it's _run.py_
file. The corresponding run method is also called in the _run.py_

### init
At initialization environment variables that have been set in the docker-compose.yml are assigned to class variables,
the existence of the required certificates and private key files is checked and if they are present, the `super().__init__`
method is called to get a MQTT connection to the AWS IoT platform. If a certificate or the private key is missing the
code exits with a failure message.

### run methods
#### Update control panel
The control panel is a device that can be used to set different threshold values, e.g. soil moisture thresholds for
different beds or the minimum water level in the rain barrel.
So the ___run_update_control_panel___  method updates the AWS IoT shadow with its 'sensor' values in an interval that was 
defined in the related part of the _docker-compose.yml_.

A. Full GPIO output is read:
```python
url = '{url}/gpios'.format(url=self.HARDWARE_URL)
# get current state from gpio
data = get_gpio(url=url)
```

B. Iteration over keys of GPIO output which correspond to the sensor names and writing sensor values in new JSON which
is used to update the AWS IoT shadow
```python
keys = list(data)
shadow_data = {}
for key in keys:
    shadow_data[key] = data[key]["state"]["value"]

self.update_device_shadow(shadow_data)
```

#### Update rain barrel sensor
The ___run_update_rain_barrel_sensor___ method updates the AWS IoT shadow with the current fill level of the rain barrel
in an interval that was defined in the related part of the _docker_compose.yml_.

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
in an interval that was defined in the related part of the _docker_compose.yml_.

A. The soil moisture sensor GPIO value of each soil moisture sensor device can be read directly:
```python
url = '{url}/gpios/soilMoistureSensor'.format(url=self.HARDWARE_URL)
# get current state from gpio
sensor_value = get_gpio(url=url)["state"]["value"]
```

B. The sensor value is written to a new JSON which is used to update the device shadow:
```python
data = {"value": sensor_value}
self.update_device_shadow(data)
```

#### Run water valves
The ___run_water_valve___ method handles all logic of valve devices.

A. When the software is started, the current state of the valve is read from GPIOs and reported to the shadow.
```python
print(f'Starting software')
url = '{url}/gpios/{sensor}'.format(url=self.HARDWARE_URL, sensor=self.DEVICE_NAME)
# ...
sensor_value = not get_gpio(url=url)["state"]["open"]
data = {"valve_open": sensor_value}
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
JSON message is published to the related shadow update topic.
```python
def update_device_shadow(self, data):
    message = {
        "state": {
            "reported": data
        }
    }
    json_message = json.dumps(message)

    # publish message to update device shadow with current value
    self.publish_message_to_topic(json_message, "$aws/things/{device}/shadow/update".format(device=self.DEVICE_NAME), 0)
```

### GPIO functions
The functions ___get_gpio___ and ___set_gpio___ are helper functions to access the switches and sensors of the emulator
devices. The emulator devices use HTTP requests to set/read the switch state/sensor values. If real hardware devices would
be used e.g. the switch state could be changed by sending high/low voltage to related GPIO pins.
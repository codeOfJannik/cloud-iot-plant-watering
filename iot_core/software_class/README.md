# Software Class
The _software_class_ directory contains the software code of all IoT devices. The specific method is called in the
___run.py___ in each device folder. For every device a connection to the AWS MQTT endpoint is setup using the
AWSIoTClient class in _aws_iot_client.py_. The _DeviceSoftware_ class in _device_software.py_ contains the logic to
update sensor values and perform actions of incoming messages.

## aws_iot_client.py
The ___AWSIotClient___ class uses the [AWS IoT Device SDK for Python](https://github.com/aws/aws-iot-device-sdk-python) to 
connect to AWS IoT through MQTT. Every device with a connection over AWSIoTClient can publish messages in MQTT topics or
subscribe to MQTT topics to receive messages, assuming they are allowed to in the device policy.

The ***\_\_init__*** function sets up the connection to the AWS ioT platform.

```python
    def __init__(self, root_ca_path, certificate_path, private_key_path, device_name):
        self.mqttClient = AWSIoTMQTTClient(device_name)
        self.mqttClient.configureEndpoint(os.getenv("AWS_IOT_ENDPOINT"), 8883)
        self.mqttClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

        self.mqttClient.connect()
```

Every instance of [___AWSIoTMQTTClient___](https://github.com/aws/aws-iot-device-sdk-python/blob/master/AWSIoTPythonSDK/MQTTLib.py#L35)
requires a client Id. We use the names of our IoT device as client Id for the connection. To define to which AWS IoT
endpoint the IoT device should connect to, we pass the endpoint address to the _configureEndpoint()_ function. The 
endpoint address was stored during terraform setup in a _.env_ file, so it is assigned as environment variable when
`docker-compose up` is called. By passing the port number 8883 the client uses TLS mutual authentication. With port number
443 it would use authentication via websocket.

The `subscribe_to_topic()` and `publish_message_to_topic()` functions map the equivalent functions of the AWS IoT SDK to
our class.


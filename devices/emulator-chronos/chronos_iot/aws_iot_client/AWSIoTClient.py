import time
import os
import urllib.request
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class AWSIoTClient:
    def __init__(self, root_ca_path, certificate_path, private_key_path, device_name):
        self.mqttClient = AWSIoTMQTTClient(device_name)
        self.mqttClient.configureEndpoint(os.getenv("AWS_IOT_ENDPOINT"), 8883)
        self.mqttClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

        # TODO: check configuration options
        # AWSIoTMQTTClient connection configuration
        # self.mqttClient.configureAutoReconnectBackoffTime(1, 32, 20)
        # self.mqttClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        # self.mqttClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        # self.mqttClient.configureConnectDisconnectTimeout(10)  # 10 sec
        # self.mqttClient.configureMQTTOperationTimeout(5)  # 5 sec

        self.mqttClient.connect()

    def subscribeToTopic(self, topic, callback, quality_of_service):
        self.mqttClient.subscribe(topic, quality_of_service, callback)

    def publishMessageToTopic(self, message, topic, quality_of_service):
        self.mqttClient.publish(topic, message, quality_of_service)


if __name__ == "__main__":
    pass

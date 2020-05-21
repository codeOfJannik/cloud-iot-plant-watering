import time
import os
import urllib.request
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

class AWSIoTClient:
    def __init__(self, rootCAPath, certificatePath, privateKeyPath, device_name):
        self.mqttClient = AWSIoTMQTTClient(v)
        self.mqttClient.configureEndpoint(os.getenv("AWS_IOT_ENDPOINT"))
        self.mqttClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # TODO: check configuration options
        # AWSIoTMQTTClient connection configuration
        # self.mqttClient.configureAutoReconnectBackoffTime(1, 32, 20)
        # self.mqttClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        # self.mqttClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        # self.mqttClient.configureConnectDisconnectTimeout(10)  # 10 sec
        # self.mqttClient.configureMQTTOperationTimeout(5)  # 5 sec

        self.mqttClient.connect()

    def subscribeToTopic(self, topic, callback, qualityOfService):
        self.mqttClient.subscribe(topic, qualityOfService, callback)

    def publishMessageToTopic(self, message, topic, qualityOfService):
        self.mqttClient.publish(topic, message, qualityOfService)

if __name__ == "__main__":
    pass

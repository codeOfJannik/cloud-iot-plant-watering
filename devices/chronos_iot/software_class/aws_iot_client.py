import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class AWSIoTClient:
    def __init__(self, root_ca_path, certificate_path, private_key_path, device_name):
        """
        TODO
        :param root_ca_path: TODO
        :param certificate_path: TODO
        :param private_key_path: TODO
        :param device_name: TODO
        """
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

    def subscribe_to_topic(self, topic, custom_callback, quality_of_service) -> bool:
        """
        TODO
        :param topic: TODO
        :param custom_callback: TODO
        :param quality_of_service: TODO
        :return: [bool]
        """
        return self.mqttClient.subscribe(topic, quality_of_service, custom_callback)

    def publish_message_to_topic(self, message, topic, quality_of_service) -> bool:
        """
        TODO
        :param message: TODO
        :param topic: TODO
        :param quality_of_service: TODO
        :return: [bool]
        """
        return self.mqttClient.publish(topic, message, quality_of_service)


if __name__ == "__main__":
    pass

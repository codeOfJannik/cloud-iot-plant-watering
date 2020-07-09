import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class AWSIoTClient:
    def __init__(self, root_ca_path, certificate_path, private_key_path, device_name):
        """
        Initializes AWSIoTClient class using the AWSIoTMQTTClient class provided by AWS in the
        aws-iot-device-sdk-python. The MQTT client is configured with the endpoint address of the AWS account and
        the credential files for the specific device need to be passed to the MQTT client.
        :param root_ca_path: path to the AWS root-CA downloaded in each device docker container (Dockerfile)
        :param certificate_path: path to the AWS IoT device specific certificate file created during terraform setup
        :param private_key_path: path to the AWS IoT device specific private key file created during terraform setup
        :param device_name: name of the AWS IoT device
        """
        self.mqttClient = AWSIoTMQTTClient(device_name)
        self.mqttClient.configureEndpoint(os.getenv("AWS_IOT_ENDPOINT"), 8883)
        self.mqttClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

        self.mqttClient.connect()

    def subscribe_to_topic(self, topic, custom_callback, quality_of_service) -> bool:
        """
        Client tries to subscribe to a defined MQTT topic, and registers callback for incoming messages on the topic.
        :param topic: the MQTT topic the client should subscribe to
        :param custom_callback: the callback that should be executed when messages on the topic are received
        :param quality_of_service: qos of the subscription (1 = confirm received message, 0 = no confirmation)
        :return: True if the subscribe attempt succeeded. False if failed.
        """
        return self.mqttClient.subscribe(topic, quality_of_service, custom_callback)

    def publish_message_to_topic(self, message, topic, quality_of_service) -> bool:
        """
        Client tries to published a message in a defined MQTT topic.
        :param message: json message to be published
        :param topic: topic where the message should be published
        :param quality_of_service: 1 if confirmation of received message required ,0 if no confirmation required
        :return: [bool]
        """
        return self.mqttClient.publish(topic, message, quality_of_service)


if __name__ == "__main__":
    pass

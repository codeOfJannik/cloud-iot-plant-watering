import time
import os
import urllib.request
import json
from .aws_iot_client import AWSIoTClient


class DeviceSoftware(AWSIoTClient):
    def __init__(self, credentials_directory: str = "../app/"):
        """
        Class to run device software in a loop
        :param credentials_directory: defines, where to find the aws device credentials for IoT Service
        """
        # set run loop value, need for unittests, value because can set f.e. range(10, -1, -1) to run 10 times
        self.running = 1
        # get environment variables (set in docker-compose file)
        self.HARDWARE_URL = os.getenv('HARDWARE_URL')
        self.DEVICE_NAME = os.getenv('DEVICE_NAME')
        self.INTERVAL_TIME = int(os.getenv('INTERVAL_TIME', default=3))
        # set aws client variables
        self.credentials_directory = credentials_directory
        self.root_ca = os.path.abspath("root-CA.crt")
        self.certificate = os.path.abspath(self.credentials_directory + self.DEVICE_NAME + ".cert.pem")
        self.private_key = os.path.abspath(self.credentials_directory + self.DEVICE_NAME + ".private.key")
        super().__init__(self.root_ca, self.certificate, self.private_key, self.DEVICE_NAME)

    def run_soil_moisture(self):
        """
        Get sensor data from hardware url and publish message in IoT Service
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')

        while self.running:
            time.sleep(self.INTERVAL_TIME)
            try:
                # get and parse switch state
                url = '{url}/gpios/{device}'.format(url=self.HARDWARE_URL, device=self.DEVICE_NAME)
                # get current state from gpio
                data = get_gpio(url=url)

                # data to IoT Service
                message = {'message': "Test from {}".format(self.DEVICE_NAME), 'data': data['state']['value']}
                message_json = json.dumps(message)
                topic = "bed/sensors/moisture"
                if self.publish_message_to_topic(message_json, topic, 0):
                    pass
                else:
                    return False

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                print(e)
                return False

    def run_water_switch(self):
        """
        Subscribe to IoT Service topic and change water switch state
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')
        gpio_url = '{url}/gpios/{device}'.format(url=self.HARDWARE_URL, device=self.DEVICE_NAME)

        # update device shadow with current state
        self.update_switch_shadow(gpio_url)

        def custom_callback(client, userdata, message):
            """
            Intern callback function to change switch state
            Parameter determined by AWSIoTPythonSDK
            """
            try:
                # received message:
                print("Received message")
                data = json.loads(message.payload)
                print(data)
                desired_switch_state = data['state']['switch_open']

                # set new switch state
                data_message = json.dumps({"open": desired_switch_state})
                success = set_gpio(url=gpio_url, data=data_message)

                # update shadow after changed to new switch state
                self.update_switch_shadow(gpio_url)
                return success

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                # print(f'unknown error')
                print("change switch state error: {}".format(e))
                return False

        # subscribe to IoT Service and define callback function, return if callback is false, else repeat
        if self.subscribe_to_topic("$aws/things/{device}/shadow/update/delta".format(device=self.DEVICE_NAME), custom_callback, 0):
            pass
        else:
            return False

        while self.running:
            pass

    def update_switch_shadow(self, gpio_url):
        # get switch state
        switch_data = get_gpio(gpio_url)
        switch_open = switch_data['state']['open']
        message = {
            "state": {
                "reported": {
                    "switch_open": switch_open
                }
            }
        }
        json_messgae = json.dumps(message)

        # publish message to update device shadow with current state
        self.publish_message_to_topic(json_messgae, "$aws/things/{device}/shadow/update".format(device=self.DEVICE_NAME), 1)


"""----helper functions----"""


def set_gpio(url: str, data: str) -> bool:
    req = urllib.request.Request(url, data=data.encode('utf-8'), method='POST')
    with urllib.request.urlopen(req) as f:
        if f.status == 200:
            return True
        return False


def get_gpio(url: str) -> dict:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as f:
        if f.status == 200:
            data = json.loads(f.read().decode('utf-8'))
    return data


if __name__ == "__main__":
    pass

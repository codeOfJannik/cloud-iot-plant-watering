import time
import os
import urllib.request
import json
from .aws_iot_client import AWSIoTClient


class DeviceSoftware(AWSIoTClient):
    def __init__(self, credentials_directory: str = "../app/"):
        """
        Class to run device software in a loop
        """
        # set run loop value, need for unittests, value because can set f.e. range(10, -1, -1) to run 10 times.
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

    def start_loop(self, software_function):
        """
        start the loop
        :param software_function: software function to run
        :return: no return, run in infinite loop
        """
        print(f'Starting software')
        # print('HARDWARE_URL: {}'.format(self.HARDWARE_URL))
        while self.running:
            time.sleep(self.INTERVAL_TIME)
            software_function()

    def run_soil_moisture(self):
        """
        Get sensor data from hardware url and publish message in IoT Service
        :return: [bool] True if no exception else False
        """
        try:
            # get and parse switch state
            url = '{url}/gpios/{device}'.format(url=self.HARDWARE_URL, device=self.DEVICE_NAME)
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as f:
                if f.status == 200:
                    data = json.loads(f.read().decode('utf-8'))
                    # data to IoT Service
                    message = {'message': "Test from {}".format(self.DEVICE_NAME), 'data': data['state']['value']}
                    message_json = json.dumps(message)
                    topic = "bed/sensors/moisture"
                    return self.publish_message_to_topic(message_json, topic, 0)
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
        :return: [bool] True if no exception else False
        """
        # set interval time to zero (not needed in water switch function)
        self.INTERVAL_TIME = 0

        def custom_callback(client, userdata, message):
            """
            Intern callback function to change switch state
            Parameter determined by AWSIoTPythonSDK
            """
            try:
                # received message:
                data = json.loads(message.payload)
                switch_state = data['switch_state']
                # set new switch state
                url = '{url}/gpios/{device}'.format(url=self.HARDWARE_URL, device=self.DEVICE_NAME)
                data = json.dumps({"open": switch_state}).encode('utf-8')
                req = urllib.request.Request(url, data=data, method='POST')
                with urllib.request.urlopen(req) as f:
                    if f.status == 200:
                        return True
                    return False
            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                # print(f'unknown error')
                print("change switch state error: {}".format(e))
                return False

        # subscribe to IoT Service and define callback function
        return self.subscribe_to_topic("bed/switch/water", custom_callback, 0)


if __name__ == "__main__":
    pass

import time
import os
import urllib.request
import json
from .aws_iot_client import AWSIoTClient


class DeviceSoftware(AWSIoTClient):
    def __init__(self, cert_directory: str = "../cert/"):
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
        self.root_ca = os.path.abspath(cert_directory + "root-CA.crt")
        self.certificate = os.path.abspath(self.DEVICE_NAME + ".cert.pem")
        self.private_key = os.path.abspath(self.DEVICE_NAME + ".private.key")
        super().__init__(self.root_ca, self.certificate, self.private_key, self.DEVICE_NAME)

    def run_update_data(self, topic=None):
        """
        Get sensor data from hardware url and publish message in IoT Service
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')

        while self.running:
            time.sleep(self.INTERVAL_TIME)
            try:
                # get and parse switch state
                url = '{url}/gpios'.format(url=self.HARDWARE_URL)
                # get current state from gpio
                data = get_gpio(url=url)

                self.update_sensor_shadow(data)
                if topic:
                    self.publish_sensor_value(data, topic)

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                print(e)
                return False

    def publish_sensor_value(self, data, topic):
        json_message = json.dumps(data)
        self.publish_message_to_topic(json_message, topic + self.DEVICE_NAME, 0)

    def update_sensor_shadow(self, data):
        message = {
            "state": {
                "reported": {
                    "data": data
                }
            }
        }
        json_message = json.dumps(message)

        # publish message to update device shadow with current value
        self.publish_message_to_topic(json_message, "$aws/things/{device}/shadow/update".format(device=self.DEVICE_NAME), 1)


    def run_water_valve(self):
        """
        Subscribe to IoT Service topic and change water switch state
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')
        gpio_url = '{url}/gpios/{device}'.format(url=self.HARDWARE_URL, device=self.DEVICE_NAME)

        def custom_callback(client, userdata, message):
            """
            Intern callback function to change switch state
            Parameter determined by AWSIoTPythonSDK
            """
            try:
                # received message:
                data = json.loads(message.payload)
                desired_switch_state = data['state']['switch_open']

                # set new switch state
                data_message = json.dumps({"open": desired_switch_state})
                success = set_gpio(url=gpio_url, data=data_message)

                # update shadow after changed to new switch state
                self.update_valve_shadow(gpio_url)
                return success

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                # print(f'unknown error')
                print("change switch state error: {}".format(e))
                return False

        try:
            # update device shadow with current state
            self.update_valve_shadow(gpio_url)
            # subscribe to IoT Service and define callback function, return if callback is false, else repeat
            if self.subscribe_to_topic("$aws/things/{device}/shadow/update/delta".format(device=self.DEVICE_NAME), custom_callback, 0):
                pass
            else:
                return False
        except ConnectionRefusedError:
            print('could not connect to {url}'.format(url=self.HARDWARE_URL))
            return False
        except Exception as e:
            # print(f'unknown error')
            print("change switch state error: {}".format(e))
            return False

        while self.running:
            pass

    def update_valve_shadow(self, gpio_url):
        # get valve state
        valve_data = get_gpio(gpio_url)
        valve_open = valve_data['state']['open']
        message = {
            "state": {
                "reported": {
                    "switch_open": valve_open
                }
            }
        }
        json_message = json.dumps(message)

        # publish message to update device shadow with current state
        self.publish_message_to_topic(json_message, "$aws/things/{device}/shadow/update".format(device=self.DEVICE_NAME), 1)


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

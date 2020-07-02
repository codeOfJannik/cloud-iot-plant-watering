import time
import os
import urllib.request
import json
from .aws_iot_client import AWSIoTClient


class DeviceSoftware(AWSIoTClient):
    def __init__(self, cert_directory: str = "../cert/"):
        """
        Class to run device software in a loop
        :param cert_directory: defines, where to find the aws root cert for IoT Service
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

    def run_update_control_panel(self):
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
                keys = list(data)
                shadow_data = {}
                for key in keys:
                    shadow_data[key] = data[key]["state"]["value"]

                self.update_sensor_shadow(shadow_data)

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                print(e)
                return False

    def run_update_rain_barrel_sensor(self):
        """
        Get sensor data from hardware url and publish message in IoT Service
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')

        while self.running:
            time.sleep(self.INTERVAL_TIME)
            try:
                # get and parse switch state
                url = '{url}/gpios/rain_barrel_sensor'.format(url=self.HARDWARE_URL)
                # get current state from gpio
                sensor_value = get_gpio(url=url)["state"]["value"]
                data = {"value": sensor_value}

                self.update_sensor_shadow(data)

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                print(e)
                return False

    def run_update_soil_moisture(self):
        """
        Get sensor data from hardware url and publish message in IoT Service
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')

        while self.running:
            time.sleep(self.INTERVAL_TIME)
            try:
                # get and parse switch state
                url = '{url}/gpios/soilMoistureSensor'.format(url=self.HARDWARE_URL)
                # get current state from gpio
                sensor_value = get_gpio(url=url)["state"]["value"]
                data = {"value": sensor_value}

                self.update_sensor_shadow(data)

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                print(e)
                return False

    def update_sensor_shadow(self, data):
        message = {
            "state": {
                "reported": data
            }
        }
        json_message = json.dumps(message)

        # publish message to update device shadow with current value
        self.publish_message_to_topic(json_message, "$aws/things/{device}/shadow/update".format(device=self.DEVICE_NAME), 0)

    def run_water_valve(self):
        """
        Subscribe to IoT Service topic and change water switch state
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')
        url = '{url}/gpios/{sensor}'.format(url=self.HARDWARE_URL, sensor=self.DEVICE_NAME)

        def custom_callback(client, userdata, message):
            """
            Intern callback function to change switch state
            Parameter determined by AWSIoTPythonSDK
            """
            try:
                # received message:
                received_data = json.loads(message.payload)
                desired_switch_state = received_data['state']['valve_open']
                data_message = json.dumps({"open": not desired_switch_state})
                set_gpio(url=url, data=data_message)

                # update shadow after changed to new switch state
                sensor_value = not get_gpio(url=url)["state"]["open"]
                data = {"valve_open": sensor_value}
                # update device shadow with current state
                self.update_valve_shadow(data)

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                # print(f'unknown error')
                print("change switch state error: {}".format(e))
                return False

        try:
            # get current state from gpio
            sensor_value = not get_gpio(url=url)["state"]["open"]
            data = {"valve_open": sensor_value}
            # update device shadow with current state
            self.update_valve_shadow(data)
            # subscribe to IoT Service and define callback function, return if callback is false, else repeat
            delta_topic = "$aws/things/{device}/shadow/update/delta".format(device=self.DEVICE_NAME)
            if self.subscribe_to_topic(delta_topic, custom_callback, 0):
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

    def update_valve_shadow(self, data):
        # get valve state
        message = {
            "state": {
                "reported": data
            }
        }
        json_message = json.dumps(message)

        # publish message to update device shadow with current state
        self.publish_message_to_topic(json_message, "$aws/things/{device}/shadow/update".format(device=self.DEVICE_NAME), 0)


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

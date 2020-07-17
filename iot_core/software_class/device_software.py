import time
import os
import urllib.request
import json
import yaml
from .aws_iot_client import AWSIoTClient
import sys


class DeviceSoftware(AWSIoTClient):
    def __init__(self, cert_directory: str = "../cert/", settings_yaml_path="settings.yaml"):
        """
        Class to run device software in a loop
        :param cert_directory: defines, where to find the aws root cert for IoT Service
        """
        # set run loop value, need for unittests, value because can set f.e. range(10, -1, -1) to run 10 times
        self.running = 1
        # get environment variables (set in docker-compose file)
        self.HARDWARE_URL = os.getenv('HARDWARE_URL')
        self.DEVICE_NAME = os.getenv('DEVICE_NAME')
        # read in yaml
        self.settings_yaml_path = settings_yaml_path
        self.INTERVAL_TIME, self.BED_ID, self.IOT_TYPE = self.read_settings_yaml()
        # set aws client variables
        self.root_ca = os.path.abspath(cert_directory + "root-CA.crt")
        self.certificate = os.path.abspath(self.DEVICE_NAME + ".cert.pem")
        self.private_key = os.path.abspath(self.DEVICE_NAME + ".private.key")
        if self.cert_files_exist():
            super().__init__(self.root_ca, self.certificate, self.private_key, self.DEVICE_NAME)
        else:
            sys.exit('CA Files not exists')

    def run_device_software(self):
        if self.IOT_TYPE == "water_valve":
            return self.run_water_valve()
        elif self.IOT_TYPE == "soil_moisture":
            return self.run_update_soil_moisture()
        elif self.IOT_TYPE == "control_panel":
            return self.run_update_control_panel()
        elif self.IOT_TYPE == "rain_barrel":
            return self.run_update_rain_barrel_sensor()

    def read_settings_yaml(self):
        # read in yaml
        with open(self.settings_yaml_path, "r") as file:
            settings = yaml.load(file, Loader=yaml.FullLoader)
        return settings.get('time_interval', 30), settings.get('bed'), settings['iot_type']

    def cert_files_exist(self):
        return os.path.exists(self.root_ca) and os.path.exists(self.certificate) and os.path.exists(self.private_key)

    def run_update_control_panel(self):
        """
        Get sensor data from hardware url and publish message in IoT Service
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')

        while self.running:
            time.sleep(self.INTERVAL_TIME)
            try:
                url = '{url}/gpios'.format(url=self.HARDWARE_URL)
                # get current state from gpio
                data = get_gpio(url=url)
                for index, key in enumerate(data):
                    shadow_data = {"value": data[key]["state"]["value"]}
                    if index != 0:
                        shadow_data["bed_id"] = index
                    self.update_device_shadow(shadow_data, shadow_name=key)

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
                url = '{url}/gpios/rain_barrel_sensor'.format(url=self.HARDWARE_URL)
                # get current state from gpio
                sensor_value = get_gpio(url=url)["state"]["value"]
                data = {"value": sensor_value}

                self.update_device_shadow(data)

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
                url = '{url}/gpios/soilMoistureSensor'.format(url=self.HARDWARE_URL)
                # get current state from gpio
                sensor_value = get_gpio(url=url)["state"]["value"]
                data = {"value": sensor_value,
                        "bed_id": self.BED_ID}

                self.update_device_shadow(data)

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                print(e)
                return False

    def run_water_valve(self):
        """
        Subscribe to IoT Service topic and change water switch state
        :return: [bool] False if exception else repeat
        """
        print(f'Starting software')
        url = f'{self.HARDWARE_URL}/gpios/valve'
        print("url:" + url)

        def custom_callback(client, userdata, message):
            """
            Intern callback function to change switch state
            Parameter determined by AWSIoTPythonSDK
            """
            try:
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

            except ConnectionRefusedError:
                print('could not connect to {url}'.format(url=self.HARDWARE_URL))
                return False
            except Exception as e:
                # print(f'unknown error')
                print("change switch state error: {}".format(e))
                self.running = False

        try:
            # get current state from gpio
            sensor_value = not get_gpio(url=url)["state"]["open"]
            data = {"valve_open": sensor_value}
            if self.BED_ID is not None:
                data['bed_id'] = self.BED_ID
            # update device shadow with current state
            print(f'update shadow value with data: {data}')
            self.update_device_shadow(data)
            # subscribe to IoT Service and define callback function, return if callback is false, else repeat
            delta_topic = "$aws/things/{device}/shadow/update/delta".format(device=self.DEVICE_NAME)
            print('subscribe to ' + delta_topic)

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
            self.running = False
            return False

        while self.running:
            pass

    def update_device_shadow(self, data, shadow_name=None):
        message = {
            "state": {
                "reported": data
            }
        }
        json_message = json.dumps(message)
        # publish message to update device shadow with current value
        if shadow_name:
            topic = f"$aws/things/{self.DEVICE_NAME}/shadow/name/{shadow_name}/update"
        else:
            topic = f"$aws/things/{self.DEVICE_NAME}/shadow/update"
        print(self.publish_message_to_topic(json_message, topic, 0))


"""----gpio functions----"""


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

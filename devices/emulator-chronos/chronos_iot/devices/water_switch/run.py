import time
import os
import urllib.request
import json
from aws_iot_client import AWSIoTClient


HARDWARE_URL = os.getenv('HARDWARE_URL')
DEVICE_NAME = os.getenv('DEVICE_NAME')
credentials_directory = "aws_credentials/"
rootCA = os.path.abspath(credentials_directory+"root-CA.crt")
certificate = os.path.abspath(credentials_directory+DEVICE_NAME+".cert.pem")
private_key = os.path.abspath(credentials_directory+DEVICE_NAME+".private.key")
awsIoTClient = AWSIoTClient.AWSIoTClient(rootCA, certificate, private_key, DEVICE_NAME)


def customCallback(client, userdata, message):
    try:
        print("Received message:")
        data = json.loads(message.payload)
        switch_state = data['switch_state']
        # set new switch state
        url = f'{HARDWARE_URL}/gpios/'+DEVICE_NAME
        data = json.dumps({"open": switch_state}).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req) as f:
            if f.status == 200:
                return True
            return False
    except ConnectionRefusedError:
        print(f'could not connect to {HARDWARE_URL}')
        return False
    except Exception as e:
        # print(f'unknown error')
        print("change switch state error: {}".format(e))
        return False


def start_loop():

    awsIoTClient.subscribeToTopic("bed/switch/water", customCallback, 0)
    print(f'Starting software')
    print(f'HARDWARE_URL: {HARDWARE_URL}')
    while True:
        pass


start_loop()

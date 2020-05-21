import time
import os
import urllib.request
import json
from .aws_iot_client import AWSIoTClient

HARDWARE_URL = os.getenv('HARDWARE_URL')
DEVICE_NAME = os.getenv('DEVICE_NAME')
credentials_directory = "aws_credentials/"
rootCA = credentials_directory+"root-CA.crt"
certificate = credentials_directory+DEVICE_NAME+".cert.pem"
private_key = credentials_directory+DEVICE_NAME+".private.key"
awsIoTClient = AWSIoTClient.AWSIoTClient(rootCA, certificate, private_key, DEVICE_NAME)


def send_value():
    try:
        # get and parse switch state
        url = f'{HARDWARE_URL}/gpios/'+DEVICE_NAME
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as f:
            if f.status == 200:
                data = json.loads(f.read().decode('utf-8'))
                # at this point to IoT Service instead print
                message = {'message': "Test from " + DEVICE_NAME, 'data': data['state']['value']}
                message_json = json.dumps(message)
                topic = "bed/sensors/moisture"
                awsIoTClient.publishMessageToTopic(message_json, topic, 0)
                return True
            return True
    except ConnectionRefusedError:
        print(f'could not connect to {HARDWARE_URL}')
        return True
    except Exception as e:
        print(e)
        return True


def start_loop():
    print(f'Starting software')
    print(f'HARDWARE_URL: {HARDWARE_URL}')
    while True:
        time.sleep(3.5)
        send_value()


start_loop()

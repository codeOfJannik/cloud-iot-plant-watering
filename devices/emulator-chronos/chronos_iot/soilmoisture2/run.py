import time
import os
import urllib.request
import json

HARDWARE_URL = os.getenv('HARDWARE_URL')


def send_value():
    try:
        # get and parse switch state
        url = f'{HARDWARE_URL}/gpios/soilMoisture2_sensor'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as f:
            if f.status == 200:
                data = json.loads(f.read().decode('utf-8'))
                # at this point to IoT Service instead print
                print(data['state']['value'])
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

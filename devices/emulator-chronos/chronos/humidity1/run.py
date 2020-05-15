import time 
import os
import urllib.request
import json

HARDWARE_URL = os.getenv('HARDWARE_URL')

def humidity():
    try:
        # get and parse humidity state
        url = f'{HARDWARE_URL}/gpios/humidity'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as f:
            if f.status == 200:
                data = json.loads(f.read().decode('utf-8'))
                return data['state']['open']
            return True
    except ConnectionRefusedError:
        print(f'could not connect to {HARDWARE_URL}')
        return True
    except:
        print(f'unknown error')
        return True


def start_loop():
    print(f'Starting software')
    print(f'HARDWARE_URL: {HARDWARE_URL}')

start_loop()

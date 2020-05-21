import time
import os
import urllib.request
import json


class SoilMoisture:
    def __init__(self, gpio: str):
        self.HARDWARE_URL = os.getenv('HARDWARE_URL')
        self.gpio = gpio

    def send_value(self):
        try:
            # get and parse switch state
            url = '{}/gpios/{}'.format(self.HARDWARE_URL, self.gpio)
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as f:
                if f.status == 200:
                    data = json.loads(f.read().decode('utf-8'))
                    # at this point to IoT Service instead print
                    print(data['state']['value'])
                    return True
                return True
        except ConnectionRefusedError:
            print(f'could not connect to {self.HARDWARE_URL}')
            return True
        except Exception as e:
            print(e)
            return True

    def start_loop(self):
        print(f'Starting software')
        print(f'HARDWARE_URL: {self.HARDWARE_URL}')
        while True:
            time.sleep(3.5)
            self.send_value()


if __name__ == "__main__":
    pass

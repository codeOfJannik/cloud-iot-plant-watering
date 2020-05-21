import time
import os
import urllib.request
import json

HARDWARE_URL = os.getenv('HARDWARE_URL')


# def open_switch():
#     try:
#         # get and parse switch state
#         url = f'{HARDWARE_URL}/gpios/switch'
#         req = urllib.request.Request(url)
#         with urllib.request.urlopen(req) as f:
#             if f.status == 200:
#                 data = json.loads(f.read().decode('utf-8'))
#                 return data['state']['open']
#             return True
#     except ConnectionRefusedError:
#         print(f'could not connect to {HARDWARE_URL}')
#         return True
#     except Exception as e:
#         # print(f'unknown error')
#         print("open switch error: {}".format(e))
#         return True


def change_switch_state(switch_open=False):
    try:
        # set new switch state
        url = f'{HARDWARE_URL}/gpios/power_switch'
        data = json.dumps({"open": switch_open}).encode('utf-8')
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
    print(f'Starting software')
    print(f'HARDWARE_URL: {HARDWARE_URL}')
    while True:
        time.sleep(6.5)
        if False:  # open_switch():
            print("set true")
            change_switch_state(switch_open=True)
        else:
            change_switch_state(switch_open=False)


start_loop()

#import time
#import os
#import urllib.request
#import json

#HARDWARE_URL = os.getenv('HARDWARE_URL')


#def switch_is_open():
#    try:
#        # get and parse switch state
#        url = f'{HARDWARE_URL}/gpios/switch'
#        req = urllib.request.Request(url)
#        with urllib.request.urlopen(req) as f:
#            if f.status == 200:
#                data = json.loads(f.read().decode('utf-8'))
#                return data['state']['open']
#            return True
#    except ConnectionRefusedError:
#        print(f'could not connect to {HARDWARE_URL}')
#        return True
#    except:
#        print(f'unknown error')
#        return True#


#def led_set(on=False):
#    try:
#        # get and parse switch state
#        url = f'{HARDWARE_URL}/gpios/led'
#        data = json.dumps({"on": on}).encode('utf-8')
#        req = urllib.request.Request(url, data=data, method='POST')
#        with urllib.request.urlopen(req) as f:
#            if f.status == 201:
#                return True
#            return False
#    except ConnectionRefusedError:
#        print(f'could not connect to {HARDWARE_URL}')
#        return False
#    except:
#        print(f'unknown error')
#        return False


#def start_loop():
#    print(f'Starting software')
#    print(f'HARDWARE_URL: {HARDWARE_URL}')
#    while True:
#        time.sleep(0.5)
#        if switch_is_open():
#            led_set(on=False)
#        else:
#            led_set(on=True)


#start_loop()

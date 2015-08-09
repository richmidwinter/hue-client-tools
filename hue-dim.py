#!/usr/local/bin/python3.4

import requests

# Turn on
url='http://192.168.0.98/api/36c2e5fc34da518f37f40bd42547d107/lights/1/state'
normal_data='{"on":true, "hue": 29000, "sat": 100, "bri": 40, "ct": 350}'

r = requests.put(url, data=normal_data)

#!/usr/local/bin/python3.4

import requests

# Turn off
url='http://192.168.0.98/api/36c2e5fc34da518f37f40bd42547d107/lights/1/state'
normal_data='{"on":false}'

r = requests.put(url, data=normal_data)

#!/usr/local/bin/python3.4

import config
import requests
import sys

light = sys.argv[1]

# Turn off
url='http://{}/api/{}/lights/{}/state'.format(
  config.hue['host'],
  config.hue['key'],
  light
)
normal_data='{"on":false}'

r = requests.put(url, data=normal_data)

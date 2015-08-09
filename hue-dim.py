#!/usr/local/bin/python3.4

import config
import requests
import sys

light = sys.argv[1]

# Turn on
url='http://{}/api/{}/lights/{}/state'.format(
  config.hue['host'],
  config.hue['key'],
  light
)
normal_data='{"on":true, "hue": 29000, "sat": 100, "bri": 40, "ct": 350}'

r = requests.put(url, data=normal_data)

#!/usr/local/bin/python3.4

import config
import requests
import sys
import datetime, time
from time import sleep
from sunrise import sun

light = sys.argv[1]

s = sun(lat=52,long=-2)

time = s.sunset(when=datetime.datetime.now())
#print('Sunset at ', time)

today = datetime.date.today()

end = datetime.datetime.combine(today, time)
start = datetime.datetime.combine(today, datetime.datetime.now().time())

delta = end - start
sleep(delta.seconds +3600)

# Turn on
url='http://{}/api/{}/lights/{}/state'.format(
  config.hue['host'],
  config.hue['key'],
  light
)
normal_data='{"on":true, "hue": 29000, "sat": 100, "bri": 80, "ct": 350}'

r = requests.put(url, data=normal_data)

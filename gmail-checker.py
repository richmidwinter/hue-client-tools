#!/usr/local/bin/python3.4

import sys
import gflags
import requests,json
from time import sleep
from datetime import datetime
import os
#from apiclient import errors
from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail Notifier'

info_url='http://192.168.0.98/api/36c2e5fc34da518f37f40bd42547d107/lights/3'
url='http://192.168.0.98/api/36c2e5fc34da518f37f40bd42547d107/lights/3/state'
normal_data='{"on":true, "hue": 29000, "sat": 100, "bri": 80, "ct": 350}}'
notify_data='{"on":true, "hue": 65280, "sat": 255, "bri": 255}'
off_data='{"on":false}'
sleep_time=1

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-notifier.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def ListMessagesMatchingQuery(service, user_id, query=''):
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def main(argv):
    try:
      gflags.FLAGS(argv)
    except gflags.FlagsError as e:
      print('%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS))
      sys.exit(1)

    credentials = get_credentials()
    service = build('gmail', 'v1', http=credentials.authorize(Http()))
    msgids = ListMessagesMatchingQuery(service, 'me', query='is:unread label:inbox')

    if (len(msgids)>0):
        # Was on?
        r = requests.get(info_url)
        was_on = json.loads(r.text)["state"]["on"]

        # Flash lights
        r = requests.put(url, data=normal_data) # On white
        sleep(sleep_time)
        r = requests.put(url, data=notify_data) # On red
        sleep(sleep_time)
        r = requests.put(url, data=normal_data) # On white
        sleep(sleep_time)
        r = requests.put(url, data=notify_data) # On red
        sleep(sleep_time)

        if was_on:
          r = requests.put(url, data=normal_data)
        else:
          r = requests.put(url, data=off_data)

if __name__ == "__main__":
  main(sys.argv)

from pprint import pprint
import time
import requests
from requests.exceptions import HTTPError
import json
import re
import configparser
import datetime
from pathlib import Path

_url_base = 'https://api.clockify.me/api/v1/user'
_url = 'https://api.clockify.me/api/v1'

# https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read('config.ini')  # config.ini file with [clockify] and API_KEY = MyAPIKeyWithoutQuotes
X_Api_Key = config.get('clockify', 'API_KEY')

_headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}


def end_current_task():
    global _url,_url_base,_headers

    response = requests.get(_url_base, headers=_headers)
    json_response_base = response.json()
    workspaceId = json_response_base['activeWorkspace']
    userId = json_response_base['id']
    api_time_entry = f'/workspaces/{workspaceId}/user/{userId}/time-entries'
    api_url = _url + api_time_entry

    current_utc = datetime.datetime.utcnow()
    response = requests.post(api_url,headers=_headers,data = {"end":current_utc.strftime("%Y-%m-%dT%H:%M:%SZ")})
    pprint(response)
    pprint(response.json())
def is_work_this_person():
    global _url,_url_base,_headers

    response = requests.get(_url_base, headers=_headers)
    json_response_base = response.json()
    workspaceId = json_response_base['activeWorkspace']
    userId = json_response_base['id']
    api_time_entry = f'/workspaces/{workspaceId}/user/{userId}/time-entries'
    api_url = _url + api_time_entry
    response = requests.get(api_url, headers=_headers)
    json_response_entry = response.json()
    # pprint(json_response_entry)
    last_task = json_response_entry[0]
    time_interval = last_task.get('timeInterval')
    # pprint("gi")
    if time_interval.get('end') is None:
        pprint("he is working")
        return True
    else:
        print(' '.join(("hi was ending at",time_interval.get('end'))))
        return False

def red_led_light():
    print("red led light\n\n\n")


def red_led_turn_down():
    print("red led turn down\n\n\n\n")

def main():
    while True:
        if is_work_this_person():
            # red_led_light()
            end_current_task()
        else:
            red_led_turn_down()


if __name__ == "__main__":
    main()
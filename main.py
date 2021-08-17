from pprint import pprint
import time
import requests
from requests.exceptions import HTTPError
import json
import re
import configparser
from pathlib import Path

def is_work_this_person():
    url_base = 'https://api.clockify.me/api/v1/user'
    url = 'https://api.clockify.me/api/v1'

    # https://docs.python.org/3/library/configparser.html
    config = configparser.ConfigParser()
    config.read('config.ini')  # config.ini file with [clockify] and API_KEY = MyAPIKeyWithoutQuotes
    X_Api_Key = config.get('clockify', 'API_KEY')

    headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}

    response = requests.get(url_base, headers=headers)

    json_response_base = response.json()
    # pprint(json_response_base)

    workspaceId = json_response_base['activeWorkspace']
    userId = json_response_base['id']

    #
    api_time_entry = f'/workspaces/{workspaceId}/user/{userId}/time-entries'
    api_url = url + api_time_entry
    #
    response = requests.get(api_url, headers=headers)
    json_response_projects = response.json()
    # pprint(json_response_projects[0])
    last_task = json_response_projects[0]
    time_interval = last_task.get('timeInterval')
    # pprint("gi")
    if time_interval.get('end') is None:
        pprint("he is working")
        return True
    else:
        print(' '.join(("hi was ending at",time_interval.get('end'))))
        return False

def red_led_light():
    print("red led light")

def red_led_turn_down():
    print("red led turn down")

def main():
    while True:
        if is_work_this_person():
            red_led_light()
        else:
            red_led_turn_down()


if __name__ == "__main__":
    main()
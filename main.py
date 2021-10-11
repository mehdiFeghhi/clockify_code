from pprint import pprint
import time
import requests
from requests.exceptions import HTTPError
import json
import re
import configparser
import datetime
from pathlib import Path
import sys

_url_base = 'https://api.clockify.me/api/v1/user'
_url = 'https://api.clockify.me/api/v1'

# https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read('config.ini')  # config.ini file with [clockify] and API_KEY = MyAPIKeyWithoutQuotes
X_Api_Key = config.get('clockify', 'API_KEY')
    # pprint(X_Api_Key)
_headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}


def end_current_task():
    global _url,_url_base,_headers

    response = requests.get(_url_base, headers=_headers)
    json_response_base = response.json()
    workspaceId = json_response_base['activeWorkspace']
    userId = json_response_base['id']
    api_time_entry = f'/workspaces/{workspaceId}/user/{userId}/time-entries'
    api_url = _url + api_time_entry
    response = requests.get(api_url, headers=_headers)
    json_response_entry = response.json()
    data = json_response_entry[0]
    # pprint(json_response_entry)
    current_utc = datetime.datetime.utcnow()
    #
    dictionary ={
                 'start': data.get('timeInterval').get('start'),
                 "billable": data.get("billable"),
                 'description': data.get('description'),
                 'projectId': data.get('projectId'),
                 'taskId': data.get('taskId'),
                 "end": current_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                 'tagIds':data.get('tagIds')}
    app_json = json.dumps(dictionary)
    response = requests.patch(api_url,headers = _headers,data=app_json)
    pprint(response)
    pprint(response.json())

def start_current_task():
    global _url,_url_base,_headers

    response = requests.get(_url_base, headers=_headers)
    json_response_base = response.json()
    workspaceId = json_response_base['activeWorkspace']
    userId = json_response_base['id']
    api_time_entry = f'/workspaces/{workspaceId}/user/{userId}/time-entries'
    api_url = _url + api_time_entry
    response = requests.get(api_url, headers=_headers)
    json_response_entry = response.json()
    data = json_response_entry[0]
    # pprint(json_response_entry)
    current_utc = datetime.datetime.utcnow()
    #
    dictionary ={
                 'start': current_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "billable": data.get("billable"),
                 'description': data.get('description'),
                 'projectId': data.get('projectId'),
                 'taskId': data.get('taskId'),
                 "end": None,
                 'tagIds':data.get('tagIds')}

    app_json = json.dumps(dictionary)
    api_time_add_entry = f'/workspaces/{workspaceId}/time-entries'
    api_url = _url + api_time_add_entry
    response = requests.post(api_url,headers = _headers,data=app_json)
    pprint(response)
    pprint(response.json())



def is_work_this_person():
    global _url,_url_base,_headers

    response = requests.get(_url_base, headers=_headers)
    json_response_base = response.json()
    # pprint(json_response_base)
    workspaceId = json_response_base['activeWorkspace']
    userId = json_response_base['id']
    api_time_entry = f'/workspaces/{workspaceId}/user/{userId}/time-entries'
    api_url = _url + api_time_entry
    response = requests.get(api_url, headers=_headers)
    json_response_entry = response.json()
    # pprint(json_response_entry[0])
    last_task = json_response_entry[0]
    time_interval = last_task.get('timeInterval')
    # pprint("gi")
    if time_interval.get('end') is None:
        # print("he is working")
        return True
    else:
        print(' '.join(("Work was ending at",time_interval.get('end'))))
        return False

def red_led_light():
    print("red led light\n\n\n")


def red_led_turn_down():
    print("red led turn down\n\n\n\n")

def main():
    com = sys.argv[1]
    if com == 'start':
        if is_work_this_person():
            print("Error : You are at work now. You can stop your work by calling 'stop' or 'toggle'")
        else:
            start_current_task()
    elif com == 'stop':
        if is_work_this_person():
            end_current_task()
        else:
            print("Error : You are not at work now. You can start your work by calling 'start' or 'toggle'")
    elif com == 'toggle':
        if is_work_this_person():
            end_current_task()
            print('You stopped your work successfully')
        else:
            start_current_task()
            print('You started your work successfully')

                
if __name__ == "__main__":
    main()
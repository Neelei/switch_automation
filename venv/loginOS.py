import json
import time
import requests
import urllib3
import base64
import pprint
from netmiko import ConnectHandler
urllib3.disable_warnings()


def login_os(data, url):
    username = data['username']
    password = data['password']
    params = {'userName': username, 'password': password}
    url_login = url + "login-sessions"
    response = requests.post(url_login, verify=False, data=json.dumps(params), timeout=10)
    print(response.text)
    if response.status_code == 201:
        print("Login to switch: {} is successful".format(url_login))
        session = response.json()
        r_cookie = session['cookie']
        return r_cookie
    else:
        print("Login to switch failed")

def delete_sessions(url, cookie):
    url_login = url + "login-sessions"
    headers = {'cookie': cookie}
    r = requests.delete(url_login, cookies=headers, verify=False, timeout=10)
    if r.status_code == 204:
        print("Session deleted!", r.status_code)
    else:
        print("Session not deleted", r.status_code)

def logout(url, cookie):
    url_login = url + "login-sessions"
    r = requests.delete(url_login, cookies=cookie, verify=False)
    if r.status_code == 204:
        print("Logged out!", r.status_code)
    else:
        print("Logout is not successful", r.status_code)





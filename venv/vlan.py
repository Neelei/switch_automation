import json
import time
import requests
import urllib3
import base64
import pprint
from netmiko import ConnectHandler

def get_vlan(baseurl, cookie):
    """
    Get all VLANs in switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: Return all vlans in json format
    """
    url = baseurl + 'vlans'
    headers = {'cookie': cookie}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
import json
import time
import requests
import urllib3
import base64
import pprint
from netmiko import ConnectHandler

def get_vlan_ports(baseurl, cookie):
    target_url = baseurl + 'vlans-ports'
    headers = cookie
    r = requests.get(target_url, verify=False, headers=headers)
    if r.ok:
        return r.json()['vlan_port_element']
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")

def post_vlan_port(vlan_id: int, port_id: str, cookie, baseurl, mode: str = 'POM_TAGGED_STATIC'):
    target_url = baseurl + 'vlans-ports'
    headers = cookie
    data = {
        'vlan_id': vlan_id,
        'port_id': port_id,
        'port_mode': mode
    }
    r = requests.post(target_url, data=json.dumps(data), verify=False, headers=headers)
    if r.ok:
        print("Vlan ajouté")
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")

def put_vlan_port(vlan_id: int, port_id: str, cookie, mode: str = 'POM_TAGGED_STATIC'):
    target_url = baseurl + 'vlans-ports'
    headers = cookie
    data = {
        'vlan_id': vlan_id,
        'port_id': port_id,
        'port_mode': mode
    }
    r = requests.put(target_url, data=json.dumps(data), verify=False, headers=headers)
    print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")

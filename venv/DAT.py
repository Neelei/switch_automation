import json
import time
import requests
import urllib3
import base64
from pprint import pprint

from loginOS import login_os, logout
from vlan import get_vlan
from vlan_ports import get_vlan_ports, post_vlan_port, put_vlan_port


urllib3.disable_warnings()

credentials = {
    "username":"admin",
    "password":"automationsquad",
        }
### Construction de l'URL pour chaque switch
baseurl = f'http://172.16.3.253/rest/v7/'
cookie = login_os(credentials,baseurl)
time.sleep(1)
vlans = get_vlan(baseurl,cookie)
print(vlans)
#logout(baseurl,cookie)
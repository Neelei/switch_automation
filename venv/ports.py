import json
import time
import requests
import urllib3
import base64
import pprint
from netmiko import ConnectHandler

def name_ports(baseurl, cookie, port_id, portname):
    """
    Change port names to a given value
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param portname: data imported from yaml file
    :return: Print status of port name update success/failure on screen
    """
    url = baseurl + 'ports/' + port_id
    headers = cookie
    response = requests.put(url, verify=False, data=json.dumps(portname), headers=headers)
    if response.status_code == 200:
        print('Changing port {} with name {} is successful'.format(port_id, portname))
    else:
        print(f'{response.text}')
        print("coucou")
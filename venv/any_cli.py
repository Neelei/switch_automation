import json
import time
import requests
import urllib3
import base64
import pprint
from netmiko import ConnectHandler
urllib3.disable_warnings()

def any_cli(baseurl, cookie, command):
    headers = {'cookie': cookie}
    # commands string
    commands = command
    # commands must be bytes not a string
    command_bytes = commands.encode()
    # perform encoding to base64
    base64_command = base64.b64encode(command_bytes)
    # bytes must be decoded as a utf-8 string for the dict. It is base64 but as a unicode string
    command_dict = {'cli_batch_base64_encoded': base64_command.decode('utf-8')}
    post_batch = requests.post(baseurl + 'cli_batch', headers=headers, data=json.dumps(command_dict), verify=False, timeout=20)
    time.sleep(0.5)
    print(post_batch.status_code)
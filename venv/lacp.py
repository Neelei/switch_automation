import json
import time
import requests

def get_lacp_port(baseurl: str, cookie: str):
    """
    Get LACP ports on switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: retun all LACP ports configured on the switch
    """
    url = baseurl + 'lacp/port'
    headers = cookie
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
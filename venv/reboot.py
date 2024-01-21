import json
import time
import requests
import urllib3
import base64
import pprint
from any_cli import any_cli
from netmiko import ConnectHandler

# def reboot(url, partition, cookie):
#     headers = {'cookie': cookie}
#     url_reboot = url + "system/reboot"
#     data = { "boot_image": partition }
#     reponse = requests.post(url_reboot, headers=headers, data=data, verify=False,timeout=100)
#     print (reponse.status_code)
#



def reboot(url, boot_image, cookie):
    headers = {
        'cookie': cookie,
        'Content-Type': 'application/json'  # Assurez-vous d'envoyer les données au format JSON
    }
    url_reboot = url + "system/reboot"
    data = {"boot_image": boot_image}  # Utilisez soit 'BI_PRIMARY_IMAGE', soit 'BI_SECONDARY_IMAGE'

    # Conversion de l'objet data en JSON
    response = requests.post(url_reboot, headers=headers, json=data, verify=False, timeout=100)

    print(response.status_code)
    print(response.text)  # Afficher le corps de la réponse pour obtenir plus d'informations en cas d'erreur




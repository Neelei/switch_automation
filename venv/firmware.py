import json
import time
import requests
import urllib3
import base64
import pprint
from any_cli import any_cli
from netmiko import ConnectHandler


def transferState(ip, cookie):
    url_file = f'http://{ip}/rest/v7/file-transfer'
    headers = {'cookie': cookie}
    r = requests.get(url_file, headers=headers, verify=False,timeout=100)
    print(r.status_code)
def update_firmware(ip, ipclient, nom_fichier, cookie):
    """
    Fonction pour mettre à jour le firmware

    :param ip: Adresse IP de l'appareil.
    :param cookie: Cookie pour l'authentification.
    """
    # URI pour le transfert de fichier
    url_file = f'http://{ip}/rest/v7/file-transfer'
    # Cette requete veut un dictionnaire
    headers = {'cookie': cookie}

    # Dictionnaire avec les informations de mise à jour
    data = {
        "file_type": "FTT_FIRMWARE",
        "url": f"http://{ipclient}:50000/firmware/{nom_fichier}",
        "action": "FTA_DOWNLOAD",
        "boot_image": "BI_PRIMARY_IMAGE"
    }
    if not isinstance(headers, dict):
        raise ValueError("Le paramètre 'cookie' doit être un dictionnaire")
    # Envoi de la requête de mise à jour
    post_file = requests.post(url_file, data=json.dumps(data), headers=headers, verify=False,timeout=100)

    if post_file.status_code == 202:
        print("Mise à jour du firmware réussie.")
        # command = f'boot system flash primary'
        # any_cli()
    else:
        print(f"Erreur lors de la mise à jour du firmware: {post_file.status_code}")
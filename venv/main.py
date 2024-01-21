import json
import os
import time
import requests
import urllib3
import base64
from pprint import pprint
from lacp import get_lacp_port
from loginOS import login_os, delete_sessions, logout
from vlan import get_vlan
from vlan_ports import get_vlan_ports, post_vlan_port, put_vlan_port
from firmware import update_firmware, transferState
from ports import *
from any_cli import any_cli
from reboot import reboot
from netmiko import ConnectHandler
urllib3.disable_warnings()

### Faire une liste des fichiers de config qui fini par "json"
config_files = [f for f in os.listdir('data') if f.endswith('.json')]

for config_file in config_files:
    config_path = os.path.join('data', config_file)
    ### Ouverture fichie JSON contenant les data récupérés de l'interface WEB
    with open(config_path, 'r') as jsonfile:
        data = json.load(jsonfile)

        dict_netmiko = {
            'device_type': 'aruba_osswitch',
            'ip': data["ip"],
            'username': data["username"],
            'password': data["password"],
                        }
    ### Construction de l'URL pour chaque switch
    baseurl = f'https://{data["ip"]}/rest/v7/'
    ### Recuperation du cookie pour les call API
    ### TEST API EN HTTPS
    try:
        cookie = login_os(data,baseurl)
        #cookie = 'sbFKoYAVOSZ89dppdRyYaWS32JZV4TsIrJyDYaSqegX6Ic6tk0RlJyk9PeOnVX6'
    ### SINON API HTTP ET ACTIVATION HTTPS EN NETMIKO
    except requests.exceptions.ConnectionError:
        print("HTTPS connection failed. Trying HTTP...")
        baseurl = f'http://{data["ip"]}/rest/v7/'
        cookie = login_os(data, baseurl)
        ### ACTIVATION HTTPS
        net_connect = ConnectHandler(**dict_netmiko)
        net_connect.send_config_set('crypto pki identity-profile gna subject common-name SW-PAL-CORE country fr locality fr org MD org-unit MD state FR')
        net_connect.send_config_set('crypto pki enroll-self-signed certificate-name certificate')
        net_connect.send_config_set('web-management ssl')
        baseurl = f'http://{data["ip"]}/rest/v7/'
        print(baseurl)


    ### DISABLE TELNET
    command = 'no telnet-server'
    print("DISABLE TELNET")
    print(any_cli(baseurl,cookie,command))
    ### TIMEOUT SESSION SSH/CONSOLE
    command = 'console idle-timeout 120'
    print("TIMEOUT SESSION 120")
    any_cli(baseurl,cookie,command)
    #
    # ### AFFECTATION HOSTNAME
    command = f'hostname {data["switch_name"]}'
    print(f'HOSTNAME {data["switch_name"]}')
    any_cli(baseurl, cookie, command)
    #
    # ### AFFECTATION DOMAIN
    command = f'ip dns domain-name {data["domain"]}'
    print(f'DOMAIN {data["domain"]}')
    any_cli(baseurl, cookie, command)
    # ### AFFECTATION DNS1
    command = f'ip dns server-address priority 1 {data["dns1"]}'
    print(f'DNS1 : {data["dns1"]}')
    any_cli(baseurl, cookie, command)
    # ### AFFECTATION DNS2
    command = f'ip dns server-address priority 2 {data["dns2"]}'
    print(f'DNS1 : {data["dns2"]}')
    any_cli(baseurl, cookie, command)

    ### AFFECTATION NTP
    print("Config NTP")
    command = f'time daylight-time-rule western-europe\ntime timezone 60\ntimesync ntp\nntp enable\nntp unicast\nntp server {data["ntp"]} iburst\n'
    any_cli(baseurl, cookie, command)

    ### COMMUNITY SNMP
    #command = f'snmp-server community {data=["snmp"]}'
    #print(f'Config SNMP : {data["snmp"]}')
    #any_cli(baseurl, cookie, command)

    # ### Disable HTTP
    command = 'no web-management plaintext'
    print(f'Disable HTTP')
    any_cli(baseurl, cookie, command)
    #
    # ### DISABLE TELNET
    command = 'no telnet-server'
    print(f'Disable TELNET')
    any_cli(baseurl, cookie, command)
    #
    ### ACTIVATION SPENNING TREE (MSTP)
    command = 'spanning-tree enable'
    print(f'Activation spanning tree MSTP')
    any_cli(baseurl, cookie, command)

    ### GENERATION KEY SSH 2048 BITS
    command = 'crypto key generate ssh rsa bits 2048\nip ssh\nip ssh timeout 60\nip ssh filetransfer'
    print(f'Generate key 2048 bits')
    any_cli(baseurl, cookie, command)

    ### PASSWORD COMPLEXITY
    command = 'password complexity all\npassword minimum-length 20\password non-plaintext-sha256\npassword composition lowercase 2\npassword composition uppercase 2\npassword composition number 2\npassword composition specialcharacter 2\n'
    print(f'Password complexity')
    any_cli(baseurl, cookie, command)

    ### CREATION VLANS
    for vlan in data["vlans"]:
        print(int(vlan["vlan_id"]), vlan["name"])
        command = f'vlan {int(vlan["vlan_id"])}\nname {vlan["name"]}'
        any_cli(baseurl,cookie,command)

    ### AFFECTATION PORTS AUX VLANS
    liste_formatee = []
    for port in data["ports"]:
        print("interface ",port["port_id"])
        print(f'name : {port["port_name"]}')
        print("untagged vlan ",port["vlan_untagged"])
        # Convertir chaque élément de la liste "vlans_tagged" en chaîne de caractères et les joindre
        list_vlans_tagged = ','.join(str(element) for element in port["vlans"])
        print("tagged vlan ",list_vlans_tagged)
        command = f'interface {port["port_id"]}\nname {port["port_name"]}\nuntagged vlan {port["vlan_untagged"]}\ntagged vlan {list_vlans_tagged}'
        any_cli(baseurl, cookie, command)


    ### AFFECTATION TRUNKS AUX VLANS
    list_vlans_tagged = []
    for aggregate in data["aggregates"]:
        list_port_aggregate = ','.join(str(element) for element in aggregate["aggregat_ports"])
        print(f'trunk {list_port_aggregate} {aggregate["aggregat_name"]} lacp')
        print(f'interface {aggregate["aggregat_name"]}')
        # Convertir chaque élément de la liste "vlans_tagged" en chaîne de caractères et les joindre
        list_vlans_tagged = ','.join(str(element) for element in aggregate["vlans_tagged"])
        print("tagged vlan ",list_vlans_tagged)
        command = f'trunk {list_port_aggregate} {aggregate["aggregat_name"]} lacp\ninterface {aggregate["aggregat_name"]}\ntagged vlan {list_vlans_tagged}\n'
        time.sleep(2)
        any_cli(baseurl, cookie, command)



    # Si un fichier est choisi on applique l'update firmware
    if data["nomfichier"]:
        update_firmware(data["ip"], data["ip-client"], data["nomfichier"], cookie)
        time.sleep(20)
        reboot(baseurl,"BI_PRIMARY_IMAGE",cookie)
    else:
        delete_sessions(baseurl, cookie)




    # #
    # time.sleep(1)
    #logout(baseurl, cookie)
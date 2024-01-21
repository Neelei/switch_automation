from netmiko import ConnectHandler

dict_netmiko = {
    'device_type': 'aruba_osswitch',
    'ip': '192.168.1.100',
    'username': 'admin',
    'password': 'admin',
}


net_connect = ConnectHandler(**dict_netmiko)

net_connect.send_config_set('crypto pki identity-profile gna subject common-name SW-PAL-CORE country fr locality fr org MD org-unit MD state FR')
net_connect.send_config_set('crypto pki enroll-self-signed certificate-name certificate')
net_connect.send_config_set('web-management ssl')



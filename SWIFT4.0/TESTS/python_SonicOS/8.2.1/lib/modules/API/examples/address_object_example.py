import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print(suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + "../../"
        print(root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

from utm import Firewall
from modules.API.Address_Objects import AddressObjects

ip = '10.5.192.24'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
print(fw)
url = 'api/sonicos/address-objects/'
AddressObject = AddressObjects(fw,url)

def hostaddr():
    address_object = {
        "object_type":"host",
        "name":"drres_host",
        "zone":"LAN",
        "value":  "10.0.0.200"
    }
    rc = AddressObject.config_addressobject(url =url, **address_object)
    if rc:
        print('Config address_object success')
    else:
        print('Config weproxy fail')

def rangeaddr():
    address_object = {
        "object_type": "range",
        "name": "drres_range",
        "zone": "LAN",
        "value": "10.0.0.100,10.0.0.142"
    }
    rc = AddressObject.config_addressobject(url=url, **address_object)
    if rc:
        print('Config address_object success')
    else:
        print('Config weproxy fail')


def networkaddr():
    address_object = {
        "object_type": "network",
        "name": "drres_network",
        "zone": "LAN",
        "value": "192.168.0.0,255.255.0.0"
    }
    rc = AddressObject.config_addressobject(url=url, **address_object)
    if rc:
        print('Config address_object success')
    else:
        print('Config weproxy fail')


def fqdnaddr():
    address_object = {
        "object_type": "fqdn",
        "name": "fqdn",
        "zone": "LAN",
        "value": "host.com",
        "dns_ttl":120
    }
    rc = AddressObject.config_addressobject(url=url, **address_object)
    if rc:
        print('Config address_object success')
    else:
        print('Config weproxy fail')

def macaddr():
    address_object = {
        "object_type": "mac",
        "name": "mac_addr",
        "zone": "LAN",
        "value": "4C:EB:42:A5:CE:F9",
        "multi_homed":True
    }
    rc = AddressObject.config_addressobject(url=url, **address_object)
    if rc:
        print('Config address_object success')
    else:
        print('Config weproxy fail')

def ipv6addr():
    address_object = {
        "object_type": "mac",
        "name": "mac_addr",
        "zone": "LAN",
        "value": "4C:EB:42:A5:CE:F9",
        "multi_homed":True
    }
    rc = AddressObject.config_addressobject(url=url, **address_object)
    if rc:
        print('Config address_object success')
    else:
        print('Config weproxy fail')

def networkipv6addr():
    address_object = {
        "object_type": "network",
        "name": "drres_ipv6network",
        "zone": "LAN",
        "value": "2001:df5:4c00:7014:ffff:ffff:ffff:1792,255.255.255.0"
    }
    rc = AddressObject.config_addressobject(url=url, **address_object)
    if rc:
        print('Config address_object success')
    else:
        print('Config weproxy fail')


# rc = address_object.edit_bypass_upon_failure(True)
# rc = address_object.edit_bypass_upon_failure(False)
# rc = address_object.edit_forward_public_requests(True)
# rc = address_object.edit_forward_public_requests(False)
# rc = address_object.add_user_proxy_server('1.1.1.1','2.2.2.2')
# rc = address_object.del_user_proxy_server('1.1.1.1','2.2.2.2')

rangeaddr()
hostaddr()
networkaddr()
fqdnaddr()
macaddr()
networkipv6addr()

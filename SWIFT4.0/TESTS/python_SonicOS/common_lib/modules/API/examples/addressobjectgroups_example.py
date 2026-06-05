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
from modules.API.Address_Objects import *

ip = '10.5.192.24'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
print(fw)
url = 'api/sonicos/address-objects/'
url1 = '/api/sonicos/address-groups'
AddressObject = AddressObjects(fw,url)
Addressgroup = AddressGroups(fw)

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
        "value": "2001:df5:4c00:7014:ffff:ffff:ffff:1792,ffff:ffff:ffff:ffff::"
    }
    rc = AddressObject.config_addressobject(url=url, **address_object)
    if rc:
        print('Config address_object success')
    else:
        print('Config weproxy fail')




rangeaddr()
hostaddr()
networkaddr()
fqdnaddr()
macaddr()
networkipv6addr()



def ipv4addrgrp():
    address_group = {
        "ipv4": {
            "name": "Address_grpnewkk",
            "address_object": {
                "ipv4": ["IPv4_Range_LAN"]
            },
            # "mac": None,
            # "fqdn":None,
            "address_group": {
               "ipv4": None
            }
        }
    }

    rc = Addressgroup.config_addressgroup(url=url1, group_type = "ipv4", **address_group)
    if rc:
        print('Config address_object success')
    else:
        print('Config address_object fail')
    resp = Addressgroup.get_addressgroup(group_type="ipv4", group_path="name", group_name_uuid="Address_grpnewkk")
    print(resp)
    # resp1 = Addressgroup.delete_addressgroup(group_type ="ipv4", group_path="name", group_name_uuid="Address_grpnew")
    # print(resp1)

def ipv4putaddrgrp():
        # address_group = {
        #     "ipv4": {
        #         "name": "Address_grpnew",
        #         "address_object": {
        #             "ipv4": ["IPv4_Range_LAN"]
        #         },
        #         "address_group": {
        #             "ipv4": None
        #         }
        #     }
        # }
        address_group = {
            "ipv4": {
                "name": "Address_grpnewkk1",
                "address_object": {
                    "ipv4": ["IPv4_Range_LAN", "IPv4_Host"]

                },
                # "mac": None,
                # "fqdn": None,
                "address_group": {
                    "ipv4": None
                }
            }
        }
        rc = Addressgroup.config_addressgroup(url=url1, group_type="ipv4", **address_group)
        if rc:
            print('Config address_object success')
        else:
            print('Config address_object fail')
        resp = Addressgroup.get_addressgroup(group_type="ipv4", group_path="name", group_name_uuid="Address_grpnewkk")
        print(resp)
        # resp1 = Addressgroup.put_addressgroup(group_type="ipv4", group_path="name", group_name_uuid="Address_grpnew2", **address_group)
        # print(resp1)

def ipv6addrgrp():
    address_group = {
        "ipv6": {
            "name": "Address_grpggnew",
            "address_object": {
                "ipv6": ["kk"]
            },
            "address_group": {
               "ipv6": ["Address_group2"]
            }
        }
    }

    rc = Addressgroup.config_addressgroup(url=url1, group_type = "ipv6", **address_group)
    if rc:
        print('Config address_object success')
    else:
        print('Config address_object fail')

def macputaddrgrp():
        # address_group = {
        #     "ipv4": {
        #         "name": "Address_grpnew",
        #         "address_object": {
        #             "ipv4": ["IPv4_Range_LAN"]
        #         },
        #         "address_group": {
        #             "ipv4": None
        #         }
        #     }
        # }
        address_group = {
            "ipv6": {
                "name": "Address_mac2",
                "address_object": {
                    "mac": ["mac_addr_object"],


                },
                "address_group": {
                    "ipv6": None
                }
            }
        }
        rc = Addressgroup.config_addressgroup(url=url1, group_type="ipv6", mac_fqdn_type ="mac" ,**address_group)
        if rc:
            print('Config address_object success')
        else:
            print('Config address_object fail')
        resp = Addressgroup.get_addressgroup(group_type="ipv6", group_path="name", group_name_uuid="Address_mac2")
        print(resp)
        # resp1 = Addressgroup.put_addressgroup(group_type="ipv4", group_path="name", group_name_uuid="Address_grpnew2",
        #                                       **address_group)
        # print(resp1)


def fqdnaddrgrp():
    # address_group = {
    #     "ipv4": {
    #         "name": "Address_grpnew",
    #         "address_object": {
    #             "ipv4": ["IPv4_Range_LAN"]
    #         },
    #         "address_group": {
    #             "ipv4": None
    #         }
    #     }
    # }
    address_group = {
        "ipv6": {
            "name": "Address_fqdn2",
            "address_object": {
                "fqdn": ["fqdn"],

            },
            "address_group": {
                "ipv6": None
            }
        }
    }
    rc = Addressgroup.config_addressgroup(url=url1, group_type="ipv6", mac_fqdn_type ="fqdn",**address_group)
    if rc:
        print('Config address_object success')
    else:
        print('Config address_object fail')
    resp = Addressgroup.get_addressgroup(group_type="ipv6", group_path="name", group_name_uuid="Address_fqdn2")
    print(resp)
    # resp1 = Addressgroup.put_addressgroup(group_type="ipv4", group_path="name", group_name_uuid="Address_grpnew2",
    #                                       **address_group)
    # print(resp1)
#macputaddrgrp()
#fqdnaddrgrp()
# ipv6addrgrp()
ipv4addrgrp()
ipv4putaddrgrp()

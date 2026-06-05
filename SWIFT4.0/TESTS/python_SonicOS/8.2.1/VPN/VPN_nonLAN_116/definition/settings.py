from inspect import Parameter
import sys
import os
import re
import time
import copy
import socket

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/VPN_nonLAN_116')

from collections import OrderedDict
import re
import paramunittest
from nose_parameterized import parameterized
from bin.global_settings import *

from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall,FirewallAPI
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network
from lib.modules.API import object
from lib.modules.API import log
from lib.modules.API import vpn
from lib.modules.API import system
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from tools.trafficGen import  MyFtp

OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
fw_api = FirewallAPI(Parameter.DUT)
Linterface = network.InterfaceIPv4Api(fw)
Rinterface = network.InterfaceIPv4Api(rt)
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
RTimeObj = system.TimeApi(rt)
LRestartObj = system.RestartApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
Lzone_obj = network.ZoneObjectsApi(fw)
Rzone_obj = network.ZoneObjectsApi(rt)
Laccess_rule_obj = firewall.AccessRuleApi(fw)

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_nonLAN_116/testplan/VPN_nonLAN_116.json'
suite_path = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_nonLAN_116'

# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
PC3 = Host(Params.testbed + '-PC3')
PC4 = Host(Params.testbed + '-PC4')
PC5 = Host(Params.testbed + '-PC5')
PCSWAN1 = Host(Params.testbed + '-PCSWAN1')
PCSWAN2 = Host(Params.testbed + '-PCSWAN2')
PC1_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
PC3_IP = OpenS.get_node_interface_ip('PC3', 'eth1')
PC4_IP = OpenS.get_node_interface_ip('PC4', 'eth0')
PC4_Eth1_IP = OpenS.get_node_interface_ip('PC4', 'eth1')
PC5_IP = OpenS.get_node_interface_ip('PC5', 'eth0')
PCSWAN1_IP = OpenS.get_node_interface_ip('PCSWAN1', 'eth0')
PCSWAN1_Eth1_IP = OpenS.get_node_interface_ip('PCSWAN1', 'eth1')
PCSWAN2_IP = OpenS.get_node_interface_ip('PCSWAN2', 'eth0')
PC4_Net = OpenS.get_node_interface_network('PC4', 'eth0')
PCSWAN1_Net = OpenS.get_node_interface_network('PCSWAN1', 'eth0')
PCSWAN2_Net = OpenS.get_node_interface_network('PCSWAN2', 'eth0')


# define ip
ppp_server = "12.12.1.100"
ppp_ip = Parameter.REMOTEX1
local_wan_pppoe = "12.1.1.2"
eth_ip = "12.1.1.1"
trans_ip = '12.12.1.5'

#cmds
show_cmds = ['show certificates status imported']

# DUT local and remote object
Rlocal = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
LDMZ = {
    'name': 'remote_dmz',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTEX3NET),
}
#RemoteDUT local and remote object
RDMZ = {
    'name': 'local_dmz',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.DUTX3NET),
}
lCustomObj = {
    'name': 'remote_custom',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(PCSWAN2_Net),
}
RCustomObj = {
    'name': 'local_custom',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(PCSWAN1_Net),
}

lTransObj = {
    'name': 'remote_trans',
    'zone': 'VPN',
    'object_type': 'range',
    'value': '12.12.1.4,12.12.1.10',
}
rTransObj = {
    'name': 'remote_trans',
    'zone': 'LAN',
    'object_type': 'range',
    'value': '12.12.1.4,12.12.1.10',
}
local_grp1 ={ 
    'address_groups': [{'ipv4':
    {"name":"local_gp",
    "address_group":{"ipv4":
        [{'name':"Custom Subnets"},
        {'name':"DMZ Subnets"}]},
    },
}]}
local_grp2 = { 
    'address_groups': [{'ipv4':
    {"name":"local_gp2",
    "address_object":{"ipv4":
    [{'name':"remote_custom"},
    {'name':"remote_dmz"}]},
    },
}]}
remote_grp1 =  { 
    'address_groups': [{'ipv4':
    {"name":"remote_gp",
    "address_object":{"ipv4":
    [{'name':"local_custom"},
    {'name':"local_dmz"}]},
    }
}]}
remote_grp2 = { 
    'address_groups': [{'ipv4':
    {"name":"remote_gp2",
    "address_group":{"ipv4":[
        {'name':"Custom Subnets"},
        {'name':"DMZ Subnets"}]},
    }   
}]}
ZONEREF = {"zones":
[{
    "name":"Custom",
    "security_type":"trusted",
}]}

Lx3 = {
        'if': 'X3',
        'zone': 'DMZ',
        'mode': 'static',
        'ip': Parameter.DUTX3,
        'netmask': '255.255.255.0',
        'gateway': Parameter.WANGW,
        'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
Rx3 = {
        'if': 'X3',
        'zone': 'DMZ',
        'mode': 'static',
        'ip': Parameter.REMOTEX3,
        'netmask': '255.255.255.0',
        'gateway': Parameter.WANGW,
        'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
Lx4 = {
    'if': 'X4',
        'zone': 'Custom',
        'mode': 'static',
        'ip': '192.168.172.168',
        'netmask': '255.255.255.0',
        'gateway': Parameter.WANGW,
        'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
}
Rx4 = {
    'if': 'X4',
        'zone': 'Custom',
        'mode': 'static',
        'ip': '172.16.5.101',
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
}

renego_obj = {
    'local_net':Parameter.DUTX3NET,
    'local_mask':'255.255.255.0',
    'remote_net':Parameter.REMOTENET,
    'remote_mask':'255.255.255.0',
    'remote_gw' :Parameter.REMOTEX1,
    'new_renegotiate':True
}

# VPN policy
#########################################
#                Notice!                #
#          Key:"_"      Value:"-"       #
#       site_to_site & site-to-site     #
#         triple_des & triple-des       #
#########################################

Lvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn',
    'enable'            : True,
    'auth_mode'         : "certificate",
    'pri_gate'          : Parameter.REMOTEX1,
    'local_cert'        : 'my_cert',
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : "/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO",
    'local_net_type'    : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_type'   : 'name',
    'remote_net_name'   : 'remote_net',
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'triple-des',
    'ike_auth'          : 'sha-1',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'triple_des',
    'ipsec_auth'        : 'sha_1',
    'ipsec_lifetime'    : '28800',
}
Rvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn',
    'enable'            : True,
    'auth_mode'         : "certificate",
    'pri_gate'          : Parameter.WANIP,
    'local_cert'        : 'my_cert',
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : "/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO",
    'local_net_type'    : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_type'   : 'name',
    'remote_net_name'   : 'remote_net',
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'triple-des',
    'ike_auth'          : 'sha-1',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'triple_des',
    'ipsec_auth'        : 'sha_1',
    'ipsec_lifetime'    : '28800',
}
signreq = {
    "certificates": {
        "generate_signing_request": [{
            "signature_algorithm": "sha-1",
            "key": {
                "type": "rsa",
                "size": "1024"
            },
            "generate": True,
            "alias": "my_cert",
            "distinguished_name": {
                "element1": {
                    "country": "CHINA"
                },
                "element2": {
                    "state": "SH"
                },
                "element3": {
                    "locality": "ShangHai"
                },
                "element4": {
                    "organization": "SNWL"
                },
                "element5": {
                    "department": "AUTO"
                },
                "element6": {
                    "group": "AUTO"
                },
                "element7": {
                    "team": "AUTO"
                },
                "element8": {
                    "common_name": "AUTO"
                }
            }
        }]
    }
}




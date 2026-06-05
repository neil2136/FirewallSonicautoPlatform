from inspect import Parameter
import sys
import os
import re
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/VPN_Tunnel_Statistics')

from collections import OrderedDict
import re
import paramunittest
from nose_parameterized import parameterized
from bin.global_settings import *

from runner.settings import logger, Params
from runner.unittest.setup import Test,repeat_method
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
from bin import Gen_Local_Cert


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
fw_api = FirewallAPI(Parameter.DUT)
interface = network.InterfaceIPv4Api(fw)
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

#show cert cmds
show_cmds = ['show certificates status imported']

# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC1_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
PC2 = Host(Params.testbed + '-PC2')
# /DEV_TESTS/python_SonicOS/7.0.1/VPN/VPN_Tunnel_Statistics/testplan/VPN_Tunnel_Statistics.json
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_Tunnel_Statistics/testplan/VPN_Tunnel_Statistics.json'
common_cert_path = os.environ["PYTHON_COMMON_HOME"] + '/util/vpn_cert'
ca_cert = common_cert_path + '/rootca.pem'
local_cert = common_cert_path + '/my_cert.pfx'
#ca_cert = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_Tunnel_Statistics/cert/rootca.pem'
#local_cert =os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_Tunnel_Statistics/cert/my_cert.pfx'
# DUT local and remote object
local_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
#RemoteDUT local and remote object
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
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




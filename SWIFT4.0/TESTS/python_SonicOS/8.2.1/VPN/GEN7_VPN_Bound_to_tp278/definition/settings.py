from inspect import Parameter
import sys
import os
import re
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/GEN7_VPN_Bound_to_tp278')

import paramunittest
from nose_parameterized import parameterized
from bin.global_settings import *
from runner.settings import logger, Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from utm import Firewall
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
PC1_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
PC2 = Host(Params.testbed + '-PC2')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/GEN7_VPN_Bound_to_tp278/testplan/VPN_Bound_to.json'
ca_cert = os.environ['PYTHON_COMMON_HOME']+'/util/vpn_cert/rootca.pem'
local_cert =os.environ['PYTHON_COMMON_HOME']+'/util/vpn_cert/my_cert.pfx'

# DUT local and remote object
local_l = {
    'name': 'local_net',
    'zone': 'LAN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
}
local_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
#RemoteDUT local and remote object
remote_l = {
    'name': 'local_net',
    'zone': 'LAN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
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

def get_vpn_policy_optionals(port,mode):
    if mode == 'MAIN' :
        ike_exchange = 'main'
        auth_mode = 'shared_secret'
    elif mode == 'AGGRESSIVE':
        ike_exchange = 'aggressive'
        auth_mode = 'shared_secret'
    elif mode == 'MANUAL':
        ike_exchange = 'main'
        auth_mode = 'manual'
    elif mode == 'THIRD':
        ike_exchange = 'main'
        auth_mode = 'certificate'

    if port == '1':
        bound_to = 'X1'
        wan_ip = Parameter.WANIP
        remote_ip = Parameter.REMOTEX1
    elif port == '2':
        bound_to = 'X2'
        wan_ip = Parameter.DUTX2
        remote_ip = Parameter.REMOTEX2

    if auth_mode == 'certificate':
        Lvpn = {
            'type'              : 'site_to_site',
            'name'              : 'vpn',
            'enable'            : True,
            'auth_mode'         : auth_mode,
            'pri_gate'          : remote_ip,
            'local_cert'        : 'my_cert',
            'local_ike_type'    : 'distinguished-name',
            'peer_ike_type'     : 'distinguished_name',
            'peer_ike_id'       : "/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO",
            'local_net_type'    : 'name',
            'local_net_name'    : 'local_net',
            'remote_net_type'   : 'name',
            'remote_net_name'   : 'remote_net',
            'ike_exchange'      : ike_exchange,
            'ike_encryption'    : 'triple-des',
            'ike_auth'          : 'sha-1',
            'ike_lifetime'      : '28800',
            'ipsec_encryption'  : 'triple_des',
            'ipsec_auth'        : 'sha_1',
            'ipsec_lifetime'    : '28800',
            'bound_to'          :["interface", bound_to],
        }
        Rvpn = {
            'type'              : 'site_to_site',
            'name'              : 'vpn',
            'enable'            : True,
            'auth_mode'         : auth_mode,
            'pri_gate'          : wan_ip,
            'local_cert'        : 'my_cert',
            'local_ike_type'    : 'distinguished-name',
            'peer_ike_type'     : 'distinguished_name',
            'peer_ike_id'       : "/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO",
            'local_net_type'    : 'name',
            'local_net_name'    : 'local_net',
            'remote_net_type'   : 'name',
            'remote_net_name'   : 'remote_net',
            'ike_exchange'      : ike_exchange,
            'ike_encryption'    : 'triple-des',
            'ike_auth'          : 'sha-1',
            'ike_lifetime'      : '28800',
            'ipsec_encryption'  : 'triple_des',
            'ipsec_auth'        : 'sha_1',
            'ipsec_lifetime'    : '28800',
            'bound_to'          :["interface", bound_to],
        }
    else:
        
        Lvpn = {
            'type'              : 'site_to_site',
            'name'              : 'vpn',
            'enable'            : True,
            'auth_mode'         : auth_mode,      
            'pri_gate'          : remote_ip,
            'secret'            : '123456',
            'local_ike_type'    : 'ipv4',
            'peer_ike_type'     : 'ipv4',
            'local_ike_id'      : Parameter.DUT,
            'peer_ike_id'       : Parameter.REMOTEX0,
            'local_net_type'    : 'name',
            'local_net_name'    : 'local_net',
            'remote_net_type'   : 'name',
            'remote_net_name'   : 'remote_net',
            'ike_exchange'      : ike_exchange,
            'ike_lifetime'      : '28800',
            'ipsec_lifetime'    : '28800',
            'bound_to'          :["interface", bound_to],
        }
        Rvpn = {
            'type'              : 'site_to_site',
            'name'              : 'vpn',
            'enable'            : True,
            'auth_mode'         : auth_mode,
            'pri_gate'          : wan_ip,
            'secret'            : '123456',
            'local_ike_type'    : 'ipv4',
            'peer_ike_type'     : 'ipv4',
            'local_ike_id'      : Parameter.REMOTEX0,
            'peer_ike_id'       : Parameter.DUT,
            'local_net_type'    : 'name',
            'local_net_name'    : 'local_net',
            'remote_net_type'   : 'name',
            'remote_net_name'   : 'remote_net',
            'ike_exchange'      : ike_exchange,
            'ike_lifetime'      : '28800',
            'ipsec_lifetime'    : '28800',
            'bound_to'          :["interface", bound_to],
        }
        if auth_mode == 'manual':
            Lvpn['encryption_key'] = '4cd0294851dfd46e8efb271f1641f788'
            Lvpn['authentication_key'] = '7023a13a19b79295daf059a2ca00f4db3b60114c'
            Lvpn['ipsec_encryption'] = 'aes_128'
            Lvpn['ipsec_auth'] = 'sha_1'
            Lvpn['apply_nat'] = True
            Lvpn['nat_local_type'] = 'name'
            Lvpn['nat_local_name'] = 'X1 Subnet'
            Lvpn['nat_remote_type'] = 'name'
            Lvpn['nat_remote_name'] = 'remote_net'

            Rvpn['encryption_key'] = '4cd0294851dfd46e8efb271f1641f788'
            Rvpn['authentication_key'] = '7023a13a19b79295daf059a2ca00f4db3b60114c'
            Rvpn['ipsec_encryption'] = 'aes_128'
            Rvpn['ipsec_auth'] = 'sha_1'
            Rvpn['apply_nat'] = True
            Rvpn['nat_local_type'] = 'name'
            Rvpn['nat_local_name'] = 'X1 Subnet'
            Rvpn['nat_remote_type'] = 'name'
            Rvpn['nat_remote_name'] = 'local_net'

    return Lvpn, Rvpn


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




import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/SuiteB_VPN_Support')

from inspect import Parameter
import paramunittest
from nose_parameterized import parameterized
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
from lib.modules.CLI.system import DiagnosticsCli


from bin import Gen_Local_Cert
from bin.global_settings import *


OpenS  = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
RTimeObj = system.TimeApi(rt)
LRestartObj = system.RestartApi(fw)
tsr_obj = system.DiagnosticApi(fw)
setting_obj = system.SettingApi(fw)

LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LRoutePolicyObj = network.RoutePolicyApi(fw)
RRoutePolicyObj = network.RoutePolicyApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)

# PC SSH
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')

ts_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/SuiteB_VPN_Support'
TESTPLAN = ts_path + '/testplan/SuiteB_VPN_Support.json'
ca_cert = ts_path + '/cert/rootca.pem'
local_cert = ts_path + '/cert/my_cert.pfx'
ecdsa_cert = ts_path + '/cert/ecdsa.pfx'
ocsp_cert = ts_path + '/cert/ocsp.pfx'


# DUT object
remote_l = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
#RemoteDUT object
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

Lvpn_3rd = {
    'type'              : 'site_to_site',  # site-to-site, tunnel_interface
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'certificate',  # certificate or shared-secret
    'local_cert'        : 'my_cert',  # add local cert
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_net_type'    : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_type'   : 'name',
    'remote_net_name'   : 'remote_net',
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
}

Rvpn_3rd = {
    'type'              : 'site_to_site',  # site-to-site, tunnel_interface
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'certificate',  # certificate or shared-secret
    'local_cert'        : 'my_cert',  # add local cert
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate'          : Parameter.WANIP,
    'local_net_type'    : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_type'   : 'name',
    'remote_net_name'   : remote_r['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
}

Lvpn_presh = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    # 'local_ike_id'      : Parameter.DUT,
    # 'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
} 

Rvpn_presh = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    # 'local_ike_id'      : Parameter.REMOTEX0,
    # 'peer_ike_id'       : Parameter.DUT,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],
}

Lvpn_manu = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'manual',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    # 'local_ike_id'      : Parameter.DUT,
    # 'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'in_spi': '0xa5ce265b',       ###  3-8 bit Hexa characters
    'out_spi': '0xed2fed7a',      ###  3-8 bit Hexa characters
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
} 

Rvpn_manu = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'manual',
    'pri_gate'          : Parameter.WANIP,
    # 'local_ike_type'    : 'ipv4',
    # 'peer_ike_type'     : 'ipv4',
    # 'local_ike_id'      : Parameter.REMOTEX0,
    # 'peer_ike_id'       : Parameter.DUT,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'in_spi': '0xed2fed7a',       ###  3-8 bit Hexa characters
    'out_spi': '0xa5ce265b',      ###  3-8 bit Hexa characters
    
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],

}

Lvpn_TI_presh = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}

Rvpn_TI_presh = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}

Lvpn_TI_3rd = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'certificate',  # certificate or shared-secret
    'local_cert'        : 'my_cert',  # add local cert
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate'          : Parameter.REMOTEX1,
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}

Rvpn_TI_3rd = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'certificate',  # certificate or shared-secret
    'local_cert'        : 'my_cert',  # add local cert
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate'          : Parameter.WANIP,
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
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

route_policy1 = [
    'config',
    'route-policy ipv4 interface vpn1 metric 1 source name X0\ Subnet destination name remote_net',
    'name ti_route1',
    'auto-add-access-rules',
    'commit',
    'exit',
    'exit',
]

route_policy2 = [
    'config',
    'route-policy ipv4 interface vpn2 metric 2 source name X0\ Subnet destination name remote_net',
    'name ti_route2',
    'auto-add-access-rules',
    'commit',
    'exit',
    'exit',
]

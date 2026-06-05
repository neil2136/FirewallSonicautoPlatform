import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/VPN_3rd_certification_Full')
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


OpenS  = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
RTimeObj = system.TimeApi(rt)
LRestartObj = system.RestartApi(fw)
Lpacket_obj = system.PacketmonitorApi(fw)

LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LRoutePolicyObj = network.RoutePolicyApi(fw)
RRoutePolicyObj = network.RoutePolicyApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)

# PC SSH
PC1_eth0 = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')

PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')

ts_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/VPN_3rd_certification_Full'
TESTPLAN = ts_path + '/testplan/VPN_3rd_certification.json'
TESTPLAN2 = ts_path + '/testplan/VPN_3rd_certification_Full.json'
ca_cert = ts_path + '/cert/rootca.pem'
local_cert = ts_path + '/cert/my_cert.pfx'
l2_cert = ts_path + '/cert/test2.p12'
ocsp_root = ts_path + '/cert/ocsp/ocsp.root.crt'
ocsp_pfx = ts_path + '/cert/ocsp/ocsp.server.pfx'
ocsp_revk_root = ts_path + '/cert/ocsp/ocsp.intermediate.crt'
ocsp_revk_pfx = ts_path + '/cert/ocsp/ocsp.revoke.pfx'
ocsp_dn_id = 'C=CN,ST=sh,L=sh,O=val,OU=val,CN=ocsprevokecert'

local_cert1 = ts_path + '/cert/testcert/req1.pfx'
local_cert2 = ts_path + '/cert/testcert/req2.pfx'
local_cert3 = ts_path + '/cert/testcert/req3.pfx'
local_cert4 = ts_path + '/cert/testcert/req4.pfx'
local_cert5 = ts_path + '/cert/testcert/req5.pfx'


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

Lvpn = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn1',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': 'my_cert',  # add local cert
    'local_ike_type': 'distinguished-name',
    'peer_ike_type': 'distinguished_name',
    'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate': Parameter.REMOTEX1,
    'local_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_type': 'name',
    'remote_net_name': 'remote_net',
    'ike_exchange': 'main',
    'ike_encryption': 'triple-des',
    'ike_auth': 'sha-1',
    'ike_lifetime': '28800',
    'ipsec_encryption': 'triple_des',
    'ipsec_auth': 'sha_1',
    'ipsec_lifetime': '28800',
    'keep_alive': True,
    'bound_to': ['zone', 'WAN'],
}

Rvpn = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn2',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': 'my_cert',  # add local cert
    'local_ike_type': 'distinguished-name',
    'peer_ike_type': 'distinguished_name',
    'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate': Parameter.WANIP,
    'local_net_type': 'name',
    'local_net_name': Parameter.REMOTESUBNET,
    'remote_net_type': 'name',
    'remote_net_name': remote_r['name'],
    'ike_exchange': 'main',
    'ike_encryption': 'triple-des',
    'ike_auth': 'sha-1',
    'ike_lifetime': '28800',
    'ipsec_encryption': 'triple_des',
    'ipsec_auth': 'sha_1',
    'ipsec_lifetime': '28800',
    'keep_alive': True,
    'bound_to': ['zone', 'WAN'],
}

Lvpn_TI_3rd = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'certificate',  # certificate or shared-secret
    'local_cert'        : 'l2_cert',  # add local cert
    'local_ike_type'    : 'email-id',
    'peer_ike_type'     : 'email_id',
    'peer_ike_id'       : 'allen@allen.com',
    'pri_gate'          : Parameter.REMOTEX1,
    'ike_exchange'      : 'main',
    'keep_alive'        : True,
}

Rvpn_TI_3rd = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'certificate',  # certificate or shared-secret
    'local_cert'        : 'l2_cert',  # add local cert
    'local_ike_type'    : 'email-id',
    'peer_ike_type'     : 'email_id',
    'peer_ike_id'       : 'allen@allen.com',
    'pri_gate'          : Parameter.WANIP,
    'ike_exchange'      : 'main',
    'keep_alive'        : True,
}

signreq = {
    "certificates": {
        "generate_signing_request": [{
            "signature_algorithm": "sha-1",
            "key": {
                "type": "rsa",
                "size": "2048"
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


local_Tran_l = {
    'name': 'local_Tran',
    'zone': 'LAN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCTRANSNET),
}
remote_Tran_l = {
    'name': 'remote_Tran',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMTRANSNET),
}
local_Tran_r = {
    'name': 'local_Tran',
    'zone': 'LAN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMTRANSNET),
}
remote_Tran_r = {
    'name': 'remote_Tran',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCTRANSNET),
}

# Lvpn_NAT = {
#     'type'              : 'site_to_site',
#     'name'              : 'vpn1',
#     'enable'            : True,
#     'auth_mode'         : 'certificate',  # certificate or shared-secret
#     'local_cert'        : 'revokecert',  # add local cert
#     'local_ike_type'    : 'distinguished-name',
#     'peer_ike_type'     : 'distinguished_name',
#     'peer_ike_id'       : ocsp_dn_id,
#     'pri_gate'          : Parameter.REMOTEX1,
#     'local_net_type'    : 'name',
#     'remote_net_type'   : 'name',
#     'local_net_name'    : Parameter.LOCALSUBNET,
#     'remote_net_name'   : remote_l['name'],
#     'bound_to'          : ['zone', 'WAN'],
#     'keep_alive'        : True,
#     'apply_nat'         : True,
#     'nat_local_type'    : 'name',
#     'nat_local_name'    : local_Tran_l['name'],
#     'nat_remote_type'   : 'original',
# }
# Rvpn_NAT = {
#     'type'              : 'site_to_site',
#     'name'              : 'vpn2',
#     'enable'            : True,
#     'auth_mode'         : 'certificate',  # certificate or shared-secret
#     'local_cert'        : 'revokecert',  # add local cert
#     'local_ike_type'    : 'distinguished-name',
#     'peer_ike_type'     : 'distinguished_name',
#     'peer_ike_id'       : ocsp_dn_id,
#     'pri_gate'          : Parameter.WANIP,
#     'local_net_type'    : 'name',
#     'remote_net_type'   : 'name',
#     'local_net_name'    : Parameter.REMOTESUBNET,
#     'remote_net_name'   : remote_Tran_r['name'],
#     'bound_to'          : ['zone', 'WAN'],
#     'keep_alive'        : True,
# }
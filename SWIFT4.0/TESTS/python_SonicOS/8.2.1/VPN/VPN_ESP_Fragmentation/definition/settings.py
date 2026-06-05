import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/VPN_ESP_Fragmentation')

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
from lib.modules.API import system,diag
from lib.modules.CLI.vpn import VpnBaseSettingsCli


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
RTimeObj = system.TimeApi(rt)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
Ldiag_obj = system.DiagnosticApi(fw)
Lvpn_adv =  vpn.VpnAdvancedsettingApi(fw)
Rvpn_adv =  vpn.VpnAdvancedsettingApi(rt)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
Rdiag_obj = diag.DiagApi(rt)

# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
PC1_eth0 = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_ESP_Fragmentation/testplan/VPN_ESP_Fragmentation.json'
ca_cert = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_ESP_Fragmentation/cert/rootca.pem'
local_cert =os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_ESP_Fragmentation/cert/my_cert.pfx'
#show cert cmds
show_cmds = ['show certificates status imported']
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
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.DUT,
    'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
}

Rvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.REMOTEX0,
    'peer_ike_id'       : Parameter.DUT,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],

}
Lvpn_cert = {
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
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-256',
    'ike_auth'          : 'sha-1',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_1',
    'ipsec_lifetime'    : '28800',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],
}
Rvpn_cert = {
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
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-256',
    'ike_auth'          : 'sha-1',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_1',
    'ipsec_lifetime'    : '28800',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],
}

# signreq = {
#     "certificates": {
#         "generate_signing_request": [{
#             "signature_algorithm": "sha-1",
#             "key": {
#                 "type": "rsa",
#                 "size": "1024"
#             },
#             "generate": True,
#             "alias": "my_cert",
#             "distinguished_name": {
#                 "element1": {
#                     "country": "CHINA"
#                 },
#                 "element2": {
#                     "state": "SH"
#                 },
#                 "element3": {
#                     "locality": "ShangHai"
#                 },
#                 "element4": {
#                     "organization": "SNWL"
#                 },
#                 "element5": {
#                     "department": "AUTO"
#                 },
#                 "element6": {
#                     "group": "AUTO"
#                 },
#                 "element7": {
#                     "team": "AUTO"
#                 },
#                 "element8": {
#                     "common_name": "AUTO"
#                 }
#             }
#         }]
#     }
# }




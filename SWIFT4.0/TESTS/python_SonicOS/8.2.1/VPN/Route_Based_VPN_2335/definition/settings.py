import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/Route_Based_VPN_2335')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/Route_Based_VPN_2335/definition')

from inspect import Parameter
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

fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')

OpenS = Openstack(Params.testbed)
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
LRestartObj = system.RestartApi(fw)
Lsetting_obj = system.SettingApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LintfaceObj = network.InterfaceIPv4Api(fw)
RintfaceObj = network.InterfaceIPv4Api(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LRoutePolicyObj = network.RoutePolicyApi(fw)
RRoutePolicyObj = network.RoutePolicyApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
LAdv_obj = vpn.VpnAdvancedsettingApi(fw)
RAdv_obj = vpn.VpnAdvancedsettingApi(rt)

# PC SSH
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Route_Based_VPN_2335/testplan/Route_Based_VPN_2335.json'
test_path = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Route_Based_VPN_2335/testcases/test.txt'

# NI IP
VPN_IF_IP_LOCAL = '1.1.1.2'
VPN_IF_IP_REMOTE = '1.1.1.1'
VPN_IF_NET = '1.1.1.0/24'
VPN_BGP_IP_LOCAL = '2.2.2.3'
VPN_BGP_IP_REMOTE = '2.2.2.5'


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
    'ipsec_encryption'  : 'aes_128',
    'keep_alive'        : True,
}
Rvpn = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_encryption'  : 'aes_128',
    'keep_alive'        : True,
}

# Tunnel_Interface = {
#             'zone'          : 'VPN',
#             'type'          : "vpn_tunnel",
#             'mode'          : 'static',
#             'ip'            : VPN_IF_IP_LOCAL,
#             'netmask'       : '255.255.255.0',
#             "tunnel_name"   : "Ni",
#             'comment'       : '',
#             "vpn_policy"    :"test",
#             'mgmt_https'    : True,
#             'mgmt_ssh'      : True,
#             'mgmt_ping'     : True,
#             'mgmt_snmp'     : True,
#             'flow_reporting': True,
#             'multicast'     : True,
#             'asymmetric_route': False,
#             'fragment_packets': True,
#             'ignore_df_bit'   :True,
#         }

# rip = {
#         'interface': 'Ni',
#         'type': 'TI',
#         'DUT':'local',
#         'mode': 'send_and_receive',
#         'receive': '2',
#         'send': '2',
#         'split_horizon': 'on',
#         'poison_reverse': 'on',
#         'password': '',
#     }

# ospf2 = {
#         'interface': 'Ni',
#         'type'     : 'TI',
#         'DUT':'local',
#         'mode': 'enable',  # enable,disable,passive
#         'dead_interval': '40',
#         'hello_interval': '10',
#         'auth': 'disable',  # disable,message diagest,simple password
#         'area': '112',
#         'area_type': 'normal',  # normal, stub area, totally stubby area, not-so-stubby area,totally stubby nssa
#         'auto': 'on',
#         'cost': '0',
#         'priority': '1',
#         'mtu': 'on',
#     }

# local_bgp_cmds = [
#     'config',
#     'routing',
#     'bgp',
#     'configure t',
#     'router bgp 2',
#     "network {}/24".format(Parameter.LOCALNET),
#     "neighbor {} remote-as 2".format(VPN_BGP_IP_REMOTE),
#     "neighbor {} update-source {}".format(VPN_BGP_IP_REMOTE,VPN_BGP_IP_LOCAL),
#     'end',
#     'exit',
#     'commit',
#     'end',
#     'exit',
# ]

# remote_bgp_cmds = [
#     'config',
#     'routing',
#     'bgp',
#     'configure t',
#     'router bgp 2',
#     "network {}/24".format(Parameter.REMOTENET),
#     "neighbor {} remote-as 2".format(VPN_BGP_IP_LOCAL),
#     "neighbor {} update-source {}".format(VPN_BGP_IP_LOCAL,VPN_BGP_IP_REMOTE),
#     'end',
#     'exit',
#     'commit',
#     'end',
#     'exit',
# ]

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

En_dpd = {
    'enable': True,
    'ike_dpd': True,
    'dpd_interval': '6',
    'dpd_trigger': '3',
    'idle_dpd': True,
    'idle_dpd_interval': '60',
}
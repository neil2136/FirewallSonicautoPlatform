import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/Fragmented_Packet_Handing')
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
from lib.modules.CLI.vpn import VpnBaseSettingsCli

OpenS = Openstack(Params.testbed)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)

VPN_Adv_obj = vpn.VpnAdvancedsettingApi(fw)
interface = network.InterfaceIPv4Api(fw)

# Rvpn_obj = vpn.VpnbasesettingApi(rt)

# PC SSH
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')
RemoteHost_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
LocalHost_IP = OpenS.get_node_interface_ip('PC1', 'eth0')


TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Fragmented_Packet_Handing/testplan/Fragmented_Packet_Handing.json'

# DUT object
local_r = {
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
    # 'local_ike_id'      : Parameter.DUT,
    # 'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : local_r['name'],
    'bound_to'          :['zone', 'WAN'],
    'keep_alive'        : True,
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
    # 'local_ike_id'      : Parameter.DUT,
    # 'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'bound_to'          :['zone', 'WAN'],
    'keep_alive'        : True,
}
# Rvpn = {
#     'type'              : 'site-to-site',
#     'name'              : 'vpn2',
#     'mode'              : 'shared-secret',
#     'secret'            : '123456',
#     'pri_gate'          : Parameter.WANIP,
#     'local_ike_id'      : 'ipv4 {}'.format(Parameter.REMOTEX0),
#     'peer_ike_id'       : 'ipv4 {}'.format(Parameter.DUT),
#     'local_net_type'    : 'name',
#     'remote_net_type'   : 'name',
#     'local_network'     : "'{}'".format(Parameter.REMOTESUBNET),
#     'remote_network'    : remote_r['name'],
#     'keep-alive'        : True,
# }

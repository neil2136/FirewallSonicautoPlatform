import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/Tunnel_All_TP16')

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
from lib.modules.API.system import PacketmonitorApi


OpenS = Openstack(Params.testbed)
LInterface_ipv4 = network.InterfaceIPv4Api(fw)
LNatPolicy_obj = network.NatpolicyApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LLogObj = log.LogMonitorApi(fw)
RLogObj = log.LogMonitorApi(rt)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
# Rvpn_obj = VpnBaseSettingsCli(rt)
Lpacket_obj = PacketmonitorApi(fw)
Rlog_set = log.LogCategoryApi(rt)


# PC SSH
PC1_eth0 = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')
PC3_eth0 = OpenS.get_node_interface_ip('PC3', 'eth0')
PC3_IP = OpenS.get_node_interface_ip('PC3', 'eth1')
PC3_login = Host(PC3_IP, user='root', password='password')


TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Tunnel_All_TP16/testplan/Tunnel_All_TP16.json'
conf_path = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Tunnel_All_TP16/bin/'

# DUT object
remote_l = {
    'name': 'remote_net',
    'zone': 'VPN',
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
Lvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_net_type'    : 'any',
    'remote_net_type'   : 'name',
    # 'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'bound_to'          : ['zone', 'WAN'],
    'ike_exchange'      : 'ikev2',
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
    'local_net_type'    : 'name',
    'remote_net_type'   : 'any',
    'local_net_name'    :  Parameter.REMOTESUBNET,
    # 'remote_net_name'   : remote_r['name'],
    'bound_to'          : ['zone', 'WAN'],
    'ike_exchange'      : 'ikev2',
}

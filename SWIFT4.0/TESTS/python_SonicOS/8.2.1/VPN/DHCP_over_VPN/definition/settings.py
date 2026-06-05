import os
import sys
import re
import time

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import firewall
from lib.modules.API.vpn import DhcpOverVpnApi
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.CLI.vpn import DhcpOverVpnCli
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.network import DhcpServerCli
from lib.modules.CLI import system
from lib.modules.API import log

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/DHCP_over_VPN')

FIREWALL = '192.168.168.168'
X0_NET = '192.168.168.0'
X1_IP = '12.12.1.200'
X1_GW = '12.12.1.1'
X1_ZONE = 'WAN'
R_X1_IP = '12.12.1.201'
R_X1_GW = X1_GW
R_X0_IP = '172.16.1.101'
R_X0_NET = '172.16.1.0'
R_X2_IP = '12.12.2.201'
R_X2_NET = '12.12.2.0'
R_X2_ZONE = 'LAN'
MASK = '255.255.255.0'
DNS1 = Params.G_DNS1
DNS2 = Params.G_DNS2
LAN_PC = '192.168.168.169'
WAN_PC = '12.12.1.169'
RELAY_IP = '192.168.168.101'
MGMT_IP = '192.168.168.201'
STATIC_IP = '192.168.168.100'
POOL_START = '192.168.168.50'
POOL_END = '192.168.168.60'
SCOPE_START = '192.168.168.20'
SCOPE_END = '192.168.168.30'
os_obj = Openstack(Params.testbed)
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/DHCP_over_VPN/testplan/DHCP_over_VPN.json'
DHCPCONF = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/DHCP_over_VPN/definition/dhcpd.conf'

ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
r_fw_api = Firewall(R_X1_IP, user='admin', password='password', supported_config_mode='api')
r_fw_cli = Firewall(R_X1_IP, user='admin', password='password', supported_config_mode='cli-ssh')

ao_api = network.AddressobjectsApi(fw_api)
ao_cli = AddressObjectCli(fw_cli)
r_ao_api = network.AddressobjectsApi(r_fw_api)
r_ao_cli = AddressObjectCli(r_fw_cli)
vpn_cli = VpnBaseSettingsCli(fw_cli)
r_vpn_cli = VpnBaseSettingsCli(r_fw_cli)
dho_vpn_api = DhcpOverVpnApi(fw_api)
r_dho_vpn_cli = DhcpOverVpnCli(r_fw_cli)
interface_api = network.InterfaceIPv4Api(fw_api)
r_interface_cli = InterfaceCli(r_fw_cli)
dhcp_svr_cli = DhcpServerCli(fw_cli)
r_dhcp_svr_cli = DhcpServerCli(r_fw_cli)
accessrule_api = firewall.AccessRuleApi(fw_api)
r_admin_cli = system.AdminCli(r_fw_cli)
LAN_HOST = Host(os_obj.get_node_interface_ip('PC1', 'eth2'))
WAN_HOST = Host(os_obj.get_node_interface_ip('PC3', 'eth1'))
RMT_HOST = Host(os_obj.get_node_interface_ip('PC2', 'eth3'))

x1_static = {
    'if': 'X1',
    'zone': X1_ZONE,
    'mode': 'static',
    'ip': X1_IP,
    'netmask': MASK,
    'gateway': X1_GW,
    'dns1': DNS1,
    'dns2': DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
r_x2_static = {
    'if': 'X2',
    'zone': R_X2_ZONE,
    'mode': 'static',
    'ip': R_X2_IP,
    'netmask': MASK,
    'mgmt-https': True,
    'mgmt-ssh': True,
    'mgmt-ping': True,
    'user_https': True,
}
remote_vpn_lan = {
    "object_type": "network",
    "name": "remote_vpn_lan",
    "zone": "VPN",
    "value": X0_NET + ',' + MASK,
}
local_vpn = {
    'type'                     : 'site-to-site',
    'name'                     : 'local_vpn',
    'mode'                     : 'shared-secret',
    'secret'                   : 'password',
    'pri_gate'                 : R_X1_IP,
    'local_ike_id'             : 'ipv4 1.1.1.1',
    'peer_ike_id'              : 'ipv4 2.2.2.2',
    'local_net_type'           : 'name',
    'remote_net_type'          : 'dhcp',
    'local_network'            : '"X0 Subnet"',
    'proposal ike exchange'    : 'main',
    'proposal ike encryption'  : 'aes-128',
    'proposal ipsec encryption': 'aes-128',
}
remote_vpn = {
    'type'                     : 'site-to-site',
    'name'                     : 'remote_vpn',
    'mode'                     : 'shared-secret',
    'secret'                   : 'password',
    'pri_gate'                 : X1_IP,
    'local_ike_id'             : 'ipv4 2.2.2.2',
    'peer_ike_id'              : 'ipv4 1.1.1.1',
    'local_net_type'           : 'dhcp',
    'remote_net_type'          : 'name',
    'remote_network'           : remote_vpn_lan['name'],
    'proposal ike exchange'    : 'main',
    'proposal ike encryption'  : 'aes-128',
    'proposal ipsec encryption': 'aes-128',
    'keep-alive'               : True,
    'management https'         : True,
}

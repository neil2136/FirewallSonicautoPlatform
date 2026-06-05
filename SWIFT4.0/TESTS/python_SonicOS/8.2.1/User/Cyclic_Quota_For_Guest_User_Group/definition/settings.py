import os
import re
import sys
import copy
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
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts
from util.enhancedinfo import show_testcase_info


sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Cyclic_Quota_For_Guest_User_Group')
from modules.API import network
from modules.API import users
from lib.modules.API import network, firewall, system, users, log
from lib.modules.API.log import LogMonitorApi
from lib.modules.API.system import AdminApi, RestartApi, DiagnosticApi,SettingApi
from modules.API import users,system
from collections import OrderedDict
from modules.API.system import TimeApi
from lib.modules.API import system as system_api
from modules.ui.fw_page import FWPage
from definition import cyclic_quota_guest_UI_helper
from lib.modules.CLI.system import LicenseCli

from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.CLI.network import ServiceCli
from lib.modules.CLI.firewall import AccessRuleCli
from lib.modules.CLI import system

FIREWALL = '192.168.168.168'
X0_NET = '192.168.168.0'
X1_IP = '12.12.1.200'
X1_GW = '12.12.1.1'
X1_ZONE = 'WAN'
X2_IP = '13.13.1.168'
X2_NET = '13.13.1.0'
X2_ZONE = 'DMZ'
R_X1_IP = '12.12.1.201'
R_X1_GW = X1_GW
R_X0_IP = '172.16.1.101'
R_X0_NET = '172.16.1.0'
MASK = '255.255.255.0'
DNS1 = '10.9.1.40'
DNS2 = '10.190.202.200'
LAN_PC = '192.168.168.169'
WAN_PC = '12.12.1.169'
DMZ_PC = '13.13.1.169'
VPN_PC = '172.16.1.169'
os_obj = Openstack(Params.testbed)
X0_LAN_MAC = ''
LAN_HOST = Host(os_obj.get_node_interface_ip('PC1', 'eth2'))
WAN_HOST = Host(os_obj.get_node_interface_ip('PC4', 'eth1'))
DMZ_HOST = Host(os_obj.get_node_interface_ip('PC3', 'eth2'))
VPN_HOST = Host(os_obj.get_node_interface_ip('PC2', 'eth2'))
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Cyclic_Quota_For_Guest_User_Group/testplan/cyclic_quota_guest_user.json'

ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='cli-ssh')
r_fw_api = Firewall(R_X1_IP, user='admin', password='S0nic@uto', supported_config_mode='api')
r_fw_cli = Firewall(R_X1_IP, user='admin', password='S0nic@uto', supported_config_mode='cli-ssh')
ui_obj = cyclic_quota_guest_UI_helper.FWPage_new(ip=ip, user ='admin', password='S0nic@uto')

guest_user = users.UserGuestApi(fw_api)
local_user = users.UserLocalApi(fw_api)
diagnostic = system_api.DiagnosticApi(fw_api)
restart_api = RestartApi(fw_api)
fw_boot = SettingApi(fw_api)
time_obj = TimeApi(fw_api)
log_obj = LogMonitorApi(fw_api)
local_host = Host('localhost')

ao_api = network.AddressobjectsApi(fw_api)
ao_cli = AddressObjectCli(fw_cli)
r_ao_api = network.AddressobjectsApi(r_fw_api)
r_ao_cli = AddressObjectCli(r_fw_cli)
vpn_cli = VpnBaseSettingsCli(fw_cli)
r_vpn_cli = VpnBaseSettingsCli(r_fw_cli)
interface_api = network.InterfaceIPv4Api(fw_api)
lc_cli = system.LicenseCli(fw_cli)
r_admin_cli = system.AdminCli(r_fw_cli)
service_cli = ServiceCli(fw_cli)

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
x2_static = {
    'if': 'X2',
    'zone': X2_ZONE,
    'mode': 'static',
    'ip': X2_IP,
    'netmask': MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
local_vpn_obj = {
    "object_type": "network",
    "name": "local_vpn",
    "zone": "VPN",
    "value": R_X0_NET + ',' + MASK,
}
remote_vpn_lan = {
    "object_type": "network",
    "name": "remote_vpn_lan",
    "zone": "VPN",
    "value": X0_NET + ',' + MASK,
}
remote_vpn_dmz = {
    "object_type": "network",
    "name": "remote_vpn_dmz",
    "zone": "VPN",
    "value": X2_NET + ',' + MASK,
}
local_group = {
    "name": "local_group",
    "version": "ipv4",
    "objects": ['ipv4 "X0 Subnet"', 'ipv4 "X2 Subnet"']
}
remote_group = {
    "name": "remote_group",
    "version": "ipv4",
    "objects": ['ipv4 ' + remote_vpn_lan['name'], 'ipv4 ' + remote_vpn_dmz['name']]
}

local_vpn = {
    'type'                     : 'site-to-site',
    'name'                     : 'local_vpn_1',
    'mode'                     : 'shared-secret',
    'secret'                   : 'password',
    'pri_gate'                 : R_X1_IP,
    'local_ike_id'             : 'ipv4 1.1.1.1',
    'peer_ike_id'              : 'ipv4 2.2.2.2',
    'local_net_type'           : 'group',
    'remote_net_type'          : 'name',
    'local_network'            : local_group['name'],
    'remote_network'           : local_vpn_obj['name'],
    'proposal ike exchange'    : 'main',
    'proposal ike encryption'  : 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'keep_alive'               : True,
}
local_lan_vpn_cmds = ['configure']
local_lan_vpn_cmds.append('vpn policy ' + local_vpn['type'] + ' ' + local_vpn['name'])
local_lan_vpn_cmds.append('network local ' + local_vpn['local_net_type'] + ' ' + local_vpn['local_network'])
local_lan_vpn_cmds.append('network remote destination-network ' + \
                          local_vpn['remote_net_type'] + ' ' + local_vpn_obj['name'])
local_lan_vpn_cmds.append('gateway primary ' + R_X1_IP)
local_lan_vpn_cmds.append('proposal ike exchange ' + local_vpn['proposal ike exchange'])
local_lan_vpn_cmds.append('proposal ike encryption ' + local_vpn['proposal ike encryption'])
local_lan_vpn_cmds.append('proposal ike authentication ' + local_vpn['proposal ike authentication'])
local_lan_vpn_cmds.append('proposal ipsec encryption ' + local_vpn['proposal ipsec encryption'])
local_lan_vpn_cmds.append('proposal ipsec authentication ' + local_vpn['proposal ipsec authentication'])
local_lan_vpn_cmds.append('auth-method ' + local_vpn['mode'])
local_lan_vpn_cmds.append('ike-id local ' + local_vpn['local_ike_id'])
local_lan_vpn_cmds.append('ike-id peer ' + local_vpn['peer_ike_id'])
local_lan_vpn_cmds.append('shared-secret ' + local_vpn['secret'])
local_lan_vpn_cmds.append('commit')
local_lan_vpn_cmds.append('end')
local_lan_vpn_cmds.append('end')

remote_vpn = {
    'type'                     : 'site-to-site',
    'name'                     : 'remote_vpn_1',
    'mode'                     : 'shared-secret',
    'secret'                   : 'password',
    'pri_gate'                 : X1_IP,
    'local_ike_id'             : 'ipv4 2.2.2.2',
    'peer_ike_id'              : 'ipv4 1.1.1.1',
    'local_net_type'           : 'name',
    'remote_net_type'          : 'group',
    'local_network'            : '"X0 Subnet"',
    'remote_network'           : remote_group['name'],
    'proposal ike exchange'    : 'main',
    'proposal ike encryption'  : 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'keep_alive'               : False,
}
remote_lan_vpn_cmds = ['configure']
remote_lan_vpn_cmds.append('vpn policy ' + remote_vpn['type'] + ' ' + remote_vpn['name'])
remote_lan_vpn_cmds.append('network local ' + remote_vpn['local_net_type'] + ' ' + remote_vpn['local_network'])
remote_lan_vpn_cmds.append('network remote destination-network ' + \
                          remote_vpn['remote_net_type'] + ' ' + remote_vpn['remote_network'])
remote_lan_vpn_cmds.append('gateway primary ' + remote_vpn['pri_gate'])
remote_lan_vpn_cmds.append('proposal ike exchange ' + remote_vpn['proposal ike exchange'])
remote_lan_vpn_cmds.append('proposal ike encryption ' + remote_vpn['proposal ike encryption'])
remote_lan_vpn_cmds.append('proposal ike authentication ' + remote_vpn['proposal ike authentication'])
remote_lan_vpn_cmds.append('proposal ipsec encryption ' + remote_vpn['proposal ipsec encryption'])
remote_lan_vpn_cmds.append('proposal ipsec authentication ' + remote_vpn['proposal ipsec authentication'])
remote_lan_vpn_cmds.append('auth-method ' + remote_vpn['mode'])
remote_lan_vpn_cmds.append('ike-id local ' + remote_vpn['local_ike_id'])
remote_lan_vpn_cmds.append('ike-id peer ' + remote_vpn['peer_ike_id'])
remote_lan_vpn_cmds.append('shared-secret ' + remote_vpn['secret'])
remote_lan_vpn_cmds.append('commit')
remote_lan_vpn_cmds.append('end')
remote_lan_vpn_cmds.append('end')



import os
import sys
import re
import time
import copy
import requests
import subprocess
import asyncio
import unittest
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
from lib.modules.API import network
from lib.modules.CLI.network import RouteCli
from lib.modules.API import system
from lib.modules.API import policy
from lib.modules.API import vpn
from lib.modules.API import object
from lib.modules.API import users
from lib.modules.API.log import LogMonitorApi
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IKE_Preshared_Keys_TP30_Part2/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
CONF_PATH = suite_path + 'definition/config'
TESTPLAN = suite_path + 'testplan/IKE_Preshared_Keys_TP30.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')
L_X2_VLAN = os_obj.get_node_interface_vlan_id('UTM', 'X2')
R_X2_VLAN = os_obj.get_node_interface_vlan_id('RemoteGEN7', 'X2')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC5_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC5_ETH1_IP: {PC5_ETH1_IP}'
            f'\n L_X2_VLAN: {L_X2_VLAN}'
            f'\n R_X2_VLAN: {R_X2_VLAN}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)
PC5_login = Host(PC5_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X3_IP = '192.168.3.168'
    X3_GW = '192.168.3.1'
    X3_SUBNET = '192.168.3.0'
    X2_VLAN_IP = '89.89.89.168'
    X2_VLAN_GW = '89.89.89.1'

    REMOTE_X0_IP = '172.16.1.101'
    REMOTE_X0_NET = '172.16.1.0'
    REMOTE_X1_IP = '12.12.1.201'
    REMOTE_X1_GW = '12.12.1.1'
    REMOTE_X1_NET = '12.12.1.0'
    REMOTE_X2_IP = '89.89.89.201'
    REMOTE_X3_IP = '12.12.3.201'
    REMOTE_X2_VLAN = '89.89.89.201'


class CaseParams:
    local_vpn_name01 = 'auto_local_s2s_01'
    local_vpn_name02 = 'auto_local_vlan_s2s'
    remote_vpn_name01 = 'auto_remote_s2s_01'
    remote_vpn_name02 = 'auto_remote_vlan_s2s'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='S0nic@uto',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='S0nic@uto',
    supported_config_mode='cli-ssh')
r_fw = Firewall(
    Parameter.REMOTE_X3_IP,
    user='admin',
    password='S0nic@uto',
    supported_config_mode='api')
r_fw_cli = Firewall(
    Parameter.REMOTE_X3_IP,
    user='admin',
    password='S0nic@uto',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)
interfaceapi = network.InterfaceIPv4Api(fw)
dynaroutingapi = network.DynamicRoutingApi(fw)
packetmonitorapi = system.PacketmonitorApi(fw)
routepolicyapi = policy.RoutePolicyApi(fw)
aoapi = network.AddressobjectsApi(fw)
routecli = RouteCli(fw_cli)
vpnapi = vpn.VpnbasesettingApi(fw)
aogroupapi = object.AddressObjectGroupApi(fw)
logapi = LogMonitorApi(fw)
accessruleapi = AccessRuleApi(fw)
userLocalapi = users.UserLocalApi(fw)
snmpapi = system.SNMPApi(fw)
statusapi = system.StatusApi(fw)


r_aogroupapi = object.AddressObjectGroupApi(r_fw)
r_vpnapi = vpn.VpnbasesettingApi(r_fw)
r_interfaceapi = network.InterfaceIPv4Api(r_fw)
r_dynaroutingapi = network.DynamicRoutingApi(r_fw)
r_routepolicyapi = policy.RoutePolicyApi(r_fw)
r_aoapi = network.AddressobjectsApi(r_fw)
r_routecli = RouteCli(r_fw_cli)

x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': PC4_ETH1_IP,
    'dns2': Parameter.X1_DNS1,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
    'mgmt-snmp': True,
}
x2_vlan_dict = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'static',
    'type': 'vlan',
    'vlan_tag': L_X2_VLAN,
    'ip': Parameter.X2_VLAN_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X2_VLAN_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True
}
r_x2_vlan_dict = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'static',
    'type': 'vlan',
    'vlan_tag': R_X2_VLAN,
    'ip': Parameter.REMOTE_X2_VLAN,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X2_VLAN_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True
}
x3_dmz_dict = {
    'if': 'X3',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}
route_base_dict = {
    "comment": "",
    "destination": {
        "name": "8.8.8.8"
    },
    "disable_on_interface_down": True,
    "distance": {
        "auto": True
    },
    "gateway": {
        "name": "X1 Default Gateway"
    },
    "interface": "X1",
    "mask": "0x00",
    "metric": 3,
    "name": "auto_lan_to_wan",
    "probe": "",
    "service": {
        "any": True
    },
    "source": {
        "any": True
    },
    "tos": "0x00",
    "type": "standard",
    "vpn_precedence": True
}
org_base_dict = copy.deepcopy(route_base_dict)
route_policy_dict = {"route_policies": [{"ipv4": route_base_dict}]}
l_s2s_vpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': CaseParams.local_vpn_name01,
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': Parameter.REMOTE_X1_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '3.3.3.3',
    'peer_ike_id': '3.3.3.3',
    'local_net_type': 'name',
    'remote_net_type': 'group',
    'local_net_name': 'X0 Subnet',
    'remote_net_group': 'vpn_ag_name01',

    'ike_exchange': 'main',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 600,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_gcm16_256',
    'ipsec_lifetime': 600,
    'ipsec_pfs': True,
    'ipsec_pfs_dhgroup': 14,
    'bound_to': ['interface', 'X1'],
    'keep_alive': False,
}
r_s2s_vpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': CaseParams.remote_vpn_name01,
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': Parameter.X1_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '3.3.3.3',
    'peer_ike_id': '3.3.3.3',
    'local_net_type': 'name',
    'remote_net_type': 'group',
    'local_net_name': 'X0 Subnet',
    'remote_net_group': 'vpn_ag_name01',

    'ike_exchange': 'main',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 600,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_gcm16_256',
    'ipsec_lifetime': 600,
    'ipsec_pfs': True,
    'ipsec_pfs_dhgroup': 14,
    'bound_to': ['interface', 'X1'],
    'keep_alive': False,
}
edit_localvpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': CaseParams.local_vpn_name01,
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': Parameter.REMOTE_X1_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '3.3.3.3',
    'peer_ike_id': '3.3.3.3',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_name': 'remote_vpn_net',

    'ike_exchange': 'aggressive',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 120,

    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_256',
    'ipsec_auth': 'sha_256',
    'ipsec_lifetime': 120,
    'bound_to': ['interface', 'X1'],
    'keep_alive': False,
}
edit_remotevpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': CaseParams.remote_vpn_name01,
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': Parameter.X1_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '3.3.3.3',
    'peer_ike_id': '3.3.3.3',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_name': 'local_vpn_net',

    'ike_exchange': 'aggressive',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 600,

    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_256',
    'ipsec_auth': 'sha_256',
    'ipsec_lifetime': 600,
    'bound_to': ['interface', 'X1'],
    'keep_alive': False,
}
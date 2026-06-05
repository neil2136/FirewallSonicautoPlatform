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
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Advanced_Routing_TP294_OSPF/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/Advanced_Routing_TP294.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')
L_X1_VLAN = os_obj.get_node_interface_vlan_id('UTM', 'X1')
R_X1_VLAN = os_obj.get_node_interface_vlan_id('RemoteGEN7', 'X1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC5_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC5_ETH1_IP: {PC5_ETH1_IP}'
            f'\n L_X1_VLAN: {L_X1_VLAN}'
            f'\n R_X1_VLAN: {R_X1_VLAN}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
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
    X2_IP = '192.168.2.168'
    X2_SUBNET = '192.168.2.0'
    X3_IP = '172.16.2.168'
    X3_GW = '172.16.2.1'
    X3_SUBNET = '172.16.2.0'
    X1_VLAN_IP = '13.13.1.168'
    X1_VLAN_GW = '13.13.1.1'

    REMOTE_X0_IP = '172.16.1.101'
    REMOTE_X0_NET = '172.16.1.0'
    REMOTE_X1_IP = '12.12.1.201'
    REMOTE_X1_GW = '12.12.1.1'
    REMOTE_X1_NET = '12.12.1.0'
    REMOTE_X2_IP = '172.16.2.201'
    REMOTE_X3_IP = '12.12.3.201'
    REMOTE_X1_VLAN = '13.13.1.201'


class CaseParams:
    interval_time = '10'
    fw_sequence = 0
    router_sequence = 0
    external_ip1 = '8.8.8.8'
    x1_sub_range = '12.12.1.200-220'
    external_network2 = '81.1.1.0'
    external_network3 = '90.1.1.0'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')
r_fw = Firewall(
    Parameter.REMOTE_X3_IP,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
r_fw_cli = Firewall(
    Parameter.REMOTE_X3_IP,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)
failoverapi = network.FailoverLbApi(fw)
interfaceapi = network.InterfaceIPv4Api(fw)
dynaroutingapi = network.DynamicRoutingApi(fw)
packetmonitorapi = system.PacketmonitorApi(fw)
routepolicyapi = policy.RoutePolicyApi(fw)
aoapi = network.AddressobjectsApi(fw)
routecli = RouteCli(fw_cli)
vpnapi = vpn.VpnbasesettingApi(fw)
aogroupapi = object.AddressObjectGroupApi(fw)

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
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
x1_vlan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'type': 'vlan',
    'vlan_tag': L_X1_VLAN,
    'ip': Parameter.X1_VLAN_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_VLAN_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True
}
r_x1_vlan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'type': 'vlan',
    'vlan_tag': L_X1_VLAN,
    'ip': Parameter.REMOTE_X1_VLAN,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_VLAN_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True
}
x2_lan_dict = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}
x3_lan_dict = {
    'if': 'X3',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}
set_rip_dict = {
    'interface': 'X3',
    'mode': 'send',
    'send': '0'
}
ospf_port_dict = {
    'interface': 'X2',
    'mode': 'enable',
    'dead_interval': '40',
    'hello_interval': '10',
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
    'name': 'auto_local_s2s_01',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': '13.13.1.201',
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
    'ike_lifetime': 120,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_gcm16_256',
    # 'ipsec_auth': 'sha-256',
    'ipsec_lifetime': 120,
    'bound_to': ['interface', f'X1:V{L_X1_VLAN}'],
    'keep_alive': True,

}
r_s2s_vpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': 'auto_remote_s2s_01',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': '13.13.1.168',
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
    'ike_lifetime': 120,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_gcm16_256',
    # 'ipsec_auth': 'sha_256',
    'ipsec_lifetime': 120,
    'bound_to': ['interface', f'X1:V{L_X1_VLAN}'],
    'keep_alive': False,

}

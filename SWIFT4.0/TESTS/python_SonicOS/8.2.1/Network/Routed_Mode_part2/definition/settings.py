import os
import re
import sys
import copy
import time
import unittest
import paramunittest
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall

# import form branch lib contents for test suit
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api, AddressobjectsApi, NatpolicyApi
from lib.modules.API.system import DiagnosticApi, AdminApi, RestartApi, StatusApi, SettingApi, PacketmonitorApi
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = (
    os.environ["PYTHON_SONICOS_HOME"] + "/Network/Routed_Mode_part2/"
)
sys.path.append(suite_path)
sys.path.append(suite_path + "testcases")
TESTPLAN = suite_path + "testplan/Routed_Mode.json"

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
consvr, conport = os_obj.get_console_info()
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC1_ETH1_NW = os_obj.get_node_interface_network('PC1', 'eth1')
PC2_ETH1_NW = os_obj.get_node_interface_network('PC2', 'eth1')
PC4_ETH1_NW = os_obj.get_node_interface_network('PC4', 'eth1')
PC3_ETH1_NW = os_obj.get_node_interface_network('PC3', 'eth1')
X4_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X4:1')
logger.info('\n' + '-' * 30 + '\n'
            + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n'
            + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n'
            + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n'
            + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n'
            + 'PC4_ETH0_IP :' + PC4_ETH0_IP + '\n'
            + 'PC4_ETH1_IP :' + PC4_ETH1_IP + '\n'
            + 'PC3_ETH0_IP :' + PC3_ETH0_IP + '\n'
            + 'PC3_ETH1_IP :' + PC3_ETH1_IP + '\n'
            + 'X4_VLAN1_ID :' + str(X4_VLAN1_ID) + '\n'
            + '-' * 30
            )
localhost = Host('localhost')
pc1_ssh = Host(PC1_ETH0_IP, user='root', password='password')
pc2_ssh = Host(PC2_ETH0_IP, user='root', password='password')
pc4_ssh = Host(PC4_ETH0_IP, user='root', password='password')
pc3_ssh = Host(PC3_ETH0_IP, user='root', password='password')

# parameters on the fw
class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X2_IP = '192.168.2.168'
    X2_GW = '192.168.2.1'
    X3_IP = '192.168.3.168'
    X3_GW = '192.168.3.1'
    X4_VLAN1_IP = '192.168.4.168'
    X4_VLAN1_GW = '192.168.4.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X0_IPv6 = '1001:1::168'
    X1_IPv6 = '2001:100::168'
    X2_IPv6 = '1001:2::168'
    PC1_ETH0 = '10.11.1.10'
    PC1_ETH1 = '192.168.168.10'
    PC2_ETH0 = '10.11.1.20'
    PC2_ETH1 = '192.168.2.20'
    PC2_ETH1_portshield = '192.168.168.20'
    PC4_ETH0 = '10.11.1.40'
    PC4_ETH1 = '12.12.1.40'
    PC3_ETH0 = '10.11.1.50'
    PC3_ETH1 = '192.168.4.5'
    lan_host1 = '1001:1::10'
    lan_host2 = '1001:2::20'
    lan_host1_if = 'eth1'
    wan_ip = '2001:100::40'
    wan_host1 = '2001:1::100'
    wan_host1_if = 'eth1'


# Instantiate objects including API,CLI import
fw = Firewall(Parameter.FIREWALL, user='admin', password='password',
              supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto',
                  supported_config_mode='cli-ssh')
license_obj = LicenseCli(fw_cli)
Status_obj = StatusApi(fw)
interface_obj = InterfaceIPv4Api(fw)
interface_obj_v6 = InterfaceIPv6Api(fw)
address_obj = AddressobjectsApi(fw)
nat_obj = NatpolicyApi(fw)
restart_obj = RestartApi(fw)
setting_obj = SettingApi(fw)
interfacecli_obj = InterfaceCli(fw_cli)
packetmonitor_obj = PacketmonitorApi(fw)
diag_obj = DiagnosticApi(fw)

# Init Settings
x0_lan_dict = {
    'if': 'X0',
    'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X0_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X0_GW,
            'routed_mode': {
                "interface": "X1"
            },
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}
x0_lan_ipv6_dict = {
    'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IPv6,
            'mgmt_ping': True,
            'mgmt_ssh': True
}
x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_ssh': True,
            'mgmt_https': True,
}
x1_wan_ipv6_dict = {
    'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPv6,
            'mgmt_ping': True,
}
x4_vlan1_dict = {
    'if': 'x4',
    'type': 'vlan',
            'vlan_tag': X4_VLAN1_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN1_IP,
            'routed_mode': {
                "interface": "X1"
            },
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    'mgmt_ping': True,
    'user_https': True,
}


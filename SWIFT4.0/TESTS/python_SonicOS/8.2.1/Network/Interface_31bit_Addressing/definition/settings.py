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
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, \
    ZoneObjectsApi, DHCPServerApi, FailoverLbApi, DynamicRoutingApi
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.API.system import PacketmonitorApi, SNMPApi
from modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.CLI.system import LicenseCli

from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                'Network/Interface_31bit_Addressing')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'Network/Interface_31bit_Addressing/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'Network/Interface_31bit_Addressing/definition')
scripts_path = os.environ["PYTHON_SONICOS_HOME"] + \
               '/Network/Interface_31bit_Addressing/definition/scripts/'
remote_conf_path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')

PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')

PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')

PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')

X4_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X4:1')

logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n X4_VLAN1_ID: {X4_VLAN1_ID} \n')

PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X1_IP = '10.11.1.200'
    X1_NET = '10.11.1.0'
    X1_GW = '10.11.1.1'
    X2_IP = '12.12.1.200'
    X2_NET = '12.12.1.0'
    X2_GW = '12.12.1.1'
    X3_IP = '192.168.30.200'
    X3_GW = '192.168.30.1'
    X3_NET = '192.168.30.0'
    X4_VLAN1_IP = '192.168.40.168'
    MASK = '255.255.255.254'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_REMOTE_IP = '12.12.1.201'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
               '/Network/Interface_31bit_Addressing/testplan/interface_31bit_address.json'


x2_static_dict = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X2_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
x2_lan_dict = {
    'if': 'X2',
    'zone': 'lan',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ping': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
}
x3_lan_dict = {
    'if': 'X3',
    'zone': 'lan',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'netmask': '255.255.255.0',
    'mgmt_https': True,
    'mgmt_ping': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
}
probe_conf_dict = {
    'name': '+Default+LB+Group',
    'interface': 'X3',
    'probe_type': 'logical',
    'probe_option': 'both',
    'main_protocol': 'tcp',
    'main_value': 50000,
    'alter_protocol': 'tcp',
    'alter_value': 50000,
}
wlb_conf_dict = {
    "failover_lb": {
        "group": [
            {
                "interface": [
                    {
                        "name": "X2",
                        "probe_condition": "always",
                        "probe_type": "physical",
                        "rank": 1
                    }
                ],
                "name": " Default LB Group",
                "type": "basic"
            }
        ]
    }
}

fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
dut1_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')
dut2_cli = Firewall(
    Parameter.X1_REMOTE_IP,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(dut1_cli)
interfacev4api = InterfaceIPv4Api(fw)
zonesapi = ZoneObjectsApi(fw)
aoapi = AddressobjectsApi(fw)
dhcpserverapi = DHCPServerApi(fw)
snmpapi = SNMPApi(fw)
failoverapi = FailoverLbApi(fw)
dynroutingapi = DynamicRoutingApi(fw)
packetmonitorapi = PacketmonitorApi(fw)
routepolicyapi = RoutePolicyApi(fw)

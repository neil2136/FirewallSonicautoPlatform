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
from lib.modules.API.network import AddressobjectsApi, ZoneObjectsApi, FailoverLbApi, InterfaceIPv4Api
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.log import LogMonitorApi, LogSettingsApi
from modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.CLI.system import LicenseCli

from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'Network/Transparent_Mode_TP270')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'Network/Transparent_Mode_TP270/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'Network/Transparent_Mode_TP270/definition')

# parameters on the openstack
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

logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC5_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC5_ETH1_IP: {PC5_ETH1_IP}')

PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)
PC5_login = Host(PC5_ETH0_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.50.50.50'
    X1_GW = '172.50.50.1'
    X2_IP = '172.20.20.100'
    X2_GW = '172.20.20.1'
    X3_IP = '192.168.30.100'
    MASK = '255.255.255.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
               '/Network/Transparent_Mode_TP270/testplan/transparent_mode_tp270.json'


# paramenters on the test case
x1_static_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
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
x3_base_dict = {
    'if': 'X3',
    'comment': 'trans mode test',
    'zone': 'LAN',
    'mode': 'transparent',
    'transparent_range': {'group': ''},
    'gratuitous_arp_wan_forwarding': False,
    'gratuitous_arp_wan_generation': False,
    'mgmt_https': True,
    'mgmt_ping': True,
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


# Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)
interfacev4api = InterfaceIPv4Api(fw)
zonesapi = ZoneObjectsApi(fw)
aoapi = AddressobjectsApi(fw)
aogroupapi = AddressObjectGroupApi(fw)
logsettingsapi = LogSettingsApi(fw)
logmonitorapi = LogMonitorApi(fw)
accessruleapi = AccessRuleIPv4Api(fw)
failoverapi = FailoverLbApi(fw)


import os
import sys
import re
import time

import unittest
import paramunittest
import paramiko
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite


# import contents from common_lib path
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info


# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.CLI.firewall import AccessRuleCli
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import AddressobjectsApi
from lib.modules.API.firewallsettings import MulticastApi
from lib.modules.API.system import PacketmonitorApi
from lib.modules.CLI.system import LicenseCli


suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Multicast_TP283'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/multicast_tp283.json'
script_path = suite_path + '/definition/scripts'
IGMP_CLIENT_CMD = f'python3 {script_path}/igmpclient.py'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC3_ETH2_IP: {PC3_ETH2_IP}')
PC1_login = Host(PC1_ETH2_IP)
PC2_login = Host(PC2_ETH2_IP)
PC3_login = Host(PC3_ETH2_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X2_IP = '13.13.1.168'
    X2_NET = '13.13.1.0'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    LAN_PC = PC1_ETH1_IP
    WAN_PC = PC2_ETH1_IP
    DMZ_PC = PC3_ETH1_IP
    MULTI_GROUP_IP = '224.10.10.10'


# Instantiate objects including API,CLI import
fw_api = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

aoapi = AddressobjectsApi(fw_api)
aocli = AddressObjectCli(fw_cli)
interfaceapi = InterfaceIPv4Api(fw_api)
multicastapi = MulticastApi(fw_api)
accessruleapi = AccessRuleApi(fw_api)
accessrulecli = AccessRuleCli(fw_cli)
packetmonitorapi = PacketmonitorApi(fw_api)
licensecli = LicenseCli(fw_cli)

# parameters on the test cases
x0_static_dict = {
    'if': 'X0',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.FIREWALL,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'multicast': True,
}
x1_static_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.DNS1,
    'dns2': Parameter.DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'multicast': True
}
x2_static_dict = {
    'if': 'X2',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'multicast': True
}
multicast_dict = {
    "object_type": "host",
    "name": "multicast_obj",
    "zone": "MULTICAST",
    "value": Parameter.MULTI_GROUP_IP
}

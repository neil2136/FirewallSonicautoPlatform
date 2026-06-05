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

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.CLI.firewall import AccessRuleCli
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import AddressobjectsApi
from lib.modules.API.firewallsettings import MulticastApi
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Multicast_283')

FIREWALL = '192.168.168.168'
X0_NET = '192.168.168.0'
X1_IP = '12.12.1.200'
X1_GW = '12.12.1.1'
X1_ZONE = 'WAN'
X2_IP = '13.13.1.168'
X2_NET = '13.13.1.0'
X2_ZONE = 'DMZ'
MASK = '255.255.255.0'
DNS1 = Params.G_DNS1
DNS2 = Params.G_DNS2
LAN_PC = '192.168.168.169'
WAN_PC = '12.12.1.169'
DMZ_PC = '13.13.1.169'
MULTICAST_IP = '224.10.10.10'
os_obj = Openstack(Params.testbed)
WAN_HOST_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
LAN_HOST = Host(os_obj.get_node_interface_ip('PC1', 'eth2'))
WAN_HOST = Host(WAN_HOST_IP)
DMZ_HOST = Host(os_obj.get_node_interface_ip('PC3', 'eth2'))
LAN_IF = 'eth1'
WAN_IF = 'eth1'
DMZ_IF = 'eth1'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Multicast_283/testplan/Multicast_283.json'
TESTPATH = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Multicast_283'
ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

ao_api = AddressobjectsApi(fw_api)
ao_cli = AddressObjectCli(fw_cli)
interface_api = InterfaceIPv4Api(fw_api)
multicast_api = MulticastApi(fw_api)
accessrule_api = AccessRuleApi(fw_api)
accessrule_cli = AccessRuleCli(fw_cli)

x0_static = {
    'if': 'X0',
    'zone': 'LAN',
    'mode': 'static',
    'ip': FIREWALL,
    'netmask': MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
    'multicast': True
}
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
    'multicast': True
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
    'multicast': True
}
multicast_obj = {
    "object_type": "host",
    "name": "multicast_obj",
    "zone": "MULTICAST",
    "value": MULTICAST_IP
}

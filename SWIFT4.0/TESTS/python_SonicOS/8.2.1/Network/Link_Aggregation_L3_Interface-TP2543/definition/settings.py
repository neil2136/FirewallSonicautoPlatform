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
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.CLI.system import StatusCli
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Link_Aggregation_L3_Interface-TP2543')

FIREWALL = '192.168.168.168'
X0_NET = '192.168.168.0'
X0_PC = '192.168.168.169'
X1_IP = '172.17.1.168'
X1_GW = '172.17.1.1'
X1_PC = '172.17.1.169'
X1_ZONE = 'WAN'
X2_IP = '182.18.1.168'
X2_NET = '182.18.1.0'
X2_PC = '182.18.1.169'
X2_ZONE = 'LAN'
MASK = '255.255.255.0'
DNS1 = Params.G_DNS1
DNS2 = Params.G_DNS2
os_obj = Openstack(Params.testbed)
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
'/Network/Link_Aggregation_L3_Interface-TP2543/testplan/Link_Aggregation_L3_Interface-TP2543.json'
TESTPATH = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Link_Aggregation_L3_Interface-TP2543'
ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(X2_IP, user='admin', password='password', supported_config_mode='cli-ssh')
interface_api = InterfaceIPv4Api(fw_api)
system_cli = StatusCli(fw_cli)

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
    'multicast': True,
    'redundancy_aggregation_port': 'aggregation',
    'aggregation_ports': ["X4"],
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
    'multicast': True,
    'redundancy_aggregation_port': 'aggregation',
    'aggregation_ports': ["X3"]
}

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

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Static_Routes_174/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Static_Routes_174')

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3','eth0')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4','eth0')
PC2_MGMT_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC3_MGMT_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC4_MGMT_IP = os_obj.get_node_interface_ip('PC4','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3','eth2')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4','eth2')

logger.info("\n" + "-" * 30 + "\n" \
    + "PC2_MGMT_IP :" + PC2_MGMT_IP + "\n" \
    + "PC3_MGMT_IP :" + PC3_MGMT_IP + "\n" \
    + "PC4_MGMT_IP :" + PC4_MGMT_IP + "\n" \
    + "-" * 30
)

PC2_login = Host(PC2_MGMT_IP, user='root', password='password')
PC3_login = Host(PC3_MGMT_IP, user='root', password='password')
PC4_login = Host(PC4_MGMT_IP, user='root', password='password')

FIREWALL = '192.168.168.168'
X1_IP  = '13.0.0.168'
X1_GW  = PC2_ETH0_IP
X1_DNS1 = Params.G_DNS1
X1_DNS2 = Params.G_DNS2
X2_IP    = '2.0.0.168'
X3_IP    = '3.0.0.168'
MASK     = '255.255.255.0'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Static_Routes_174/testplan/staticroutes_174.json'

ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface_obj = network.InterfaceIPv4Api(fw_api)
route_obj = network.RoutePolicyApi(fw_api)
ao_obj = network.AddressobjectsApi(fw_api)

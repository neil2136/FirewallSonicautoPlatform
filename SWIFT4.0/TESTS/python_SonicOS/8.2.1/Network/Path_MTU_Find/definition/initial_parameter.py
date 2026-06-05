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
from lib.modules.API import system
from lib.modules.API import diag

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Path_MTU_Find/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Path_MTU_Find')

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth2')
PC2_ETH3_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth3')
logger.info("\n" + "-" * 30 + "\n" \
    + "PC1_ETH0_IP :" + PC1_ETH0_IP + "\n" \
    + "PC2_ETH1_IP :" + PC2_ETH1_IP + "\n" \
    + "PC2_ETH2_IP :" + PC2_ETH2_IP + "\n" \
    + "PC2_ETH3_IP :" + PC2_ETH3_IP + "\n" \
    + "-" * 30
)

PC2_login = Host(PC2_ETH3_IP, user='root', password='password')
X1_IP  = '172.17.1.168'
X1_GW  = '172.17.1.1'
X1_DNS1 = Params.G_DNS1
X1_DNS2 = Params.G_DNS2
FIREWALL = '192.168.168.168'
X2_IP    = '14.1.1.168'
MASK     = '255.255.255.0'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Path_MTU_Find/testplan/Path_MTU_Find.json'

ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface_obj = network.InterfaceIPv4Api(fw_api)
zone_obj = network.ZoneObjectsApi(fw_api)
diag_obj = system.DiagnosticApi(fw_api)
diagObj = diag.DiagApi(fw_api)
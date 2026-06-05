import os
import sys
import re
import time
import copy
import requests

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
from lib.modules.API.log import LogMonitorApi, LogCategoryApi, LogSettingsApi
from lib.modules.API import system
from lib.modules.API import object
from lib.modules.API import firewall

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/NAT_HA_LB_1381/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/NAT_HA_LB_1381')

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3','eth0')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5','eth0')
PC6_ETH0_IP = os_obj.get_node_interface_ip('PC6','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5','eth1')
PC6_ETH1_IP = os_obj.get_node_interface_ip('PC6','eth1')
logger.info("\n" + "-" * 30 + "\n" \
    + "PC1_ETH1_IP :" + PC1_ETH1_IP + "\n" \
    + "PC2_ETH1_IP :" + PC2_ETH1_IP + "\n" \
    + "PC3_ETH1_IP :" + PC3_ETH1_IP + "\n" \
    + "PC5_ETH1_IP :" + PC5_ETH1_IP + "\n" \
    + "PC6_ETH1_IP :" + PC6_ETH1_IP + "\n" \
    + "-" * 30
)

localhost = Host('localhost')
PC2_login = Host(PC2_ETH1_IP, user='root', password='password')
PC3_login = Host(PC3_ETH1_IP, user='root', password='password')
PC5_login = Host(PC5_ETH1_IP, user='root', password='password')
PC6_login = Host(PC6_ETH1_IP, user='root', password='password')

FIREWALL = '192.168.168.168'
X1_IP = '6.6.6.168'
X1_GW = '6.6.6.1'
X1_DNS1 = Params.G_DNS1
X1_DNS2 = Params.G_DNS2
MASK = '255.255.255.0'
WAN_HOST = '6.6.6.10'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/NAT_HA_LB_1381/testplan/nat_lb_1381.json'

ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface_obj = network.InterfaceIPv4Api(fw_api)
address_obj = network.AddressobjectsApi(fw_api)
address_group_obj = object.AddressObjectGroupApi(fw_api)
access_rule_obj = firewall.AccessRuleApi(fw_api)
natpolicy_obj = network.NatpolicyApi(fw_api)
log_obj = LogMonitorApi(fw_api)
log_set = LogCategoryApi(fw_api)
log_settings = LogSettingsApi(fw_api)
pm_obj = system.PacketmonitorApi(fw_api)

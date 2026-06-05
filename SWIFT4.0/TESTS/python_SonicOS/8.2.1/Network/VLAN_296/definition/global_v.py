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

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/VLAN_296/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/VLAN_296')

os_obj = Openstack(Params.testbed)
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4','eth0')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4','eth2')
X4_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X4:1') 
X4_VLAN2_ID = os_obj.get_node_interface_vlan_id('UTM', 'X4:2') 
logger.info("\n" + "-" * 30 + "\n" \
    + "PC1_ETH3_IP :" + PC1_ETH3_IP + "\n" \
    + "PC2_ETH0_IP :" + PC2_ETH0_IP + "\n" \
    + "PC2_ETH2_IP :" + PC2_ETH2_IP + "\n" \
    + "PC3_ETH1_IP :" + PC3_ETH1_IP + "\n" \
    + "PC4_ETH2_IP :" + PC4_ETH2_IP + "\n" \
    + "X4_VLAN1_ID :" + str(X4_VLAN1_ID) + "\n" \
    + "X4_VLAN2_ID :" + str(X4_VLAN2_ID) + "\n" \
    + "-" * 30
)

PC2_login = Host(PC2_ETH0_IP, user='root', password='password')
PC4_login = Host(PC4_ETH0_IP, user='root', password='password')
bin_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/VLAN_296/bin/'


class Parameter():
    FIREWALL = '192.168.168.168'
    X2_IP = '10.11.0.30'
    X4_IP = "100.1.1.168"
    X2_SUB = "10.11.0.0"
    X4_VLAN1_SUB = "4.4.4.0"
    X4_VLAN1_IP = "4.4.4.168"
    X4_VLAN2_IP = "5.5.5.168"
    MASK = '255.255.255.0'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/VLAN_296/testplan/VLAN_296.json'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface_obj = network.InterfaceIPv4Api(fw)

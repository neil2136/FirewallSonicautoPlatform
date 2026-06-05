import os
import re
import sys
import copy
import time

import unittest
import paramunittest
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from nose_parameterized import parameterized
from time import sleep


sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Routed_Mode')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Routed_Mode/testcases')

from lib.modules.API import policy
from lib.modules.API import network
from lib.modules.API import dpissl
from lib.modules.ui.fw_page import FWPage
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.API import log
from lib.modules.API import securityservices
class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '13.0.0.168'
    X1_GW = '13.0.0.1'
    X2_IP = '2.2.2.168'
    X2_GW = '2.2.2.1'
    X3_IP = '3.3.3.168'
    X3_GW = '3.3.3.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    PC2_ETH0 = '192.168.2.3'
    PC1_ETH1 = '192.168.168.169'
    PC1_ETH2 = '192.168.100.10'
    PC2_ETH0 = '192.168.3.2'
    PC2_ETH1 = '13.0.0.100'
    PC2_ETH2 = '192.168.100.20'
    PC3_ETH0 = '192.16.4.2'
    PC3_ETH1 = '2.2.2.100'
    PC3_ETH2 = '192.168.100.30'
    PC4_ETH0 = '192.168.5.2'
    PC4_ETH1 = '4.4.4.100'
    PC4_ETH2 = '192.168.100.40'
 
    X3VLAN_IP = '4.4.4.168'
 
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/Routed_Mode/testplan/Routed_Mode.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3','eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3','eth2')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4','eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4','eth1')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4','eth2')
logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
    + 'PC2_ETH2_IP :' + PC2_ETH2_IP + '\n' \
    + 'PC3_ETH0_IP :' + PC3_ETH0_IP + '\n' \
    + 'PC3_ETH1_IP :' + PC3_ETH1_IP + '\n' \
    + 'PC3_ETH2_IP :' + PC3_ETH2_IP + '\n' \
    + 'PC4_ETH0_IP :' + PC4_ETH0_IP + '\n' \
    + 'PC4_ETH1_IP :' + PC4_ETH1_IP + '\n' \
    + 'PC4_ETH2_IP :' + PC4_ETH2_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/Routed_Mode'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_obj = network.InterfaceIPv4Api(fw)
zone_obj = network.ZoneObjectsApi(fw)
licenseObj = LicenseCli(fw_cli)
natObj = network.NatpolicyApi(fw)

local_host = Host('localhost')
pc2_ssh = Host(PC2_ETH2_IP, user='root', password='password')

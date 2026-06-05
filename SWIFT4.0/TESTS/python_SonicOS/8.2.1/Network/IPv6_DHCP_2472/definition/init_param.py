import os
import re
import sys

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
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_2472')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_2472/testcases')

from lib.modules.API import network
from lib.modules.API import system

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X0_IPv6 = '2001::3'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'

    PC1_ETH0 = '192.168.2.3'
    PC1_ETH1 = '192.168.168.201'
    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_2472/testplan/IPv6_DHCP_2472.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')

logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/IPv6_DHCP_2472'


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

interface_ipv6_obj = network.InterfaceIPv6Api(fw)
settingObj = system.SettingApi(fw)
dhcpObj = network.DHCPServerApi(fw)

local_host = Host('localhost')




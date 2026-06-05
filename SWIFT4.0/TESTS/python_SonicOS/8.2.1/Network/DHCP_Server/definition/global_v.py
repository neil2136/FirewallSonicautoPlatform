import os
import sys
import re
import copy
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest

from runner.unittest.setup import Test, skip_if_dts
from runner.utils.assertion import Assertion
    
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DHCP_Server/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DHCP_Server')
os_obj = Openstack(Params.testbed)
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')
PC2_login = Host(PC2_ETH2_IP, user='root', password='password')

FIREWALL = '192.168.168.168'
X2_IP = '2.2.2.168'
MASK = '255.255.255.0'
X1_IP = '172.17.1.168'
X1_GW = '172.17.1.1'
X1_DNS1 = Params.G_DNS1
X1_DNS2 = Params.G_DNS2
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DHCP_Server/testplan/DHCP_Server_Steps.json'
ip = FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface_obj = network.InterfaceIPv4Api(fw)
dhcp_obj = network.DHCPServerApi(fw)

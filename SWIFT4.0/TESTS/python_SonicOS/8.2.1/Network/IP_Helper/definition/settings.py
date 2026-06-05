import os
import sys
import unittest
import re
from time import sleep


sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
testpath = os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper'


from utm import Firewall, FirewallAPI
from runner.unittest.setup import Test
from runner.settings import logger, Params
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from lib.modules.API import network, object
from networkdevice import Host


class Parameter():
    FIREWALL = '192.168.168.168'
    TESTPLAN = testpath + '/testplan/ip_helper.json'

    X2_DMZ_IP = '2.2.2.100'
    DMZ_GW = '2.2.2.1'
    MASK = '255.255.255.0'

    X3_IP = '3.3.3.168'

    PC2_DMZ_IP = '2.2.2.22'

    PC1_LAN_IP = '192.168.168.169'
    PC3_LAN_IP = '3.3.3.22'

    INTERFACE_LAN = 'eth0'


fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
dhcp_obj = network.DHCPServerApi(fw)
iphelper = network.IpHelperApi(fw)
address_obj = network.AddressobjectsApi(fw)
interface = network.InterfaceIPv4Api(fw)
address_group_obj = object.AddressObjectGroupApi(fw)


pc2_ssh = Host(Params.testbed + '-PC2')


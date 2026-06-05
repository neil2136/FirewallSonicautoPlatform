import os
import sys
import unittest
import re
from time import sleep


sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper_v3')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper_v3/lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from utm import Firewall,FirewallAPI
from runner.unittest.setup import Test, repeat_method
from runner.settings import Params, logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from modules.API import network
from networkdevice import Host
from modules.CLI import system


TEST_PATH = os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper_v3'


class Parameter():
    FIREWALL = '192.168.168.168'
    WAN_IP = '13.0.0.168'
    WAN_GW = '13.0.0.1'
    WAN_DNS1 = '10.9.1.40'
    DMZ_IP = '172.16.0.1'
    MASK = '255.255.255.0'

    PC1_WAN_IP = '13.0.0.3'
    PC1_LAN_IP = '192.168.168.169'
    PC1_DMZ_IP = '172.16.0.2'

    PC2_WAN_IP = '13.0.0.5'
    PC2_DMZ_IP = '172.16.0.3'

    DstPort = 53
    SrcPort = 36646
    INTERFACE_LAN = 'eth0'

    TESTPLAN = TEST_PATH + '/testplan/ip_helper_v3.json'


fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli=Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
interface = network.InterfaceIPv4Api(fw)
address_obj = network.AddressobjectsApi(fw)
dhcp_obj = network.DHCPServerApi(fw)
iphelper = network.IpHelperApi(fw)
pc2_ssh = Host(Params.testbed + '-PC2')
local_host = Host('localhost')
sonicos_api=system.AdminCli(fw_cli)

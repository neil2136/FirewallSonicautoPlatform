import os
import sys
import unittest
from time import sleep


sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface/lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
testplan = os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface/testplan/ipv6_interface.json'


class Parameter():
    FIREWALL = '192.168.168.168'
    MGMT_SSH = True
    MGMT_HTTP = True
    MGMT_HTTPS = True
    MGMT_Ping = True
    MGMT_SNMP = True
    Mask = '255.255.255.0'
    TESTPLAN = testplan
    lan_ipv6 = '2000:1111::100'
    wan_ipv6 = '2001:222::100'
    x0_ipv6 = '2000:1111::150'
    x1_ipv6 = '2001:222::182'


from utm import Firewall,FirewallAPI
from runner.unittest.setup import Test, repeat_method
from runner.settings import logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from lib.settings import Parameter
from lib.modules.API.network import InterfaceIPv6Api,InterfaceIPv4Api
from testcases.setup import *
from lib import utils
from lib.modules.API.accessrule import Access_Rule

fw = Firewall(Parameter.FIREWALL, user= 'admin', password= 'password', supported_config_mode='api')
interface = InterfaceIPv6Api(fw)
interface_v4 = InterfaceIPv4Api(fw)
accessrule = Access_Rule(fw)



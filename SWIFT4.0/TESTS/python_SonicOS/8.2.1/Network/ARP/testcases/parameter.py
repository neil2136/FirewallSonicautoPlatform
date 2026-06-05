import os
import sys
import re
from runner.unittest.suite import UnittestSuite
import unittest
from utm import Firewall
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import ArpApi
from lib.modules.API.system import PacketmonitorApi
from runner.settings import logger
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from runner.settings import logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from scapy.all import *
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ARP')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ARP/lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
import time
#PYTHON_SONICOS_HOME='/DEV_TESTS/python_SonicOS/7.0.0_tz'
#PYTHON_COMMON_HOME='/DEV_TESTS/python_SonicOS/common_lib'
#sys.path.append(PYTHON_SONICOS_HOME+'/QuickSmoke/ARP_Smoke')
#sys.path.append(PYTHON_COMMON_HOME)
#sys.path.append(PYTHON_SONICOS_HOME+'/QuickSmoke/ARP_Smoke/lib')
testplan = os.environ["PYTHON_SONICOS_HOME"]+'/Network/'
class Parameter():
    FIREWALL = '192.168.168.168'
    X2_IP = '172.16.1.168'
    DMZ_HOST_MGMT = '172.16.2.101'
    DMZ_HOST = '172.16.1.101'
    TESTPLAN = testplan + 'ARP/testplan/arp.json'
    X2_MAC = ''
    DMZ_HOST_MAC = ''

fw = Firewall(Parameter.FIREWALL,
              user='admin',
              password='password')

arpApi = ArpApi(fw)
interface = InterfaceIPv4Api(fw)
PC2 = Host(Parameter.DMZ_HOST_MGMT, user='root', password='password')

import sys
import re
import os
import time
from nose_parameterized import parameterized
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Split_DNS')
from runner.unittest.setup import Test, repeat_method
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import vpn
from lib.modules.CLI.system import LicenseCli
from utm import Firewall
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info


class Parameter():
    DUT_X0_IP = "192.168.168.168"    
    DUT_X2_IP = "2.2.2.168"    
    ZONES=['public','trusted']
    DUT_X1_IP="11.11.11.168"
    # DUT_X1_IPv6 = "2001::168"
    # MY_WAN_PC_IPv6="2001::169"
    DUT_X1_GW="11.11.11.1"
    ZONES=['public','trusted']
    DESTINATION = "10.9.1.40"
    MY_WAN_PC_IP="11.11.11.169"
    MY_DMZ_PC_IP="2.2.2.169"
    DNS_SERVER = MY_WAN_PC_IP
    REACH_WEB = "www.baidu.com"
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/Split_DNS/testplan/split_DNS.json"



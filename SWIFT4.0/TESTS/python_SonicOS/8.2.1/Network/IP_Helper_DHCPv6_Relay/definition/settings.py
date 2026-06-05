import os
import re
import sys
import copy
import time
import unittest

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest
from modules.API import network
from modules.API import object
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.system import StatusApi
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relayr')
class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/testplan/testplan.json'


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

iphelper_obj= network.IpHelperApi(fw_api)
interface = network.InterfaceIPv4Api(fw_api)
license = LicenseCli(fw_cli)

static_pc = Params.testbed + '-PC1'
static_client = Host(static_pc)
status_api = StatusApi(fw_api)
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

from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
    
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.API.log import LogMonitorApi, LogCategoryApi, LogSettingsApi

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Dynamic_Address_Object/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Dynamic_Address_Object')
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_login = Host(PC2_ETH0_IP, user='root', password='password')
confs_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Dynamic_Address_Object/confs/'

FIREWALL = '192.168.168.168'
X2_IP = '2.2.2.168'
MASK = '255.255.255.0'
X1_IP = '13.0.0.168'
X1_GW = '13.0.0.10'
X1_DNS1 = '13.0.0.10'
X1_DNS2 = Params.G_DNS1


class Parameter():
    PC1_ETH0_MAC = ''

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Dynamic_Address_Object/testplan/Dynamic_Address_Object.json'
ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface_obj = network.InterfaceIPv4Api(fw_api)
ao_obj = network.AddressobjectsApi(fw_api)
access_rule_obj = firewall.AccessRuleApi(fw_api)
access_rule_obj_ipv6 = firewall.AccessRuleIPv6Api(fw_api)
log = LogMonitorApi(fw_api)
system_obj = system.DiagnosticApi(fw_api)
log_set = LogCategoryApi(fw_api)
restart = system.RestartApi(fw_api)
log_settings = LogSettingsApi(fw_api)

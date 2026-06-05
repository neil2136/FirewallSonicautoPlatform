import os
import sys
import re
import time
import copy
import requests

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from lib.modules.API.network import InterfaceIPv4Api
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, repeat_method

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from lib.modules.CLI.system import LicenseCli


sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API.system import RestartApi,SettingApi
from lib.modules.API.log import LogMonitorApi, LogCategoryApi, LogSettingsApi, LogAutomationApi, LogResolutionApi, SyslogSettingsApi

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Log_Monitor_TP2582/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Log_Monitor_TP2582')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Log_Monitor_TP2582/lib/')
print(sys.path)
import pop3_client

os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
localhost = Host('localhost')

FIREWALL = '192.168.168.168'
X1_IP = '172.17.1.168'
X1_IP_TMP = '172.17.1.169'
X1_GW = '172.17.1.1'
X1_DNS1 = Params.G_DNS1
X1_DNS2 = Params.G_DNS2
X2_IP = '14.1.1.168'
MASK = '255.255.255.0'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Log_Monitor_TP2582/testplan/Log_Monitor_TP2582.json'
config_path = os.environ["PYTHON_SONICOS_HOME"] + "/Log/Log_Monitor_TP2582/config"
ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='S0nicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='S0nicauto', supported_config_mode='cli-ssh')
license = LicenseCli(fw_cli)
interface_obj = network.InterfaceIPv4Api(fw_api)
log_obj = LogMonitorApi(fw_api)
log_set = LogCategoryApi(fw_api)
log_settings = LogSettingsApi(fw_api)
log_automation = LogAutomationApi(fw_api)
fw_restart = RestartApi(fw_api)
fw_boot = SettingApi(fw_api)
log_res = LogResolutionApi(fw_api)
log_sys = SyslogSettingsApi(fw_api)
addrObj = network.AddressobjectsApi(fw_api)


static_pc = Params.testbed + '-PC1'
static_client = Host(static_pc)
import os
import sys
import re
import time
import copy
import requests

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.CLI.system import LicenseCli, AdminCli, ScheduleCli, TimeCli, DiagnosticsCli, SettingCli, \
    StatusCli
from lib.modules.API.network import AddressobjectsApi, InterfaceIPv4Api
from lib.modules.API.diag import DiagApi
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.firewall import AccessRuleCli
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from util.openstack import Openstack

import unittest
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                'CLI/CLI3_System/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'CLI/CLI3_System')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
           '/CLI/CLI3_System/testplan/system.json'


# parameters on the openstack
class Parameter:
    FIREWALL = '10.8.105.173'
    X1_IP = '10.8.105.173'
    MASK = '255.255.255.0'
    X1_GW = '10.8.105.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_SUBNET = '10.8.105.0/24'
    PC2_IP = '10.8.105.174'
    AUTO_GW = '10.6.0.1'
    FW_VERSION = Params.sonicos_ver
    FW_NUMBER = re.sub('\D', '', Params.product)


# paramenters on the test case
# case 1
# os_obj = Openstack(Params.testbed)
# consvr, conport = os_obj.get_console_info()
# case 4
EXTERNAL_URL = ['us.sonicwall.com', 'sonicwall.com', 'eng.sonicwall.com']
# case 5
pinglist = [Parameter.PC2_IP, Parameter.AUTO_GW, Parameter.X1_GW]
# case 6
schedule_dict = {
    'name': 'autoadded',
    'ocr-mode': 'recurring',
    'rec-time': '12:00 18:00 mon tue wed thu fri'
}


# Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password2',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password2',
    new_password='password2',
    supported_config_mode='cli-ssh')
# lc = LicenseCli(fw_cli)
interfacecfg = InterfaceIPv4Api(fw)
diagcfg = DiagApi(fw)
interfaceclicfg = InterfaceCli(fw_cli)
admincli = AdminCli(fw_cli)
schedulecli = ScheduleCli(fw_cli)
timecli = TimeCli(fw_cli)
diagnosticscli = DiagnosticsCli(fw_cli)
statuscli = StatusCli(fw_cli)
settingcli = SettingCli(fw_cli)

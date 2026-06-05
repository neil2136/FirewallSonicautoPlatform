import os
import sys
import re
import time
import copy
import requests
from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'CLI/CLI3_Configuration_Audit/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + 'CLI/CLI3_Configuration_Audit')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
    '/CLI/CLI3_Configuration_Audit/testplan/configuration_audit.json'


from utm import Firewall
from util.enhancedinfo import show_testcase_info
from lib.modules.CLI.log import AuditLogsCli, LogAutomationCli
from lib.modules.CLI.network import RouteCli
from lib.modules.API.network import AddressobjectsApi, InterfaceIPv4Api
from lib.modules.CLI.system import LicenseCli

# parameters on the openstack
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.168'
    MASK = '255.255.255.0'
    X1_GW = '172.16.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2

# paramenters on the test case
audit_log_list = ['display-on-console', 'enable', 'supplemental-changes']
e_au_format_list = ['csv', 'html', 'plain-text']
send_period_list = ['daily', 'weekly', 'when-full']

log_auto_eaddr = {
    'type': 'audit',
    'email': 'test@sonicwall.com'
}

log_auto_period = {
    'hour': 10,
    'minute': 30,
    'week': 'fri'
}

# Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')
lc = LicenseCli(fw_cli)
interfacecfgapi = InterfaceIPv4Api(fw)
auditlogcli = AuditLogsCli(fw_cli)
auditautocli = LogAutomationCli(fw_cli)

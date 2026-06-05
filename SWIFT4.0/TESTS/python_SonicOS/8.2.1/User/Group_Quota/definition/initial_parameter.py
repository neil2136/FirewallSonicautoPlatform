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

from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network, firewall, system, users
from lib.modules.API import accessrule
from lib.modules.CLI.system import AdminCli
from lib.modules.CLI.system import LicenseCli


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Group_Quota')

tc_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Group_Quota/testcases'

class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Group_Quota/testplan/group_quota_testplan.json'


ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

user = users.UserLocalApi(fw)
user_status = users.UserStatusApi(fw)
interface = network.InterfaceIPv4Api(fw)
admin = AdminCli(fw_cli)
license = LicenseCli(fw_cli)
diagnostic = system.DiagnosticApi(fw)
access_rules = accessrule.AccessRuleIPv4Api(fw)
address_obj = network.AddressobjectsApi(fw)


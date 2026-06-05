import os
import re
import sys
import copy
import time
import unittest
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')

from runner.settings import logger
from modules.ui.ui_wrapper import Browser

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from utm import FirewallCGI
from util.enhancedinfo import show_testcase_info
from utm import Firewall
#from lib.modules.CLI.system import LicenseCli
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network, firewall, system, users, log
from lib.modules.API import accessrule
from lib.modules.CLI.system import AdminCli

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Localuser_Quota/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Localuser_Quota')
print(sys.path)
import ui_user

os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
pc1_defaultgw = os_obj.get_pc_default_gw_ip('PC1')

tc_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Localuser_Quota/testcases'
lib_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Localuser_Quota/definition'

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api
from runner.settings import Params, logger

class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Localuser_Quota/testplan/local_user.json'

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
restart = system.RestartApi(fw)
local_user = users.UserLocalApi(fw)
user_status = users.UserStatusApi(fw)
interface = network.InterfaceIPv4Api(fw)
admin = AdminCli(fw_cli)
diagnostic = system.DiagnosticApi(fw)
logs=log.LogMonitorApi(fw)
access_rules = accessrule.AccessRuleIPv4Api(fw)
address_obj = network.AddressobjectsApi(fw)
natpolicy_obj = network.NatpolicyApi(fw)
license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw)
localhost = Host('localhost')
#static_pc = Params.testbed + '-PC2'
#static_client = Host(static_pc)

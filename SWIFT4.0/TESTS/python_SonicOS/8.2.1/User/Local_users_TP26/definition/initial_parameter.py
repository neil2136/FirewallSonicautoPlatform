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
from lib.modules.API import network, firewall, system, users,log
from lib.modules.API import accessrule
from lib.modules.CLI.system import AdminCli
#from lib.modules.CLI.system import LicenseCli

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_users_TP26/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_users_TP26')
import ui_user

os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
pc1_defaultgw = os_obj.get_pc_default_gw_ip('PC1')

tc_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_users_TP26/testcases'
lib_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_users_TP26/definition'

class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_users_TP26/testplan/local_user.json'


ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
restart = system.RestartApi(fw)
local_user = users.UserLocalApi(fw)
user_status = users.UserStatusApi(fw)
interface = network.InterfaceIPv4Api(fw)
admin = AdminCli(fw_cli)
diagnostic = system.DiagnosticApi(fw)
logs=log.LogCategoryApi(fw)
access_rules = accessrule.AccessRuleIPv4Api(fw)
address_obj = network.AddressobjectsApi(fw)
natpolicy_obj = network.NatpolicyApi(fw)
#license = LicenseCli(fw_cli)
localhost = Host('localhost')
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)


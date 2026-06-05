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
from lib.modules.API.users import UserLocalApi
from lib.modules.API.users import UserStatusApi
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import AddressobjectsApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.system import DiagnosticApi
from lib.modules.CLI.system import AdminCli
from lib.modules.CLI.system import LicenseCli

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke1/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke1')
import ui_group

os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
pc1_defaultgw = os_obj.get_pc_default_gw_ip('PC1')

tc_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke1/testcases'
lib_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke1/lib'


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke1/testplan/local_groups_testplan.json'


ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

user = UserLocalApi(fw)
user_status = UserStatusApi(fw)
interface = InterfaceIPv4Api(fw)
admin = AdminCli(fw_cli)
license = LicenseCli(fw_cli)
diagnostic = DiagnosticApi(fw)
access_rules = AccessRuleIPv4Api(fw)
address_obj = AddressobjectsApi(fw)

localhost = Host('localhost')
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)

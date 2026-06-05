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
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import AddressobjectsApi, InterfaceIPv4Api
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.users import LdapApi, UserLocalApi, UsersettingApi, UserStatusApi
from lib.modules.API.system import RestartApi, SettingApi, DiagnosticApi

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_Mirrorred_groups')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_Mirrorred_groups/lib')
import ui_ldap
import ui_login
import ui_user

os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
pc1_defaultgw = os_obj.get_pc_default_gw_ip('PC1')

class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = '10.50.129.149'
    X1_DNS2 = '10.50.129.148'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_Mirrorred_groups/testplan/ldap_mirrored_groups.json'

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')
license = LicenseCli(fw_cli)
user = UserLocalApi(fw_api)
user_status = UserStatusApi(fw_api)
ldap = LdapApi(fw_api)
user_settings = UsersettingApi(fw_api)
interface = InterfaceIPv4Api(fw_api)
access_rules = AccessRuleIPv4Api(fw_api)
address_obj = AddressobjectsApi(fw_api)
reboot_sys = RestartApi(fw_api)
diagnostic = DiagnosticApi(fw_api)
setting = SettingApi(fw_api)

localhost = Host('localhost')
static_pc = Params.testbed + '-PC1'
static_client = Host(static_pc)

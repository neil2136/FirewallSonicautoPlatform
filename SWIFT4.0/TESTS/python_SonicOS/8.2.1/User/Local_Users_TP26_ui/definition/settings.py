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

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Local_Users_TP26_ui')

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.users import UserLocalApi, UsersettingApi, UserStatusApi
from lib.modules.API.users import LdapApi
from lib.modules.API.system import TimeApi, StatusApi
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.sslvpn import SSLVPNVirtualOfficeAPI


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/testplan/local_user_ui.json'   

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')

license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
local_user = UserLocalApi(fw_api)
access_rules = AccessRuleIPv4Api(fw_api)
localhost = Host('localhost')
user_settings = UsersettingApi(fw_api)
ldap = LdapApi(fw_api)
user_status = UserStatusApi(fw_api)
time_obj = TimeApi(fw_api)
sslvpnvirtual = SSLVPNVirtualOfficeAPI(fw_api)
status_api = StatusApi(fw_api)





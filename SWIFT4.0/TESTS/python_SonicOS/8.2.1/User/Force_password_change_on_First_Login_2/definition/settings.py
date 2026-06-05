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
import pexpect
from pexpect import pxssh
from concurrent.futures import ThreadPoolExecutor


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Force_password_change_on_First_Login_2')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login_2/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login_2/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login_2/lib/')

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.system import SettingApi, AdminApi
from lib.modules.API.users import UserStatusApi, UsersettingApi, UserLocalApi, LdapApi, RadiusApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI, SSLVPNClientSettingsAPI
from lib. modules.API.network import AddressobjectsApi
from ui_user_change_pw import FWPage
from ui_user import FWlogin
from sslvpn.common_lib import netextender


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login_2/testplan/force_password_change_on_first_login.json'   

G_PASSWORD_NEW = Params.G_NEW_PASSWORD
ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')

license = LicenseCli(fw_cli)
interface_obj = InterfaceIPv4Api(fw_api)
local_user = UserLocalApi(fw_api)
user_status = UserStatusApi(fw_api)
user_setting = UsersettingApi(fw_api)
access_rules = AccessRuleIPv4Api(fw_api)
setting = SettingApi(fw_api)
admin_setting = AdminApi(fw_api)
ldap = LdapApi(fw_api)
Radius_user = RadiusApi(fw_api)
sslvpnserver = SSLVPNServerSettingsAPI(fw_api)
address_objects = AddressobjectsApi(fw_api)
clientsetobj = SSLVPNClientSettingsAPI(fw_api)
cp_nx = netextender.InstallNX()
localhost = Host('localhost')
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)
uiobj = FWPage("https://13.0.0.100", "admin", "password")
fw_ui_obj = FWlogin("13.0.0.100", "admin", "password")




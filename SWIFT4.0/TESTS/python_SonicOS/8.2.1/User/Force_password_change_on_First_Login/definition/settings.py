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
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Force_password_change_on_First_Login')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login/lib/')
import ui_user_change_pw
import ui_user


from modules.API import network
#from modules.API import firewallsettings
from modules.API import users
from lib.modules.API.system import SettingApi
from lib.modules.API.users import UserStatusApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.network import InterfaceIPv4Api


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login/testplan/force_password_change_on_first_login.json'   


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cgi = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cgi')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

interface_obj = InterfaceIPv4Api(fw_api)
local_user = users.UserLocalApi(fw_api)
user_status = UserStatusApi(fw_api)
access_rules = AccessRuleIPv4Api(fw_api)
setting = SettingApi(fw_api)
localhost = Host('localhost')
static_pc = Params.testbed + '-DUT-X1-GW-PC'
static_client = Host(static_pc)





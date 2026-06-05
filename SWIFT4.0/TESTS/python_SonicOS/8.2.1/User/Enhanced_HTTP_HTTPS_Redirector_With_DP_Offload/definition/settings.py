import os
import sys
import re
import time
import copy
import requests
import asyncio
import unittest
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

import os
import sys
import time
import json

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/')

from utm import Firewall
from networkdevice import Host
from definition.fwpage_ui import FWPage_UI
from modules.CLI import network
from runner.settings import logger
from runner.settings import Params
from util.openstack import Openstack
from modules.ui.ui_wrapper import Browser
from modules.API.users import UserLocalApi
from runner.utils.assertion import Assertion
from modules.API.firewall import AccessRuleApi
from lib.modules.API.users import UsersettingApi
from util.enhancedinfo import show_testcase_info
from lib.modules.API.network import InterfaceIPv4Api
from runner.unittest.setup import Test, repeat_method
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from lib.modules.API.system import AdminApi, DiagnosticApi
# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
from lib.modules.API import network
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import policy
from lib.modules.API import users
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.CLI.firewall import AccessRuleCli
from lib.modules.API.users import UsersettingApi

suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
CONF_PATH = suite_path + 'definition/config'
HTTPS_SERVER_PATH = CONF_PATH + '/httpserver'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
configPath = os.environ["PYTHON_SONICOS_HOME"] + '/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_login = Host(PC1_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X2_IP = '12.12.2.168'
    X2_GW = '12.12.2.1'
    X2_SUBNET = '12.12.2.0'
    FAKE_DNS1 = '2.2.2.2'
    FAKE_DNS2 = '3.3.3.3'
    X3_IP = '192.168.3.168'

    prebuild = Params.prebuild
    testbuild = Params.build

    R_X0_IP = '172.16.1.101'
    R_X1_IP = '12.12.1.201'
    R_X2_IP = '12.12.2.201'
    R_X0_NET = '172.16.1.0'
    R_X3_IP = '12.12.3.201'
    VPN_IF_IP_LOCAL = '1.1.1.2'
    VPN_IF_IP_REMOTE = '1.1.1.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/testplan/testplan.json'
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/testplan/testplan.json'


class CaseParams:
   
    ula_user_name = 'auto_ula_test'


ip = Parameter.FIREWALL

fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

local_user = UserLocalApi(fw_api)
user_settings = UsersettingApi(fw_api)
admin_obj = AdminApi(fw_api)
interface = InterfaceIPv4Api(fw_api)
diag_obj = DiagnosticApi(fw_api)
sslvpn_server_api = SSLVPNServerSettingsAPI(fw_api)

OpenS = Openstack(Params.testbed)
PC2 = Host(Params.testbed + '-PC2')
ui_obj = FWPage_UI(ip, "admin", "S0nic@uto")
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
os_obj = Openstack(Params.testbed)
interface_obj = InterfaceIPv4Api(fw_api)
access_rules = AccessRuleApi(fw_api)
access_rules_ipv4 = AccessRuleIPv4Api(fw_api)


PC1_login = Host(PC1_ETH0_IP)

fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='S0nic@uto',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='S0nic@uto',
    supported_config_mode='cli-ssh')

interfaceapi = network.InterfaceIPv4Api(fw)
licensecli = LicenseCli(fw_cli)
fwupgradeapi = system.SettingApi(fw)
statusapi = system.StatusApi(fw)
userLocalapi = users.UserLocalApi(fw)
usersettingapi = users.UsersettingApi(fw)
userstatusapi = users.UserStatusApi(fw)
restartapi = system.RestartApi(fw)
access_rules = AccessRuleIPv4Api(fw)
accessrulecli = AccessRuleCli(fw_cli)
user_status = users.UserStatusApi(fw)
user_setting = UsersettingApi(fw)



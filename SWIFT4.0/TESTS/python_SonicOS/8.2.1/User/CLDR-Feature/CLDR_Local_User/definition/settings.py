import os
import re
import sys
import copy
import time
import unittest

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from lib.modules.API import system
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts
from util.enhancedinfo import show_testcase_info
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from sslvpn.common_lib import netextender
from modules.ui.fw_page import FWPage
from modules.API import users
from lib.modules.API.network import AddressobjectsApi
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from lib.modules.API.sslvpn import SSLVPNClientSettingsAPI
from lib.modules.API.users import SSOApi, UsersettingApi, UserStatusApi, UserLocalApi
from networkdevice import Host
from concurrent.futures import ThreadPoolExecutor
from sslvpn.common_lib import virtualoffice_page

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/CLDR-Feature/CLDR_Local_User')


from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network  import InterfaceIPv4Api
from lib.modules.API.users import UserLocalApi


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    # TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/CLDR_Local_User/testplan/testplan.json'


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='cli-ssh')

local_user = UserLocalApi(fw_api)
license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
nx = netextender.NetextenderConnect(fw_api)
cp_nx = netextender.InstallNX()
address_objects = AddressobjectsApi(fw_api)
sslvpnserver = SSLVPNServerSettingsAPI(fw_api)
clientsetobj = SSLVPNClientSettingsAPI(fw_api)
user_local = UserLocalApi(fw_api)
user_settings = UsersettingApi(fw_api)
# users = UserLocalApi(fw_api)
localhost = Host('localhost')
static_pc1 = Params.testbed + '-PC1'
static_pc2 = Params.testbed + '-PC2'
static_client1 = Host(static_pc1)
static_client2 = Host(static_pc2)
admin_setting = system.AdminApi(fw_api)
user_status = users.UserStatusApi(fw_api)
fwobj = FWPage("https://192.168.168.168", "admin", "S0nic@uto")




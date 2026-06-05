from inspect import Parameter
import sys
import os
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'User/Guest_Users-TP349_2')

import re
import paramunittest
from nose_parameterized import parameterized

from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method

from runner.utils.assertion import Assertion
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from modules.API import system
from modules.API import users
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from lib.modules.API.sslvpn import SSLVPNClientSettingsAPI
from sslvpn.common_lib import virtualoffice_page
from sslvpn.common_lib import netextender
from collections import OrderedDict
from lib.modules.API import network
from lib.modules.API.network import AddressobjectsApi
from networkdevice import Host
from lib.modules.CLI.network  import InterfaceCli
from lib.modules.API.system import RestartApi
from lib.modules.CLI.system import LicenseCli

ip ="192.168.168.168"
fw = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='cli-ssh')
guest_user = users.UserGuestApi(fw)
local_user = users.UserLocalApi(fw)
user_status = users.UserStatusApi(fw)
user_setting = users.UsersettingApi(fw)
sslvpnserver = SSLVPNServerSettingsAPI(fw)
clientsetobj = SSLVPNClientSettingsAPI(fw)
diag_obj = system.DiagnosticApi(fw)
setting = system.SettingApi(fw)
configure_user = network.InterfaceIPv4Api(fw)
cp_nx = netextender.InstallNX()
address_objects = AddressobjectsApi(fw)
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)
interface = InterfaceCli(fw_cli)
license = LicenseCli(fw_cli)
restartapi = RestartApi(fw)
zone_obj = network.ZoneObjectsApi(fw)
# define path
class Parameter():
	FIREWALL = '192.168.168.168'
	X1_IP = '13.0.0.100'
	X1_GW = '13.0.0.1'
	X1_DNS1 = Params.G_DNS1
	X1_DNS2 = Params.G_DNS2
	X1_DNS3 = Params.G_DNS3

	TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/User/Guest_Users_TP349_2/testplan/Guest_Users_TP349_2.json'


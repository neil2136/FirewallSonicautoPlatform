import sys
import os
import copy
import time
import re
import pexpect

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts')

from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from modules.API import system,firewall
from lib.modules.API.system import AdminApi,RestartApi,SettingApi
from lib.modules.API.users import UserLocalApi,UserGuestApi,UserStatusApi
from lib.modules.API.system import DiagnosticApi
from modules.API import network
from lib.modules.API.log import LogMonitorApi
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from lib.modules.API.sslvpn import SSLVPNClientSettingsAPI
from lib.modules.API.sslvpn import SSLVPNVirtualOfficeAPI
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import AddressobjectsApi
from utm import FirewallCLI

OpenS = Openstack(Params.testbed)
class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
fw = Firewall('192.168.168.168', user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall('192.168.168.168', user='admin', password='sonicauto', supported_config_mode='cli-ssh')
admin_api = AdminApi(fw)
user_api = UserLocalApi(fw)
user_guest_api = UserGuestApi(fw)
tsr_ojb = DiagnosticApi(fw)
zone_obj = network.ZoneObjectsApi(fw)
user_status = UserStatusApi(fw)
restart_api = RestartApi(fw)
settingapi = SettingApi(fw)
log_obj = LogMonitorApi(fw)
address_objects = AddressobjectsApi(fw)
sslvpnserver = SSLVPNServerSettingsAPI(fw)
sslvpnvirtual = SSLVPNVirtualOfficeAPI(fw)
clientsetobj = SSLVPNClientSettingsAPI(fw)
interface = network.InterfaceIPv4Api(fw)
license = LicenseCli(fw_cli)
# define path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/User/Lockout_User_Accounts/testplan/testplan.json'
# PC SSH


static_pc = Params.testbed + '-PC1'
static_client = Host(static_pc)
url = "https://192.168.168.168"
sslvpn_url = "https://192.168.168.168:4433"
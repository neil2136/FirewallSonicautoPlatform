import os
import sys
import re
import copy
import time
from collections import OrderedDict

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall
from utm import FirewallAPI
from util.enhancedinfo import show_testcase_info
from lib.modules.CLI.dpissl import ClientSslCli
from lib.modules.CLI.system import LicenseCli, AdminCli
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.users import LdapApi, UserLocalApi, UsersettingApi, UserStatusApi
from lib.modules.API.users import RadiusApi,TacacsApi
from lib.modules.API.system import SettingApi, StatusApi, AdminApi
from modules.API import users
from modules.API import network

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Compromised_Pwd_Check_In_DMZ/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Compromised_Pwd_Check_In_DMZ/definition/')

os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
PC1 = os_obj.get_pc_default_gw_ip('PC1')
PC2 = os_obj.get_pc_default_gw_ip('PC2')

class Parameter():

    FIREWALL = '192.168.168.168'
    X1_DNS1 = '10.50.129.149'
    X1_DNS2 = '10.50.129.148'
    X1_IP = '10.10.0.100'
    X1_GW = '10.10.0.1'
    MASK = '255.255.255.0'
    X2_IP = '10.11.0.100'
    X2_GW = '10.11.0.1'

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Compromised_Pwd_Check_In_DMZ/testplan/CLDR_testplan.json'

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')
fw_cli_dmz = Firewall(Parameter.X2_IP, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')
LDAP_api_Login = Firewall(ip, user='test', password='password', supported_config_mode='api')

admini_cli = AdminCli(fw_cli)
license_cli = LicenseCli(fw_cli)
dpissl_obj = ClientSslCli(fw_cli)
user = UserLocalApi(fw_api)
https_enable = InterfaceIPv4Api(fw_api)
user_status = UserStatusApi(fw_api)
admin_setting = AdminApi(fw_api)
ldap = LdapApi(fw_api)
Radius_user = RadiusApi(fw_api)
Tacacs_user = TacacsApi(fw_api)
user_settings = UsersettingApi(fw_api)
interface = InterfaceIPv4Api(fw_api)
setting = SettingApi(fw_api)
status_api = StatusApi(fw_api)




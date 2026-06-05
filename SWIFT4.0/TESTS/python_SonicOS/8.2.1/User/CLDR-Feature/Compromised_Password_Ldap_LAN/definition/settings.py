import os
import sys
import re
import copy
import time
import unittest


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
from lib.modules.CLI.system import LicenseCli, AdminCli
from collections import OrderedDict

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Compromised_Password_Ldap_LAN/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Compromised_Password_Ldap_LAN/definition/')


from modules.API import users
from modules.API import network
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.users import LdapApi, UserLocalApi, UsersettingApi, UserStatusApi, UserLoginApi
from lib.modules.API.users import RadiusApi,TacacsApi
from lib.modules.API.system import SettingApi, StatusApi, AdminApi


os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
PC1 = os_obj.get_pc_default_gw_ip('PC1')

class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Compromised_Password_Ldap_LAN/testplan/compromised_pswd_lan.json'


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='cli-ssh')

admini_cli = AdminCli(fw_cli)
license = LicenseCli(fw_cli)
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
Local_User=UserLoginApi(headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')]),ip = '192.168.168.168', username = 'test', password = 'password')



logger.info("The Firewall LAN IP is {}".format(ip))
WAN_IP = Parameter.X1_IP
logger.info("Wan IP is {}".format(WAN_IP))
localhost = Host('localhost')
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)
netexurl1 = WAN_IP + ':' + '4433'
logger.info("The netexend url is {}".format(netexurl1))


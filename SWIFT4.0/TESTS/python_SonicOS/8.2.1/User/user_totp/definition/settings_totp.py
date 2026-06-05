import os
import re
import sys
import copy
import time
import unittest
import json
import pexpect
import pyotp
import requests
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from util.enhancedinfo import show_testcase_info
from collections import OrderedDict
import paramunittest
from pexpect import pxssh
from lib.modules.API.network import InterfaceIPv4Api,AddressobjectsApi
from lib.modules.API.users import UserLocalApi, LdapApi, UsersettingApi,RadiusApi
from lib.modules.API.system import AdminApi,RestartApi,TimeApi
from lib.modules.CLI.users import UsersStatusCli

from lib.modules.CLI.system import AdminCli
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI,SSLVPNClientSettingsAPI,SSLVPNPortalSettingsAPI
from concurrent.futures import ThreadPoolExecutor
from lib.modules.API.system import DiagnosticApi
from lib.modules.CLI.system import LicenseCli


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/sslvpn')

import pop3_client
from sslvpn.common_lib import netextender
from sslvpn.common_lib import virtualoffice_page
from sslvpn.common_lib import virtualoffice
from lib.ui_password import FWlogin

config_path = os.environ["PYTHON_SONICOS_HOME"] + "/User/user_totp/config"



class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/testplan/user_totp.json'

os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
localhost = Host('localhost')

ip = Parameter.FIREWALL
ldap_server_ip = '192.168.168.85'
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')




interface_ipv4 = InterfaceIPv4Api(fw_api)
cp_nx = netextender.InstallNX()
address_objects = AddressobjectsApi(fw_api)
sslvpnserver = SSLVPNServerSettingsAPI(fw_api)
clientsetobj = SSLVPNClientSettingsAPI(fw_api)
user_setting = UsersettingApi(fw_api)
nx = netextender.NetextenderConnect(fw_api)
user_local = UserLocalApi(fw_api)
admin_obj = AdminApi(fw_api)
portalsetobj = SSLVPNPortalSettingsAPI(fw_api)
cli_obj = AdminCli(fw_cli)
ldap = LdapApi(fw_api)
userstatus1 = UsersStatusCli(fw_cli)
diagnostic = DiagnosticApi(fw_api)
timeapi = TimeApi(fw_api)
localhost_1 = Host('localhost')
localhost_2 = Host('localhost')
static_pc1 = Params.testbed + '-PC2'
user_radius = RadiusApi(fw_api)
static_pc2 = Params.testbed + '-PC3'
static_client1 = Host(static_pc1)
static_client2 = Host(static_pc2)
fw_ui_obj = FWlogin("192.168.168.168", "admin", "password")
reboot_sys = RestartApi(fw_api)
lc = LicenseCli(fw_cli)


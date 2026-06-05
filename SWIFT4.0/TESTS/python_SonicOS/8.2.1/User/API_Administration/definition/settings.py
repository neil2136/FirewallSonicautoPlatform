import os
import re
import sys
import copy
import paramiko
import time
import unittest

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts
from util.enhancedinfo import show_testcase_info
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method

sys.path.append(os.environ["PYTHON_COMMON_HOME"])

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/API_Administration')

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')

from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.CLI.system import LicenseCli
from definition.ui_fw import FWPage

from modules.API import network
from modules.API import system
from modules.API import firewallsettings
from lib.modules.API.system import RestartApi
from lib.modules.API.system import SettingApi

class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/API_Administration/testplan/testplan.json'

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='api')
fw_cgi = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cgi')
fw_cli = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

url = "https://192.168.168.168" 
user = "admin" 
password = "password"
fw_ui = FWPage(url, user, password)

license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)

static_pc = Params.testbed + '-PC1'

Admin_settings = system.AdminApi(fw_api)
restartapi = RestartApi(fw_api)
setting_obj = SettingApi(fw_api)
Edit_users = system.SNMPApi(fw_api)
cloudbackup = system.CloudBackupApi
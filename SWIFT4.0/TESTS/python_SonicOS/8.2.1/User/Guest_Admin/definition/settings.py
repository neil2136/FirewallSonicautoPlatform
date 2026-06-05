import os
import re
import sys
import copy
import time
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
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
from runner.unittest.setup import Test, repeat_method
from collections import OrderedDict

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
#from modules.API import firewallsettings
from lib.modules.API import users,system
from lib.modules.CLI.system import LicenseCli
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Guest_Admin')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Guest_Admin/lib')
import ui_group


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = '10.50.129.149'
    X1_DNS2 = '10.50.129.148'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin/testplan/testplan.json'   


ip = '192.168.168.168'
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cgi = Firewall(ip, user='admin', password='password', supported_config_mode='cgi')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
headers = OrderedDict([('Accept', 'application/json'),
                                        ('Content-Type', 'application/json'),
                                        ('Accept-Encoding', 'application/json'),
                                        ('charset', 'UTF-8')])

guest_admin = users.UserLocalApi(fw_api)
user_status = users.UserStatusApi(fw_api)
user_guest = users.UserGuestApi(fw_api)
diagnostic = system.DiagnosticApi(fw_api)
reboot_sys = system.RestartApi(fw_api)
configure_user = network.InterfaceIPv4Api(fw_api)
license_fw = LicenseCli(fw_cli)
localhost = Host('localhost')
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)




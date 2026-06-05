import os
import re
import sys
import copy
import json
import time
import unittest
import urllib3
import requests
import paramiko
import pexpect
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Stronger_Password_Requirement_By_Default')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Stronger_Password_Requirement_By_Default/definition')

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.users import UserLocalApi
from lib.modules.API.system import AdminApi, SettingApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from ui_user import UIPage

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_GW = '192.168.168.1'
    X0_SUBNET = '192.168.168.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.168'
    X1_GW = '13.0.0.1'
    MASK = '255.255.255.0'
    WAN_IP = '13.0.0.169'
    LAN_IP = '192.168.168.169'

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Stronger_Password_Requirement_By_Default/testplan/testplan.json'
    

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='cli-ssh')


os_obj = Openstack(Params.testbed)
pc1 = Host('localhost')

ui_login = UIPage()
license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
user_local = UserLocalApi(fw_api)
admin_api = AdminApi(fw_api)
settings_obj = SettingApi(fw_api)
access_rules_ipv4 = AccessRuleIPv4Api(fw_api)

admin_json = {
            "administration": {
            "password": {
                "complexity": {
                        'type': 'alpha-and-numeric-and-symbols',
                        'upper_case': 1,
                        'lower_case': 1,
                        'digital': 1,
                        'symbolic': 1
                    },
                "constraints_apply_to": {
                    'builtin_admin': True,
                    'full_admins': True,
                    'limited_admins': True,
                    'local_users': True,
                    'guest_admins': True,
                    'system_admins': True,
                    'crypto_admins': True,
                    'audit_admins': True
                    }
               }
            }
        }
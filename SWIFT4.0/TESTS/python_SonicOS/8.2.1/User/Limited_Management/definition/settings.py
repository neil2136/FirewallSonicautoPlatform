import os
import sys
import re

from runner.unittest.suite import UnittestSuite
import unittest
from runner.settings import Params, logger
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
from utm import Firewall

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.users import UserLocalApi, UserLoginApi

testplan = os.environ["PYTHON_SONICOS_HOME"] + '/User/'
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Limited_Management')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Limited_Management/definition')


class Parameter:
    FIREWALL = '192.168.168.168'
    TESTPLAN = testplan + 'Limited_Management/testplan/limited_management.json'
    X0_IP = '192.168.168.168'
    X0_HOST = '192.168.168.199'
    X1_HOST = '172.16.1.101'


fw = Firewall(Parameter.FIREWALL,
              user='admin',
              password=Params.G_NEW_PASSWORD)

# case 1
add_guest_user = {
    'action': 'add',
    'username': 'guestuser',
    'userpassword': Params.G_NEW_PASSWORD
}
add_guest_member = {
    'action': add_guest_user['action'],
    'username': add_guest_user['username'],
    'userpassword': add_guest_user['userpassword'],
    'member_of': ['Guest Services']
    # member:SonicWALL Administrators/Content Filtering Bypass/Limited Administrators
    # /SSLVPN Services/SonicWALL Read-Only Admins/Guest Services/
}
guest_group_name = add_guest_member['member_of'][0]
guest_user_name = add_guest_user['username']

# case 2
add_limit_user = {
    'action': 'add',
    'username': 'limituser',
    'userpassword': Params.G_NEW_PASSWORD
}
add_limit_member = {
    'action': add_limit_user['action'],
    'username': add_limit_user['username'],
    'userpassword': add_limit_user['userpassword'],
    'member_of': ['Limited Administrators']
}
limit_group_name = add_limit_member['member_of'][0]
limit_user_name = add_limit_user['username']

# case 3
add_limit_admin = {
    'action': 'add',
    'username': 'limitadmin',
    'userpassword': Params.G_NEW_PASSWORD
}
add_limit_admin_member = {
    'action': add_limit_admin['action'],
    'username': add_limit_admin['username'],
    'userpassword': add_limit_admin['userpassword'],
    'member_of': ['Limited Administrators']
}
X0_static_opt = {
    'if': 'X0',
    'zone': 'LAN',
    'ip': Parameter.X0_IP,
    'netmask': '255.255.255.0',
    'mgmt_https': True,
    'mgmt_ping': True,
    'mgmt_ssh': True,
    "user_https": True
}
local_user_config = {
    "user": {
        "user": [
            {
                "name": "localuser111",
                "password": Params.G_NEW_PASSWORD
            }
        ]
    }
}
guest_user_config = {
    "user": {
        "guest": {
            "user": [
                {
                    "name": "guest11",
                    "comment": "Auto-Generated",
                    "password": Params.G_NEW_PASSWORD,
                    "enable": True,
                    "login_uniqueness": True,
                    "prune_on_expiry": True,
                    "activate_on_login": False,
                    "account_lifetime": {"days": 7},
                    "idle_timeout": {"minutes": 10},
                    "quota_cycle": {},
                    "session_lifetime": {"hours": 1},
                    "limit": {"receive": 0, "transmit": 0}
                }
            ]
        }
    }
}

interface = InterfaceIPv4Api(fw)
userlocal = UserLocalApi(fw)
limituserlogin = UserLoginApi(headers=None,
                              ip=Parameter.FIREWALL,
                              username=add_limit_admin['username'],
                              password=add_limit_admin['userpassword'])

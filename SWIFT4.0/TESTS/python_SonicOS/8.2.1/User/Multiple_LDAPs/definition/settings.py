import os
import re
import sys
import copy
import time
import unittest

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Multiple_LDAPs/testcases')

from modules.API import network
from modules.API import users
from lib.modules.API.users import UsersettingApi
from modules.CLI.system import LicenseCli

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Multiple_LDAPs')
from definition import ui_tcs


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Multiple_LDAPs/testplan/multiple_ldaps.json'


ip = '192.168.168.168'
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

user_ldap = users.LdapApi(fw_api)
user_auth_partition = users.AuthPartitionsApi(fw_api)
local_user = users.UserLocalApi(fw_api)
interface = network.InterfaceIPv4Api(fw_api)
user_setting = UsersettingApi(fw_api)
password = Params.G_NEW_PASSWORD
ui_obj = ui_tcs.Ui_Tests("https://192.168.168.168", "admin", password)

ldap_server = {
    "user": {
        "ldap": {
            "server": [{
                "host": '192.168.168.85',
                "enable": True,
                "role": {
                    "primary": True
                },
                "port": 389,
                "timeout": {
                    "server": 10,
                    "operation": 5
                },
                "use_tls": False,
                "schema": "microsoft-active-directory",
                "user_class": "user",
                "user_attribute": {
                    "logon_name": "sAMAccountName",
                    "qualified_logon_name": "userPrincipalName",
                    "group_membership": "memberOf",
                    "additional_group_id": "primaryGroupID",
                    "use_additional_group_id": False,
                    "framed_ip_address": "msRADIUSFramedIPAddress"
                },
                "user_group_class": "group",
                "user_group_attribute": {
                    "member": {
                        "type": "distinguished-name",
                        "name": "member"
                    },
                    "additional_group_match": "primaryGroupToken"
                },
                "directory": {
                    "primary_domain": "os-autosnwl.com",
                    "users_tree": [{
                        "name": "os-autosnwl.com/Users"
                    }],
                    "user_groups_tree": [{
                        "name": "os-autosnwl.com/Users"
                    }]
                },
                "bind": {
                    "acct": {
                        "name": "Administrator",
                        "location": "os-autosnwl.com/Users"
                    }
                },
                "bind_password": "password",
                "referred_bind_with_account": "local"
            }]
        }
    }
}

ldap_server2 = {
    "user": {
        "ldap": {
            "server": [{
                "host": '192.168.168.86',
                "enable": True,
                "role": {
                    "secondary": True
                },
                "port": 389,
                "timeout": {
                    "server": 10,
                    "operation": 5
                },
                "use_tls": False,
                "schema": "microsoft-active-directory",
                "user_class": "user",
                "user_attribute": {
                    "logon_name": "sAMAccountName",
                    "qualified_logon_name": "userPrincipalName",
                    "group_membership": "memberOf",
                    "additional_group_id": "primaryGroupID",
                    "use_additional_group_id": False,
                    "framed_ip_address": "msRADIUSFramedIPAddress"
                },
                "user_group_class": "group",
                "user_group_attribute": {
                    "member": {
                        "type": "distinguished-name",
                        "name": "member"
                    },
                    "additional_group_match": "primaryGroupToken"
                },
                "directory": {
                    "primary_domain": "wsv2.os-autosnwl.com",
                    "users_tree": [{
                        "name": "wsv2.os-autosnwl.com/Users"
                    }],
                    "user_groups_tree": [{
                        "name": "wsv2.os-autosnwl.com/Users"
                    }]
                },
                "bind": {
                    "acct": {
                        "name": "Administrator",
                        "location": "wsv2.os-autosnwl.com/Users"
                    }
                },
                "bind_password": "password",
                "referred_bind_with_account": "local"
            }]
        }
    }
}

backup_server = {
    "user": {
        "ldap": {
            "server": [
                {
                    "host": "192.168.168.105",
                    "enable": True,
                    "role": {
                        "backup": True
                    },
                    "backup_for": "192.168.168.85",
                    "same_bind_credentials": True
                }
            ]
        }
    }
}

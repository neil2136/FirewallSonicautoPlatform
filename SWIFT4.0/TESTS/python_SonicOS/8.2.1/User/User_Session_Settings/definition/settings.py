import os
import re
import sys
import copy
import time
import unittest
import paramiko

from util.openstack import Openstack
from modules.ui.ui_wrapper import Browser
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
from modules.API import users
from modules.ui import appflow_ui
from collections import OrderedDict
from networkdevice import Host
from lib.modules.API.system import DiagnosticApi
from lib.modules.API.accessrule import AccessRuleIPv4Api

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/User_Session_Settings')


from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network  import InterfaceIPv4Api
from lib.modules.API.users import UserLocalApi


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    SSO_SERV = '192.168.168.65'
    PC2_USER = 'openstack_win10'
    PC2_UP = 'sonicwall'
    PC2_DGW = '192.168.168.1'
    DOMAIN = 'os-autosnwl'
    DOMAIN_AU = 'administrator'
    DOMAIN_AP = 'password'
    DOMAIN_U1 = 'test'
    DOMAIN_UP1 = 'password'
    DOMAIN_U2 = 'sslvpntest'
    DOMAIN_UP2 = 'password'
    WORKSTATION_IP = '192.168.168.62'
    WORKSTATION_U = 'openstack_win10'
    WORKSTATION_P = 'sonicwall'
    WAN_PC4_IP = '13.0.0.140'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/User_Session_Settings/testplan/User_Session_Settings_testplans.json'


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='cli-ssh')

os_obj = Openstack(Params.testbed)
pc1 = Host('localhost')

local_user = UserLocalApi(fw_api)
license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
user_setting = users.UsersettingApi(fw_api)
local_user = users.UserLocalApi(fw_api)
user_status = users.UserStatusApi(fw_api)
tsr_ojb = DiagnosticApi(fw_api)
user_sso = users.SSOApi(fw_api)
user_ldap = users.LdapApi(fw_api)
accessrule = AccessRuleIPv4Api(fw_api)
app_flow = appflow_ui.AppFlow(ip, user='admin', password='S0nic@uto')


lan_wan_rule = {
            'name': 'Default Access Rule',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {},
        }
ldap_server = {
    "user": {
        "ldap": {
            "server": [{
                "host": f'{Parameter.SSO_SERV}',
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
                    "primary_domain": f"{Parameter.DOMAIN}.com",
                    "users_tree": [{
                        "name": f"{Parameter.DOMAIN}.com/Users"
                    }],
                    "user_groups_tree": [{
                        "name": f"{Parameter.DOMAIN}.com/Users"
                    }]
                },
                "bind": {
                    "acct": {
                        "name": f"{Parameter.DOMAIN_AU}",
                        "location": f"{Parameter.DOMAIN}.com/Users"
                    }
                },
                "bind_password": f"{Parameter.DOMAIN_AP}",
                "referred_bind_with_account": "local"
            }]
        }
    }
}



# static_pc1 = Params.testbed + '-PC1'
# pc = Host(static_pc1)




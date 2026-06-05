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

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Transparent_Authentication')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Transparent_Authentication/definition')

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api, ZoneObjectsApi
from lib.modules.API.users import SSOApi, UsersettingApi, UserStatusApi, UserLocalApi, LdapApi
from lib.modules.API.system import DiagnosticApi, RestartApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.log import LogSettingsApi, LogCategoryApi, LogMonitorApi
from lib.modules.API.securityservices import IPSApi, AntiSpywareApi
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


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
    TESTPLAN = os.environ[
                   "PYTHON_SONICOS_HOME"] + '/User/Transparent_Authentication/testplan/transparent_authentication.json'


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

os_obj = Openstack(Params.testbed)
pc1 = Host('localhost')

license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
user_sso = SSOApi(fw_api)
user_setting = UsersettingApi(fw_api)
user_status = UserStatusApi(fw_api)
accessrule = AccessRuleIPv4Api(fw_api)
diag_api = DiagnosticApi(fw_api)
user_ldap = LdapApi(fw_api)
user_local = UserLocalApi(fw_api)
log_settings = LogSettingsApi(fw_api)
log_category = LogCategoryApi(fw_api)
log_monitor = LogMonitorApi(fw_api)
ips_api = IPSApi(fw_api)
antispyware_api = AntiSpywareApi(fw_api)
zone_object = ZoneObjectsApi(fw_api)
restart_api = RestartApi(fw_api)

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

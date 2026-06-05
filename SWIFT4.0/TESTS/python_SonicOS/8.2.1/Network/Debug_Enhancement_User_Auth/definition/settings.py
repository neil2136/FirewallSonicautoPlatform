import os
import sys
import gzip
import io
import zipfile
import time
import paramunittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])

from lib.modules.CLI import network
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi
from lib.modules.API.log import SyslogSettingsApi
from lib.modules.API.diag import DiagApi
from modules.API import users
from modules.CLI.system import LicenseCli
from modules.API.users import SSOApi
from modules.API.users import UsersettingApi, RadiusApi, TacacsApi
from networkdevice import Host

from util.enhancedinfo import show_testcase_info
from utm import Firewall
from util.openstack import Openstack

import unittest
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')

PC3_login = Host(PC3_ETH0_IP)

console_name_before_command = "command_before"
console_name_after_command = "command_after"
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                'Network/Debug_Enhancement_User_Auth/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/Debug_Enhancement_User_Auth/')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
           '/Network/Debug_Enhancement_User_Auth/testplan/Debug_Enhancement_User_Auth.json'
Console_File_Location = '/tmp/console'
Console_File_Location_Before_Commod = Console_File_Location + console_name_before_command
Console_File_Location_After_Commod = Console_File_Location + console_name_after_command


# configure fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_SUBNET = '12.12.1.0'
    MASK = "255.255.255.0"
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    LDAP_SEVER = "192.168.168.85"


# Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fwcli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

diag_api = DiagApi(fw)
interfaceapi = InterfaceIPv4Api(fw)
user_ldap = users.LdapApi(fw)
usersetting = UsersettingApi(fw)
syslog_api = SyslogSettingsApi(fw)
ao_api = AddressobjectsApi(fw)
radius_api = RadiusApi(fw)
sso_api = SSOApi(fw)
tacacs_api = TacacsApi(fw)

interfacecli = network.InterfaceCli(fwcli)
licensecli = LicenseCli(fwcli)

ldap_server = {
    "user": {
        "ldap": {
            "server": [{
                "host": Parameter.LDAP_SEVER,
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
                        "name": "ldap_auto_1",
                        "location": "os-autosnwl.com/Users"
                    }
                },
                "bind_password": "S0nic@uto",
                "referred_bind_with_account": "local"
            }]
        }
    }
}
ldap_server_not_access = {
    "user": {
        "ldap": {
            "server": [{
                "host": Parameter.LDAP_SEVER,
                "enable": True,
                "role": {
                    "primary": True
                },
                "port": 389,
                "timeout": {
                    "server": 10,
                    "operation": 5
                },
                "use_tls": False
            }]
        }
    }
}
ldap_server_with_domain = {
    "user": {
        "ldap": {
            "server": [{
                "host": "ForestDnsZones.ldapqa.com",
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
                        "name": "ldap_auto_1",
                        "location": "os-autosnwl.com/Users"
                    }
                },
                "bind_password": "S0nic@uto",
                "referred_bind_with_account": "local"
            }]
        }
    }
}

radius_server = {
    "enable": True,
    "host": "10.8.141.162",
    "port_num": 1812,
    "secret": "12345678",
}

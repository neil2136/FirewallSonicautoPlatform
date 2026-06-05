import os
import sys
import re
import time
import copy
import requests
from collections import OrderedDict
import pexpect
from pexpect import pxssh

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import securityservices
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import log
from modules.API import users
from lib.modules.API import network, firewall, system, users, log
from lib.modules.API.users import LdapApi
from lib.modules.API.users import UsersettingApi
from lib.modules.API.network import AddressobjectsApi
from lib.modules.API.users import RadiusApi,TacacsApi
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from lib.modules.API.sslvpn import SSLVPNClientSettingsAPI
from lib.modules.API.accessrule import AccessRuleIPv4Api
from modules.CLI.firewall import AccessRuleCli

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Combinations/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Combinations')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Combinations/definition')

from ui_user import FWPage
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/sslvpn/')
from sslvpn.common_lib import netextender

local_host = Host('localhost')

FIREWALL = '192.168.168.168'
X1_IP = '172.17.1.168'
X1_GW = '172.17.1.1'
X1_DNS1 = '10.9.1.40'
X1_DNS2 = '10.190.202.200'
X2_IP = '14.1.1.168'
MASK = '255.255.255.0'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Combinations/testplan/auth_combinations.json'
ip = FIREWALL
fw = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
interface_obj = network.InterfaceIPv4Api(fw)
lc = LicenseCli(fw_cli)
log_obj = log.LogMonitorApi(fw)
log_set = log.LogCategoryApi(fw)
gav = securityservices.GAV(fw)

user_setting = UsersettingApi(fw)
local_user = users.UserLocalApi(fw)
user_ldap = LdapApi(fw)
address_objects = AddressobjectsApi(fw)
user_radius = RadiusApi(fw)
user_tacacs = TacacsApi(fw)
sslvpnserver = SSLVPNServerSettingsAPI(fw)
clientsetobj = SSLVPNClientSettingsAPI(fw)
cp_nx = netextender.InstallNX()
nx = netextender.NetextenderConnect(fw)
static_pc = Params.testbed + '-PC1'
static_client = Host(static_pc)
accessrulecli = AccessRuleCli(fw_cli)
access_rules = AccessRuleIPv4Api(fw)
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

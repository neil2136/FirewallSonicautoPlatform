import os
import sys
import re
import copy
import time
import random
import json

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network,firewall,system,users,object,log


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_Enhancements')
print(sys.path)

FIREWALL = '192.168.168.168'
X1 = '12.12.1.100'
X1_GW = '12.12.1.1'
Mask = '255.255.255.0'
LAN2 = '192.168.168.223'
sso_ip = '9.9.9.9'
sso_ip_2 = '8.8.8.0'
sso_hostname = 'newaddssoagent'
sso_default_port = 2258
sso_new_port = 2256
new_max_requests=16
wan_pc_ip = '12.12.1.3'

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_Enhancements/testplan/SSO_Enhancements.json'

os_obj = Openstack(Params.testbed)
SSO_CLIENT1_lanip = os_obj.get_node_interface_ip('PC_SSO_CLIENT1','eth0')
SSO_CLIENT1_wanip = os_obj.get_node_interface_ip('PC_SSO_CLIENT1','eth1')
SSO_CLIENT2_lanip = os_obj.get_node_interface_ip('PC_SSO_CLIENT2','eth0')
SSO_CLIENT2_wanip = os_obj.get_node_interface_ip('PC_SSO_CLIENT2','eth1')
ldap_host = os_obj.get_node_interface_ip('PC3','eth0')
service_agent1 = ldap_host
service_agent2 = os_obj.get_node_interface_ip('PC4','eth0')


fw = Firewall(FIREWALL, user='admin', password='S0nic@uto', supported_config_mode='api')

fw_cli = Firewall(FIREWALL, user='admin', password='S0nic@uto', supported_config_mode='cli-ssh')





interface_ipv4 = network.InterfaceIPv4Api(fw)
user_settings_obj = users.UsersettingApi(fw)
user_sso_obj = users.SSOApi(fw)
user_local_obj = users.UserLocalApi(fw)
ldap_obj = users.LdapApi(fw)
user_status = users.UserStatusApi(fw)
log_config = log.LogCategoryApi(fw)
zone_obj = network.ZoneObjectsApi(fw)
access_rules_obj = firewall.AccessRuleApi(fw)
ao_obj = network.AddressobjectsApi(fw)
ag_obj = object.AddressObjectGroupApi(fw)
so_obj = network.ServiceObjectApi(fw)
sg_obj = network.ServiceGroupApi(fw)
log_obj = log.LogMonitorApi(fw)
servicegroupapi = network.ServiceGroupApi(fw)



ldap_server = {
	"user": {
		"ldap": {
			"server": [{
				"host": ldap_host,
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
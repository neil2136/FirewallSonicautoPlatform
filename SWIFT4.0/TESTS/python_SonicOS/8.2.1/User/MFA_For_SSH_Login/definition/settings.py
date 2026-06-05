import os
import sys
import re
import time
import copy
import pyotp
import requests
import json

import unittest
import paramunittest
from nose_parameterized import parameterized
from pexpect import pxssh

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
from lib.modules.API import network, firewall, system, users,log
from lib.modules.API.log import LogMonitorApi, LogCategoryApi, LogSettingsApi, LogAutomationApi

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/MFA_For_SSH_Login/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/MFA_For_SSH_Login')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/MFA_For_SSH_Login/lib/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/sslvpn')
print(sys.path)
import pop3_client
from common_lib import netextender
from common_lib import virtualoffice_page

from definition.ssh_login import *
from definition.ssh_totp_login import *
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.network  import InterfaceCli
from lib.modules.API.network import AddressobjectsApi
from lib.modules.CLI.users import UsersStatusCli
from lib.modules.API.users import UserLocalApi
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from lib.modules.API.sslvpn import SSLVPNClientSettingsAPI
from lib.modules.API.users import LdapApi
from lib.modules.API.users import UsersettingApi
from lib.modules.API.users import RadiusApi
from lib.modules.API.system import TimeApi
from lib.modules.API.system import AdminApi
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
localhost = Host('localhost')

PC2_LOGIN_IP = Host(os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth1'))

FIREWALL = '192.168.168.168'
X1_IP = '172.17.1.168'
X1_IP_TMP = '172.17.1.169'
X1_GW = '172.17.1.1'
X1_DNS1 = Params.G_DNS1
X1_DNS2 = Params.G_DNS2
X2_IP = '14.1.1.168'
MASK = '255.255.255.0'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/MFA_For_SSH_Login/testplan/testplan.json'
config_path = os.environ["PYTHON_SONICOS_HOME"] + "/User/MFA_For_SSH_Login/config"
ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
license = LicenseCli(fw_cli)
interface_obj = network.InterfaceIPv4Api(fw_api)
local_user = users.UserLocalApi(fw_api)
admin_user=AdminApi(fw_api)
log_obj = LogMonitorApi(fw_api)
accessrule_api = firewall.AccessRuleApi(fw_api)
log_set = LogCategoryApi(fw_api)
log_settings = LogSettingsApi(fw_api)
logautomationapi = LogAutomationApi(fw_api)

static_pc = Params.testbed + '-PC1'
static_client = Host(static_pc)

static_pc2 = Params.testbed + '-DUT-X1-GW-PC'
PC2_login = Host(static_pc2)



###########################

address_objects = AddressobjectsApi(fw_api)
time_obj = TimeApi(fw_api)
sslvpnserver = SSLVPNServerSettingsAPI(fw_api)
clientsetobj = SSLVPNClientSettingsAPI(fw_api)

user_ldap = LdapApi(fw_api)
user_setting = UsersettingApi(fw_api)
user_local = UserLocalApi(fw_api)
user_radius = RadiusApi(fw_api)


# userstatus1 = UsersStatusCli(fw_cli)

cp_nx = netextender.InstallNX()
nx = netextender.NetextenderConnect(fw_api)

#Parameter assigned to be used through out.
logger.info("The Firewall LAN IP is {}".format(ip))
WAN_IP = X1_IP
logger.info("Wan IP is {}".format(WAN_IP))

netexurl1 = WAN_IP + ':' + '4433'
logger.info("The netexend url is {}".format(netexurl1))


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

default_acl_dict = {
    # "uuid": target_rule_uuid,
    "name": "Default Access Rule",
    "enable": True,
    "from": "LAN",
    "to": "DMZ",
    "action": "Allow",
    "source": {
        "address": {
            "any": True
        },
        "port": {
            "any": True
        }
    },
    "service": {
        "any": True
    },
    "destination": {
        "address": {
            "any": True
        }
    },
    "schedule": {
        "always_on": True
    },
    "users": {
        "included": {
            "all": True
        },
        "excluded": {
            "none": True
        }
    },
    "comment": "Modified",
    "fragments": True,
    "logging": True,
    "sip": False,
    "h323": False,
    "flow_reporting": False,
    "botnet_filter": False,
    "geo_ip_filter": {
        "enable": False,
        "global": True
    },
    "block": {
        "countries": {
            "unknown": False
        }
    },
    "packet_monitoring": False,
    "management": False,
    "max_connections": 100,
    "priority": {
        "manual": {
            "value": 7
        }
    },
    "tcp": {
        "timeout": 15,
        "urgent": False
    },
    "udp": {
        "timeout": 30
    },
    "connection_limit": {
        "source": {},
        "destination": {}
    },
    "dpi": True,
    "dpi_ssl": {
        "client": True,
        "server": True
    },
    "redirect_unauthenticated_users_to_log_in": True,
    "quality_of_service": {
        "class_of_service": {},
        "dscp": {
            "preserve": True
        }
    }
}
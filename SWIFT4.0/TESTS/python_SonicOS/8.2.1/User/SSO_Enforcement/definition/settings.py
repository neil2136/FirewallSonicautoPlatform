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
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enforcement')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enforcement/definition')

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api, ZoneObjectsApi, DHCPServerApi, AddressobjectsApi
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.API.users import SSOApi, UsersettingApi, UserStatusApi, UserLocalApi, LdapApi
from lib.modules.API.system import DiagnosticApi, RestartApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.log import LogSettingsApi, LogCategoryApi, LogMonitorApi
from lib.modules.API.securityservices import IPSApi, AntiSpywareApi
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X2_IP = '192.168.3.168'
    X2_GW = '192.168.3.1'
    X2_SUBNET = '192.168.3.0'
    MASK = '255.255.255.0'
    SSO_SERV = '192.168.168.120'
    PC2_USER = 'openstack_win10'
    PC2_UP = 'sonicwall'
    PC2_LAN_DGW = '192.168.168.1'
    PC3_DMZ_DGW = '192.168.3.1'
    DOMAIN = 'os-autosnwl'
    DOMAIN_AU = 'administrator'
    DOMAIN_AP = 'password'
    DOMAIN_U1 = 'test'
    DOMAIN_UP1 = G_PASSWORD_NEW
    DOMAIN_U2 = 'sslvpntest'
    DOMAIN_UP2 = 'password'
    LAN_IP = '192.168.168.121'
    DMZ_IP = '192.168.3.140'
    WORKSTATION_U = 'openstack_win10'
    WORKSTATION_P = 'sonicwall'
    PC5_WAN_IP = '12.12.1.150'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_Enforcement/testplan/testplan.json'


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')
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
dhcpserverapi = DHCPServerApi(fw_api)

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
dmz_lan_rule = {
            'name': 'Default Access Rule',
            'from': 'DMZ',
            'to': 'LAN',
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
                "bind_password": "S0nic@uto",
                "referred_bind_with_account": "local"
            }]
        }
    }
}
signature = {
            "intrusion_prevention": {
                "policy": [{
                    "id": 293,
                    "included": {
                        "ip": {
                            "category": True
                        },
                        "users": {
                            "group": "Everyone"
                        }
                    },
                    "excluded": {
                        "ip": {
                            "category": True
                        },
                        "users": {
                            "category": True
                        }
                    },
                    "schedule": {
                        "category": True
                    },
                    "log_redundancy": {
                        "category": True
                    },
                    "category": "ICMP",
                    "name": "PING",
                    "prevention": {},
                    "detection": {}
                }]
            }
        }


dynamic_scope_base = {
    "dhcp_server":
        {"ipv4": {
            "scope": {
                "dynamic": [
                    {
                        "from": "",
                        "to": "",
                        "enable": True,
                        "lease_time": 60,
                        "default_gateway": "",
                        "netmask": "255.255.255.0",
                        "comment": "",
                        "domain_name": "",
                        "dns": {"server": {"inherit": True}},
                    }
                ]
            }
        }
        }
}

x0_dhcp_edit_dict1 = {
    "from": "192.168.168.120",
    "to": "192.168.168.121",
    "default_gateway": "192.168.168.168"
}

x2_dhcp_dict = {
    "from": "192.168.3.140",
    "to": "192.168.3.140",
    "default_gateway": "192.168.3.168"
}


sso_agent = {
 "user": {
  "sso": {
   "agent": [
    {
     "host": "192.168.168.120",
     "enable": True,
     "port": 2258,
     "timeout": 5,
     "retries": 3,
     "max_requests": 3,
     "shared_key": "225abc"
    }
   ]
  }
 }
}

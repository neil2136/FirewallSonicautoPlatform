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
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enforcement_TP2560')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enforcement_TP2560/definition')

from lib.modules.CLI.system import LicenseCli, AdminCli
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


class Parameter():
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    MASK = '255.255.255.0'
    SSO_SERV = '192.168.168.120'
    DOMAIN = 'os-autosnwl'
    DOMAIN_AU = 'ldap_auto_1'
    DOMAIN_AP = 'S0nic@uto'
    DOMAIN_U1 = 'ldap_auto_1'
    DOMAIN_UP1 = 'S0nic@uto'
    DOMAIN_U2 = 'sslvpntest'
    DOMAIN_UP2 = 'password'
    LAN_IP = '192.168.168.110'
    VPN_IP = '172.16.1.140'
    WORKSTATION_U = 'openstack_win10'
    WORKSTATION_P = 'sonicwall'
    PC5_WAN_IP = '12.12.1.150'
     
    R_X0_IP = '172.16.1.101'
    R_X0_SUBNET = '172.16.1.0'
    R_X1_IP = '12.12.1.201'
    R_X1_GW = X1_GW

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_Enforcement_TP2560/testplan/testplan.json'

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
r_fw_api = Firewall(Parameter.R_X1_IP, user='admin', password='sonicauto', supported_config_mode='api')
r_fw_cli = Firewall(Parameter.R_X1_IP, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

os_obj = Openstack(Params.testbed)
pc1 = Host('localhost')

license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
user_sso = SSOApi(fw_api)
user_setting = UsersettingApi(fw_api)
user_status = UserStatusApi(fw_api)
accessrule = AccessRuleIPv4Api(fw_api)
r_accessrule = AccessRuleIPv4Api(r_fw_api)
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
r_dhcpserverapi = DHCPServerApi(r_fw_api)
address_objects = AddressobjectsApi(fw_api)
r_address_objects = AddressobjectsApi(r_fw_api)
address_objects_cli = AddressObjectCli(fw_cli)
r_address_objects_cli = AddressObjectCli(r_fw_cli)
vpn_cli = VpnBaseSettingsCli(fw_cli)
r_vpn_cli = VpnBaseSettingsCli(r_fw_cli)
r_admin_cli = AdminCli(r_fw_cli)

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
                "bind_password": f"{Parameter.DOMAIN_AP}",
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
    "to": "192.168.168.120",
    "default_gateway": "192.168.168.168"
}
r_x0_dhcp_edit_dict1 = {
    "from": "172.16.1.140",
    "to": "172.16.1.140",
    "default_gateway": "172.16.1.101"
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


local_vpn_obj = {
    "object_type": "network",
    "name": "local_vpn",
    "zone": "VPN",
    "value": Parameter.R_X0_SUBNET+','+Parameter.MASK,
}
remote_lan_obj = {
    "object_type": "network",
    "name": "local_vpn",
    "zone": "LAN",
    "value": Parameter.R_X0_SUBNET+','+Parameter.MASK,
}
remote_vpn_lan = {
    "object_type": "network",
    "name": "remote_vpn_lan",
    "zone": "VPN",
    "value": Parameter.X0_SUBNET+','+Parameter.MASK,
}
local_group = {
    "name": "local_group",
    "version": "ipv4",
    "objects": ['ipv4 "X0 Subnet"']
}
remote_group = {
    "name": "remote_group",
    "version": "ipv4",
    "objects": ['ipv4 ' + remote_vpn_lan['name']]
}

local_vpn = {
    'type'                     : 'site-to-site',
    'name'                     : 'local_vpn_1',
    'mode'                     : 'shared-secret',
    'secret'                   : 'password',
    'pri_gate'                 :  Parameter.R_X1_IP,
    'local_ike_id'             : 'ipv4 1.1.1.1',
    'peer_ike_id'              : 'ipv4 2.2.2.2',
    'local_net_type'           : 'group',
    'remote_net_type'          : 'name',
    'local_network'            : local_group['name'],
    'remote_network'           : local_vpn_obj['name'],
    'proposal ike exchange'    : 'ikev2',
    'proposal ike encryption'  : 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'keep_alive'               : True,
}
local_lan_vpn_cmds = ['configure']
local_lan_vpn_cmds.append('vpn policy ' + local_vpn['type'] + ' ' + local_vpn['name'])
local_lan_vpn_cmds.append('network local ' + local_vpn['local_net_type'] + ' ' + local_vpn['local_network'])
local_lan_vpn_cmds.append('network remote destination-network ' + \
                          local_vpn['remote_net_type'] + ' ' + local_vpn['remote_network'])
local_lan_vpn_cmds.append('gateway primary ' + local_vpn['pri_gate'])
local_lan_vpn_cmds.append('proposal ike exchange ' + local_vpn['proposal ike exchange'])
local_lan_vpn_cmds.append('proposal ike encryption ' + local_vpn['proposal ike encryption'])
local_lan_vpn_cmds.append('proposal ike authentication ' + local_vpn['proposal ike authentication'])
local_lan_vpn_cmds.append('proposal ipsec encryption ' + local_vpn['proposal ipsec encryption'])
local_lan_vpn_cmds.append('proposal ipsec authentication ' + local_vpn['proposal ipsec authentication'])
local_lan_vpn_cmds.append('auth-method ' + local_vpn['mode'])
local_lan_vpn_cmds.append('ike-id local ' + local_vpn['local_ike_id'])
local_lan_vpn_cmds.append('ike-id peer ' + local_vpn['peer_ike_id'])
local_lan_vpn_cmds.append('shared-secret ' + local_vpn['secret'])
local_lan_vpn_cmds.append('commit')
local_lan_vpn_cmds.append('end')
local_lan_vpn_cmds.append('end')

remote_vpn = {
    'type'                     : 'site-to-site',
    'name'                     : 'remote_vpn_1',
    'mode'                     : 'shared-secret',
    'secret'                   : 'password',
    'pri_gate'                 :  Parameter.X1_IP,
    'local_ike_id'             : 'ipv4 2.2.2.2',
    'peer_ike_id'              : 'ipv4 1.1.1.1',
    'local_net_type'           : 'name',
    'remote_net_type'          : 'group',
    'local_network'            : local_vpn_obj['name'],
    'remote_network'           : remote_group['name'],
    'proposal ike exchange'    : 'ikev2',
    'proposal ike encryption'  : 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ipsec encryption': 'aes-128', 
    'proposal ipsec authentication': 'sha-1',
    'keep_alive'               : False,
}
remote_lan_vpn_cmds = ['configure']
remote_lan_vpn_cmds.append('vpn policy ' + remote_vpn['type'] + ' ' + remote_vpn['name'])
remote_lan_vpn_cmds.append('network local ' + remote_vpn['local_net_type'] + ' ' + remote_vpn['local_network'])
remote_lan_vpn_cmds.append('network remote destination-network ' + \
                          remote_vpn['remote_net_type'] + ' ' + remote_vpn['remote_network'])
remote_lan_vpn_cmds.append('gateway primary ' + remote_vpn['pri_gate'])
remote_lan_vpn_cmds.append('proposal ike exchange ' + remote_vpn['proposal ike exchange'])
remote_lan_vpn_cmds.append('proposal ike encryption ' + remote_vpn['proposal ike encryption'])
remote_lan_vpn_cmds.append('proposal ike authentication ' + remote_vpn['proposal ike authentication'])
remote_lan_vpn_cmds.append('proposal ipsec encryption ' + remote_vpn['proposal ipsec encryption'])
remote_lan_vpn_cmds.append('proposal ipsec authentication ' + remote_vpn['proposal ipsec authentication'])
remote_lan_vpn_cmds.append('auth-method ' + remote_vpn['mode'])
remote_lan_vpn_cmds.append('ike-id local ' + remote_vpn['local_ike_id'])
remote_lan_vpn_cmds.append('ike-id peer ' + remote_vpn['peer_ike_id'])
remote_lan_vpn_cmds.append('shared-secret ' + remote_vpn['secret'])
remote_lan_vpn_cmds.append('commit')
remote_lan_vpn_cmds.append('end')
remote_lan_vpn_cmds.append('end')
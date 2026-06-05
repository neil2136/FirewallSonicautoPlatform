import os
import sys
import re
import time
import copy
import requests
import asyncio
import unittest
import subprocess
import json
from collections import OrderedDict
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
from lib.modules.API import network
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.API import dpissl
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import securityservices
from lib.modules.API import policy
from lib.modules.API import log
from lib.modules.API import object
from lib.modules.API import vpn
from lib.modules.API import sslvpn
from lib.modules.API import users
from lib.modules.API import accessrule 
from lib.modules.API import accessrule 

from lib.modules.CLI.users import UsersStatusCli

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/sslvpn')
from sslvpn.common_lib import netextender
from sslvpn.common_lib import virtualoffice_page


# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Upgrade/Feature_Upgrade_Gen7_VPN/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/Feature_Upgrade_Gen7.json'
CONF_PATH = suite_path + 'definition/config'
HTTPS_SERVER_PATH = CONF_PATH + '/httpserver'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
configPath = os.environ["PYTHON_SONICOS_HOME"] + '/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC5_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC5_ETH1_IP: {PC5_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
# PC1_login = Host(PC1_ETH0_IP)
# PC2_login = Host(PC2_ETH0_IP)
# PC3_login = Host(PC3_ETH0_IP)
# PC4_login = Host(PC4_ETH0_IP)
# PC5_login = Host(PC5_ETH0_IP)


# parameters on the fw
class Parameter:
    ip = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X2_IP = '12.12.2.168'
    X2_GW = '12.12.2.1'
    X2_SUBNET = '12.12.2.0'
    VALID_DNS = PC4_ETH1_IP
    FAKE_DNS1 = '2.2.2.2'
    FAKE_DNS2 = '3.3.3.3'
    X3_IP = '192.168.3.168'

    prebuild = Params.prebuild
    testbuild = Params.build

    R_X0_IP = '172.16.1.101'
    R_X1_IP = '12.12.1.201'
    R_X2_IP = '12.12.2.201'
    R_X0_NET = '172.16.1.0'
    R_X3_IP = '12.12.3.201'
    VPN_IF_IP_LOCAL = '1.1.1.2'
    VPN_IF_IP_REMOTE = '1.1.1.1'


class CaseParams:
    sslvpn_user_name = 'auto_sslvpn_test'
    ula_user_name = 'auto_ula_test'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.ip,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
r_fw = Firewall(
    Parameter.R_X3_IP,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.ip,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

PC1_login = Host('localhost')
static_pc2 = Params.testbed + '-PC2'
PC2_login = Host(static_pc2)
static_pc3 = Params.testbed + '-PC3'
PC3_login = Host(static_pc3)
static_pc4 = Params.testbed + '-PC4'
PC4_login = Host(static_pc4)
static_pc5 = Params.testbed + '-PC5'
PC5_login = Host(static_pc5)
user_settings = users.UsersettingApi(fw)
Radius_user = users.RadiusApi(fw)
userstatus1 = UsersStatusCli(fw_cli)
local_user = users.UserLocalApi(fw)
user_ldap = users.LdapApi(fw)
access_rules = accessrule.AccessRuleIPv4Api(fw)
lc = LicenseCli(fw_cli)
interfaceapi = network.InterfaceIPv4Api(fw)
licensecli = LicenseCli(fw_cli)
failoverapi = network.FailoverLbApi(fw)
vpnapi = vpn.VpnbasesettingApi(fw)
r_vpnapi = vpn.VpnbasesettingApi(r_fw)
r_interfaceapi = network.InterfaceIPv4Api(r_fw)
r_aoapi = network.AddressobjectsApi(r_fw)
r_routepolicyapi = policy.RoutePolicyApi(r_fw)
r_accessruleapi = firewall.AccessRuleApi(r_fw)
aoapi = network.AddressobjectsApi(fw)
sslvpnserverapi = sslvpn.SSLVPNServerSettingsAPI(fw)
sslvpnclientapi = sslvpn.SSLVPNClientSettingsAPI(fw)
fwupgradeapi = system.SettingApi(fw)
statusapi = system.StatusApi(fw)
userLocalapi = users.UserLocalApi(fw)
userstatusapi = users.UserStatusApi(fw)
restartapi = system.RestartApi(fw)
accessruleapi = firewall.AccessRuleApi(fw)
routepolicyapi = policy.RoutePolicyApi(fw)
cp_nx = netextender.InstallNX()
nxconnect = netextender.NetextenderConnect(fw)
localhost = Host('localhost')
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)

x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
x2_wan_dict = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X2_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
x3_dmz_dict = {
    'if': 'X3',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}
l_s2s_vpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': 'auto_local_s2s_vpn01',
    'enable': False,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': '12.12.2.202',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '3.3.3.3',
    'peer_ike_id': '3.3.3.3',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_name': 'remote_vpn_net',

    'ike_exchange': 'main',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 120,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_gcm16_256',
    # 'ipsec_auth': 'sha-256',
    'ipsec_lifetime': 120,
    'bound_to': ['interface', 'X2'],
    'keep_alive': True,

}
r_s2s_vpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': 'auto_remote_s2s_vpn01',
    'enable': False,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': '12.12.2.169',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '3.3.3.3',
    'peer_ike_id': '3.3.3.3',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_name': 'local_vpn_net',

    'ike_exchange': 'main',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 120,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_gcm16_256',
    # 'ipsec_auth': 'sha_256',
    'ipsec_lifetime': 120,
    'bound_to': ['interface', 'X2'],
    'keep_alive': False,

}
l_tunnel_dict = {
    'type': 'tunnel_interface',
    'name': 'auto_local_tunnel01',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': 'password',
    'pri_gate': Parameter.R_X2_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '2.2.2.2',
    'peer_ike_id': '2.2.2.2',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_name': "remote_vpn_net",
    'ike_exchange': 'main',
    'ike_encryption': 'aes-128',
    'ipsec_encryption': 'aes_128',
    'ipversion': 'ipv4',
    'ike_auth': 'sha-1',
    'ike_dh_group': '2',
    'ike_lifetime': '28800',
    'ipsec_lifetime': '28800',
    'ipsec_protocol': 'esp',
    'ipsec_auth': 'sha_1',
    'ipsec_pfs': True,
    'ipsec_pfs_dhgroup': 2,
    'bound_to': ['interface', 'X2'],
    'keep_alive': True,
}
r_tunnel_dict = {
    'type': 'tunnel_interface',
    'name': 'auto_remote_tunnel01',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': 'password',
    'pri_gate': Parameter.X2_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '2.2.2.2',
    'peer_ike_id': '2.2.2.2',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_name': "local_vpn_net",
    'ike_exchange': 'main',
    'ike_encryption': 'aes-128',
    'ipsec_encryption': 'aes_128',
    'ipversion': 'ipv4',
    'ike_auth': 'sha-1',
    'ike_dh_group': '2',
    'ike_lifetime': '28800',
    'ipsec_lifetime': '28800',
    'ipsec_protocol': 'esp',
    'ipsec_auth': 'sha_1',
    'ipsec_pfs': True,
    'ipsec_pfs_dhgroup': 2,
    'bound_to': ['interface', 'X2'],
    'keep_alive': True,
}
l_ti_dict = {
    'zone': 'VPN',
    'type': "vpn_tunnel",
    'mode': 'static',
    'ip': Parameter.VPN_IF_IP_LOCAL,
    'netmask': '255.255.255.0',
    "tunnel_name": "Ni",
    'comment': '',
    "vpn_policy": l_tunnel_dict['name'],
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'flow_reporting': True,
    'multicast': True,
    'asymmetric_route': False,
    'fragment_packets': True,
    'ignore_df_bit': True,
}
r_ti_dict = {
    'zone': 'VPN',
    'type': "vpn_tunnel",
    'mode': 'static',
    'ip': Parameter.VPN_IF_IP_REMOTE,
    'netmask': '255.255.255.0',
    "tunnel_name": "Ni",
    'comment': '',
    "vpn_policy": r_tunnel_dict['name'],
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'flow_reporting': True,
    'multicast': True,
    'asymmetric_route': False,
    'fragment_packets': True,
    'ignore_df_bit': True,
}
lan_vpn_acl_dict = {
  "access_rules": [
    {
      "ipv4": {
        "name": "lan_to_vpn_name01",
        "comment": "",
        "action": "allow",
        "priority": {
          "auto": True
        },
        "enable": True,
        "from": "LAN",
        "source": {
          "address": {
            "any": True
          },
          "port": {
            "any": True
          }
        },
        "to": "VPN",
        "destination": {
          "address": {
            "any": True
          }
        },
        "service": {
          "any": True
        },
        "users": {
          "included": {
            "all": True
          },
          "excluded": {
            "none": True
          }
        },
        "tcp": {
          "timeout": 15,
          "urgent": False
        },
        "udp": {
          "timeout": 30
        },
        "dpi": True,
        "dpi_ssl": {
          "client": True,
          "server": True
        },
        "quality_of_service": {
          "class_of_service": {},
          "dscp": {
            "preserve": True
          }
        },
        "botnet_filter": False,
        "geo_ip_filter": {
          "enable": False
        },
        "logging": True,
        "flow_reporting": False,
        "connection_limit": {
          "source": {},
          "destination": {}
        },
        "sip": False,
        "h323": False,
        "fragments": True,
        "management": False,
        "max_connections": 100,
        "packet_monitoring": False,
        "reflexive": False
      }
    }
  ]
}
route_base_dict = {
    "name": 'auto_local_ti_route1',
    "comment": "",
    "interface": "Ni",
    "metric": 8,
    "service": {
        "any": True
    },
    "gateway": {
        "default": True
    },
    "source": {
        "name": "X0 Subnet"
    },
    "destination": {
        "name": 'remote_vpn_net'
    },
    "disable_on_interface_down": True,
    "probe": "",
    "distance": {
        "auto": True
    },
    "tos": "0x00",
    "mask": "0x00",
    "type": "standard",
    "auto_add_access_rules": True
}
org_base_dict = copy.deepcopy(route_base_dict)
route_policy_dict = {"route_policies": [{"ipv4": route_base_dict}]}
default_acl_dict = {
    # "uuid": '',
    "name": "Default Access Rule",
    "enable": True,
    "from": "LAN",
    "to": "WAN",
    "action": "allow",
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
            'all': True
        },
        "excluded": {
            "none": True
        }
    },
    "comment": "",
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
            "value": 13
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

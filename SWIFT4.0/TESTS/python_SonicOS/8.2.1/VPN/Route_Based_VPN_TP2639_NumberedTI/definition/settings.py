import os
import sys
import copy
import ast
import re
import time
import json
import requests
import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, FirewallCLI
from util.enhancedinfo import show_testcase_info

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api, AddressobjectsApi, DynamicRoutingApi
from lib.modules.CLI.network import RouteCli
from lib.modules.API.policy import RoutePolicyApi, RoutePolicyApi
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/Route_Based_VPN_TP2639_NumberedTI'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/route_based_vpn_tp2639_numberedti.json'


# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')


logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            )

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    # X1_NAT = '12.12.1.0'
    X1_NET = '12.12.1.0'
    X2_IP = '193.168.1.168'
    X2_SUBNET = '193.168.1.0'
    # X2_GW = '192.168.2.1'
    X3_IP = '192.168.3.168'
    X3_SUBNET = '192.168.3.0'
    X0_REMOTE_IP = '172.16.1.101'
    X1_REMOTE_IP = '12.12.1.201'
    X2_REMOTE_IP = '12.12.2.201'
    X3_REMOTE_IP = '12.12.3.201'
    X3_REMOTE_NET = '12.12.3.0'
    MASK = '255.255.255.0'
    TUNNEL_INTERFACE = 'Ni'
    L_TI_IP = '11.1.1.10'
    R_TI_IP = '11.1.1.11'
    LOCAL_VPN_NAME = 'localtunnelvpn'
    REMOTE_VPN_NAME = 'remotetunnelvpn'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


ip = Parameter.FIREWALL
r_ip = Parameter.X0_REMOTE_IP
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
r_fw_cli = Firewall(r_ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
r_fw_api = Firewall(r_ip, user='admin', password='sonicauto', supported_config_mode='api')

interfacev4api = InterfaceIPv4Api(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
routepolicyapi = RoutePolicyApi(fw_api)
r_routepolicyapi = RoutePolicyApi(r_fw_api)
dynamicroutingapi = DynamicRoutingApi(fw_api)
r_dynamicroutingapi = DynamicRoutingApi(r_fw_api)
vpnbasesettingapi = VpnbasesettingApi(fw_api)
r_vpnbasesettingapi = VpnbasesettingApi(r_fw_api)
r_interfacev4api = InterfaceIPv4Api(r_fw_api)
accessruleapi = AccessRuleApi(fw_api)
r_accessruleapi = AccessRuleApi(r_fw_api)
r_addressobjectsapi = AddressobjectsApi(r_fw_api)
routecli = RouteCli(fw_cli)
r_routecli = RouteCli(r_fw_cli)
licensecli = LicenseCli(fw_cli)


accessrule_dict = {
    "access_rules": [
        {
            "ipv4": {
                "name": "l_lan_to_vpn",
                "comment": "",
                "action": "allow",
                "priority": {
                    "auto": True
                },
                "enable": True,
                "from": "LAN",
                "source": {
                    "address": {
                        "name": "X2 Subnet"
                    },
                    "port": {
                        "any": True
                    }
                },
                "to": "VPN",
                "destination": {
                    "address": {
                        "name": "remote_x3_subnet"
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
                "reflexive": False,
                "redirect_unauthenticated_users_to_log_in": True
            }
        }
    ]
}

lvpn = {
    'type': 'tunnel_interface',
    'name': Parameter.LOCAL_VPN_NAME,
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': 'password',
    'pri_gate': Parameter.X1_REMOTE_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'ike_exchange': 'ikev2',
    # 'ike_encryption': 'aes-128',
    'ipversion': 'ipv4',
    # 'ike_auth': 'sha-1',
    # 'ike_dh_group': '2',
    'ike_lifetime': '28800',
    'ipsec_lifetime': '28800',
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_gcm16_256',
    # 'ipsec_pfs': True,
    'keep_alive': True,
}

tunnel_interface_dict = {
    'zone': 'VPN',
    'type': "vpn_tunnel",
    'mode': 'static',
    'ip': '',
    'netmask': '255.255.255.0',
    "tunnel_name": Parameter.TUNNEL_INTERFACE,
    'comment': '',
    "vpn_policy": '',
    'mgmt_ping': True,
}

vpn_policy_dict = {
    'type': 'tunnel_interface',
    'name': '',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': 'password',
    'pri_gate': '',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'ike_exchange': 'ikev2',
    # 'ike_encryption': 'aes-128',
    'ipversion': 'ipv4',
    # 'ike_auth': 'sha-1',
    # 'ike_dh_group': '2',
    'ike_lifetime': '28800',
    'ipsec_lifetime': '28800',
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_gcm16_256',
    # 'ipsec_pfs': True,
    'keep_alive': True,
}

default_ospf2 = {
    'interface': Parameter.TUNNEL_INTERFACE,
    'type': 'TI',
    'num_id': '',
    # 'DUT': 'local',
    'mode': 'enable',  # enable,disable,passive
    'dead_interval': '40',
    'hello_interval': '10',
    'auth': 'disable',  # disable,message diagest,simple password
    'area': '0',
    'area_type': 'normal',  # normal, stub area, totally stubby area, not-so-stubby area,totally stubby nssa
    'auto': 'on',
    # 'cost': '0',
    'priority': '1',
    'mtu': 'off',
}

default_rip_dict = {
    'type': 'TI',
    'interface': Parameter.TUNNEL_INTERFACE,
    'num_id': ' ',
    'mode': 'send_and_receive',
    'receive': '2',
    'send': '2',
}

pbr_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "pbr_ti",
                "comment": "",
                "interface": Parameter.TUNNEL_INTERFACE,
                "metric": 20,
                "service": {
                    "any": True
                },
                "gateway": {
                    "default": True
                },
                "source": {
                    "name": "X2 Subnet"
                },
                "destination": {
                    "name": "remote_x3_subnet"
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
        }
    ]
}

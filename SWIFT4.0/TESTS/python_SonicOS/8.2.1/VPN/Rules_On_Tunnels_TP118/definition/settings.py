import os
import sys
import copy
import ast
import re
import time
import json
import winrm
import requests
import unittest
import paramunittest
from nose_parameterized import parameterized
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, FirewallCLI
from util.enhancedinfo import show_testcase_info
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.vpn import VpnbasesettingApi
# from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.system import DiagnosticApi
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/Rules_On_Tunnels_TP118'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/rules_on_tunnels_tp118.json'
SCRIPTS_PATH = suite_path + '/definition/scripts'


# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            )

PC1_Login = Host(PC1_ETH0_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)


#################################################################################################################
#
#
#  PC1(eth1)--------x0(192.168.168.168)DUT x1(12.12.1.101)---------(12.12.1.201) X1 remote DUT(X3)---------PC3
#  PC2(eth1)--------x2(193.168.1.168) |
#
#
#
#################################################################################################################


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X2_NET = '193.168.1.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X2_IP = '193.168.1.168'
    X0_REMOTE_IP = '172.16.1.101'
    X1_REMOTE_IP = '12.12.1.201'
    X3_REMOTE_IP = '12.12.3.201'
    X3_REMOTE_NET = '12.12.3.0'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


class ParamCases:
    tc03hittimebefore = ''
    tc07hittimebefore = ''


ip = Parameter.FIREWALL
r_ip = Parameter.X0_REMOTE_IP
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
r_fw_api = Firewall(r_ip, user='admin', password='sonicauto', supported_config_mode='api')


interfacev4api = InterfaceIPv4Api(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
vpnbasesettingapi = VpnbasesettingApi(fw_api)
r_vpnbasesettingapi = VpnbasesettingApi(r_fw_api)
r_addressobjectsapi = AddressobjectsApi(r_fw_api)
accessruleapi = AccessRuleApi(fw_api)
diagnosticapi = DiagnosticApi(fw_api)
licensecli = LicenseCli(fw_cli)

accessrule_dict = {
    "access_rules": [
        {
            "ipv4": {
                "name": "vpnhost_httpserver",
                "comment": "",
                "action": "deny",
                "priority": {
                    "auto": True
                },
                "enable": True,
                "from": "VPN",
                "source": {
                    "address": {
                        "name": "pc3_eth1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "to": "LAN",
                "destination": {
                    "address": {
                        "name": "pc2_eth1"
                    }
                },
                "service": {
                    "name": "HTTP"
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
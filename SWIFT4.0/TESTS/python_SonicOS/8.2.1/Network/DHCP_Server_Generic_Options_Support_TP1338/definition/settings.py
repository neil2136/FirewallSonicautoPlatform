import os
import sys
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

# from runner.unittest.suite import UnittestSuite

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, DHCPServerApi, ZoneObjectsApi,  AddressobjectsApi
from lib.modules.API.system import PacketmonitorApi, RestartApi, SettingApi
from lib.modules.API.policy import RoutePolicyApi

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DHCP_Server_Generic_Options_Support_TP1338'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/dhcp_server_generic_options_support_tp1338.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            )

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)


##########################################################################################
#                                                                                        #
#  PC1(eth1)---------(192.168.168.168)DUT1 x2(193.168.1.168)--------PC2 client(eth1)     #
#                                                                                        #
##########################################################################################


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X2_IP = '193.168.1.168'
    MASK = '255.255.255.0'
    START_IP = '193.168.1.100'
    END_IP = '193.168.1.120'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

dhcpserverapi = DHCPServerApi(fw_api)
interfacev4api = InterfaceIPv4Api(fw_api)
packetmonitorapi = PacketmonitorApi(fw_api)
zoneobjectsapi = ZoneObjectsApi(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
routepolicyapi = RoutePolicyApi(fw_api)
restartapi = RestartApi(fw_api)
settingapi = SettingApi(fw_api)


dhcp_option_base_dict = {
    'name': '',
    'number': '',
    'array': False,
    'value': [
        # {
        #     'ip': Object_ip1
        # }
    ]
}
dhcp_option_dict = {"dhcp_server": {"ipv4": {"option": {"object": [dhcp_option_base_dict]}}}}

dhcp_server_dynamic_base_dict = {
    "from": "",
    "to": "",
    "enable": True,
    "lease_time": 1440,
    "default_gateway": "",
    "netmask": "255.255.255.0",
    "comment": "",
    "allow_bootp": False,
    "domain_name": "",
    "dns": {
        "server": {
            "inherit": True
        }
    },
    "wins": {
        "primary": "0.0.0.0",
        "secondary": "0.0.0.0"
    },
    "call_manager": {
        "primary": "",
        "secondary": "",
        "tertiary": ""
    },
    "network_boot": {
        "next_server": "0.0.0.0",
        "boot_file": "",
        "server_name": ""
    },
    "generic_option": {},
    "always_send_option": False
}
dhcp_server_dynamic_scope_dict = {"dhcp_server": {"ipv4": {"scope": {"dynamic": [dhcp_server_dynamic_base_dict]}}}}

dhcp_option_group_base_dict = {
    'dhcp_server': {
        'ipv4': {
            'option': {
                'group': [

                ]
            }
        }
    }
}
dhcp_option_group_dict = {"dhcp_server": {"ipv4": {"option": {"group": [dhcp_option_group_base_dict]}}}}

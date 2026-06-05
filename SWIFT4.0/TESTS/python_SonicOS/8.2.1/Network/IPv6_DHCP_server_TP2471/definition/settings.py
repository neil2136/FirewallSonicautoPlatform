import os
import sys
# import re
# import time
import json
# import winrm
# import requests
# import unittest
# import paramunittest
# from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
# from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, FirewallCLI
from util.enhancedinfo import show_testcase_info

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api, DHCPServerApi, DnsSettingsApi, ZoneObjectsApi, IpHelperApi, AddressobjectsApi
from lib.modules.CLI.network import InterfaceCli, DhcpServerCli
# from lib.modules.API import firewall
from lib.modules.API.system import PacketmonitorApi, RestartApi, SettingApi
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_server_TP2471'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/ipv6_dhcp_server_tp2471.json'
config_path = suite_path + '/configfile/dhclient6.conf'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            f"\n PC4_ETH0_IP : {PC4_ETH0_IP}"
            f"\n PC4_ETH1_IP : {PC4_ETH1_IP}"
            f"\n PC5_ETH0_IP : {PC5_ETH0_IP}"
            f"\n PC5_ETH1_IP : {PC5_ETH1_IP}"
            )

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)
PC4_Login = Host(PC4_ETH0_IP)
PC5_Login = Host(PC5_ETH0_IP)

#
#  *********************************DHCPv6 server***************************************
#                                       x3-----PC5
#  PC1(eth1)---------(192.168.168.168)DUT1 x3(3001:1::169)--------X3(dhcpv6) remote
#                                    |  |X2(2001:1::168)
#                                    |  |
#                                   PC2 PC3  dhcpv6 client
#
#  *********************************DHCPv6 Relay*****************************************
#
#      DUT1 x3(3001:1::168)--------(3001:1::169)X3 remote X4(4001:1::100)--------------PC4
#          dhcpv6 server                               dhcpv6 realy
#
#   Note: 7.1.1 need add 3001:1:0 scope on dhcpv6 server,this is by design,7.0.1 needn't
#


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X2_REMOTE_IP = '12.12.2.201'
    X4_REMOTE_IP = '173.16.1.168'
    X3_REMOTE_IP = '172.17.1.169'
    X2_IP = '193.168.1.168'
    X3_IP = '194.168.1.168'
    X0_V6_IP = '1001:1::168'
    X2_V6_IP = '2001:1::168'
    X3_V6_IP = '3001:1::168'
    X3_REMOTE_V6_IP = '3001:1::169'
    X4_REMOTE_V6_IP = '4001:1::100'
    MASK = '255.255.255.0'
    PRIMARY_DNS = '100::100'
    SECONDARY_DNS = '200::100'
    TERTIARY_DNS = '300::100'
    STATIC_PRIMARY_DNS = '2001:25de::cade'
    STATIC_SECONDARY_DNS = '2001:db8:85a3:8d3:1319:8a2e:370:7344'
    STATIC_TERTIARY_DNS = '300:100::100'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    PREFIX_LENGTH = 64


class ParamCases:
    tc31result = False
    tc24result = False


ip = Parameter.FIREWALL
r_ip = Parameter.X2_REMOTE_IP

fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
r_fw_api = Firewall(r_ip, user='admin', password='sonicauto', supported_config_mode='api')
r_fw_cli = Firewall(r_ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

dhcpserverapi = DHCPServerApi(fw_api)
interfacev4api = InterfaceIPv4Api(fw_api)
interfacev6api = InterfaceIPv6Api(fw_api)
dnssettingsapi = DnsSettingsApi(fw_api)
packetmonitorapi = PacketmonitorApi(fw_api)
zoneobjectsapi = ZoneObjectsApi(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
routepolicyapi = RoutePolicyApi(fw_api)
restartapi = RestartApi(fw_api)
dhcpservercli = DhcpServerCli(fw_cli)
license_cli = LicenseCli(fw_cli)
settingapi = SettingApi(fw_api)

reinterfacev4api = InterfaceIPv4Api(r_fw_api)
reinterfacev6api = InterfaceIPv6Api(r_fw_api)
reinterfacecli = InterfaceCli(r_fw_cli)
reiphelperapi = IpHelperApi(r_fw_api)
readdressobjectsapi = AddressobjectsApi(r_fw_api)

dhcpv6_server_dynamic_base_dict = {
    "name": "",
    "range": {
        "from": "",
        "to": ""
    },
    "enable": True,
    "prefix": "",
    "lifetime": {
        "valid": 2160,
        "preferred": 1440
    },
    "comment": "",
    "domain_name": "autotest",
    "dns": {
        "server": {
            "inherit": True
        }
    },
    "generic_option": {},
    "always_send_option": False
}

dhcpv6_server_static_base_dict = {
    "name": "static_dhcpv6_scope",
    "enable": True,
    "prefix": "5001:1::",
    "ip": "5001:1::300",
    "iaid": 12345,
    "duid": "11223344",
    "lifetime": {
        "valid": 2160,
        "preferred": 1440
    },
    "comment": "",
    "always_send_option": False,
    "domain_name": "",
    "dns": {
        "server": {
            "inherit": True
        }
    },
    "generic_option": {}
    }

dhcpv6_server_dynamic_scope_dict = {"dhcp_server": {"ipv6": {"scope": {"dynamic": [dhcpv6_server_dynamic_base_dict]}}}}
dhcpv6_server_static_scope_dict = {"dhcp_server": {"ipv6": {"scope": {"static": [dhcpv6_server_static_base_dict]}}}}


ipv6_route_base_dict = {
    "comment": "",
    "interface": "X3",
    "metric": 20,
    "service": {"any": True},
    "gateway": {"name": "gw"},
    "source": {"any": True},
    "destination": {"any": True},
    "disable_on_interface_down": True,
    "vpn_precedence": False,
    "probe": "",
    "distance": {"auto": True},
    "tos": "0x00",
    "mask": "0x00",
    "type": "standard"
}
ipv6_route_policy_dict = {"route_policies": [{"ipv6": ipv6_route_base_dict}]}

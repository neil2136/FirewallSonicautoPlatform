import os
import sys
import re
import time
import json
import requests
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api, AddressobjectsApi
from lib.modules.API import firewall
from lib.modules.API.system import RestartApi, PacketmonitorApi, DiagnosticApi, SettingApi
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.system import AdminCli, DiagnosticsCli
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
basic_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_PBR_TP2518'
sys.path.append(basic_path)
defi_path = basic_path + '/definition'
TESTPLAN = basic_path + '/testplan/ipv6_pbr_tp2518.json'
FILE_PATH_HTTP_REQ = basic_path + 'definition/tools/httprequestsend.py'
SCRIPT_PATH = basic_path + 'definition/tools/'

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
PC1_ETH1_IPv6 = os_obj.get_node_interface_ipv6('PC1', 'eth1').split('/')[0]
PC2_ETH1_IPv6 = os_obj.get_node_interface_ipv6('PC2', 'eth1').split('/')[0]
PC3_ETH1_IPv6 = os_obj.get_node_interface_ipv6('PC3', 'eth1').split('/')[0]

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            + f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            + f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            + f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            + f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            + f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            + f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            + f"\n PC4_ETH1_IP : {PC4_ETH1_IP}"
            + f"\n PC1_ETH1_IPv6 : {PC1_ETH1_IPv6}"
            + f"\n PC2_ETH1_IPv6 : {PC2_ETH1_IPv6}"
            + f"\n PC3_ETH1_IPv6 : {PC3_ETH1_IPv6}"
            )

console_info_UTM = os_obj.get_console_info('UTM')
console_info_RemoteGEN7 = os_obj.get_console_info('RemoteGEN7')
logger.info(console_info_UTM)
logger.info(console_info_RemoteGEN7)

if console_info_RemoteGEN7:
    consvr_RemoteGEN7 = console_info_RemoteGEN7[0]
    conport_RemoteGEN7 = console_info_RemoteGEN7[1]
    logger.info(consvr_RemoteGEN7)
    logger.info(conport_RemoteGEN7)
else:
    consvr_RemoteGEN7 = ''
    conport_RemoteGEN7 = ''

# PC1--------X0 DUT X2-------------X2 remote X3--------------PC3
# PC2--------X3 DUT X4--------PC4

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)
PC4_Login = Host(PC4_ETH0_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X2_IP = '172.16.1.168'
    X3_IP = '192.169.168.168'
    X4_IP = '172.16.2.168'
    X0_V6_IP = '1001:1::168'
    X0_V6_PREFIX = '1001:1::'
    X3_V6_PREFIX = '1001:2::'
    X2_V6_IP = '2001:1::168'
    X3_V6_IP = '1001:2::168'
    X4_V6_IP = '2001:2::168'
    X1_SUBNET = '12.12.1.0'
    X2_SUBNET = '172.16.2.0'
    MASK = '255.255.255.0'
    X2_V6_PREFIX = '2001:1::'
    X2_V6_IP_MODIFY = '3000:100::10'
    X2_V6_MODIFY_PREFIX = '3000:100::'
    R_X0_IP = '172.17.1.168'
    R_X1_IP = '12.12.1.201'
    R_X2_IP = '172.16.1.169'
    R_X3_IP = '172.17.2.168'
    R_X2_IPV6 = '2001:1::169'
    R_X3_IPV6 = '2002:1::10'
    R_X3_V6_PREFIX = '2002:1::'
    ZONE_1 = 'WAN'
    ZONE_2 = 'LAN'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    PC1_ETH1_IPV6 = '1001:1::10'
    PC2_ETH1_IPV6 = '1001:2::10'
    PC3_ETH1_IPV6 = '2002:1::20'
    PC3_ETH1_IPV6_112 = '2002:1:0:0:1:2:3:20'
    PREFIX_LENGTH_1 = 64
    PREFIX_LENGTH_2 = 32


ip = Parameter.FIREWALL
fw_api = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
# fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli_ssh')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
r_fw_api = Firewall(Parameter.R_X0_IP, user='admin', password='password', supported_config_mode='api')
r_fw_console = Firewall(
    ip=Parameter.R_X0_IP,
    console_ip=consvr_RemoteGEN7,
    console_port=conport_RemoteGEN7,
    user='admin',
    password='password',
    supported_config_mode='cli-console'
)

interfacev4api = InterfaceIPv4Api(fw_api)
interfacev6api = InterfaceIPv6Api(fw_api)
routepolicyapi = RoutePolicyApi(fw_api)
addressobjectapi = AddressobjectsApi(fw_api)
packetmonitorapi = PacketmonitorApi(fw_api)
diagnosticapi = DiagnosticApi(fw_api)
settingapi = SettingApi(fw_api)
restartapi = RestartApi(fw_api)
diagnosticscli = DiagnosticsCli(fw_cli)
licensecli = LicenseCli(fw_cli)

r_addressobjectapi = AddressobjectsApi(r_fw_api)
r_interfacev4api = InterfaceIPv4Api(r_fw_api)
r_interfacev6api = InterfaceIPv6Api(r_fw_api)
r_routepolicyapi = RoutePolicyApi(r_fw_api)

r_interfaceconsole = InterfaceCli(r_fw_console)
# r_adminconsole = AdminCli(r_fw_console)


ipv6_route_base_dict = {
    "comment": "",
    "interface": "X2",
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

x2_static = {
    'if': 'X2',
    'zone': Parameter.ZONE_2,
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}

x2_v6_dict = {
    'name': 'X2',
    'mode': 'static',
    'zone': 'LAN',
    'ip': Parameter.X2_V6_IP,
    'prefix_length': Parameter.PREFIX_LENGTH_1,
    'mgmt_ping': True,
    'mgmt_https': True
}

x2_v6_modify_dict = {
    'name': 'X2',
    'mode': 'static',
    'zone': 'LAN',
    'ip': Parameter.X2_V6_IP_MODIFY,
    'prefix_length': Parameter.PREFIX_LENGTH_2,
    'mgmt_ping': True,
    'mgmt_https': True
}

x3_static = {
    'if': 'X3',
    'zone': Parameter.ZONE_2,
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}

x3_v6_dict = {
    'name': 'X3',
    'mode': 'static',
    'zone': 'LAN',
    'ip': Parameter.X3_V6_IP,
    'prefix_length': Parameter.PREFIX_LENGTH_1,
    'mgmt_ping': True,
    'mgmt_https': True
}

x4_static = {
    'if': 'X4',
    'zone': Parameter.ZONE_2,
    'mode': 'static',
    'ip': Parameter.X4_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}

x4_v6_dict = {
    'name': 'X4',
    'mode': 'static',
    'zone': 'LAN',
    'ip': Parameter.X4_V6_IP,
    'prefix_length': Parameter.PREFIX_LENGTH_1,
    'mgmt_ping': True,
    'mgmt_https': True
}

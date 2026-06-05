import os
import sys
import re
import time
import json
import requests

import unittest
import paramunittest
from nose_parameterized import parameterized

# import contents from common_lib path
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
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api, AddressobjectsApi, DynamicRoutingApi
from lib.modules.API.system import RestartApi, PacketmonitorApi, DiagnosticApi, SettingApi
from lib.modules.CLI.network import InterfaceCli, RouteCli
from lib.modules.CLI.system import AdminCli, DiagnosticsCli,  StatusCli
from lib.modules.API.policy import RoutePolicyApi

# import form test suite root path like definition
basic_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_OSPFv3'
sys.path.append(basic_path)
defi_path = basic_path + '/definition'
TESTPLAN = basic_path + '/testplan/ipv6_ospfv3.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
UTM_X4_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X4:1')
REMOTRGEN7_X4_VLAN1_ID = os_obj.get_node_interface_vlan_id('RemoteGEN7', 'X4:1')

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            + f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            + f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            + f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            + f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            + f"\n PC2_ETH2_IP : {PC2_ETH2_IP}"
            + f'\n UTM_X4_VLAN1_ID: {UTM_X4_VLAN1_ID}'
            + f'\n REMOTEGEN7_X4_VLAN1_ID: {REMOTRGEN7_X4_VLAN1_ID}'
            )

console_info_RemoteGEN7 = os_obj.get_console_info('RemoteGEN7')
if console_info_RemoteGEN7:
    consvr_RemoteGEN7 = console_info_RemoteGEN7[0]
    conport_RemoteGEN7 = console_info_RemoteGEN7[1]
    logger.info(consvr_RemoteGEN7)
    logger.info(conport_RemoteGEN7)
else:
    consvr_RemoteGEN7 = ''
    conport_RemoteGEN7 = ''

# PC1--------X0 DUT X2-------------X2 remote X3--------------PC3
# PC2--------X3 DUT X4:1-------------X4:1 remote

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X2_IP = '172.16.1.168'
    X3_IP = '192.169.168.168'
    X4_IP = '172.22.1.168'
    X0_V6_IP = '1001:1::168'
    X0_V6_PREFIX = '1001:1::'
    X3_V6_PREFIX = '1001:2::'
    X2_V6_IP = '2001:1::168'
    X3_V6_IP = '1001:2::168'
    X4_V6_IP = '2022:1::168'
    X1_SUBNET = '12.12.1.0'
    X2_SUBNET = '172.16.2.0'
    MASK = '255.255.255.0'
    X2_V6_PREFIX = '2001:1::'
    R_X0_IP = '172.17.1.168'
    R_X1_IP = '12.12.1.201'
    R_X2_IP = '172.16.1.169'
    R_X3_IP = '172.17.2.168'
    R_X4_IP = '172.22.1.169'
    R_X2_IPV6 = '2001:1::169'
    R_X3_IPV6 = '2002:1::10'
    R_X4_IPV6 = '2022:1::169'
    R_X3_V6_PREFIX = '2002:1::/64'
    ZONE_1 = 'WAN'
    ZONE_2 = 'LAN'
    UTM_DEST_NETWORK = '100:1:1::0'
    UTM_DEST_PREFIX = '100:1:1::/64'
    REMOTE_DEST_NETWORK = '200:1:1::0'
    REMOTE_DEST_HOST = '200:1:1::10'
    REMOTE_DEST_PREFIX = '200:1:1::/64'
    UTM_ROUTER_ID = '10.10.10.10'
    REMOTE_ROUTER_ID = '20.20.20.20'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    PC1_ETH1_IPV6 = '1001:1::10'
    PREFIX_LENGTH = 64


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')

fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

remotegen7_fw = Firewall(
    Parameter.R_X0_IP,
    user='admin',
    password='password',
    supported_config_mode='api'
)

remotegen7_fw_cli = Firewall(
    Parameter.R_X0_IP,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

remotegen7_fw_console = Firewall(
    ip=Parameter.R_X0_IP,
    console_ip=consvr_RemoteGEN7,
    console_port=conport_RemoteGEN7,
    user='admin',
    password='password',
    supported_config_mode='cli-console'
)

dyroutingapi = DynamicRoutingApi(fw_api)
r_dyroutingapi = DynamicRoutingApi(remotegen7_fw)
interfacev4api = InterfaceIPv4Api(fw_api)
interfacev6api = InterfaceIPv6Api(fw_api)
r_interfacev4api = InterfaceIPv4Api(remotegen7_fw)
r_interfacev6api = InterfaceIPv6Api(remotegen7_fw)

routepolicyapi = RoutePolicyApi(fw_api)
r_routepolicyapi = RoutePolicyApi(remotegen7_fw)
addressobjectapi = AddressobjectsApi(fw_api)
r_addressobjectapi = AddressobjectsApi(remotegen7_fw)
r_packetmonitorapi = PacketmonitorApi(fw_api)
packetmonitorapi = PacketmonitorApi(fw_api)
restartapi = RestartApi(fw_api)
diagnosticapi = DiagnosticApi(fw_api)

routecli = RouteCli(fw_cli)
r_routecli = RouteCli(remotegen7_fw_cli)
statuscli = StatusCli(fw_cli)


remotegen7_interfaceconsole = InterfaceCli(remotegen7_fw_console)
remotegen7_adminconsole = AdminCli(remotegen7_fw_console)

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


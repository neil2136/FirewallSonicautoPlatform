import sys
import os
import re
import copy
import paramunittest
from time import sleep
import subprocess
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion


# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall


# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api
from lib.modules.API.system import PacketmonitorApi, RestartApi, SettingApi, DiagnosticApi
from lib.modules.CLI.network import InterfaceCli
# from definition.network_2 import InterfaceIPv6Api

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
suite_path = os.environ['PYTHON_SONICOS_HOME']+'/Network/IPv6_DHCP_Client_Part2/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/ipv6_dhcp_client.json'
server_conf_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_Part2/definition/file'

os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
logger.info(f"""
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
PC3_ETH1_IP is: {PC3_ETH1_IP}
PC3_ETH2_IP is: {PC3_ETH2_IP}
""")
pc1_login = Host(PC1_ETH1_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)


# Params on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X2_IP = '13.13.1.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    V6_Prefix_1 = '2001:1:2:4::'
    V6_Prefix_2 = '2002:1:2:4::'


# Instantiate objects including API import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

if_v4_api = InterfaceIPv4Api(fw)
if_v6_api = InterfaceIPv6Api(fw)
if_v6_cli = InterfaceCli(fw_cli)
pkt_api = PacketmonitorApi(fw)
restart_api = RestartApi(fw)
settings_api = SettingApi(fw)
diag_api = DiagnosticApi(fw)

x1_v6_dict = {
    'name': 'X1',
    'mode': 'dhcpv6',
    'listen_router_advertisement': False,
    "dhcpv6": {
        "mode": "manual",
        "rapid_commit": True,
        "info_only": False
    },
    'mgmt_https': True,
    'mgmt_ping': True
}

x2_v6_dict = {
    'name': 'X2',
    'mode': 'dhcpv6',
    'listen_router_advertisement': False,
    'ipv6_traffic': True,
    "dhcpv6": {
        "mode": "manual",
        "rapid_commit": True,
        "info_only": False
    },
    'mgmt_https': True,
    'mgmt_ping': True
}

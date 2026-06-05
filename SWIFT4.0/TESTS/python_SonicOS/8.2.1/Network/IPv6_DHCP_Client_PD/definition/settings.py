import sys
import os
import re
import copy
import time
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
from lib.modules.API import network
from lib.modules.API.system import PacketmonitorApi, DiagnosticApi, SettingApi
from lib.modules.CLI.network import InterfaceCli, RouteCli, AddressObjectCli


sys.path.append(os.environ['PYTHON_COMMON_HOME'])
suite_path = os.environ['PYTHON_SONICOS_HOME']+'/Network/IPv6_DHCP_Client_PD/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/ipv6_dhcp_client_pd.json'
conf_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_PD/definition/file'

os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
logger.info(f"""
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
""")
pc1_login = Host(PC1_ETH1_IP)
pc2_login = Host(PC2_ETH2_IP)


# Params on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_PD1 = "2024:1:2:3::"
    X1_PD2 = "2025:1:2:3::"
    V6_Prefix = '2001:1:2:4::'


class CasePara:
    tsr_msg = ''
    captured_pkts1 = ''
    captured_pkts2 = ''
    captured_pkts3 = ''
    solicit_pkt = ''
    rc_case101 = False


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

if_v4_api = network.InterfaceIPv4Api(fw)
if_v6_api = network.InterfaceIPv6Api(fw)
if_v6_cli = InterfaceCli(fw_cli)
pkt_api = PacketmonitorApi(fw)
ao_api = network.AddressobjectsApi(fw)
route_api = network.RoutePolicyApi(fw)
diag_api = DiagnosticApi(fw)
route_cli = RouteCli(fw_cli)
set_api = SettingApi(fw)
ao_cli = AddressObjectCli(fw_cli)

x3_param_1 = {
    'name': 'X3',
    'type': 'prefix_delegation',
    'delegated_prefix': 'X1 Delegated Prefix',
    'preferred_ip': '::1',
    'prefix_length': 64,
}
x3_param_2 = {
    'name': 'X3',
    'type': 'prefix_delegation',
    'delegated_prefix': 'X1 Delegated Prefix',
    'preferred_ip': '::1',
    'prefix_length': 72,
}
x3_param_3 = {
    'name': 'X3',
    'type': 'prefix_delegation',
    'delegated_prefix': 'X1 Delegated Prefix',
    'preferred_ip': '::1',
    'prefix_length': 48,
}

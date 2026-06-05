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
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.API.system import PacketmonitorApi, SettingApi, DiagnosticApi


suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay_Full/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/dhcpv6_relay.json'


# parameters on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')

logger.info(f'''
PC1_ETH0_IP: {PC1_ETH0_IP}
PC1_ETH1_IP: {PC1_ETH1_IP}
PC1_ETH2_IP: {PC1_ETH2_IP}
PC1_ETH3_IP: {PC1_ETH3_IP}
PC2_ETH0_IP: {PC2_ETH0_IP}
PC2_ETH1_IP: {PC2_ETH1_IP}
PC2_ETH2_IP: {PC2_ETH2_IP}
PC3_ETH0_IP: {PC3_ETH0_IP}
PC3_ETH1_IP: {PC3_ETH1_IP}
PC3_ETH2_IP: {PC3_ETH2_IP}
''')

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.0.168'
    X2_IP = '13.13.1.168'
    X3_IP = '12.12.3.168'
    REM_X1_IP = '12.12.1.201'
    REM_X3_IP = '12.12.3.201'
    X1_DNS_1 = Params.G_DNS1
    X2_DNS_2 = Params.G_DNS2
    X2_V6_IP = "2001:1:2:3::168"
    X3_V6_IP = "2001:1:2:4::168"
    REM_X3_V6_IP = "2001:1:2:4::169"


# Instantiate objects including API,CLI import
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
rem_fw = Firewall(
    Parameter.REM_X1_IP,
    user='admin',
    password='password',
    supported_config_mode='api'
)
rem_fw_cli = Firewall(
    Parameter.REM_X1_IP,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

iface_v4_api = network.InterfaceIPv4Api(fw)
licensecli = LicenseCli(fw_cli)
iface_v6_api = network.InterfaceIPv6Api(fw)
dhcpv6_api = network.DHCPServerApi(fw)
ip_helper_api = network.IpHelperApi(fw)
pkt_api = PacketmonitorApi(fw)
settings_api = SettingApi(fw)
diag_api = DiagnosticApi(fw)

rem_if_api = network.InterfaceIPv4Api(rem_fw)
rem_iface_v6_api = network.InterfaceIPv6Api(rem_fw)
rem_dhcpv6_api = network.DHCPServerApi(rem_fw)
rem_ao_api = network.AddressobjectsApi(rem_fw)
rem_route_api = RoutePolicyApi(rem_fw)
import sys
import os
import time
import re
import json
import random
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall

# import form branch lib contents for testsuite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API.system import PacketmonitorApi, SettingApi, AdminApi, DiagnosticApi
from lib.modules.CLI.system import LicenseCli

suite_path = os.environ['PYTHON_SONICOS_HOME'] + \
             '/Network/IPv6_Network_Monitor_Part2/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/ipv6_network_monitor.json'

# parameters on openstack
os_obj = Openstack(Params.testbed)
Console_Info = os_obj.get_console_info(dut='UTM')
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')

logger.info(f"""
PC1_ETH0_IP is: {PC1_ETH0_IP}
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH0_IP is: {PC2_ETH0_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
""")

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


# Instantiate objects including API, CLI import
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

license_cli = LicenseCli(fw_cli)
if_v4_api = network.InterfaceIPv4Api(fw)
if_v6_api = network.InterfaceIPv6Api(fw)
nm_obj = network.NetworkMonitorApi(fw)
pkt_api = PacketmonitorApi(fw)
nat_v6_api = network.NatpolicyApi(fw)
ao_api = network.AddressobjectsApi(fw)
diag_api = DiagnosticApi(fw)
setting_api = SettingApi(fw)
route_api = network.RoutePolicyApi(fw)


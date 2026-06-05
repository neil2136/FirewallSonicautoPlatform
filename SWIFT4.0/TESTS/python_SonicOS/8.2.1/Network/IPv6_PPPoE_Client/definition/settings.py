import os
import sys
import re
import copy
import time
import json
from contextvars import ContextVar
from datetime import datetime

from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from nose_parameterized import parameterized
import paramunittest

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API.system import SettingApi, DiagnosticApi
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Network/IPv6_PPPoE_Client/'
sys.path.append(suite_path)
TESTPLAN = suite_path + 'testplan/IPv6_PPPoE_Client.json'
defi_path = suite_path + 'definition/'
CONF_PATH = defi_path +'config/'
# from definition import network

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4', 'eth2')
X3_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X3:1')
logger.info(f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC3_ETH2_IP: {PC3_ETH2_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC4_ETH2_IP: {PC4_ETH2_IP}'
            f'\n X3_VLAN1_ID: {X3_VLAN1_ID}'

            )

PC1_login = Host(PC1_ETH2_IP)
PC2_login = Host(PC2_ETH1_IP)
PC3_login = Host(PC3_ETH1_IP)
PC4_login = Host(PC4_ETH1_IP)

# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_PC = PC2_ETH2_IP
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2

# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api'
)

fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh'
)


routeapi = network.RoutePolicyApi(fw)
interfaceapi = network.InterfaceIPv4Api(fw)
interfacev6api = network.InterfaceIPv6Api(fw)
failoverapi = network.FailoverLbApi(fw)
routepolicyapi = network.RoutePolicyApi(fw)
aoapi = network.AddressobjectsApi(fw)

interfacecli = InterfaceCli(fw_cli)
settingapi = SettingApi(fw)
diagnosticapi = DiagnosticApi(fw)
licensecli = LicenseCli(fw_cli)

x1_v6_dict = {
            'name': 'x1',
            'mode': 'pppoe6',
            "listen_router_advertisement": True,
            'pppoe6': {
                'mode_assign': 'dhcpv6',
                'prefix_delegation': {},
                'rapid_commit': False,
                'inactivity': 5,
                'lcp_echo_packets': False,
                'ncp_neg_retrans': 5,
                'reconnect': 5,
            }
        }
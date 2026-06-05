import os
import sys
import re
import time
import copy
import requests
import subprocess
import asyncio
import unittest
import json
import asyncio
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.API import securityservices
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.log import LogMonitorApi
from lib.modules.API.dpissl import ClientSslApi

##############################################################################
# PC1(eth1) ---(X0) FW (X1) --- (eth1)PC4 --- external network
#                      (X2)
#                 (eth2)↑
# PC1(eth2) --- (eth1)PC2(eth3) ---(eth1)PC3
##############################################################################

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/One_arm_Mode/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
CONF_PATH = suite_path + 'definition/conf'
SCRIPTS_PATH = suite_path + 'definition/scripts'
TESTPLAN = suite_path + 'testplan/One_arm_Mode.json'
HTTPS_SERVER_PATH = CONF_PATH + '/httpserver'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
configPath = os.environ["PYTHON_SONICOS_HOME"] + '/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/'


# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH2_NET = '172.168.1.0'
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC2_ETH3_IP = os_obj.get_node_interface_ip('PC2', 'eth3')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH1_NET = '13.13.1.0'
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC2_ETH3_IP: {PC2_ETH3_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X2_IP = '192.168.20.168'
    X2_GW = '192.168.20.1'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)
interfaceapi = InterfaceIPv4Api(fw)
accessruleapi = AccessRuleApi(fw)
logapi = LogMonitorApi(fw)
interfacecli = InterfaceCli(fw_cli)
spywareapi = securityservices.AntiSpywareApi(fw)
gavapi = securityservices.GAV(fw)
ipsapi = securityservices.IPSApi(fw)
clientsslapi = ClientSslApi(fw)
routepolicyapi = RoutePolicyApi(fw)


x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
    'mgmt-snmp': True,
}
x2_wan_arm_dict = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X2_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
    'mgmt-snmp': True,
    'one_arm_mode': True,
    'one_arm_peer': PC2_ETH2_IP
}
x2_dhcp_arm_dict = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'dhcp',
    'mgmt_https': True,
    'mgmt_ping': True,
    'one_arm_mode': True,
    'one_arm_peer': PC2_ETH2_IP
}

x2_lan_dict = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}
x2_lan_arm_dict = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
    'one_arm_mode': True,
    'one_arm_peer': PC2_ETH2_IP
}

import os
import sys
import re
import time
import json

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

# import form branch lib contents for test suit
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, DnsSettingsApi
from lib.modules.API.system import DiagnosticApi, RestartApi, PacketmonitorApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_TP53/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
FILE_PATH = suite_path + 'definition/files'
SCRIPT_PATH = suite_path + 'definition/files/scripts'
TESTPLAN = suite_path + 'testplan/DNS_TP53.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.168'
    X1_GW = '172.16.1.1'
    X1_NET = '172.16.1.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    VALID_DNS = PC3_ETH1_IP
    FAKE_DNS1 = '2.2.2.2'
    FAKE_DNS2 = '3.3.3.3'
    X2_IP = '192.168.20.168'
    MASK = '255.255.255.0'
    DNS_SERVER_IP = PC3_ETH1_IP
    NS_TEST_COM_IP = '114.114.114.114'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)
interfacev4api = InterfaceIPv4Api(fw)
diagapi = DiagnosticApi(fw)
dnssettingapi = DnsSettingsApi(fw)
restartapi = RestartApi(fw)
packetmonitorapi = PacketmonitorApi(fw)


# parameters on the test cases
class CaseParm:
    tc11testres= False
    tc6backupip = '172.16.1.200'


dns_dict = {
    "dns": {
        "server": {
            "inherit": False,
            "static": {
                "primary": Parameter.VALID_DNS,
                "secondary": Parameter.FAKE_DNS1,
                "tertiary": Parameter.FAKE_DNS2,
            }
        }
    }
}

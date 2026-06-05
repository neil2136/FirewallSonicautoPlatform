import os
import sys
import re
import copy
import time
import paramiko
import requests

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, ArpApi
from lib.modules.API.system import PacketmonitorApi, RestartApi
from lib.modules.CLI.system import DiagnosticsCli, LicenseCli

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DHCP_Client_TP54/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DHCP_Client_TP54')

os_obj = Openstack(Params.testbed)
PC2_ETH0_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC', 'eth2')
PC2_ETH3_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC', 'eth3')
PC2_GW = os_obj.get_node_interface_ip('DUT-X1-GW-PC', 'eth2')
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')

logger.info(f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            + f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            + f"\n PC2_ETH2_IP : {PC2_ETH2_IP}"
            + f"\n PC2_ETH3_IP : {PC2_ETH3_IP}"
            + f"\n PC2_GW : {PC2_GW}"
            + f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            + f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            )

pc1login = Host(PC1_ETH0_IP)
pc2login = Host(PC2_ETH3_IP)
script_path = os.environ["PYTHON_SONICOS_HOME"] \
              + '/Network/DHCP_Client_TP54/definition/script/'


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '0.0.0.0'
    X1_DNS = Params.G_DNS1
    X2_IP = '14.1.1.168'
    MASK = '255.255.255.0'
    X1_DHCP_IP = '0.0.0.0'
    X3_GW = '0.0.0.0'
    ALL0IP = '0.0.0.0'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] \
               + '/Network/DHCP_Client_TP54/testplan/dhcp_client_tp54.json'


x1_dhcp_dict = {
    'if': 'x1',
    'zone': 'wan',
    'mode': 'dhcp',
    'dhcp_hostname': '',
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    'mgmt_ping': True,
    'user_https': True,
}

x3_dhcp_dict = {
    'if': 'x3',
    'zone': 'wan',
    'mode': 'dhcp',
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    'mgmt_ping': True,
    'user_https': True,
}

ip = Parameter.FIREWALL
fw_cli = Firewall(ip,
                  user='admin',
                  password='password',
                  supported_config_mode='cli-ssh')
fw = Firewall(ip,
              user='admin',
              password='password')
interfacev4api = InterfaceIPv4Api(fw)
restartapi = RestartApi(fw)
packetmonitorapi = PacketmonitorApi(fw)
diagnosticscli = DiagnosticsCli(fw_cli)
arpapi = ArpApi(fw)
licensecli = LicenseCli(fw_cli)

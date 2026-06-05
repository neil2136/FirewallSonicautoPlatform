import os
import sys
import re
import time

import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, ArpApi, AddressobjectsApi
from lib.modules.API.policy import NatPolicyApi, SecurityPolicyApi
from lib.modules.API.accessrule import AccessRuleIPv4Api

from lib.modules.CLI.network import AddressObjectCli, InterfaceCli
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.API.vpn import VpnbasesettingApi, VpnAdvancedsettingApi

from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/VLAN_TP296')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'Network/VLAN_TP296/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'Network/VLAN_TP296/definition')
scripts_path = os.environ["PYTHON_SONICOS_HOME"] + \
               '/Network/VLAN_TP296/definition/scripts/'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')
X2_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X2:1')
X4_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X4:1')
X4_VLAN2_ID = os_obj.get_node_interface_vlan_id('UTM', 'X4:2')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC1_ETH3_IP: {PC1_ETH3_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC5_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC5_ETH1_IP: {PC5_ETH1_IP}'
            f'\n X2_VLAN1_ID: {X2_VLAN1_ID}'
            f'\n X4_VLAN1_ID: {X4_VLAN1_ID}'
            f'\n X4_VLAN2_ID: {X4_VLAN2_ID} \n')

PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)
PC5_login = Host(PC5_ETH0_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '10.10.0.168'
    X3_IP = '13.13.1.168'
    X4_IP = "100.1.1.168"
    X2_SUB = "12.12.1.0"
    X2_VLAN_IP = '12.12.1.168'
    X4_VLAN1_IP = "4.4.4.168"
    X4_VLAN1_SUB = "4.4.4.0"
    X4_VLAN2_IP = "5.5.5.168"
    MASK = '255.255.255.0'
    X1_GW = '10.10.0.1'
    X2_GW = '12.12.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_NAT_IP = '10.10.0.200'

    X1_REMOTE_IP = '12.12.1.201'
    X0_REMOTE_IP = '172.16.1.101'
    X0_REMOTE_SUB = '172.16.1.0'

    PC1_ETH0_IP = '192.168.168.169'
    PC1_ETH1_IP = '13.13.1.169'
    PC1_ETH2_IP = '14.14.1.169'
    PC2_ETH0_IP = '172.16.1.30'
    PC2_ETH1_IP = '192.168.2.30'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
        '/Network/VLAN_TP296/testplan/vlan_tp296.json'

from lib.modules.CLI.system import LicenseCli

fw_cli = Firewall(
    '192.168.168.168',
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)


x4_vlan1_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN1_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN1_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
arp_dict = {
            'ip': PC2_ETH1_IP,
            'mac': None,
            'interface': f'X4:V{X4_VLAN1_ID}',
            'publish': False,
            'bind_mac': False,
        }

ip = Parameter.FIREWALL
fw = Firewall(
    ip,
    user='admin',
    password='password',
    supported_config_mode='api')
R_fw = Firewall(
    Parameter.X1_REMOTE_IP,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')
R_fw_api = Firewall(
    Parameter.X1_REMOTE_IP,
    user='admin',
    password='password',
    supported_config_mode='api')

interfacev4api = InterfaceIPv4Api(fw)
aoapi = AddressobjectsApi(fw)
localvpnapi = VpnbasesettingApi(fw)
localvpnadvancedapi = VpnAdvancedsettingApi(fw)
remoteinterfacecli = InterfaceCli(R_fw)
remoteaocli = AddressObjectCli(R_fw)
remotevpncli = VpnBaseSettingsCli(R_fw)
remotevpnapi = VpnbasesettingApi(R_fw_api)

arpapi = ArpApi(fw)
natpolicyconfapi = NatPolicyApi(fw)
securitypolicyapi = SecurityPolicyApi(fw)
accessruleapi = AccessRuleIPv4Api(fw)

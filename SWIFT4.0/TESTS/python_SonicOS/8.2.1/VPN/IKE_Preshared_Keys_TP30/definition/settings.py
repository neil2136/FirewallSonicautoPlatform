import os
import sys
import re
import time
import copy
import requests
import subprocess
import asyncio
import unittest
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from tools.trafficGen import MyFtp

# import form branch lib contents for test suit
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.vpn import VpnbasesettingApi, VpnAdvancedsettingApi
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.API.log import LogMonitorApi
from lib.modules.API.securityservices import GAV
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.system import PacketmonitorApi, TimeApi

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IKE_Preshared_Keys_TP30/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/ike_preshared_keys_tp30.json'
CONF_PATH = suite_path + 'definition/config/'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC6_ETH0_IP = os_obj.get_node_interface_ip('PC6', 'eth0')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC5_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC6_ETH0_IP: {PC6_ETH0_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)


# parameters on the fw
class Parameter:
    PC2_ETH0_NewIP = '2.2.2.200'
    PC2_ETH2_GW = '192.168.2.1'
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_SUBNET = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X2_IP = '192.168.2.168'
    MASK = '255.255.255.0'
    X2_SUBNET = '192.168.2.0'

    LOCAL_X0_NET = '192.168.168.0'
    REMOTE_X0_IP = '172.16.1.101'
    REMOTE_X0_NET = '172.16.1.0'
    REMOTE_X1_IP = '12.12.1.201'
    REMOTE_X1_NET = '12.12.1.0'
    REMOTE_X3_IP = '12.12.3.201'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')
r_fw = Firewall(
    Parameter.REMOTE_X3_IP,
    user='admin',
    password='password')

interfaceapi = network.InterfaceIPv4Api(fw)
iphelperapi = network.IpHelperApi(fw)
zonesapi = network.ZoneObjectsApi(fw)
timeapi = TimeApi(fw)
logapi = LogMonitorApi(fw)
gav = GAV(fw)
packetmonitorapi = PacketmonitorApi(fw)
vpnsettingapi = VpnAdvancedsettingApi(fw)
accessruleapi = AccessRuleApi(fw)

licensecli = LicenseCli(fw_cli)
vpnsettingscli = VpnBaseSettingsCli(fw_cli)

l_vpnbasesettingapi = VpnbasesettingApi(fw)
r_vpnbasesettingapi = VpnbasesettingApi(r_fw)
l_aoapi = network.AddressobjectsApi(fw)
r_aoapi = network.AddressobjectsApi(r_fw)
l_vpnapi = VpnbasesettingApi(fw)
r_vpnapi = VpnbasesettingApi(r_fw)
r_iphelperapi = network.IpHelperApi(r_fw)

localfile = '/root/Downloads/test.txt'
remotefile = '/var/www/html/virus/test.txt'
my_ftp = MyFtp(host=PC4_ETH1_IP, user='root', password='password')


x1_static_dict = {
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
}
edit_localvpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': 'localvpn',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': Parameter.REMOTE_X1_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '2.2.2.2',
    'peer_ike_id': '2.2.2.2',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_name': 'remote_vpn_net',

    'ike_exchange': 'main',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 120,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_256',
    'ipsec_auth': 'sha_256',
    'ipsec_lifetime': 120,

    'keep_alive': True,
}
edit_remotevpn_dict = {
    'edit_auth': True,
    'edit_network': True,
    'edit_proposal': True,
    'edit_advanced': True,
    'type': 'site_to_site',
    'name': 'remotevpn',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'pri_gate': Parameter.X1_IP,
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '2.2.2.2',
    'peer_ike_id': '2.2.2.2',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_name': 'local_vpn_net',

    'ike_exchange': 'main',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 120,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_256',
    'ipsec_auth': 'sha_256',
    'ipsec_lifetime': 120,

    'keep_alive': False,
}
tc72_vpn_dict = {
    'type': 'site_to_site',
    'name': 'tc72_modify_test1',
    'pri_gate': '19.19.19.19',
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '35.35.35.35',
    'peer_ike_id': '35.35.35.35',

    'local_net_type': 'name',
    'local_net_name': 'X3 Subnet',
    'remote_net_type': 'name',
    'remote_net_name': 'test_vpn_net1',

    'ike_exchange': 'main',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 12000,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_256',
    'ipsec_auth': 'sha_256',
    'ipsec_lifetime': 12000,

    'keep_alive': False,
}

import os
import sys
import re
import time
import json
import requests

import unittest
import paramunittest
from nose_parameterized import parameterized

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import AddressobjectsApi, AddressobjectsApi, InterfaceIPv4Api, DHCPServerApi
from lib.modules.API import firewall
from lib.modules.API.vpn import DhcpOverVpnApi, VpnbasesettingApi, VpnAdvancedsettingApi
from lib.modules.API.system import PacketmonitorApi, RestartApi, TimeApi
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.API.log import LogSettingsApi, LogCategoryApi, LogMonitorApi
from lib.modules.API.system import PacketmonitorApi, RestartApi, TimeApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
basic_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/DHCP_Relay_TP28'
sys.path.append(basic_path)
TESTPLAN = basic_path + '/testplan/dhcp_relay_tp28.json'
DHCPCONF = basic_path + '/definition/dhcpd.conf'
script_path = basic_path + '/definition/'
dhcpconfpath = "/etc/dhcp/dhcpd.conf"

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH3_IP = os_obj.get_node_interface_ip('PC2', 'eth3')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
logger.info(f"\n PC1_ETH0_IP : {PC2_ETH0_IP}"
            + f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            + f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            + f"\n PC1_ETH3_IP : {PC1_ETH3_IP}"
            + f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            + f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            + f"\n PC2_ETH1_IP : {PC3_ETH1_IP}"
            )

LAN_HOST = Host(PC1_ETH2_IP)
RMT_HOST = Host(PC2_ETH3_IP)
WAN_HOST = Host(PC3_ETH1_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X1_ZONE = 'WAN'
    X1_SUBNET = '12.12.1.0'
    R_X1_IP = '12.12.1.201'
    R_X1_GW = X1_GW
    R_X0_IP = '172.16.1.101'
    R_X0_IP_START = '172.16.1.102'
    R_X0_IP_END = '172.16.1.254'
    R_X0_NET = '172.16.1.0'
    R_X2_IP = '12.12.2.201'
    R_X2_NET = '12.12.2.0'
    R_X2_ZONE = 'LAN'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    LAN_PC = '192.168.168.169'
    WAN_PC = '12.12.1.169'
    RELAY_IP = '172.16.1.10'
    MGMT_IP = '172.16.1.11'
    STATIC_IP = '172.16.1.15'
    R_X0_SCOPE_START = '172.16.1.5'
    R_X0_SCOPE_END = '172.16.1.120'
    R_X0_SCOPE_START_RENEW = '172.16.1.7'
    RELAY_IP_X2 = '12.12.2.10'
    MGMT_IP_X2 = '12.12.2.11'
    R_X2_SCOPE_START = '12.12.2.5'
    R_X2_SCOPE_END = '12.12.2.120'


class ParamCases:
    TC01dhcplease = ''
    TC03dhcplease = ''
    TC03dhcpleaserenew = ''
    TC03dhcpleaserestore = ''
    TC03fw_time = ''
    TC21rlanmac = ''
    TC23vpnstatusbefore = ''
    TC65dhcplease = ''
    TC66dhcplease = ''


ip = Parameter.FIREWALL
r_ip = Parameter.R_X1_IP
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
r_fw_api = Firewall(r_ip, user='admin', password='password', supported_config_mode='api')
r_fw_cli = Firewall(r_ip, user='admin', password='password', supported_config_mode='cli-ssh')
r_login_mgmt_ip = Firewall(Parameter.MGMT_IP, user='admin', password='password', supported_config_mode='api')
r_login_mgmt_ip_x2 = Firewall(Parameter.MGMT_IP_X2, user='admin', password='password', supported_config_mode='api')

ao_api = AddressobjectsApi(fw_api)
r_ao_api = AddressobjectsApi(r_fw_api)
interface_api = InterfaceIPv4Api(fw_api)
r_interface_api = InterfaceIPv4Api(r_fw_api)
accessrule_api = firewall.AccessRuleApi(fw_api)
centralvpnapi = VpnbasesettingApi(fw_api)
remotevpnapi = VpnbasesettingApi(r_fw_api)
rdhcpserverapi = DHCPServerApi(r_fw_api)
dhcpovervpnapi = DhcpOverVpnApi(fw_api)
rdhcpovervpnapi = DhcpOverVpnApi(r_fw_api)
logsettingapi = LogSettingsApi(fw_api)
logcategapi = LogCategoryApi(fw_api)
logmonitorapi = LogMonitorApi(fw_api)
lotimeapi = TimeApi(fw_api)
remotevpncli = VpnBaseSettingsCli(r_fw_cli)
license_cli = LicenseCli(fw_cli)

x1_static = {
    'if': 'X1',
    'zone': Parameter.X1_ZONE,
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.DNS1,
    'dns2': Parameter.DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
r_x2_static = {
    'if': 'X2',
    'zone': Parameter.R_X2_ZONE,
    'mode': 'static',
    'ip': Parameter.R_X2_IP,
    'netmask': Parameter.MASK,
    'mgmt-https': True,
    'mgmt-ssh': True,
    'mgmt-ping': True,
    'user_https': True,
}
remote_vpn_lan = {
    "object_type": "network",
    "name": "remote_vpn_lan",
    "zone": "VPN",
    "value": Parameter.X0_NET + ',' + Parameter.MASK,
}

s2svpn_main_central_vpn = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'centralvpn',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': 'password',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '1.1.1.1',
    'peer_ike_id': '2.2.2.2',
    'pri_gate': Parameter.R_X1_IP,
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'X0 Subnet',
    'remote_net_type': 'dhcp',
    'ike_exchange': 'main',
}

s2svpn_main_remote_vpn = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'remotevpn',
    'enable': True,
    'auth_mode': 'shared_secret',
    'secret': 'password',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '2.2.2.2',
    'peer_ike_id': '1.1.1.1',
    'pri_gate': Parameter.X1_IP,
    'local_net_type': 'dhcp',  ### name, group, host, network, range, any,chcp
    'remote_net_type': 'name',
    'remote_net_name': remote_vpn_lan['name'],
    'ike_exchange': 'main',
    'management_https': True,
    'keep_alive': True,
}

s2svpn_main_remote_vpn_disable = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'remotevpn',
    'enable': False,
}

s2svpn_main_remote_vpn_enable = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'remotevpn',
    'enable': True,
}

s2svpn_main_central_vpn_disable = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'centralvpn',
    'enable': False,
}

s2svpn_main_central_vpn_enable = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'centralvpn',
    'enable': True,
}

check_lease_dict_TC01_TC02 = {
    'staticleaseip': [Parameter.RELAY_IP, Parameter.MGMT_IP],
    'dhcpleaseip': [ParamCases.TC01dhcplease],
}

check_lease_dict_TC03 = {
    'staticleaseip': [Parameter.RELAY_IP, Parameter.MGMT_IP],
    'dhcpleaseip': [ParamCases.TC03dhcpleaserenew, ParamCases.TC03dhcplease]
}

check_lease_dict_TC21 = {
    'staticleaseip': [Parameter.RELAY_IP, Parameter.MGMT_IP, Parameter.STATIC_IP],
    'dhcpleaseip': ''
}

check_lease_dict_TC23 = {
    'staticleaseip': [Parameter.RELAY_IP, Parameter.MGMT_IP, Parameter.STATIC_IP],
    'dhcpleaseip': ''
}

check_lease_dict_TC65 = {
    'staticleaseip': [Parameter.RELAY_IP_X2, Parameter.MGMT_IP_X2],
    'dhcpleaseip': [ParamCases.TC65dhcplease]
}

check_lease_dict_TC66 = {
    'staticleaseip': [Parameter.RELAY_IP_X2, Parameter.MGMT_IP_X2],
    'dhcpleaseip': [ParamCases.TC66dhcplease]
}

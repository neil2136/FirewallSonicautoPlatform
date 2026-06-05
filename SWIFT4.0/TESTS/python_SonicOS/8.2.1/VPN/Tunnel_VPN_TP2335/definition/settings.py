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
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
from lib.modules.API import network
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.system import SettingApi, PacketmonitorApi
from lib.modules.API import log
from lib.modules.API.dpissl import ClientSslApi
from lib.modules.CLI.system import LicenseCli, StatusCli

# import form test suite root path like definition
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/Tunnel_VPN_TP2335/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/Tunnel_VPN_TP2335.json'
SCRIPTS_PATH = suite_path + 'definition/scripts'
CONF_PATH = suite_path + 'definition/config'

virus_server = '10.6.0.69'
https_virus_download = f'curl https://{virus_server}/new_virus/sboxSample/Macro.Word97.Appder.doc -k -o /tmp/virus.log'
http_ips_high = f'curl -k https://{virus_server}/ips/high_priority/IPS_5342_high_poc.xls -o /tmp/high_ips.log'
http_ips_medium = f'curl -k https://{virus_server}/ips/medium_priority/ips_3532_webclient.txt -o /tmp/medium_ips.log'
http_ips_low = f'curl -k http://{virus_server}/ips/low_priority/Exploit.JS.ActiveX.k -o /tmp/low_ips.log'

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
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')
PC5_ETH2_IP = os_obj.get_node_interface_ip('PC5', 'eth2')
PC5_ETH1_IPv6 = '2001:222::50'
X4_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X4:1')
logger.info(f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC3_ETH2_IP: {PC3_ETH2_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC4_ETH2_IP: {PC4_ETH2_IP}'
            f'\n PC5_ETH1_IP: {PC5_ETH1_IP}'
            f'\n PC5_ETH2_IP: {PC5_ETH2_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}'
            f'\n X4_VLAN1_ID: {X4_VLAN1_ID}')
PC1_login = Host(PC1_ETH2_IP)
PC2_login = Host(PC2_ETH2_IP)
PC3_login = Host(PC3_ETH2_IP)
PC4_login = Host(PC4_ETH2_IP)
PC5_login = Host(PC5_ETH2_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_SUBNET = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DHCP_IP = '12.12.1.20'
    X2_IP = '12.12.2.168'
    MASK = '255.255.255.0'
    X2_GW = '12.12.2.1'
    X2_SUBNET = '12.12.2.0'
    X2_V6_IP = '2001:100::101'
    X3_IP = '192.168.3.168'
    X3_GW = '192.168.3.1'
    X3_SUBNET = '192.168.3.0'
    X3_PPPoE_IP = '192.168.3.120'
    X4_VLAN1_IP = '44.44.44.168'

    NET_WAN_IP = '12.12.1.100'
    LAN_HOST_IP = PC2_ETH1_IP

    REMOTE_X0_IP = '172.16.1.101'
    REMOTE_X0_NET = '172.16.1.0'
    REMOTE_X1_IP = '12.12.1.201'
    REMOTE_X1_NET = '12.12.1.0'
    REMOTE_X2_IP = '12.12.2.201'
    REMOTE_X3_IP = '12.12.3.201'


class CaseParams:
    last_checked_time = ''
    tc66_test_res = False


class VPNParams:
    local_vpn1_name = 'localtivpn1'
    remote_vpn1_name = 'remotetivpn1'
    local_route1_name = 'localvpnroute1'
    remote_route1_name = 'remoetvpnroute1'
    local_vpn2_name = 'localtivpn2'
    remote_vpn2_name = 'remotetivpn2'
    local_route2_name = 'localvpnroute2'
    remote_route2_name = 'remoetvpnroute2'


class PPPoeParams:
    PPPOE_IF = "eth1"
    LOCAL_IP = PC5_ETH2_IP
    PPPOE_ASSIGN = Parameter.X1_IP
    PPP_SECRETS = CONF_PATH +'/pppoe/pap-secrets'
    PPPOE_OPTIONS = CONF_PATH +'/pppoe/pppoe-server-options'
    PPPOE_DOWN_IP = "0.0.0.0"


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
r_fw = Firewall(
    Parameter.REMOTE_X3_IP,
    user='admin',
    password='sonicauto')

interface_api = network.InterfaceIPv4Api(fw)
ao_api = network.AddressobjectsApi(fw)
networkroute_api = network.RoutePolicyApi(fw)
logcategory_api = log.LogCategoryApi(fw)
license_cli = LicenseCli(fw_cli)
accessrule_api = AccessRuleApi(fw)
packetmonitorapi = PacketmonitorApi(fw)

l_vpnbasesettingapi = VpnbasesettingApi(fw)
r_vpnbasesettingapi = VpnbasesettingApi(r_fw)
l_aoapi = network.AddressobjectsApi(fw)
r_aoapi = network.AddressobjectsApi(r_fw)
l_vpnapi = VpnbasesettingApi(fw)
r_vpnapi = VpnbasesettingApi(r_fw)
l_routepolicyapi = RoutePolicyApi(fw)
r_routepolicyapi = RoutePolicyApi(r_fw)
r_networkroute_api = network.RoutePolicyApi(r_fw)

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
x1_pppoe_opt_dynamic_dict = {
    'if': 'x1',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': 'root',
    'pppoe_servicename': '',
    'pppoe_passwd': 'password',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': True,
    'pppoe_inactivity': 2,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,
    'mgmt_ping': True,
    'mgmt_https': True,
    'mgmt_ssh': True
}
x2_wan_dict = {
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
}
x3_lan_dict = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
ti_vpn_dict = {
    'type': 'tunnel_interface',
    'name': VPNParams.local_vpn1_name,
    'pri_gate': Parameter.REMOTE_X1_IP,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '33.33.33.33',
    'peer_ike_id': '33.33.33.33',

    'ike_exchange': 'ikev2',
    'ike_dh_group': '14',
    'ike_encryption': 'aes-256',
    'ike_auth': 'sha-256',
    'ike_lifetime': 300,
    'ipsec_protocol': 'esp',
    'ipsec_encryption': 'aes_256',
    'ipsec_auth': 'sha_256',
    'ipsec_lifetime': 180,

    'keep_alive': True,
}
l_route_base_dict = {
    "auto_add_access_rules": True,
    "comment": "",
    "destination": {
        "name": "remote_vpn_net"
    },
    "disable_on_interface_down": True,
    "distance": {
        "auto": True
    },
    "gateway": {
        "default": True
    },
    "interface": VPNParams.local_vpn1_name,
    "mask": "0x00",
    "metric": 6,
    "name": VPNParams.local_route1_name,
    "probe": "",
    "service": {
        "any": True
    },
    "source": {
        "name": "X0 Subnet"
    },
    "tos": "0x00",
    "type": "standard"
}
r_route_base_dict = {
    "auto_add_access_rules": True,
    "comment": "",
    "destination": {
        "name": "local_vpn_net"
    },
    "disable_on_interface_down": True,
    "distance": {
        "auto": True
    },
    "gateway": {
        "default": True
    },
    "interface": VPNParams.remote_vpn1_name,
    "mask": "0x00",
    "metric": 6,
    "name": VPNParams.remote_route1_name,
    "probe": "",
    "service": {
        "any": True
    },
    "source": {
        "name": "X0 Subnet"
    },
    "tos": "0x00",
    "type": "standard"
}
edit_local_route_dict = {
    "name": 'ti_route1',
    "comment": "",
    "interface": 'seclocaltivpn',
    "metric": 2,
    "service": {
        "any": True
    },
    "gateway": {
        "default": True
    },
    "source": {
        "name": "X0 Subnet"
    },
    "destination": {
        "name": "remote_vpn_net"
    },
    "disable_on_interface_down": True,
    "probe": "",
    "distance": {
        "auto": True
    },
    "tos": "0x00",
    "mask": "0x00",
    "type": "standard",
    "auto_add_access_rules": True
}
unnumber_ti_dict = {
    'zone': 'VPN',
    'type': "vpn_tunnel",
    'mode': 'static',
    'ip': '2.2.2.2',
    'netmask': '255.255.255.0',
    "tunnel_name": 'AutoNITest',
    'comment': '',
    "vpn_policy": VPNParams.local_vpn1_name,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'flow_reporting': True,
    'multicast': True,
    'asymmetric_route': False,
    'fragment_packets': True,
    'ignore_df_bit': True,
}


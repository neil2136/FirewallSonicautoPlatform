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
from lib.modules.API.system import SettingApi, PacketmonitorApi,DiagnosticApi
from lib.modules.API import network
from lib.modules.CLI.network import InterfaceCli, RouteCli
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.vpn import VpnbasesettingApi
# from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.accessrule import AccessRuleIPv4Api

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Network/Split_DNS_Full/'
sys.path.append(suite_path)
TESTPLAN = suite_path + 'testplan/split_DNS.json'
defi_path = suite_path + 'definition/'
CONF_PATH = defi_path +'config/'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4', 'eth2')
PC1_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC1', 'eth2')
PC2_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC2', 'eth2')
PC3_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC3', 'eth2')
PC4_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC4', 'eth2')
logger.info(f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC1_ETH3_IP: {PC1_ETH3_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC3_ETH2_IP: {PC3_ETH2_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC4_ETH2_IP: {PC4_ETH2_IP}'
            f'\n PC1_ETH2_IPV6: {PC1_ETH2_IPV6}'
            f'\n PC2_ETH2_IPV6: {PC2_ETH2_IPV6}'
            f'\n PC3_ETH2_IPV6: {PC3_ETH2_IPV6}'
            f'\n PC4_ETH2_IPV6: {PC4_ETH2_IPV6}'
            )

console_info_rmt = os_obj.get_console_info('RemoteGEN7')
logger.info(console_info_rmt)

if console_info_rmt:
    consvr_rmt = console_info_rmt[0]
    conport_rmt = console_info_rmt[1]
else:
    consvr_rmt = ''
    conport_rmt = ''

logger.info(f"consvr_rmt is {consvr_rmt}")
logger.info(f"conport_rmt is {conport_rmt}")

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
    X2_IP = '12.12.2.101'
    X2_GW = '12.12.2.201'
    X3_IP = '13.13.1.168'
    X3_GW = PC3_ETH2_IP
    X3_SUBNET = '13.13.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2

    PREFIX_LENGTH = 64
    X0_IPV6 = "2001:2018::168"
    X0_NET_V6 = "2001:2018::/64"
    X0_PC_IPV6 = PC1_ETH2_IPV6[:-3]
    X1_IPV6 = '2001:2011::168'
    X1_GW_IPV6 = PC2_ETH2_IPV6[:-3]
    X2_IPV6 = '2001:2012::168'
    X2_GW_IPV6 = '2001:2012::201'
    X3_IPV6 = '2001:2013::168'
    X3_GW_IPV6 = PC4_ETH2_IPV6[:-3]

    REM_X0_IP = '172.16.1.101'
    REM_X2_IP = '12.12.2.201'
    REM_X2_GW = '12.12.2.101'
    REM_X3_IP = '12.12.3.201'
    REM_X3_GW = PC4_ETH2_IP

    REM_X3_SUBNET = "12.12.3.0"

    REM_X0_IPV6 = '2001:2016::201'
    REM_X2_IPV6 = '2001:2012::201'
    REM_X2_GW_IPV6 = '2001:2012::168'
    REM_X3_IPV6 = '2001:2103::201'
    REM_X3_GW_IPV6 = PC4_ETH2_IPV6[:-3]

    QUERY_DOMAIN_TC69 = "pc1.baidu.com"
    QUERY_DOMAIN_TC68 = "pc6.baidu.com"
    QUERY_DOMAIN_TC70 = "pc2.baidu.com"
    QUERY_DOMAIN_TC72 = "pc3.baidu.com"
    QUERY_DOMAIN_TC77 = "pc4.baidu.com"
    QUERY_DOMAIN_TC94 = "pc5.baidu.com"
    QUERY_DOMAIN_TC79 = "www.baidu.com"

    VPN_IF_IP_LOCAL = '72.1.1.2'
    VPN_IF_IP_REMOTE = '72.1.1.1'
    VPN_IF_IP_LOCAL_MODIFY = '72.2.1.2'
    VPN_IF_IP_REMOTE_MODIFY = '72.2.1.1'

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

rmt_fw = Firewall(
    Parameter.REM_X0_IP,
    user='admin',
    password='sonicauto',
    supported_config_mode='api'
)

rmt_fw_cli = Firewall(
    Parameter.REM_X0_IP,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh'
)

rmt_fw_console = Firewall(
    ip=Parameter.REM_X0_IP,
    console_ip=consvr_rmt,
    console_port=conport_rmt,
    user='admin',
    password='password',
    supported_config_mode='cli-console'
)

splitdnsapi = network.DnsSettingsApi(fw)
dnsproxyapi = network.DnsProxyApi(fw)
dnspolicyapi = network.DnsPolicyApi(fw)
routeapi = network.RoutePolicyApi(fw)
rmtrouteapi = network.RoutePolicyApi(rmt_fw)
interfaceapi = network.InterfaceIPv4Api(fw)
rmtinterfaceapi = network.InterfaceIPv4Api(rmt_fw)
interfacev6api = network.InterfaceIPv6Api(fw)
rmtinterfacev6api = network.InterfaceIPv6Api(rmt_fw)
zonesapi = network.ZoneObjectsApi(fw)
aclapi= AccessRuleIPv4Api(fw)
rmtaclapi= AccessRuleIPv4Api(rmt_fw)
interfacecli = InterfaceCli(fw_cli)
settingapi = SettingApi(fw)
routepolicyapi = RoutePolicyApi(fw)
routecli = RouteCli(fw_cli)
aoapi = network.AddressobjectsApi(fw)
rmtaoapi = network.AddressobjectsApi(rmt_fw)
dnsapi = network.DnsSettingsApi(fw)
pkgmonitorapi = PacketmonitorApi(fw)
rmtpkgmonitorapi = PacketmonitorApi(rmt_fw)
diagnosticapi = DiagnosticApi(fw)
licensecli = LicenseCli(fw_cli)
vpnapi = VpnbasesettingApi(fw)
rmtvpnapi = VpnbasesettingApi(rmt_fw)


# DUT ao
local_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REM_X3_SUBNET),
}

# RemoteDUT ao
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.X3_SUBNET),
}

# tunnel VPN policy
Lvpn = {
    'type'              : 'tunnel_interface',
    'name'              : 'test',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.REM_X2_IP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.FIREWALL,
    'peer_ike_id'       : Parameter.REM_X0_IP,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.X3_SUBNET,
    'remote_net_name'   : "remote_net",
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_encryption'  : 'aes_128',

    'ipversion'          : 'ipv4',
    'ike_auth'          : 'sha-1',
    'ike_dh_group'      : '2',
    'ike_lifetime'      : '28800',
    'ipsec_lifetime'    : '28800',
    'ipsec_protocol'    : 'esp',
    'ipsec_auth'        : 'sha_1',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'advanced_routing': True,
    'bound_to': ['interface', 'X2'],
}

Rvpn = {
    'type'              : 'tunnel_interface',
    'name'              : 'test',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.X2_IP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.REM_X0_IP,
    'peer_ike_id'       : Parameter.FIREWALL,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.X3_SUBNET,
    'remote_net_name'   : "remote_net",
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_encryption'  : 'aes_128',
    'ipversion'          : 'ipv4',
    'ike_auth'          : 'sha-1',
    'ike_dh_group'      : '2',
    'ike_lifetime'      : '28800',
    'ipsec_lifetime'    : '28800',
    'ipsec_protocol'    : 'esp',
    'ipsec_auth'        : 'sha_1',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'advanced_routing'  : True,
    'bound_to': ['interface', 'X2'],
}
Tunnel_Interface = {
            'zone'          : 'VPN',
            'type'          : "vpn_tunnel",
            'mode'          : 'static',
            'ip'            : Parameter.VPN_IF_IP_LOCAL,
            'netmask'       : '255.255.255.0',
            "tunnel_name"   : "Ni",
            'comment'       : '',
            "vpn_policy"    :"test",
            'mgmt_https'    : True,
            'mgmt_ssh'      : True,
            'mgmt_ping'     : True,
            'mgmt_snmp'     : True,
            'flow_reporting': True,
            'multicast'     : True,
            'asymmetric_route': False,
            'fragment_packets': True,
            'ignore_df_bit'   :True,
        }

## site_to_site_vpn
local_vpn_dict = {
    'type': 'site_to_site',
    'name': 'local_vpn_1',
    'pri_gate': Parameter.REM_X2_IP,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '1.1.1.1',
    'peer_ike_id': '2.2.2.2',
    'local_net_type': 'name',
    'local_net_name': 'X3 Subnet',
    'remote_net_type': 'name',
    'remote_net_name': 'remote_net',
    'keep_alive': True,
    'bound_to': ['interface', 'X2'],
}

remote_vpn_dict = {
    'type': 'site_to_site',
    'name': 'remote_vpn_1',
    'pri_gate': Parameter.X2_IP,
    'auth_mode': 'shared_secret',
    'secret': '123456',
    'local_ike_type': 'ipv4',
    'peer_ike_type': 'ipv4',
    'local_ike_id': '2.2.2.2',
    'peer_ike_id': '1.1.1.1',
    'local_net_type': 'name',
    'local_net_name': 'X3 Subnet',
    'remote_net_type': 'name',
    'remote_net_name': 'remote_net',
    'keep_alive': True,
    'bound_to': ['interface', 'X2'],
}

route_policy_dict = {
    "route_policies": [
        {
            "ipv4": {
                "interface": "Ni",
                "metric": 1,
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "remote_net"
                },
                "service": {
                    "any": True
                },
                "gateway": {
                    "default": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "distance": {
                    "auto": True
                },
                "name": "to_remote_x3",
                "type": "standard",
                "comment": "",
                "disable_on_interface_down": False,
                "probe": "",
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": "",
                }
            }
        }
    ]
}

acl_dict = {
    'name': 'test_vpn_lan',
    'from': 'VPN',
    'to': 'LAN',
    'source_addr': {'any': True},
    'dst_addr': {'any': True},
    'service': {'any': True},
    'action': 'allow',
}

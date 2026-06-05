import os
import sys
import re
import copy
import time
import json
from contextvars import ContextVar

from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from nose_parameterized import parameterized

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from config.restore_gw_rmt_tel import ConfigInterfaceTelnet
from config.restore_tel import RestoreFwTelnet
from utm import is_Firewall_up
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.system import PacketmonitorApi, SettingApi
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, DynamicRoutingApi, RoutePolicyApi
from lib.modules.API.vpn import VpnbasesettingApi



from lib.modules.API.users import UserLocalApi
from lib.modules.API.firewallsettings import AdvanceApi
from lib.modules.CLI.network import InterfaceCli, RouteCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/Dynamic_Route_Based_VPN-TP2438/'
sys.path.append(suite_path)
defi_path = suite_path + 'definition'
TESTPLAN = suite_path + 'testplan/Dynamic_Route_Based_VPN-TP2438.json'
script_path = defi_path + '/script'
# from definition.vpn import VpnbasesettingApi
# from definition.network import InterfaceIPv4Api, AddressobjectsApi, DynamicRoutingApi, RoutePolicyApi

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC2_ETH3_IP = os_obj.get_node_interface_ip('PC2', 'eth3')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC3_ETH3_IP = os_obj.get_node_interface_ip('PC3', 'eth3')

X3_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X3:1')
logger.info(f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC1_ETH3_IP: {PC1_ETH3_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC2_ETH3_IP: {PC2_ETH3_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC3_ETH2_IP: {PC3_ETH2_IP}'
            f'\n PC3_ETH3_IP: {PC3_ETH3_IP}'
            f'\n X3_VLAN1_ID: {X3_VLAN1_ID}'
            )
console_info_gw = os_obj.get_console_info('VPNGW')
logger.info(console_info_gw)

if console_info_gw:
    consvr_gw = console_info_gw[0]
    conport_gw = console_info_gw[1]
else:
    consvr_gw = ''
    conport_gw = ''

logger.info(f"consvr_gw is {consvr_gw}")
logger.info(f"conport_gw is {conport_gw}")

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH3_IP)
PC3_Login = Host(PC3_ETH3_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.101'
    X1_DNS1 = '10.190.202.200'
    X2_IP = '192.168.22.168'
    X3_VLAN1_IP = '192.168.33.168'
    X2_VLAN1_IP = '192.168.100.168'
    X2_VLAN1_ID = '100'
    GW_X0_IP = '11.11.11.101'
    GW_X1_IP = '12.12.1.101'
    GW_X2_IP = '12.12.2.101'
    GW_X3_IP = '12.12.3.101'
    LOCALSUBNET = '192.168.168.0'
    REMOTESUBNET = '11.11.11.0'
    X3_VLAN1_SUBNET = '192.168.33.0/24'
    X2_SUBNET = '192.168.22.0/24'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api'
)

fw_gw = Firewall(
    Parameter.GW_X0_IP,
    user='admin',
    password='password',
    supported_config_mode='api'
)

fwcli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh'
)

gwcli = Firewall(
    Parameter.GW_X0_IP,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh'
)

fw_gw_console = Firewall(
    ip=Parameter.GW_X0_IP,
    console_ip=consvr_gw,
    console_port=conport_gw,
    user='admin',
    password='password',
    supported_config_mode='cli-console'
)

settingapi = SettingApi(fw)

pkgapi = PacketmonitorApi(fw)
gwpkgapi = PacketmonitorApi(fw_gw)

vpnapi = VpnbasesettingApi(fw)
gwvpnapi = VpnbasesettingApi(fw_gw)

aoapi = AddressobjectsApi(fw)
gwaoapi = AddressobjectsApi(fw_gw)

interfaceapi = InterfaceIPv4Api(fw)
gwinterfaceapi = InterfaceIPv4Api(fw_gw)

interfacecli = InterfaceCli(fwcli)
gwinterfacecli = InterfaceCli(gwcli)

dyrouteapi = DynamicRoutingApi(fw)
gwdyrouteapi = DynamicRoutingApi(fw_gw)

routeapi = RoutePolicyApi(fw)
gwrouteapi = RoutePolicyApi(fw_gw)

routecli = RouteCli(fwcli)
gwroutecli = RouteCli(gwcli)


# DUT ao
local_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTESUBNET),
}
ao_base_dict = {
            "object_type": "network",
            "name": 'test_59',
            "zone": "LAN",
            "value": "1.1.1.0,255.255.255.0"
        }
aogw_dict = {
    "object_type": "host",
    "name": 'X0GW',
    "zone": "LAN",
    "value": "192.168.168.111"
}

# RemoteDUT ao
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCALSUBNET),
}

route_base_dict = {
            "interface": "",
            "metric": 1,
            "source": {"any": True},
            'destination': {'any': True},
            'service': {'any': True},
            'gateway': {'name': ''},
            "tos": "0x00",
            "mask": "0x00",
            "distance": {"auto": True},
            "name": 'test_route',
            "type": "standard",
            "priority": 1,
            "comment": "",
            "disable_on_interface_down": False,
            "vpn_precedence": False,
            "probe": "",
            "ticket": {"tag1": "", "tag2": "", "tag3": ""}
        }

# VPN policy
Lvpn = {
    'type'              : 'tunnel_interface',
    'name'              : 'test',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.GW_X1_IP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.FIREWALL,
    'peer_ike_id'       : Parameter.GW_X0_IP,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
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
    # 'bound_to': ['interface', 'X1'],
}
Rvpn = {
    'type'              : 'tunnel_interface',
    'name'              : 'test',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.X1_IP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.GW_X0_IP,
    'peer_ike_id'       : Parameter.FIREWALL,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
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
}

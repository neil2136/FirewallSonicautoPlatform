
import os
import sys
import re
import copy
import time

from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from nose_parameterized import parameterized
import paramunittest

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
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, DynamicRoutingApi, RoutePolicyApi
from lib.modules.CLI.system import AdminCli
from lib.modules.API.system import PacketmonitorApi, DiagnosticApi, SettingApi
from lib.modules.CLI.network import InterfaceCli, RouteCli


# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Network/Advanced_Routing_TP294_With_3_DUTs/'
sys.path.append(suite_path)
defi_path = suite_path + 'definition'
TESTPLAN = suite_path + 'testplan/AdvanceRoutingSmoke.json'
# from definition.network import AddressobjectsApi, RoutePolicyApi, DynamicRoutingApi, InterfaceIPv4Api

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC1_ETH4_IP = os_obj.get_node_interface_ip('PC1', 'eth4')
X2_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X2:1')
X3_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X3:1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC1_ETH3_IP: {PC1_ETH3_IP}'
            f'\n PC1_ETH4_IP: {PC1_ETH4_IP}'
            f'\n X2_VLAN1_ID: {X2_VLAN1_ID}'
            f'\n X3_VLAN1_ID: {X3_VLAN1_ID}'
            )
console_info_UTM = os_obj.get_console_info('UTM')
console_info_LBOX = os_obj.get_console_info('LBOX')
console_info_RBOX = os_obj.get_console_info('RBOX')
logger.info(console_info_UTM)
if console_info_UTM:
    consvr_UTM = console_info_UTM[0]
    conport_UTM = console_info_UTM[1]
else:
    consvr_UTM = ''
    conport_UTM = ''
logger.info(console_info_LBOX)
if console_info_LBOX:
    consvr_LBOX = console_info_LBOX[0]
    conport_LBOX = console_info_LBOX[1]
else:
    consvr_LBOX = ''
    conport_LBOX = ''
logger.info(console_info_RBOX)
if console_info_RBOX:
    consvr_RBOX = console_info_RBOX[0]
    conport_RBOX = console_info_RBOX[1]
else:
    consvr_RBOX = ''
    conport_RBOX = ''


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_DNS1 = '10.190.202.200'
    X2_VLAN1_IP = '12.1.1.168'
    X3_VLAN1_IP = '13.1.1.168'
    LBOX_X0_IP = '192.1.1.100'
    LBOX_X1_IP = '12.12.1.100'
    LBOX_X1_GW = '12.12.1.1'
    LBOX_X1_DNS1 = '10.190.202.200'
    LBOX_X2_IP = '12.1.1.100'
    RBOX_X0_IP = '192.2.1.101'
    RBOX_X1_IP = '12.12.1.101'
    RBOX_X1_GW = '12.12.1.1'
    RBOX_X1_DNS1 = '10.190.202.200'
    RBOX_X3_IP = '13.1.1.101'
    LAN_PC = PC1_ETH1_IP
    X2_VLAN1_INDEX = 0
    X2_VLAN1_INDEX = 0
    

# parameters on the test cases
class CaseParams:
    res_57 = False


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)


lbox_fw = Firewall(
    Parameter.LBOX_X0_IP,
    user='admin',
    password='password',
    supported_config_mode='api'
)

rbox_fw = Firewall(
    Parameter.RBOX_X0_IP,
    user='admin',
    password='password',
    supported_config_mode='api'
)

fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

lbox_fw_cli = Firewall(
    Parameter.LBOX_X0_IP,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

rbox_fw_cli = Firewall(
    Parameter.RBOX_X0_IP,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

UTM_fw_console = Firewall(
    ip=Parameter.FIREWALL,
    console_ip=consvr_UTM,
    console_port=conport_UTM,
    user='admin',
    password='password',
    supported_config_mode='cli-console'
)

LBOX_fw_console = Firewall(
    ip=Parameter.LBOX_X0_IP, 
    console_ip=consvr_LBOX, 
    console_port=conport_LBOX,
    user='admin', 
    password='password', 
    supported_config_mode='cli-console'
    )
    
RBOX_fw_console = Firewall(
    ip=Parameter.RBOX_X0_IP, 
    console_ip=consvr_RBOX, 
    console_port=conport_RBOX,   
    user='admin', 
    password='password', 
    supported_config_mode='cli-console'
    )


diagnosticapi = DiagnosticApi(fw)
pkgapi = PacketmonitorApi(fw)
settingapi = SettingApi(fw)

interfaceapi = InterfaceIPv4Api(fw)
lbox_interfaceapi = InterfaceIPv4Api(lbox_fw)
rbox_interfaceapi = InterfaceIPv4Api(rbox_fw)

interfacecli = InterfaceCli(fw_cli)

interfaceconsole = InterfaceCli(UTM_fw_console)
LBOX_interfaceconsole = InterfaceCli(LBOX_fw_console)
RBOX_interfaceconsole = InterfaceCli(RBOX_fw_console)

adminconsole = AdminCli(UTM_fw_console)
LBOX_adminconsole = AdminCli(LBOX_fw_console)
RBOX_adminconsole = AdminCli(RBOX_fw_console)

dyrouteapi = DynamicRoutingApi(fw)
lbox_dyrouteapi = DynamicRoutingApi(lbox_fw)
rbox_dyrouteapi = DynamicRoutingApi(rbox_fw)

routeapi = RoutePolicyApi(fw)
lbox_routeapi = RoutePolicyApi(lbox_fw)
rbox_routeapi = RoutePolicyApi(rbox_fw)

routecli = RouteCli(fw_cli)
lbox_routecli = RouteCli(lbox_fw_cli)
rbox_routecli = RouteCli(rbox_fw_cli)

aoapi = AddressobjectsApi(fw)
lbox_aoapi = AddressobjectsApi(lbox_fw)
rbox_aoapi = AddressobjectsApi(rbox_fw)


# parameters on the test cases
api_dict = {'sonicos-api': True, 'basic': True, }
PC1_login = Host(Parameter.LAN_PC)

ao_base_dict = {
            "object_type": "network",
            "name": 'test',
            "zone": "LAN",
            "value": "1.1.1.0,255.255.255.0"
        }

aogw_dict = {
            "object_type": "host",
            "name": 'X0GW',
            "zone": "LAN",
            "value": "192.168.168.200"
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

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
from lib.modules.API.network import AddressobjectsApi, RoutePolicyApi, DynamicRoutingApi, InterfaceIPv4Api
from lib.modules.CLI.system import AdminCli,StatusCli
from lib.modules.API.system import PacketmonitorApi, SettingApi
from lib.modules.CLI.network import InterfaceCli, RouteCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Network/Advanced_Routing_TP294_With_2_DUTs/'
sys.path.append(suite_path)
defi_path = suite_path + 'definition'
TESTPLAN = suite_path + 'testplan/AdvanceRoutingSmoke.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC1_ETH3_IP: {PC1_ETH3_IP}'   
            )
console_info_UTM = os_obj.get_console_info('UTM')
console_info_LBOX = os_obj.get_console_info('LBOX')
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


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_DNS1 = '10.190.202.200'
    X2_IP = '12.1.1.168'
    LBOX_X0_IP = '192.1.1.100'
    LBOX_X1_IP = '12.12.1.100'
    LBOX_X1_GW = '12.12.1.1'
    LBOX_X1_DNS1 = '10.190.202.200'
    LBOX_X2_IP = '12.1.1.100'
    LAN_PC = PC1_ETH1_IP


# parameters on the test cases
class CaseParams:
    res_143 = ''
   
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

utm_fw_console = Firewall(
    ip=Parameter.FIREWALL,
    console_ip=consvr_UTM,
    console_port=conport_UTM,
    user='admin',
    password='password',
    supported_config_mode='cli-console'
)

lbox_fw_console = Firewall(
    ip=Parameter.LBOX_X0_IP, 
    console_ip=consvr_LBOX, 
    console_port=conport_LBOX,
    user='admin', 
    password='password', 
    supported_config_mode='cli-console'
    )


pkgapi = PacketmonitorApi(fw)
settingapi = SettingApi(fw)
interfacecli = InterfaceCli(fw_cli)
statuscli = StatusCli(fw_cli)

interfaceapi = InterfaceIPv4Api(fw)
lbox_interfaceapi = InterfaceIPv4Api(lbox_fw)

interfaceconsole = InterfaceCli(utm_fw_console)
lbox_interfaceconsole = InterfaceCli(lbox_fw_console)

adminconsole = AdminCli(utm_fw_console)
lbox_adminconsole = AdminCli(lbox_fw_console)

dyrouteapi = DynamicRoutingApi(fw)
lbox_dyrouteapi = DynamicRoutingApi(lbox_fw)

routeapi = RoutePolicyApi(fw)
lbox_routeapi = RoutePolicyApi(lbox_fw)

routecli = RouteCli(fw_cli)
lbox_routecli = RouteCli(lbox_fw_cli)
lbox_statuscli = StatusCli(lbox_fw_cli)

aoapi = AddressobjectsApi(fw)
lbox_aoapi = AddressobjectsApi(lbox_fw)

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

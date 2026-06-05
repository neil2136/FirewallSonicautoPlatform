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
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.system import PacketmonitorApi
from lib.modules.API.vpn import VpnbasesettingApi, L2tpServerApi
from lib.modules.API.users import UserLocalApi
from lib.modules.API.firewallsettings import AdvanceApi
from lib.modules.CLI.network import InterfaceCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/L2TP_Server_TP373/'
sys.path.append(suite_path)
defi_path = suite_path + 'definition'
TESTPLAN = suite_path + 'testplan/l2tpserver.json'
script_path = defi_path + '/script'

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
X2_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X2:1')
logger.info(f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC1_ETH3_IP: {PC1_ETH3_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC3_ETH2_IP: {PC3_ETH2_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC4_ETH2_IP: {PC4_ETH2_IP}'
            f'\n X2_VLAN1_ID: {X2_VLAN1_ID}'
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
PC2_Login = Host(PC2_ETH2_IP)
PC3_Login = Host(PC3_ETH2_IP)
PC4_Login = Host(PC4_ETH2_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.112'
    X1_DNS1 = '10.190.202.200'
    X2_VLAN1_IP = '12.12.3.168'
    X2_VLAN1_GW = '12.12.3.113'
    X3_IP = '192.168.3.168'
    GW_X1_IP = '12.12.1.101'
    GW_X0_IP = '11.11.11.101'
    GW_X2_IP = '12.12.2.101'


# parameters in cases
class CaseParams:
    client_ip_tc07_def06 = ''
    client_ip_tc18_def03 = ''


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

fw_gw_console = Firewall(
    ip=Parameter.GW_X0_IP,
    console_ip=consvr_gw,
    console_port=conport_gw,
    user='admin',
    password='password',
    supported_config_mode='cli-console'
)

interfaceapi = InterfaceIPv4Api(fw)
pkgapi = PacketmonitorApi(fw)
vpnapi = VpnbasesettingApi(fw)
l2tpapi = L2tpServerApi(fw)
localuserapi = UserLocalApi(fw)
interfacecli = InterfaceCli(fwcli)
firewalladvanceapi = AdvanceApi(fw)
gwinterfacecli = InterfaceCli(fw_gw_console)

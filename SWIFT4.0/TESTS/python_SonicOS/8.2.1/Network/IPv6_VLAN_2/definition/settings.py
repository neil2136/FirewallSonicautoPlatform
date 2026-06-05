import sys
import os
import re
import json
import time
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion


# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall


# import form branch lib contents for testsuite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API.system import PacketmonitorApi, SettingApi, SNMPApi
from lib.modules.API.switching import VlanTrunkApi

suite_path = os.environ['PYTHON_SONICOS_HOME']+'/Network/IPv6_VLAN_2/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/ipv6_vlan.json'

# parameters on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
logger.info(f"""
PC1_ETH2_IP is: {PC1_ETH0_IP}
PC2_ETH0_IP is: {PC2_ETH0_IP}
PC3_ETH0_IP is: {PC3_ETH0_IP}
PC4_ETH0_IP is: {PC4_ETH0_IP}
""")
pc1_login = Host(PC1_ETH0_IP)
pc2_login = Host(PC2_ETH0_IP)
pc3_login = Host(PC3_ETH0_IP)
pc4_login = Host(PC4_ETH0_IP)

X1_VLAN_ID = os_obj.get_node_interface_vlan_id('UTM', 'X1:1')
X3_VLAN_ID1 = os_obj.get_node_interface_vlan_id('UTM', 'X3:1')
X3_VLAN_ID2 = os_obj.get_node_interface_vlan_id('UTM', 'X3:2')
logger.info(f"""
DUT X1:1 VLAN ID is: {X1_VLAN_ID}
DUT X3:1 VLAN ID is: {X3_VLAN_ID1}
DUT X3:2 VLAN ID is: {X3_VLAN_ID2}
""")


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_V1_IP = '12.12.1.168'
    X1_V1_V6IP = "2022::168"
    X2_IP = "12.12.2.168"
    X3_V1_IP = '3.3.3.3'
    X3_V2_IP = '4.4.4.4'
    X0_V6 = "2010::168"
    X2_V6 = "2012::168"
    X3_V1_V6 = '2013:1::168'
    X3_V2_V6 = '2013:2::168'


# Instantiate objects including API, CLI import
fw = Firewall(
    Parameter.FIREWALL,
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


interfacev4api = network.InterfaceIPv4Api(fw)
interfacecli = InterfaceCli(fw_cli)
interfacev6api = network.InterfaceIPv6Api(fw)
packetapi = PacketmonitorApi(fw)
settingapi = SettingApi(fw)
vlanTrunkApi = VlanTrunkApi(fw)
snmpapi = SNMPApi(fw)

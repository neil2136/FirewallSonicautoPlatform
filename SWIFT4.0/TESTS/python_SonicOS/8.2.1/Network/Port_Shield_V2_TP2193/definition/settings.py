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


suite_path = os.environ['PYTHON_SONICOS_HOME'] + \
    '/Network/Port_Shield_V2_TP2193/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/port_shield_v2_tp2193.json'
script_path = suite_path+'definition/script/arp_send.py'

# parameters on openstack
os_obj = Openstack(Params.testbed)

PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
logger.info(f"""
PC1_ETH2_IP is: {PC2_ETH0_IP}
PC2_ETH2_IP is: {PC2_ETH1_IP}
PC2_ETH1_IP is: {PC3_ETH0_IP}
PC3_ETH2_IP is: {PC4_ETH0_IP}""")

pc2_ssh = Host(Params.testbed + '-PC2')
pc3_ssh = Host(Params.testbed + '-PC3')
pc4_ssh = Host(Params.testbed + '-PC4')


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X2_IP = '12.12.2.101'
    X3_IP = '3.3.3.168'
    X3_NET = '3.3.3.0'


# Instantiate objects including API, CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)

interfacev4api = network.InterfaceIPv4Api(fw)
dhcpserverapi = network.DHCPServerApi(fw)
droutingapi = network.DynamicRoutingApi(fw)
aoapi = network.AddressobjectsApi(fw)
arpapi = network.ArpApi(fw)
natapi = network.NatpolicyApi(fw)
routeapi = network.RoutePolicyApi(fw)

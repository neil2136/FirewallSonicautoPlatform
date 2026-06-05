import os
import sys
import re
import time
import copy
import requests
import unittest
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
from lib.modules.API import network


# import form test suite root path like definition
suite_path = (
    os.environ["PYTHON_SONICOS_HOME"] + "/Network/IP_Helper_DHCP_TP59/"
)
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/IP_Helper_DHCP_TP59.json'
CONF_PATH = suite_path + 'definition/config'
DHCP_SERVER_PATH = CONF_PATH + '/dhcpserver'


# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
logger.info(
    f"\n PC1_ETH0_IP: {PC1_ETH0_IP}"
    f"\n PC1_ETH1_IP: {PC1_ETH1_IP}"
    f"\n PC2_ETH0_IP: {PC2_ETH0_IP}"
    f"\n PC2_ETH1_IP: {PC2_ETH1_IP}"
    f"\n PC3_ETH0_IP: {PC3_ETH0_IP}"
    f"\n PC3_ETH1_IP: {PC3_ETH1_IP}"
    f"\n PC4_ETH0_IP: {PC4_ETH0_IP}"
    f"\n PC4_ETH1_IP: {PC4_ETH1_IP}"
    f"\n FW_DNS1_IP: {Params.G_DNS1}"
    f"\n FW_DNS2_IP: {Params.G_DNS2}"
)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X2_IP = '192.168.2.168'
    X2_SUBNET = '192.168.2.0'
    X3_IP = '192.168.3.168'
    X3_GW = '192.168.3.1'
    X3_SUBNET = '192.168.3.0'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
dhcp_obj = network.DHCPServerApi(fw)
iphelper_obj = network.IpHelperApi(fw)
address_obj = network.AddressobjectsApi(fw)
interfaceapi = network.InterfaceIPv4Api(fw)


# Init Settings
x1_wan_dict = {
    "if": "X1",
    "zone": "WAN",
    "mode": "static",
    "ip": Parameter.X1_IP,
    "netmask": Parameter.MASK,
    "gateway": Parameter.X1_GW,
    "dns1": Parameter.X1_DNS1,
    "dns2": Parameter.X1_DNS2,
    "mgmt_https": True,
    "mgmt_ssh": False,
    "mgmt_ping": True,
    "user_https": False,
    "mgmt_snmp": False,
}

x2_dmz_dict = {
    "if": "X2",
    "zone": "DMZ",
    "mode": "static",
    "ip": Parameter.X2_IP,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_ping": True,
    "user_https": False,
    "mgmt_snmp": False,
}

x3_lan_dict = {
    "if": "X3",
    "zone": "LAN",
    "mode": "static",
    "ip": Parameter.X3_IP,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_ping": True,
    "user_https": False,
    "mgmt_snmp": False,
}

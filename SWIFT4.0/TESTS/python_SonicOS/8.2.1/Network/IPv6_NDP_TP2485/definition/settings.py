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
from lib.modules.API.network import NeighborDiscoveryApi, InterfaceIPv4Api, InterfaceIPv6Api
from lib.modules.API import firewall
from lib.modules.API.system import RestartApi

# import form test suite root path like definition
basic_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_NDP_TP2485'
sys.path.append(basic_path)
TESTPLAN = basic_path + '/testplan/ipv6_ndp_tp2485.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            + f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            + f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            + f"\n PC1_ETH3_IP : {PC1_ETH3_IP}"
            )

LOCAL_HOST = Host(PC1_ETH0_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X1_ZONE = 'WAN'
    X1_SUBNET = '12.12.1.0'
    MASK = '255.255.255.0'
    X0_V6_IP = '2000:2401::1:10'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    PC1_ETH0_IPV6 = '2000:2401::1:100'
    PC1_ETH1_IPV6 = '2000:2402::1:100'
    PC1_ETH2_IPV6 = '2000:2402::1:100'
    IPV6_EDIT = '8008:8008::1'
    PREFIX_LENGTH = 64
    INTERFACE = 'X0'
    INTERFACE_NEW = 'X2'
    MAC1 = '11:22:33:44:55:66'


class ParamCases:
    TC1lopceth0mac = ''
    TC1addres = ''
    TC9deleteres = ''
    TC11deleteres = ''
    TC13editres = ''


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')

ndpapi = NeighborDiscoveryApi(fw_api)
restartapi = RestartApi(fw_api)
interfacev4api = InterfaceIPv4Api(fw_api)
interfacev6api = InterfaceIPv6Api(fw_api)

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

x0_v6_dict = {
    'name': 'X0',
    'mode': 'static',
    'zone': 'LAN',
    'ip': Parameter.X0_V6_IP,
    'prefix_length': Parameter.PREFIX_LENGTH,
    'mgmt_ping': True,
    'mgmt_https': True
}

ip_addrs_list_1 = ["3000::1", "3001::1", "3002::1", "3003::1", "3004::1", "3005::1", "3006::1", "3007::1",
                   "3008::1"]

ip_addrs_list_2 = ["4000::1", "4001::1", "4002::1", "4003::1", "4004::1", "4005::1", "4006::1", "4007::1",
                   "4008::1"]

import os
import sys
import copy
import re
import time
import json
import requests
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from bs4 import BeautifulSoup
from requests.auth import HTTPDigestAuth
import urllib3
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.network import InterfaceCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DNS_Client_Full'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/IPv6_DNS_Client_2479.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC1_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC1', 'eth2')
PC2_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC2', 'eth2')
logger.info(f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC1_ETH2_IPV6: {PC1_ETH2_IPV6}'
            f'\n PC2_ETH2_IPV6: {PC2_ETH2_IPV6}'
            )
PC1_login = Host(PC1_ETH2_IP)
PC2_login = Host(PC2_ETH1_IP)



class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.100'
    X1_GW = '12.12.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2

    PREFIX_LENGTH = 64
    X0_IPV6 = "2001:2018::168"
    X0_NET_V6 = "2001:2018::/64"
    X0_PC_IPV6 = PC1_ETH2_IPV6[:-3]
    X1_IPV6 = '2001:2011::168'
    X1_GW_IPV6 = PC2_ETH2_IPV6[:-3]
    V6_Prefix = '2001:2011:2:3::'
    IPV6_DNS1 = '2001::1234:1'
    IPV6_DNS2 = '2001::1234:2'
    IPV6_DNS3 = '2001::1234:3'


fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

if_v4_api = network.InterfaceIPv4Api(fw)
if_v6_api = network.InterfaceIPv6Api(fw)
if_v6_cli = InterfaceCli(fw_cli)
time_api = system.TimeApi(fw)
pkt_mon_api = system.PacketmonitorApi(fw)
diag_api = system.DiagnosticApi(fw)
licensecli = LicenseCli(fw_cli)
set_api = system.SettingApi(fw)
dns_api = network.DnsSettingsApi(fw)


dns_dict = {
    "dns": {
        "server": {
            "inherit": True,
            "static": {
                "primary": "0.0.0.0",
                "secondary": "0.0.0.0",
                "tertiary": "0.0.0.0"
            },
            "ipv6": {
                "inherit": False,
                "static": {
                    "primary": "::",
                    "secondary":"::",
                    "tertiary": "::"
                },
                "preferred": False
            }
        },
        "rebinding": {
            "enable": False,
            "action": "log-attack-only",
            "allowed_domains": {}
        },
        "fqdn_binding": False,
        "split_servers": True,
        "fqdn_over_tcp_dns": False
    }
}
dns_tupple = ()
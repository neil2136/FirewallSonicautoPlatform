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
from lib.modules.CLI.network import NatpolicyCli
from lib.modules.API.log import LogCategoryApi, LogMonitorApi
from lib.modules.API.users import UsersettingApi
from lib.modules.API.system import DiagnosticApi, SettingApi
from lib.modules.API.object import AddressObjectGroupApi
from definition.config.ui_login_fw import FWPage

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/FQDN_based_NAT_Part2/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/FQDN_based_NAT.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)

# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = PC4_ETH1_IP
    X1_DNS2 = Params.G_DNS1
    MASK = '255.255.255.0'
    X2_IP = '192.168.2.168'
    X2_SUBNET = '192.168.2.0'


class CaseParams:
    wan_host_ip = PC4_ETH1_IP
    in_wan_range1 = '12.12.1.30-40'
    custom_zone = 'auto_test1'
    domain_dns_baidu = 'A.dns.baidu.com'
    domain_pc2_baidu = 'A.pc2.baidu.com'
    domain_pc3_baidu = 'pc3.baidu.com'
    domain_ipv6_baidu = 'A.ipv6.baidu.com'
    fqdn_group1 = 'auto_fqdn_group1'
    ui_test_v4 = []
    ui_test_v6 = []


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password=Params.G_NEW_PASSWORD,
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password=Params.G_NEW_PASSWORD,
    supported_config_mode='cli-ssh')
FWPage_login = FWPage(
    url=f'https://{Parameter.FIREWALL}',
    appurl=f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/policies/ngpe-nat-policies',
    user='admin',
    pwd=Params.G_NEW_PASSWORD)

interfaceapi = network.InterfaceIPv4Api(fw)
aoapi = network.AddressobjectsApi(fw)
zonesapi = network.ZoneObjectsApi(fw)
aogroupapi = AddressObjectGroupApi(fw)
tsrfromlanapi = DiagnosticApi(fw)
natpolicyapi = network.NatpolicyApi(fw)
natpolicycli = NatpolicyCli(fw_cli)
logmonitorapi = LogMonitorApi(fw)
logcategoryapi = LogCategoryApi(fw)
settingapi = SettingApi(fw)


x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
x1_dhcp_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'dhcp',
    'mgmt_https': True,
    'mgmt_ping': True,
}
x2_lan_dict = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
negtive_nat_dict = {
    "nat_policies": [
        {
            "ipv4": {
                "uuid": "00000000-0000-0001-0800-2cb8ed6d8008",
                "name": 'auto_nat_test_3',
                "enable": True,
                "comment": "",
                "dns_doctoring": False,
                "inbound": "X1",
                "outbound": "any",
                "source": {
                    "any": True
                },
                "translated_source": {
                    "original": True
                },
                "destination": {
                    "group": CaseParams.fqdn_group1
                },
                "translated_destination": {
                    "original": True
                },
                "service": {
                    "any": True
                },
                "translated_service": {
                    "original": True
                }
            }
        }
    ]
}
tsr_nat_dict = {
  "nat_policies": [
    {
      "ipv4": {
        "uuid": "00000000-0000-0004-0800-2cb8ed694a24",
        "name": "auto_nat_test_1",
        "dns_doctoring": False,
        "source_port_remap": True,
        "inbound": "X1",
        "outbound": "any",
        "comment": "",
        "enable": True,
        "translated_destination": {
          "original": True
        },
        "translated_source": {
          "name": "X1 IP"
        },
        "translated_service": {
          "original": True
        },
        "source": {
          "any": True
        },
        "destination": {
          "name": CaseParams.domain_dns_baidu
        },
        "service": {
          "any": True
        },
        "priority": {
          "auto": True
        },
        "ticket": {
          "tag1": "",
          "tag2": "",
          "tag3": ""
        }
      }
    }
  ]
}
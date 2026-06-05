import os
import sys
import re
import copy
import time
import json
from contextvars import ContextVar
from datetime import datetime

from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from nose_parameterized import parameterized
import paramunittest

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.system import SettingApi, PacketmonitorApi, DiagnosticApi
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.firewallsettings import AdvanceApi
from lib.modules.CLI.firewallsettings import AdvancedCli
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, ArpApi, DHCPServerApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Network/Native_Bridge/'
sys.path.append(suite_path)
TESTPLAN = suite_path + 'testplan/Native_Bridge.json'
defi_path = suite_path + 'definition/'
DHCLIEN_LEASE_FILE = '/var/lib/dhclient/dhclient.leases'


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
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')
PC1_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC1', 'eth1')
PC2_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC2', 'eth1')
PC3_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC3', 'eth1')
PC4_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC4', 'eth1')
PC5_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC5', 'eth1')
X3_VLAN1_ID = os_obj.get_node_interface_vlan_id('UTM', 'X3:1')
PLATFORM_NAME = os_obj.get_node_platform('UTM')


logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC5_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC5_ETH1_IP: {PC5_ETH1_IP}'
            f'\n PC1_ETH1_IPV6: {PC1_ETH1_IPV6}'
            f'\n PC2_ETH1_IPV6: {PC2_ETH1_IPV6}'
            f'\n PC3_ETH1_IPV6: {PC3_ETH1_IPV6}'
            f'\n PC4_ETH1_IPV6: {PC4_ETH1_IPV6}'
            f'\n PC5_ETH1_IPV6: {PC5_ETH1_IPV6}'
            f'\n X3_VLAN1_ID: {X3_VLAN1_ID}'
            )
PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)
PC4_Login = Host(PC4_ETH0_IP)
PC5_Login = Host(PC5_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X0_PC = PC1_ETH1_IP
    X1_IP = '11.1.1.168'
    X1_GW = PC2_ETH1_IP
    X2_PC = '192.168.168.22'
    X2_GW = PC3_ETH1_IP
    X3_IP = '13.1.1.168'
    X3_GW = PC4_ETH1_IP
    X4_GW = PC5_ETH1_IP
    X4_PC = '13.1.1.55'
    X2_PC_2 = '13.1.1.22'
    DNS1 = '10.103.202.200'

    X2_PC_MAC = ''
    X3_PC_MAC = ''
    X4_PC_MAC = ''


# Params on case
class CaseParams:
    tc48_pc3_ip = ''
    tc48_pc4_ip = ''
    tc48_pc5_ip = ''


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api'
)

fwcli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh'
)

interfaceapi = InterfaceIPv4Api(fw)
settingapi = SettingApi(fw)
aoapi = AddressobjectsApi(fw)
pkgmonitorapi = PacketmonitorApi(fw)
diagnosticapi = DiagnosticApi(fw)
arpapi = ArpApi(fw)
acl_api = AccessRuleApi(fw)
dhcpserverapi = DHCPServerApi(fw)
licensecli = LicenseCli(fwcli)

acl_base = {
    "enable": True,
    "name": "",
    "from": "LAN",
    "to": "LAN",
    "action": "deny",
    "source": {
        "address": {
            "any": True
        },
        "port": {
            "any": True
        }
    },
    "service": {
        "group": "ICMP"
    },
    "destination": {
        "address": {
            "any": True
        }
    },
    "schedule": {
        "always_on": True
    },
    "users": {
        "included": {
            "all": True
        },
        "excluded": {
            "none": True
        }
    },
    "comment": "",
    "fragments": True,
    "logging": True,
    "sip": False,
    "h323": False,
    "flow_reporting": False,
    "botnet_filter": False,
    "geo_ip_filter": {
        "enable": False,
        "global": True
    },
    "priority": {
        "auto": True
    }
}

static_arp_dict = {
    'ip': '',
    'mac': '',
    'interface': 'X2',
    'publish': False,
    'bind_mac': False,
    'dynamic': False
}


dynamic_scope_base = {
    "dhcp_server":
        {"ipv4": {
            "scope": {
                "dynamic": [
                    {
                        "from": "13.1.1.180",
                        "to": "13.1.1.220",
                        "enable": True,
                        "lease_time": 60,
                        "default_gateway": "13.1.1.168",
                        "netmask": "255.255.255.0",
                        "comment": "dhcp lease for x4 interface",
                        # "allow_bootp":False,
                        "domain_name": "example.com",
                        "dns": {"server": {"inherit": True}},
                    }
                ]
            }
        }
        }
}

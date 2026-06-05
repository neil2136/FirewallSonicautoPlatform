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
from lib.modules.API.system import SettingApi, PacketmonitorApi
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api, AddressobjectsApi, DnsSettingsApi
from lib.modules.CLI.network import InterfaceCli, RouteCli
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.CLI.system import LicenseCli
from tools.trafficGen import ScapyPacketSend

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Network/TOS_in_Route_Policies/'
sys.path.append(suite_path)
TESTPLAN = suite_path + 'testplan/tos.json'
defi_path = suite_path + 'definition/'

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
PC1_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC1', 'eth1')
PC2_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC2', 'eth1')
PC3_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC3', 'eth1')
PC4_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC4', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC1_ETH1_IPV6: {PC1_ETH1_IPV6}'
            f'\n PC2_ETH1_IPV6: {PC2_ETH1_IPV6}'
            f'\n PC3_ETH1_IPV6: {PC3_ETH1_IPV6}'
            f'\n PC4_ETH1_IPV6: {PC4_ETH1_IPV6}'
            )
PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)
PC4_Login = Host(PC4_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X1_IP = '11.1.1.168'
    X1_GW = PC2_ETH1_IP
    X2_IP = '12.1.1.168'
    X2_GW = PC3_ETH1_IP
    X3_IP = '13.1.1.168'
    X3_GW = PC4_ETH1_IP
    DNS1 = '10.103.202.200'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2

    PREFIX_LENGTH = 64
    X0_IPV6 = "2001:2018::168"
    X0_NET_V6 = "2001:2018::/64"
    X0_PC_IPV6 = PC1_ETH1_IPV6[:-3]
    X1_IPV6 = '2001:2011::168'
    X1_GW_IPV6 = PC2_ETH1_IPV6[:-3]
    X2_IPV6 = '2001:2012::168'
    X2_GW_IPV6 = PC3_ETH1_IPV6[:-3]
    X3_IPV6 = '2001:2013::168'
    X3_GW_IPV6 = PC4_ETH1_IPV6[:-3]

    SRC_HOST = '192.168.168.60/30'
    DST_HOST = '8.8.8.8'
    DST_NET = "8.8.8.0/24"

    IPV6_DST_HOST = "2001:8888::1000"
    IPV6_DST_NET = "2001:8888::/64"


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
interfacev6api = InterfaceIPv6Api(fw)
interfacecli = InterfaceCli(fwcli)
settingapi = SettingApi(fw)
routepolicyapi = RoutePolicyApi(fw)
routecli = RouteCli(fwcli)
aoapi = AddressobjectsApi(fw)
dnsapi = DnsSettingsApi(fw)
pkgmonitorapi = PacketmonitorApi(fw)
licensecli = LicenseCli(fwcli)

icmp_dict = {
    'IP': {
        'version': '4',
        'tos': '0x14',
        'src': Parameter.SRC_HOST,
        'dst': Parameter.DST_HOST,
    },
    'ICMP': {
        'type': '8'
    },
    'conf': {
        'iface': 'eth1',
        'route': {
            'net': Parameter.DST_NET,
            'gw': Parameter.FIREWALL
        }
    }
}

icmpv6_dict = {
    'IPv6': {
        'version': '6',
        'tc': '0x14',
        'src': Parameter.X0_PC_IPV6,
        'dst': Parameter.IPV6_DST_HOST,
    },
    'ICMPv6EchoRequest': {
        'type': '128'
    },
    'conf': {
        'route6': {
            'src': Parameter.X0_PC_IPV6,
            'dst': Parameter.IPV6_DST_NET,
            'gw': Parameter.X0_IPV6,
            'dev': 'eth1'
        }
    }
}

expect_pkt_dict = {
    'src': '192.168.168.',
    'dst': '8.8.8.8',
    'in': 'X0',
    'out': '',
    'proto': 'ICMP',
}

ipv6_expect_pkt_dict = {
    'src': '2001:2013::101',
    'dst': '2001:8888::1000',
    'in': 'X3',
    'out': '',
    'proto': 'ICMPv6',
}

initial_pbr_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "test",
                "comment": "",
                "interface": "X2",
                "metric": 20,
                "service": {
                    "any": True
                },
                "gateway": {
                    "default": True
                },
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "130.1.1.0"
                },
                "disable_on_interface_down": True,
                "probe": "",
                "distance": {
                    "auto": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "type": "standard",
            }
        }
    ]
}

initial_ipv6_rt_dict = {
    "route_policies": [{
        "ipv6": {
            "name": "ecmp_ipv6_4gw_api",
            "comment": "",
            "interface": "X1",
            "metric": 10,
            "service": {
                "any": True
            },
            "gateway": {
                "name": "GW1_IPV6"
            },
            "source": {
                "any": True
            },
            "destination": {
                "name": "server_pc_v6"
            },
            "disable_on_interface_down": True,
            "vpn_precedence": False,
            "probe": "",
            "distance": {
                "auto": True
            },
            "tos": "0x00",
            "mask": "0x00",
            "type": "multi-path"
        }
    }]
}

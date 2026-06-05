import os
import sys
import re
import copy
import time
from contextvars import ContextVar

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

from lib.modules.API import network
from lib.modules.API.system import PacketmonitorApi
from lib.modules.CLI.network import RouteCli, AddressObjectCli
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/ECMP/'
sys.path.append(suite_path)
defi_path = suite_path + 'definition'
TESTPLAN = suite_path + 'testplan/ecmp_smoke.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC_Server_ETH1_IP = os_obj.get_node_interface_ip('PC-Server', 'eth1')
PC_Server_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC-Server', 'eth1')
PC_Server_ETH2_IP = os_obj.get_node_interface_ip('PC-Server', 'eth2')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC_GW1_ETH1_IP = os_obj.get_node_interface_ip('PC-GW1', 'eth1')
PC_GW1_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC-GW1', 'eth1')
PC_GW1_ETH2_IP = os_obj.get_node_interface_ip('PC-GW1', 'eth2')
PC_GW1_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC-GW1', 'eth2')
PC_GW1_ETH3_IP = os_obj.get_node_interface_ip('PC-GW1', 'eth3')
PC_GW2_ETH1_IP = os_obj.get_node_interface_ip('PC-GW2', 'eth1')
PC_GW2_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC-GW2', 'eth1')
PC_GW2_ETH2_IP = os_obj.get_node_interface_ip('PC-GW2', 'eth2')
PC_GW2_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC-GW2', 'eth2')
PC_GW2_ETH3_IP = os_obj.get_node_interface_ip('PC-GW2', 'eth3')
PC_GW3_ETH1_IP = os_obj.get_node_interface_ip('PC-GW3', 'eth1')
PC_GW3_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC-GW3', 'eth1')
PC_GW3_ETH2_IP = os_obj.get_node_interface_ip('PC-GW3', 'eth2')
PC_GW3_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC-GW3', 'eth2')
PC_GW3_ETH3_IP = os_obj.get_node_interface_ip('PC-GW3', 'eth3')
PC_GW4_ETH1_IP = os_obj.get_node_interface_ip('PC-GW4', 'eth1')
PC_GW4_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC-GW4', 'eth1')
PC_GW4_ETH2_IP = os_obj.get_node_interface_ip('PC-GW4', 'eth2')
PC_GW4_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC-GW4', 'eth2')
PC_GW4_ETH3_IP = os_obj.get_node_interface_ip('PC-GW4', 'eth3')

logger.info(f"\n PC_Server_ETH1_IP : {PC_Server_ETH1_IP}"
            + f"\n PC_Server_ETH1_IPV6 : {PC_Server_ETH1_IPV6}"
            + f"\n PC_Server_ETH3_IP : {PC_Server_ETH2_IP}"

            + f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            + f"\n PC1_ETH1_IPV6 : {PC1_ETH1_IPV6}"
            + f"\n PC1_ETH3_IP : {PC1_ETH3_IP}"

            + f"\n PC_GW1_ETH1_IP : {PC_GW1_ETH1_IP}"
            + f"\n PC_GW1_ETH1_IPV6 : {PC_GW1_ETH1_IPV6}"
            + f"\n PC_GW1_ETH2_IP : {PC_GW1_ETH2_IP}"
            + f"\n PC_GW1_ETH2_IPV6 : {PC_GW1_ETH2_IPV6}"
            + f"\n PC_GW1_ETH3_IP : {PC_GW1_ETH3_IP}"

            + f"\n PC_GW2_ETH1_IP : {PC_GW2_ETH1_IP}"
            + f"\n PC_GW2_ETH1_IPV6 : {PC_GW2_ETH1_IPV6}"
            + f"\n PC_GW2_ETH2_IP : {PC_GW2_ETH2_IP}"
            + f"\n PC_GW2_ETH2_IPV6 : {PC_GW2_ETH2_IPV6}"
            + f"\n PC_GW2_ETH3_IP : {PC_GW2_ETH3_IP}"

            + f"\n PC_GW3_ETH1_IP : {PC_GW3_ETH1_IP}"
            + f"\n PC_GW3_ETH1_IPV6 : {PC_GW3_ETH1_IPV6}"
            + f"\n PC_GW3_ETH2_IP : {PC_GW3_ETH2_IP}"
            + f"\n PC_GW3_ETH2_IPV6 : {PC_GW3_ETH2_IPV6}"
            + f"\n PC_GW3_ETH3_IP : {PC_GW3_ETH3_IP}"

            + f"\n PC_GW4_ETH1_IP : {PC_GW4_ETH1_IP}"
            + f"\n PC_GW4_ETH1_IPV6 : {PC_GW4_ETH1_IPV6}"
            + f"\n PC_GW4_ETH2_IP : {PC_GW4_ETH2_IP}"
            + f"\n PC_GW4_ETH2_IPV6 : {PC_GW4_ETH2_IPV6}"
            + f"\n PC_GW4_ETH3_IP : {PC_GW4_ETH3_IP}"
            )

PC1_Login = Host(PC1_ETH2_IP)
PC_Server_Login = Host(PC_Server_ETH2_IP)
PC_GW1_Login = Host(PC_GW1_ETH3_IP)
PC_GW2_Login = Host(PC_GW2_ETH3_IP)
PC_GW3_Login = Host(PC_GW3_ETH3_IP)
PC_GW4_Login = Host(PC_GW4_ETH3_IP)


class Parameter:

    X0_IP = "192.168.168.168"
    FIREWALL = X0_IP
    X0_NET = "192.168.168.0"
    X0_IPV6 = "2001:2018::168"
    X0_NET_V6 = "2001:2018::/64"
    X1_IP = "13.11.1.168"
    X1_MASK = "255.255.255.0"
    X1_IPV6 = "2001:2011::168"
    X2_IP = "13.12.0.168"
    X2_MASK = "255.255.0.0"
    X2_IPV6 = "2001:2012:12:12::168"
    PREFIX_LENGTH = 64

    X2_GW1_IP = PC_GW1_ETH2_IP
    X2_GW2_IP = PC_GW2_ETH2_IP
    X2_GW3_IP = PC_GW3_ETH2_IP
    X2_GW4_IP = PC_GW4_ETH2_IP
    X2_GW1_MAC = ''
    X2_GW2_MAC = ''
    X2_GW3_MAC = ''
    X2_GW4_MAC = ''
    # the ou os_obj.get_node_interface_ipv6 is with netmask 
    # PC_GW1_ETH1_IPV6 : 2001:1000::11/64
    X2_GW1_IPV6 = PC_GW1_ETH2_IPV6[:-3]
    X2_GW2_IPV6 = PC_GW2_ETH2_IPV6[:-3]
    X2_GW3_IPV6 = PC_GW3_ETH2_IPV6[:-3]
    X2_GW4_IPV6 = PC_GW4_ETH2_IPV6[:-3]

    X0_PC_V6 = PC1_ETH1_IPV6[: -3]

    SERVER_PC = PC_Server_ETH1_IP
    SERVER_PC_V6 = PC_Server_ETH1_IPV6[:-3]
    SERVER_NET = "100.100.10.0"
    SERVER_NET_V6 = "2001:1000:1000:1000::/64"

    SRC_HOST = '192.168.168.60/27'
    DST_HOST = "100.100.10.200"
    DST_NET = "100.100.10.0/24"
    SRC_RANGE = '192.168.168.160/27'
    DST_NETWORK = "100.100.10.192/27"
    SRC_NETWORK = '192.168.168.192/27'

    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2

# mark-- format warning
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api'
)

fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh'
)

interfacev4api = network.InterfaceIPv4Api(fw)
interfacev6api = network.InterfaceIPv6Api(fw)
aoapi = network.AddressobjectsApi(fw)
routeapi = network.RoutePolicyApi(fw)
routecli = RouteCli(fw_cli)
pkgapi = PacketmonitorApi(fw)
arpapi = network.ArpApi(fw)
aocli = AddressObjectCli(fw_cli)
licensecli = LicenseCli(fw_cli)

# parameters on the test cases
tcp_dict = {
    'IP': {
        'src': Parameter.SRC_HOST,
        'dst': Parameter.SERVER_PC,
    },
    'TCP': {
        'dport': 20000,
        'flags': "S",
    },
    'conf': {
        'iface': 'eth0',
        'route': {
            'net': "100.100.10.0/24",
            'gw': "192.168.168.168"
        }
    }
}
udp_dict = {
    'IP': {
        'src': Parameter.SRC_RANGE,
        'dst': Parameter.SERVER_PC,
    },
    'UDP': {
        'sport': 10000,
        'dport': 20000
    },
    'conf': {
        'iface': 'eth0',
        'route': {
            'net': "100.100.10.0/24",
            'gw': "192.168.168.168"
        }
    }
}
icmp_dict = {
    'IP': {
        'version': '4',
        'src': Parameter.SRC_NETWORK,
        'dst': Parameter.SERVER_PC,
    },
    'ICMP': {
        'type': '8'
    },
    'conf': {
        'iface': 'eth0',
        'route': {
            'net': "100.100.10.0/24",
            'gw': "192.168.168.168"
        }
    }
}

icmpv6_dict = {
    'IPv6': {
        'src': Parameter.X0_PC_V6,
        'dst': Parameter.SERVER_PC_V6,
    },
    'ICMPv6EchoRequest': {
        'type': '128'
    },
    'conf': {
        'route6': {
            'dst': Parameter.SERVER_NET_V6,
            'gw': Parameter.X0_IPV6,
            'dev': 'eth1'
        }
    }
}




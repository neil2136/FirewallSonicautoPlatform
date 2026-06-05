import os
import sys
import unittest
import time
from parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import content from common_lib path
from util.openstack import Openstack
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from networkdevice import Host

# import from branch lib contents for test suite
from lib.modules.API import network, accessrule, policy
from lib.modules.CLI.system import LicenseCli

# import form test suite root path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Static_Routes_TP174_Part2/testplan/static_routes_tp174.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
logger.info("\n" + "-" * 30 + "\n" \
            + "PC2_ETH1_IP :" + str(PC2_ETH0_IP) + "\n" \
            + "PC3_ETH1_IP :" + str(PC3_ETH0_IP) + "\n" \
            + "-" * 30
            )
PC1_HOST = Host(PC1_ETH0_IP, user='root', password='password')
PC2_HOST = Host(PC2_ETH0_IP, user='root', password='password')
PC3_HOST = Host(PC3_ETH0_IP, user='root', password='password')


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_SUBNET = '12.12.1.0'
    X2_IP = "12.12.2.168"
    X2_GW = '12.12.2.1'
    X3_IP = "192.168.3.168"
    X3_NET = "192.168.3.0"
    R_X1_IP = '12.12.1.201'
    R_X2_IP = '12.12.2.201'
    R_X2_NET = '12.12.2.0'
    R_X3_IP = '12.12.3.201'
    R_X3_NET = '12.12.3.0'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


class CaseParams:
    route_list_before_add = {}
    route_list_after_add = {}
    added_route_policy = {}
    fw_added_route_dis = {}
    route_list_after_edit = {}
    route_list_after_delete = {}


# Instantiate objects including API,CLI import
fw_api = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
interface_api = network.InterfaceIPv4Api(fw_api)
route_api = policy.RoutePolicyApi(fw_api)
access_rule_api = accessrule.AccessRuleIPv4Api(fw_api)
ao_api = network.AddressobjectsApi(fw_api)
licensecli = LicenseCli(fw_cli)

fw_api_remote = Firewall(
    Parameter.R_X1_IP,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
interface_api_remote = network.InterfaceIPv4Api(fw_api_remote)
route_api_remote = policy.RoutePolicyApi(fw_api_remote)
ao_api_remote = network.AddressobjectsApi(fw_api_remote)

r_x2_config_dic = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.R_X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}

dut_x1_static = {
    'if': 'X1',
    'zone': 'WAN',
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
dut_x2_static = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}
dut_x2_wan_static = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X2_GW,
    'dns1': Parameter.DNS1,
    'dns2': Parameter.DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
dut_x3_static = {
    'if': 'X3',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}

dmz_to_lan_dict = {
    'name': 'dmz_to_lan',
    'from': 'DMZ',
    'to': 'LAN',
    'source_addr': {'any': True},
    'dst_addr': {'any': True},
    'service': {'group': 'ICMP'},
    'action': 'allow',
    'comment': '',
}

route_policy_dict = {
    "route_policies": [
        {
            "ipv4": {
                "interface": "X2",
                "metric": 1,
                "source": {
                    "name": "X3 Subnet"
                },
                "destination": {
                    "name": "X2 Subnet"
                },
                "service": {
                    "any": True
                },
                "gateway": {
                    "name": "12.2.201"
                },
                "tos": "0x00",
                "mask": "0x00",
                "distance": {
                    "auto": True
                },
                "name": "to_remote_x3",
                "type": "standard",
                "priority": 6,
                "comment": "",
                "disable_on_interface_down": False,
                "vpn_precedence": False,
                "tcp_acceleration": False,
                "probe": "",
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": "",
                }
            }
        }
    ]
}

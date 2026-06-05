import os
import sys
import re
import time
import copy
import requests
import unittest
import paramunittest
from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from nose_parameterized import parameterized

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.API.system import PacketmonitorApi
from lib.modules.API.network import NetworkMonitorApi, NetworkMonitorApi, \
    InterfaceIPv4Api, AddressobjectsApi, FailoverLbApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.system import SettingApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Policy_Based_Routing_TP274/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/Policy_Based_Routing.json'
FILE_PATH_HTTP_REQ = suite_path + 'definition/tools/httprequestsend.py'
SCRIPT_PATH = suite_path + 'definition/tools/'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC1_ETH3_IP: {PC1_ETH3_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    X1_DNS = '10.102.1.60'
    X2_IP = '172.20.1.168'
    X2_GW = '172.20.1.1'
    X2_DNS = '10.102.1.60'
    X3_IP = '172.30.1.168'
    X3_GW = '172.30.1.1'
    X3_DNS = '10.102.1.60'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)
routepolicyapi = RoutePolicyApi(fw)
packetmonitorapi = PacketmonitorApi(fw)
networkmonitorapi = NetworkMonitorApi(fw)
aoapi = AddressobjectsApi(fw)
aogroupapi = AddressObjectGroupApi(fw)
interfacev4api = InterfaceIPv4Api(fw)
failoverapi = FailoverLbApi(fw)
settingapi = SettingApi(fw)


# parameters on the test cases
class CasesParam:
    tc17_edit_res = False
    tc47_traffic_res = False


pc_run_dict = {
    'type': 'ping',  # ping, cmd, http, script
    'pc': 'pc1',
    'eth': 'eth1',
    'des': Parameter.DNS1
}
route_base_dict = {
    "interface": "X2",
    "metric": 1,
    "source": {"any": True},
    'destination': {'any': True},
    'service': {'group': 'Ping'},
    'gateway': {'name': 'X2 Default Gateway'},
    "tos": "0x00",
    "mask": "0x00",
    "distance": {"auto": True},
    "name": 'test_route',
    "type": "standard",
    "priority": 1,
    "comment": "",
    "disable_on_interface_down": True,
    "vpn_precedence": False,
    "probe": "",
    "ticket": {"tag1": "", "tag2": "", "tag3": ""}
}
org_base_dict = copy.deepcopy(route_base_dict)
route_policy_dict = {"route_policies": [{"ipv4": route_base_dict}]}

route_policy_json_with_probe = {
    "route_policies": [
        {
            "ipv4": {
                "interface": "X2",
                "metric": 1,
                "source": {"any": True},
                'destination': {'any': True},
                'service': {'group': 'Ping'},
                'gateway': {'name': 'X2 Default Gateway'},
                "tos": "0x00",
                "mask": "0x00",
                "distance": {"auto": True},
                "name": "route_policy_tc12",
                "type": "standard",
                "priority": 1,
                "comment": "",
                "disable_on_interface_down": True,
                "vpn_precedence": False,
                "probe": "",
                "disable_when_probes_succeed": False,  # have to disable
                "default_probe_state_up": False,
                "ticket": {"tag1": "", "tag2": "", "tag3": ""}
            }
        }
    ]
}
wlb_conf_dict = {
    "failover_lb": {
        "group": [
            {
                "final_backup": "",
                "interface": [
                    {
                        "name": "X1",
                        "probe_condition": "always",
                        "probe_type": "physical",
                        "rank": 1
                    },
                    {
                        "default_target": {
                            "value": "204.212.170.23"
                        },
                        "main_target": {
                            "host": "responder.global.sonicwall.com",
                            "protocol": {
                                "tcp": {
                                    "value": 50000
                                }
                            }
                        },
                        "name": "X2",
                        "probe_condition": "main",
                        "probe_type": "logical",
                        "rank": 2
                    },
                    {}
                ],
                "name": " Default LB Group",
                "preempt": True,
                "probing": {
                    "global_responder": False,
                    "health_check": 5,
                    "missed_intervals": 3,
                    "successful_intervals": 3
                },
                "type": "basic"
            }
        ]
    }
}


import os
import sys
import re
import time
import requests
import urllib.request as ftp_request

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import policy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Policy_Based_Routing/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Policy_Based_Routing')


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    X1_DNS = '10.9.1.40'
    X2_IP = '172.20.1.168'
    X2_GW = '172.20.1.1'
    X2_DNS = '10.9.1.40'
    X3_IP = '172.30.1.168'
    X3_GW = '172.30.1.1'
    X3_DNS = '10.9.1.40'
    MASK = '255.255.255.0'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Policy_Based_Routing/testplan/Policy_Based_Routing.json'
    FILE_PATH_TEST_HTTP = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Policy_Based_Routing/definition/testHTTP.py'

    default_route_policy_json = {
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
                    "ticket": {"tag1": "","tag2": "","tag3": ""}
                }
            }      
        ]
    }

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
                    "disable_when_probes_succeed": False,#have to disable 
                    "default_probe_state_up": False,
                    "ticket": {"tag1": "","tag2": "","tag3": ""}
                }
            }      
        ]
    } 

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
route_policy_obj    = policy.RoutePolicyApi(fw)
packet_obj          = system.PacketmonitorApi(fw)
network_monitor_obj = network.NetworkMonitorApi(fw)
address_obj         = network.AddressobjectsApi(fw)
interface_obj       = network.InterfaceIPv4Api(fw)

os_obj      = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC3_login   = Host(PC3_ETH1_IP, user='root', password='password')

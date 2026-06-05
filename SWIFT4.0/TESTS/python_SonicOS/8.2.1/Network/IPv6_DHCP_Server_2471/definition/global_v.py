import os
import sys
import re
import time

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import system

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Server_2471/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Server_2471')

confs_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Server_2471/confs/'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Server_2471/testplan/IPv6_DHCP_Server_2471.json'

FIREWALL = '192.168.168.168'
X1_IP = '172.17.1.168'
X1_GW = '172.17.1.1'
X1_DNS = Params.G_DNS1
DMZ_IP= '2.2.2.10'
SEC_LAN_IP = '3.3.3.10'
MASK = '255.255.255.0'

PC1_WAN_IP = '13.0.0.2'
PC1_DMZ_IP = '2.2.2.20'
PC1_SEC_LAN_IP = '3.3.3.20' 

X0_ipv6 = '2003::5'
X2_ipv6 = '2004::5'
X3_ipv6 = '2001::5'

dhcpserver_dict = {
    "dhcp_server":{
        "ipv6":{
            "scope":{
                "dynamic":[
                {
                    "name": 'test_x0',
                    "enable": True,
                    "prefix": '2003::',
                    "range":{
                        "from": '2003::6',
                        "to": '2003::9',
                    },
                    "lifetime": {
                        "valid": 2160,
                        "preferred": 1440
                    },
                    "comment": "",
                    "always_send_option": False,
                    "domain_name": "",
                    "dns":{
                        "server":{"inherit":True}
                    }
                }
                ]
            }
        }
    }
}

dhcpserver_dict_tc45 = {
    "dhcp_server":{
        "ipv6":{
            "scope":{
                "dynamic":[
                {
                    "name": 'test_x0',
                    "enable": True,
                    "prefix": '2003::',
                    "range":{
                        "from": '2003::6',
                        "to": '2003::9',
                    },
                    "lifetime": {
                        "valid": 2160,
                        "preferred": 1440
                    },
                    "comment": "",
                    "always_send_option": True,
                    "domain_name": "",
                    "dns":{
                        "server":{
                            "static": {
                                "primary": "1::1",
                                "secondary": "::",
                                "tertiary": "::"
                            }
                        }
                    },
                    "generic_option": {}
                }
                ]
            }
        }
    }
}

fw = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='api')
os_obj = Openstack(Params.testbed)
interface_obj = network.InterfaceIPv4Api(fw)
interface_v6_obj = network.InterfaceIPv6Api(fw)
dhcpserver_obj = network.DHCPServerApi(fw)
pkg_api = system.PacketmonitorApi(fw)

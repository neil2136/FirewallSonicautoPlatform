import os
import sys
import re
import time

import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite


# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, ArpApi, AddressobjectsApi, ZoneObjectsApi
# from lib.modules.API.policy import NatPolicyApi, SecurityPolicyApi
from lib.modules.API.system import PacketmonitorApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.CLI.system import LicenseCli

suite_path = os.environ["PYTHON_SONICOS_HOME"]+'/Network/Custom_Zones_TP440/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
sys.path.append(suite_path+'definition')
TESTPLAN = suite_path+'testplan/custom_zones_tp440.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')

PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X1_IP = '10.11.1.168'
    X1_NET = '10.11.1.0'
    X1_GW = '10.11.1.1'
    X2_IP = '192.168.20.168'
    X2_NET = '192.168.20.0'
    X2_GW = '192.168.20.1'
    X3_IP = '192.168.30.168'
    X3_GW = '192.168.30.1'
    X3_NET = '192.168.30.0'
    MASK = '255.255.255.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)
licensecli = LicenseCli(fw_cli)
interfacev4api = InterfaceIPv4Api(fw)
zonesapi = ZoneObjectsApi(fw)
aoapi = AddressobjectsApi(fw)
packetmonitorapi = PacketmonitorApi(fw)


# parameters on the test cases
custom_zone_dict = {
    "zones": [
        {
            "name": 'AutoTest1',
            "security_type": 'trusted',
            "interface_trust": True,
            "auto_generate_access_rules": {
                "allow_from_to_equal": True,
                "allow_from_higher": True,
                "allow_to_lower": True,
                "deny_from_lower": True
            },
            "gateway_anti_virus": True,
            "intrusion_prevention": False
        }
    ]
}

import sys
import os
import re
import copy
import time
import subprocess
import json
import requests
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall

# import form branch lib contents for testsuite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API.firewall import AccessRuleIPv6Api
from lib.modules.API.system import SettingApi
from lib.modules.CLI.network import NatpolicyCli
from lib.modules.CLI.system import LicenseCli

suite_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_Nat_Policy_TP2511/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/ipv6_nat_policies.json'

# parameters on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC1_ETH1_V6 = os_obj.get_node_interface_ipv6('PC1', 'eth1').split('/')[0]
PC2_ETH1_V6 = os_obj.get_node_interface_ipv6('PC2', 'eth1').split('/')[0]
logger.info(f"""
PC1_ETH1_IP: {PC1_ETH1_IP}
PC1_ETH2_IP: {PC1_ETH2_IP}
PC2_ETH1_IP: {PC2_ETH1_IP}
PC2_ETH2_IP: {PC2_ETH2_IP}
PC1_ETH1_V6: {PC1_ETH1_V6}
PC2_ETH1_V6: {PC2_ETH1_V6}
""")

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_V6_IP = "2001::168"
    X0_V6_IP = "2000::168"
    X2_V6_IP = "2002::168"
    X1_V6_NAT = "2001::170"
    X2_V6_NAT = "2002::170"
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


# Instantiate objects including API, CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

if_v4_api = network.InterfaceIPv4Api(fw)
if_v6_api = network.InterfaceIPv6Api(fw)
ao_api = network.AddressobjectsApi(fw)
nat_api = network.NatpolicyApi(fw)
acl_api = AccessRuleIPv6Api(fw)
service_api = network.ServiceObjectApi(fw)
set_api = SettingApi(fw)
nat_cli = NatpolicyCli(fw_cli)
licensecli = LicenseCli(fw_cli)

init_nat_json = {
    "nat_policies": [{
        "ipv6": {
            "name": "",
            "reflexive": False,
            # "source_port_remap": True,
            "comment": "test",
            "enable": True,
            "inbound": "any",
            "outbound": "any",
            "source": {
                "any": True
            },
            "translated_source": {
                "original": True
            },
            "destination": {
                "any": True
            },
            "translated_destination": {
                "original": True
            },
            "service": {
                "any": True
            },
            "translated_service": {
                "original": True
            },
            "ticket": {
                "tag1": "",
                "tag2": "",
                "tag3": ""
            }
        }
    }]
}

import os
import sys
import re
import time
import copy
import requests
import unittest
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
from tools.trafficGen import MyHttpClinet, MyFtp

# import form branch lib contents for test suit
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.system import RestartApi, TimeApi
from lib.modules.API.policy import AppRulesApi
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API.network import InterfaceIPv4Api, ZoneObjectsApi
from lib.modules.API.log import LogMonitorApi
from lib.modules.API.securityservices import GAV
from lib.modules.API.firewall import MatchobjectApi

# import form test suite root path like definition
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Wiremode_Consolidated/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/wiremode_consolidated.json'
CONF_PATH = suite_path + 'definition/config/*'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH2_IP)
PC2_login = Host(PC2_ETH1_IP)


# parameters on the fw
class Parameter:
    PC2_ETH0_NewIP = '2.2.2.200'
    PC2_ETH2_GW = '192.168.2.1'
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X2_IP = '2.2.2.168'
    MASK = '255.255.255.0'
    PUBLIC_SERVER = '10.6.0.69'
    PC1_ETH1_IP = '2.2.2.169'
    PC1_ETH1_IP_NEW = '2.2.2.12'


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
    supported_config_mode='cli-ssh')

interfaceapi = InterfaceIPv4Api(fw)
interfacecli = InterfaceCli(fw_cli)
licensecli = LicenseCli(fw_cli)
logapi = LogMonitorApi(fw)
gav = GAV(fw)
restartapi = RestartApi(fw)
apprulesapi = AppRulesApi(fw)
matchobjapi = MatchobjectApi(fw)
zonesapi = ZoneObjectsApi(fw)
timeapi = TimeApi(fw)

# http ftp traffic test parameter
http_url = 'http://2.2.2.200/virus/'
localfile = '/root/Downloads/test.txt'
remotefile = '/var/www/html/virus/test.txt'
localgavfile = '/root/Downloads/Exploit.VBS.Agent.q.gz'
remotegavfile = '/var/www/html/virus/Exploit.VBS.Agent.q.gz'
http_send = MyHttpClinet(http_url)
my_ftp = MyFtp(host=Parameter.PC2_ETH0_NewIP, user='root', password='password')

X2_wiremode_dict = {
    'if': 'X2',
    'zone': 'LAN',  # LAN, DMZ, custom zone name
    'mode': 'wire-mode',
    'type': 'bypass',  # bypass, inspect, secure
    'wire_paired_interface': 'X3',
    'wire_paired_zone': 'LAN',
    'wire_link_propagation': False,
    'stateful_inspection': False,
    'restrict_analysis': False,
}
x2_tapmode_dict = {
    'if': 'X2',
    'zone': 'LAN',  # LAN, DMZ, custom zone name
    'mode': 'tap-mode',
    'stateful_inspection': True,
}
match_opt_dict = {
            'name': 'auto_test',
            'object_type': 'ips-signature-category-list',
            'ips': {"category": [{"id": 10}]}
        }
apprule_dict = {
            "app_rules": {
                "policy": [
                    {
                        "action_object": "Reset/Drop",
                        "address": {
                            "any": True
                        },
                        "enable": True,
                        "exclusion": {
                            "address": {},
                            "service": {}
                        },
                        "flow_reporting": False,
                        "ips_message_format": False,
                        "log": {
                            "individual": False,
                            "redundancy": {
                                "global": True
                            }
                        },
                        "logging": True,
                        "match_object": {
                            "object": 'match_obj'
                        },
                        "name": 'obj_name',
                        "schedule": {
                            "always_on": True
                        },
                        "type": {
                            "ips": True
                        },
                        "users": {
                            "excluded": {},
                            "included": {
                                "all": True
                            }
                        },
                        "zone": {
                            "any": True
                        }
                    }
                ]
            }
        }

import sys
import os
import re
import copy
import paramunittest
from time import sleep
import subprocess
import json
import random
import string
from threading import Thread
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall


# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, DHCPServerApi
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.system import DiagnosticApi, RestartApi,PacketmonitorApi,SettingApi


sys.path.append(os.environ['PYTHON_COMMON_HOME'])
suite_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/DHCP_Server_ENH_Part2/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/dhcp_server_enhance_part2.json'
lease_file = '/var/lib/dhclient/dhclient.leases'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4', 'eth2')

logger.info(f"""
PC1_ETH0_IP is: {PC1_ETH0_IP}
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH0_IP is: {PC2_ETH0_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
PC3_ETH0_IP is: {PC3_ETH0_IP}
PC3_ETH2_IP is: {PC3_ETH2_IP}
PC4_ETH0_IP is: {PC4_ETH0_IP}
PC4_ETH2_IP is: {PC4_ETH2_IP}
""")
pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)
pc4_login = Host(PC4_ETH2_IP)



# Params on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X2_IP = '13.13.1.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


class CaseParams:
    invalid_ips = ('260.1.1.1', "1.260.1.1", "1.1.260.1", "1.1.1.260")
    invalid_lease_time = (0, -1, 10000)
    valid_lease_time = (1, 9999)
    static_ip = "13.13.1.99"
    dynamic_from = "13.13.1.100"
    dynamic_to = "13.13.1.110"
    domain_name = "cyuan.test"


# Instantiate objects including API import
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


iface_v4_api = InterfaceIPv4Api(fw)
dhcp_api = DHCPServerApi(fw)
license_cli = LicenseCli(fw_cli)
diag_api = DiagnosticApi(fw)
restart_api = RestartApi(fw)
pkt_api = PacketmonitorApi(fw)
set_api = SettingApi(fw)

x1_opt = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': '255.255.255.0',
    'mgmt_https': True,
    'mgmt_ping': True,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'gateway': "12.12.1.1"

}
x2_opt = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': '255.255.255.0',
    'mgmt_https': True,
    'mgmt_ping': True
}

static_scope = {
    "dhcp_server":
        {"ipv4": {
            "scope": {
                "static": [{
                    "ip": CaseParams.static_ip,
                    "mac": "11:22:33:44:55:66",
                    "name": "",
                    "enable": True,
                    "lease_time": 60,
                    "default_gateway": "",
                    "netmask": "255.255.255.0",
                    "comment": "",
                    "domain_name": "",
                    "dns": {"server": {"inherit": True}}
                }]
            }
        }
    }
}
dynamic_scope = {
    "dhcp_server":
        {"ipv4": {
            "scope": {
                "dynamic": [{
                    "from": CaseParams.dynamic_from,
                    "to": CaseParams.dynamic_to,
                    "enable": True,
                    "lease_time": 60*24,
                    "default_gateway": Parameter.X2_IP,
                    "netmask": "255.255.255.0",
                    "comment": "",
                    "domain_name": "",
                    "dns": {"server": {"inherit": True}}
                }]
            }
        }
    }
}
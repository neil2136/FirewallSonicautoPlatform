import sys
import os
import re
import copy
import time
import subprocess
import json
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
from lib.modules.API.network import InterfaceIPv4Api, DNSSecurityApi
from lib.modules.API.log import LogSettingsApi, LogMonitorApi
from lib.modules.API.system import DiagnosticApi, PacketmonitorApi, SettingApi
from lib.modules.API.securityservices import ContentFilterApi
from lib.modules.CLI.system import LicenseCli


suite_path = os.environ['PYTHON_SONICOS_HOME']+'/Network/DNS_Tunnel_Detect/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/dns_tunnel_detect.json'
script_file = suite_path+'definition/script/dns.py'
iodine_path = suite_path+'definition/file/iodine-master'
install_iodine_path = '/tmp/iodine-master'
exp_file = '/tmp/cyuan_exp.exp'


os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
logger.info(f"""PC1_ETH1_IP is: {PC1_ETH1_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
PC3_ETH1_IP is: {PC3_ETH1_IP}
PC3_ETH2_IP is: {PC3_ETH2_IP}""")


pc1_login = Host(PC1_ETH1_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)


# Params on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_NET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    DNS_IP = '10.0.0.1'


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
interfacev4api = InterfaceIPv4Api(fw)
dnssecurityapi = DNSSecurityApi(fw)
logsettingsapi = LogSettingsApi(fw)
logmonitorapi = LogMonitorApi(fw)
licensecli = LicenseCli(fw_cli)
diagapi = DiagnosticApi(fw)
pktapi = PacketmonitorApi(fw)
cfsapi = ContentFilterApi(fw)
settingsapi = SettingApi(fw)

udp_packet = {
            'IP': {
                'dst': '12.12.1.169',
            },
            'UDP': {
                'sport': 5000,
                'dport': 53,
                },
                'data': 'automation',
            }

dns_packet = {
            'IP': {
                'dst': '12.12.1.169',
            },
            'UDP': {
                'sport': 5555,
                'dport': 53,
                },
                'data': 'automation',
            }

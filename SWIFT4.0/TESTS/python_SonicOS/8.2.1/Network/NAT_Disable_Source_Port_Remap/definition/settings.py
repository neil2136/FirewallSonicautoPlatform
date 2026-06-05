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
from tools.trafficGen import ScapyPacketSend


# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API.system import PacketmonitorApi, SettingApi
from lib.modules.CLI.system import LicenseCli

suite_path = os.environ['PYTHON_SONICOS_HOME'] + \
    '/Network/NAT_Disable_Source_Port_Remap/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/nat_disable_source_port_remap.json'
script_file = suite_path+'definition/script/send_tcp_v6.py'


os_obj = Openstack(Params.testbed)
scapyobj = ScapyPacketSend(iface='eth1', count=5)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')  # 192.168.168.169
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')  # 12.12.1.169
PC1_ETH1_IPv6 = os_obj.get_node_interface_ipv6(
    'PC1', 'eth1').split('/')[0]  # 2000::100
PC2_ETH1_IPv6 = os_obj.get_node_interface_ipv6(
    'PC2', 'eth1').split('/')[0]  # 2001::100
pc1_login = Host(PC1_ETH1_IP)
logger.info(f"""
            PC1_ETH1_IP is : {PC1_ETH1_IP}
            PC2_ETH1_IP is : {PC2_ETH1_IP}
            PC1_ETH1_IPv6 is : {PC1_ETH1_IPv6}
            PC2_ETH1_IPv6 is : {PC2_ETH1_IPv6}
            """)


# Params on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X0_V6_IP = '2000::168'
    X1_V6_IP = '2001::168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


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
interfacev4api = network.InterfaceIPv4Api(fw)
interfacev6api = network.InterfaceIPv6Api(fw)
natpolicyapi = network.NatpolicyApi(fw)
packetapi = PacketmonitorApi(fw)
settingsapi = SettingApi(fw)
licensecli = LicenseCli(fw_cli)


nat_base_dict = {
    "name": '',
    "enable": True,
    "comment": "test for add a nat policy",
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

nat_v6_base_dict = {
    "name": '',
    "enable": True,
    "comment": "test for add a v6 nat policy",
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

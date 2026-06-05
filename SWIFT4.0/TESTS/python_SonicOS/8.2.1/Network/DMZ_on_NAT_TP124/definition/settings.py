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


# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.system import PacketmonitorApi
from lib.modules.CLI.system import LicenseCli


suite_path = os.environ["PYTHON_SONICOS_HOME"]+\
    '/Network/DMZ_on_NAT_TP124/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/dmz_on_nat_tp124.json'
PPTP_CONFIG_PATH = suite_path+'definition/conf_files/pptp/'
HTTPS_CONF_PATH = suite_path+'definition/conf_files'


# parameters on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4', 'eth2')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')


PC1_ETH3_NW = os_obj.get_node_interface_network('PC1', 'eth3')
PC1_ETH1_NW = os_obj.get_node_interface_network('PC1', 'eth1')
PC2_ETH1_NW = os_obj.get_node_interface_network('PC2', 'eth1')
PC3_ETH1_NW = os_obj.get_node_interface_network('PC3', 'eth1')
PC4_ETH1_NW = os_obj.get_node_interface_network('PC4', 'eth1')

logger.info(f'''
PC1_ETH1_IP: {PC1_ETH1_IP}
PC2_ETH1_IP: {PC2_ETH1_IP}
PC3_ETH1_IP: {PC3_ETH1_IP}
PC4_ETH1_IP: {PC4_ETH1_IP}
PC1_ETH3_IP: {PC1_ETH3_IP}
PC1_ETH1_NW: {PC1_ETH1_NW}
PC2_ETH1_NW: {PC2_ETH1_NW}
PC3_ETH1_NW: {PC3_ETH1_NW}
PC4_ETH1_NW: {PC4_ETH1_NW}
    ''')

localhost = Host(PC1_ETH1_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)
pc4_login = Host(PC4_ETH2_IP)


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '10.10.0.168'
    X1_NAT_IP = '10.10.0.170'
    X1_GW = PC2_ETH1_IP 
    X3_IP = '13.13.0.168'
    X3_NAT_IP = '13.13.0.170'
    X3_GW = PC1_ETH3_IP
    X4_IP = '14.14.14.168'
    X4_NAT_IP = '14.14.14.170'
    X1_PPTP_NAT_IP = '11.11.11.200'
    X5_IP = '15.15.15.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


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
    password='password',
    supported_config_mode='cli-ssh'
)
interfacev4api = network.InterfaceIPv4Api(fw)
natpolicyapi = network.NatpolicyApi(fw)
serviceobjectapi = network.ServiceObjectApi(fw)
aoapi = network.AddressobjectsApi(fw)
agapi = AddressObjectGroupApi(fw)
aclapi = AccessRuleIPv4Api(fw)
packetapi = PacketmonitorApi(fw)
wlbapi = network.FailoverLbApi(fw)
licensecli = LicenseCli(fw_cli)


nat_base_dict = {
    "name": "",
    "enable": True,
    "comment": "",
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

edit_dict_tc34 = {
    "name": "test_for_case_34",
    "source": {"name": 'X4 Subnet'},
    "translated_source": {"name": 'X1 IP'},
    "inbound": "X4",
    "outbound": "X1"
}

edit_dict_tc35 = {
    "name": "test_for_case_35",
    "destination": {
        "name": "wan_ao1"
    },
    "translated_destination": {
        "name": "dmz_pc1"
    },
    "inbound": "X1"
}

edit_dict_tc37 = {
    "name": "test_for_case_37",
    "destination": {
        "group": "wan_nat_group"
    },
    "translated_destination": {
        "group": "dmz_pc_group"
    },
}

edit_dict_tc40 = {
    "name": "test_for_case_40",
    "destination": {
        "name": "wan_ao1"
    },
    "translated_destination": {
        "group": "dmz_pc_group"
    },
}

edit_dict_tc44 = {
    "name": "test_for_case_44",
    "destination": {
        "name": "dmz_ao"
    },
    "translated_destination": {
        "name": "dmz_pc2"
    },
    "inbound": "X0"
}

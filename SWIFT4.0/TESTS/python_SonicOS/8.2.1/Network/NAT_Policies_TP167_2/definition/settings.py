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
from lib.modules.API import network
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.system import PacketmonitorApi, RestartApi, DiagnosticApi
from lib.modules.API.policy import NatPolicyApi
from lib.modules.CLI.system import LicenseCli


suite_path = os.environ["PYTHON_SONICOS_HOME"]+'/Network/NAT_Policies_TP167_2/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
SERVER_PATH_FILE = suite_path+'definition/conf_files/test_file.txt'
TESTPLAN = suite_path+'testplan/nat_policy_tp167.json'


# parameters on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')

logger.info(f'''
PC1_ETH0_IP: {PC1_ETH0_IP}
PC1_ETH1_IP: {PC1_ETH1_IP}
PC1_ETH2_IP: {PC1_ETH2_IP}
PC2_ETH0_IP: {PC2_ETH0_IP}
PC2_ETH1_IP: {PC2_ETH1_IP}
PC2_ETH2_IP: {PC2_ETH2_IP}
PC3_ETH0_IP: {PC3_ETH0_IP}
PC3_ETH1_IP: {PC3_ETH1_IP}
PC3_ETH2_IP: {PC3_ETH2_IP}''')

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X2_IP = '13.13.1.168'
    X1_GW = PC2_ETH1_IP
    X1_DNS_1 = Params.G_DNS1
    X2_DNS_2 = Params.G_DNS2
    X1_NAT_IP = '12.12.1.170'
    X2_NAT_IP = '13.13.1.170'
    DMZ_PUB = "13.13.1.171"
    LAN_PUB = "192.168.168.171"


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
iface_api = network.InterfaceIPv4Api(fw)
nat_api = NatPolicyApi(fw)
ao_api = network.AddressobjectsApi(fw)
ag_api = network.AddressgroupsApi(fw)
srv_api = network.ServiceObjectApi(fw)
srv_grp_api = network.ServiceGroupApi(fw)
acl_api = AccessRuleApi(fw)
pkt_api = PacketmonitorApi(fw)
restart_api = RestartApi(fw)
diag_api = DiagnosticApi(fw)
licensecli = LicenseCli(fw_cli)


# parameters on the test cases
class CaseParams:
    tc26_res = False
    tc27_res = False
    tc28_res = False
    tc29_res = False
    tc34_res = False
    tc23_res = False
    tc44_res = False
    tc47_res = False
    tc43_res = False


x1_opt = {
    'if': 'X1',
    'zone': "WAN",
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': '255.255.255.0',
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS_1,
    'dns2': Parameter.X2_DNS_2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True
}
x2_opt = {
    'if': 'X2',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': '255.255.255.0',
    'mgmt_ping': True,
    'mgmt_ssh': True,
    'mgmt_https': True
}
nat_base = {
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
acl_base = {
    "name": "",
    "enable": True,
    "from": "WAN",
    "to": "LAN",
    "action": "allow",
    "source": {
        "address": {
            "any": True
        },
        "port": {
            "any": True
        }
    },
    "service": {

    },
    "destination": {
        "address": {
            "any": True
        }
    },
    "schedule": {
        "always_on": True
    },
    "users": {
        "included": {
            "all": True
        },
        "excluded": {
            "none": True
        }
    },
    "comment": "",
    "fragments": True,
    "logging": True,
    "sip": False,
    "h323": False,
    "flow_reporting": False,
    "botnet_filter": False,
    "geo_ip_filter": {
        "enable": False,
        "global": True
    },
    "priority": {
        "auto": True
    }
}
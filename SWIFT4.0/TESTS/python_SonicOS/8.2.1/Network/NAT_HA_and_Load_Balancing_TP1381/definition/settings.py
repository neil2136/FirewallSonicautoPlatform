import sys
import os
import re
from time import sleep
from copy import deepcopy
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
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.system import PacketmonitorApi, DiagnosticApi
from lib.modules.API.log import LogMonitorApi
from lib.modules.CLI.system import LicenseCli


suite_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/NAT_HA_and_Load_Balancing_TP1381/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/nat_ha.json'


# parameters on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4', 'eth2')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')
PC5_ETH2_IP = os_obj.get_node_interface_ip('PC5', 'eth2')

logger.info(f"""
PC1_ETH1_IP: {PC1_ETH1_IP}
PC1_ETH2_IP: {PC1_ETH2_IP}
PC2_ETH1_IP: {PC2_ETH1_IP}
PC2_ETH2_IP: {PC2_ETH2_IP}
PC3_ETH1_IP: {PC3_ETH1_IP}
PC3_ETH2_IP: {PC3_ETH2_IP}
PC4_ETH1_IP: {PC4_ETH1_IP}
PC4_ETH2_IP: {PC4_ETH2_IP}
PC5_ETH1_IP: {PC5_ETH1_IP}
PC5_ETH2_IP: {PC5_ETH2_IP}
""")


pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)
pc4_login = Host(PC4_ETH2_IP)
pc5_login = Host(PC5_ETH2_IP)


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X2_IP = '13.13.1.168'
    X1_NAT_IP = '12.12.1.180'
    X1_NET = '12.12.1.0'
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
acl_api = AccessRuleApi(fw)
ao_api = network.AddressobjectsApi(fw)
nat_api = network.NatpolicyApi(fw)
pkt_api = PacketmonitorApi(fw)
log_api = LogMonitorApi(fw)
diag_api = DiagnosticApi(fw)
licensecli = LicenseCli(fw_cli)


acl_base = {
    "enable": True,
    "name": "",
    "from": "WAN",
    "to": "WAN",
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
        "any": True
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
    },
    "high_availability": {
        "probing":
            {
                "deactivate_after": 3,
                "probe_every": 5,
                "probe_type": {"icmp_ping": True},
                "reactivate_after": 3,
                "reply_timeout": 1
            }
    },
    "nat_method": "sticky-ip",
    "dns_doctoring": False
}

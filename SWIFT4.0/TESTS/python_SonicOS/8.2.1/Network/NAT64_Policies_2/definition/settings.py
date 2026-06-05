import sys
import os
import re
from time import sleep
from copy import deepcopy
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


# import form branch lib contents for testsuite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API.firewall import AccessRuleApi, AccessRuleIPv6Api
from lib.modules.API.system import SettingApi
from lib.modules.API.policy import SecurityPolicyApi, NatPolicyApi
from lib.modules.API.system import PacketmonitorApi, DiagnosticApi, RestartApi
from lib.modules.API.log import LogMonitorApi, LogSettingsApi
from lib.modules.CLI.system import LicenseCli


suite_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/NAT64_Policies_2/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/nat64_policies.json'
ftp_conf_file = suite_path + 'definition/conf_file/vsftpd.conf'
ftp_user_file = suite_path + 'definition/conf_file/ftpusers'
script_file = suite_path+'definition/conf_file/script.py'


# parameters on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC1_ETH1_V6 = os_obj.get_node_interface_ipv6('PC1', 'eth1').split('/')[0]
PC2_ETH1_V6 = os_obj.get_node_interface_ipv6('PC2', 'eth1').split('/')[0]
PC3_ETH1_V6 = os_obj.get_node_interface_ipv6('PC3', 'eth1').split('/')[0]
logger.info(f"""
PC1_ETH1_IP: {PC1_ETH1_IP}
PC1_ETH2_IP: {PC1_ETH2_IP}
PC2_ETH1_IP: {PC2_ETH1_IP}
PC2_ETH2_IP: {PC2_ETH2_IP}
PC3_ETH1_IP: {PC3_ETH1_IP}
PC3_ETH2_IP: {PC3_ETH2_IP}
PC1_ETH1_V6: {PC1_ETH1_V6}
PC2_ETH1_V6: {PC2_ETH1_V6}
PC3_ETH1_V6: {PC3_ETH1_V6}
""")

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X2_IP = '13.13.1.168'
    X0_V6_IP = "2000::168"
    X1_V6_IP = "2001::168"
    X2_V6_IP = "2002::168"
    X1_NAT64_IP = '64:ff9b::c0c:1a9'
    Well_Know_Pref64 = '64:ff9b:://96'
    Well_Know_Pref64_NET = '64:ff9b::/96'
    X1_DNS_1 = Params.G_DNS1
    X2_DNS_2 = Params.G_DNS2


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
nat64_api = NatPolicyApi(fw)
pkt_api = PacketmonitorApi(fw)
diag_api = DiagnosticApi(fw)
log_mon_api = LogMonitorApi(fw)
log_set_api = LogSettingsApi(fw)
ao_api = network.AddressobjectsApi(fw)
acl_api = AccessRuleApi(fw)
acl_v6_api = AccessRuleIPv6Api(fw)
set_api = SettingApi(fw)
restart_api = RestartApi(fw)
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

import os
import sys
import re
import time
import copy


from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test, skip_if_fail_method, repeat_method
from runner.utils.assertion import Assertion
from runner.settings import Params, logger


# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.enhancedinfo import show_testcase_info
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
import unittest


# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from modules.API.log import LogSettingsApi,LogCategoryApi,LogMonitorApi
from modules.API.network import ZoneObjectsApi, InterfaceIPv4Api,  AddressobjectsApi
from lib.modules.API.network import DNSSecurityApi, DnsFilteringApi, DnsSettingsApi, DnsProxyApi
from modules.API.firewall import DNSRuleApi
from modules.API.system import PacketmonitorApi, DiagnosticApi
from modules.CLI.network import DNSfilteringCli
from modules.CLI.system import LicenseCli


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Policy_Filter/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/DNS_Filtering_Policy_Filter.json'

# PC addresses
OpenS = Openstack(Params.testbed)
PC1_ETH0_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = OpenS.get_node_interface_ip('PC2', 'eth2')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}')
PC1_LOGIN = Host(PC1_ETH0_IP)
PC2_LOGIN = Host(PC2_ETH1_IP)



# parameters on the firewall
class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    Route_Host_1 = '10.0.0.0'
    Route_Mask_1 = '255.0.0.0'
    Route_Mask_2 = '0.0.0.0'
    PC1_GW = '16.16.1.1'
    Route_Host_2 = '0.0.0.0'
    DUT_X2 = "192.168.200.10"
    DUT_X3 = "33.33.0.10"
    Neustar_server = '156.154.54.200'


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

zone_api = ZoneObjectsApi(fw)
interface_api = InterfaceIPv4Api(fw)
addrObj_api = AddressobjectsApi(fw)
dnsSec_api = DNSSecurityApi(fw)
dnsRule_api = DNSRuleApi(fw)
dnsFilter_api = DnsFilteringApi(fw)
dnsSett_api = DnsSettingsApi(fw)
dnspxy_api = DnsProxyApi(fw)
packet_api = PacketmonitorApi(fw)
diag_api = DiagnosticApi(fw)
logSet_api = LogSettingsApi(fw)
logCata_api = LogCategoryApi(fw)
logMonitor_api = LogMonitorApi(fw)
dnsSec_cli = DNSfilteringCli(fw_cli)
license_cli = LicenseCli(fw_cli)


# parameters on the test cases
X1_static_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
}
config_X2_dict = {
    'if': 'x2',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.DUT_X2,
    'netmask': '255.255.255.0',
    'gateway': '12.12.12.1',
    'mgmt_ping': True,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True
}
custom_zone_dict = {
    "zones": [
        {
            "name": "custom_zone",
            "security_type": "public",
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
# # for 7.1.1 nssp
# custom_zone_dict = {
#     "zones": [
#         {
#             "name": "custom_zone",
#             "security_type": "public"
#         }
#     ]
# }
ao_dict = {
    'name': 'PC1',
    'zone': 'LAN',
    'object_type': 'host',
    'value': PC1_ETH0_IP
}
add_file_dict = {
    "dns_security": {
        "dns_filtering": {
            "profile": [
                {
                    "name": "Gaming_Negative",
                    "actions": "{\"2\":2}"
                }
            ]
        }
    }
}
add_rule_dict = {
    "dns_policies": [
        {
            "name": "test",
            "priority": {
                "manual": 1
            },
            "enable": True,
            "source": {
                "address": {
                    "any": True
                }
            },
            "service": {
                "name": "DNS (Name Service) UDP"
            },
            "from": "X0",
            "action": {
                "filter_profile": "Default Profile"
            }
        }
    ]
}

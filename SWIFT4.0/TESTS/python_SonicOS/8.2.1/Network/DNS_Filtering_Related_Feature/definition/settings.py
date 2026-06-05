import os
import sys
import re
import json
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


# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi
from lib.modules.API.network import DnsSettingsApi, DnsProxyApi, DNSSecurityApi, DnsFilteringApi
from lib.modules.API.system import PacketmonitorApi, DiagnosticApi, LicenseApi, SettingApi
from lib.modules.API.firewall import DNSRuleApi
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.network import DNSPolicyCli


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Related_Feature/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/DNS_Filtering_Related_Feature.json'

# PC addresses
OpenS = Openstack(Params.testbed)
PC1_ETH0_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}')
PC1_LOGIN = Host(PC1_ETH0_IP)


# parameters on the firewall
class Parameter:
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
    Filtering_server = '156.154.54.200'


# parameters used by suite cases
class CParam:
    Domain = 'www.ea.com'
    Profile_Name = 'NewProfile'


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_api = InterfaceIPv4Api(fw)
ao_api = AddressobjectsApi(fw)
license_api = LicenseApi(fw)
dnsRule_api = DNSRuleApi(fw)
dnsSett_api = DnsSettingsApi(fw)
dnspxy_api = DnsProxyApi(fw)
dnsSec_api = DNSSecurityApi(fw)
dnsFil_api = DnsFilteringApi(fw)
packet_api = PacketmonitorApi(fw)
sett_api = SettingApi(fw)
diagnostic_api = DiagnosticApi(fw)
license_cli = LicenseCli(fw_cli)
dnsPolicy_cli = DNSPolicyCli(fw_cli)


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
filter_policy_cli_dict = {
    'name': 'TestFilter', 
    'service': 'name "DNS (Name Service) UDP"',
    'action': f'filter-profile "Default Profile"'
}
filter_rule_dict = {
    "dns_policies": [
        {
            "name": "Filter",
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
                "filter_profile": CParam.Profile_Name
            }
        }
    ]
}
add_profile_dict = {
    "dns_security": {
        "dns_filtering": {
            "profile": [
                {
                    "name": CParam.Profile_Name,
                    "actions": "{\"1\":2,\"2\":0,\"3\":2,\"4\":2,\"5\":2,\"6\":2,\"7\":2,\"8\":0,\"9\":2,\"10\":2,\"11\":0,\"12\":2,\"13\":2,\"14\":2,\"15\":2,\"16\":2,\"17\":2,\"18\":2,\"19\":2}"
                }
            ]
        }
    }
}
ao_dict = {
    'name': 'bypass',
    'zone': 'LAN',
    'object_type': 'fqdn',
    'value': CParam.Domain
    }
base_config_dict = {
    "dns_security": {
        "dns_filtering": {
            "use_whitelist": False,
            "forged_ip": {
                "ipv4": "192.168.100.100",
                "ipv6": "1001::1"
            }
        }
    }
}
custom_domain_dict = {
    "dns_security": {
        "dns_filtering": {
            "custom_domain": [
                {
                    "domain": CParam.Domain,
                    "category":"1. Adult"
                }
            ]
        }
    }
}

import os
import sys
import re
import time
import copy
import json


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
from lib.modules.API.network import InterfaceIPv4Api, DNSSecurityApi, DnsFilteringApi, DnsProxyApi
from lib.modules.API.system import DiagnosticApi, PacketmonitorApi
from lib.modules.API.firewall import DNSRuleApi
from lib.modules.API.log import LogSettingsApi, LogMonitorApi, LogCategoryApi
from lib.modules.CLI.network import DNSfilteringCli, DNSCli
from lib.modules.CLI.system import LicenseCli


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Settings_part/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/DNS_Filtering_Settings_part.json'

# PC addresses
OpenS = Openstack(Params.testbed)
PC1_ETH0_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}')
PC1_LOGIN = Host(PC1_ETH0_IP)


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
    Filtering_server = '156.154.54.200'

class CParam:
    test_Domain = "*.ea.com"
    www_Domain = "www.ea.com"
    Category = "1. Adult"
    Forged_IPv4 = "10.1.1.1"
    Forged_IPv6 = "1001::1"


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_api = InterfaceIPv4Api(fw)
dnspxy_api = DnsProxyApi(fw)
dnsSec_api = DNSSecurityApi(fw)
dnsRule_api = DNSRuleApi(fw)
dnsFilter_api = DnsFilteringApi(fw)
packet_api = PacketmonitorApi(fw)
diag_api = DiagnosticApi(fw)
logSet_api = LogSettingsApi(fw)
logCate_api = LogCategoryApi(fw)
logMonitor_api = LogMonitorApi(fw)
dnsFilter_cli = DNSfilteringCli(fw_cli)
dns_cli = DNSCli(fw_cli)
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
dns_rule_dict = {
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
custom_domain_dict = {
    "dns_security":{
        "dns_filtering":{
            "custom_domain":[
                {"domain": "*.ea.com", "category": "4. Malware"}
            ]
        }
    }
}
domain_name_list = ["adult.com", "ea.com", "bing.com", "playboy.com"]
log_dict = {
    "log": {
        "event": [
            {
                "id": 1687,
                "category": "Network",
                "group": "DNS Security",
                "priority_level": "alert",
                "log_monitor": {
                    "redundancy_interval": 0
                },
                "email_alert": {
                    "redundancy_interval": 0
                },
                "syslog": {
                    "redundancy_interval": 0
                },
                "event_profile": {
                    "syslog_server_profile": 0
                }
            }
        ]
    }
}
log_group_dict = {
    "log":{
        "group":[
            {
                "id":107,
                "name":"DNS Security",
                "priority_level":"alert",
                "log_email":{},
                "log_monitor":{
                    "type":"enabled",
                    "redundancy_interval":{}
                },
                "email_alert":{"type":"mixed"},
                "syslog":{"type":"mixed"},
                "trap":{"type":"mixed","redundancy_interval":{"value":60}},
                "ipfix":{"type":"mixed"},
                "event_profile":{"syslog_server_profile":0},
                "log_digest":{"mixed":True},
                "color":{"leave_unchanged":True},
                "alert_email":{}
            }
        ]
    }
}
profile_dict = {
    "dns_security": {
        "dns_filtering": {
            "profile": [
                {
                    "name": "Gaming_Negative",
                    "actions": '{"2":1}'
                }
            ]
        }
    }
}

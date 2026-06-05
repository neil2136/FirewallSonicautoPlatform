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
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi
from lib.modules.API.network import DnsProxyApi, DNSSecurityApi, DnsFilteringApi, DnsSettingsApi
from lib.modules.API.system import PacketmonitorApi, DiagnosticApi, SettingApi
from lib.modules.API.firewall import DNSRuleApi
from lib.modules.API.log import LogSettingsApi, LogMonitorApi, AuditlogMonitorApi
from lib.modules.CLI.network import DNSCli
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.diag import DiagCli


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Sinkhole_full/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/DNS_Sinkhole.json'
script_path = suite_path + 'definition/script/'


# PC addresses
OpenS = Openstack(Params.testbed)
PC1_ETH0_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}')
PC1_LOGIN = Host(PC1_ETH0_IP)
PC2_LOGIN = Host(PC2_ETH1_IP)


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
    Route_Host_2 = '0.0.0.0'
    PC1_GW = '16.16.1.1'


class CParam:
    Forged_IP_log = 1549
    Hit_Malicious_Pkt_log = 1550
    Domain = "nordvpn.com"
    Custom_Domain_1 = "bing.com"
    Custom_Domain_2 = "baidu.com"
    Database_list = []


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_api = InterfaceIPv4Api(fw)
dnsSecurity_api = DNSSecurityApi(fw)
dnsProxy_api = DnsProxyApi(fw)
dnsFil_api = DnsFilteringApi(fw)
dnsRule_api = DNSRuleApi(fw)
dnsSett_api = DnsSettingsApi(fw)
logSet_api = LogSettingsApi(fw)
logMonitor_api = LogMonitorApi(fw)
audit_api = AuditlogMonitorApi(fw)
packet_api = PacketmonitorApi(fw)
ao_api = AddressobjectsApi(fw)
diagnostic_api = DiagnosticApi(fw)
sett_api = SettingApi(fw)
dns_cli = DNSCli(fw_cli)
license_cli = LicenseCli(fw_cli)
diag_cli = DiagCli(fw_cli)


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
            "name": 'test',
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
                "proxy": True
            }
        }
    ]
}
drop_log_dict = {
    "log": {
        "event": [
            {
                "id": CParam.Hit_Malicious_Pkt_log,
                "category": "Network",
                "group": "DNS Security",
                "priority_level": "alert",
                "log_monitor": {
                    "redundancy_interval": 0
                }
            }
        ]
    }
}
forged_reply_dict = {
    'action': 'dropping_with_dns_reply_of_forged_ip',
    'ipv4': '11.11.11.11',
    'ipv6': '1001:1:1:1:1:1:1:100'
}
domain_pool = (
    'whoer.net',
    'samhacker.com',
    'hola.org',
    'unbl.org',
    'futurepast.xyz',
    'us1.unbl.org',
    'websitevpn.com',
    'biscoint.io',
    'lizzbiz.com',
    'teatroleopardisanginesio.it',
    'endlesswaltz.xyz',
    'mynervisit.com',
    'site2unblock.com',
    'hackearcorreos.net',
    'vpngate.net',
    'yotids.com',
    'safervpn.com',
    'surf6003.appspot.com',
    'vpnvip.com',
    'safersurf.com',
    'shadowsocks.org',
    'ezyonlinesupport.com'
)
sinkhole_service_cmds_list = (
    {
        'enable': False,
        'use-whitelist': False
    },
    {
        'enable': True,
        'action-type': '1'
    },
    {
        'enable': True,
        'action-type': '2'
    },
    {
        'enable': True,
        'use-whitelist': True,
        'action-type': '3'
    },
    {
        'enable': True,
        'action-type': '3',
        'forged_ipv4': '11.1.1.1',
        'forged_ipv6': '1001:10::10'
    }
)
show_check_cli_dict = {
    'dns-security dns-sinkhole base': 'enable',
    'dns-security dns-sinkhole custom-malicious-entries': CParam.Custom_Domain_1,
    'dns-security white-list-entries': CParam.Custom_Domain_1
}
ao_dict = {
    'name': 'bypass',
    'zone': 'LAN',
    'object_type': 'fqdn',
    'value': CParam.Domain,
    'dns_ttl': 0
}

import os
import re
import sys
import time
import copy
import json
import paramunittest

from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API.system import SettingApi, PacketmonitorApi,DiagnosticApi
from lib.modules.API.firewall import DNSRuleApi, AccessRuleApi
from lib.modules.API.log import LogCategoryApi, LogMonitorApi
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.network import DNSCli, DNSPolicyCli


# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Proxy_Part2/'
sys.path.append(suite_path)
TESTPLAN = suite_path + 'testplan/DNS_Proxy_Part2.json'
CONF_PATH = suite_path +'definition/config/'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4', 'eth2')
PC1_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC1', 'eth2')
PC2_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC2', 'eth2')
PC3_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC3', 'eth2')
PC4_ETH2_IPV6 = os_obj.get_node_interface_ipv6('PC4', 'eth2')
logger.info(f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC3_ETH2_IP: {PC3_ETH2_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC4_ETH2_IP: {PC4_ETH2_IP}'
            f'\n PC1_ETH2_IPV6: {PC1_ETH2_IPV6}'
            f'\n PC2_ETH2_IPV6: {PC2_ETH2_IPV6}'
            f'\n PC3_ETH2_IPV6: {PC3_ETH2_IPV6}'
            f'\n PC4_ETH2_IPV6: {PC4_ETH2_IPV6}'
            )
PC1_login = Host(PC1_ETH2_IP)
PC2_login = Host(PC2_ETH1_IP)
PC3_login = Host(PC3_ETH1_IP)
PC4_login = Host(PC4_ETH1_IP)

# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X2_IP = '12.12.3.168'
    X2_GW = '12.12.3.1'
    X3_IP = '13.13.1.168'
    X3_GW = PC3_ETH2_IP
    X3_SUBNET = '13.13.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2

    PREFIX_LENGTH = 64
    X0_IPV6 = "2001:2018::168"
    X0_NET_V6 = "2001:2018::/64"
    X0_PC_IPV6 = PC1_ETH2_IPV6[:-3]
    X1_IPV6 = '2001:2011::168'
    X1_GW_IPV6 = PC2_ETH2_IPV6[:-3]
    X2_IPV6 = '2001:2103::168'
    X2_GW_IPV6 = PC4_ETH2_IPV6[:-3]
    X3_IPV6 = '2001:2013::168'
    X3_GW_IPV6 = PC3_ETH2_IPV6[:-3]

class CaseParams:
    DOMAIN = "pc1.baidu.com"
    DOMAIN_IP = "192.16.2.100"
    DOMAIN_IPv6 = '1009:3:2::1'
    Max_Cache = 0
    ttl = 10
    log = ''
    DNS_PC2 = PC2_ETH2_IP
    DNS_PC3 = PC3_ETH2_IP
    DNS_PC4 = PC4_ETH2_IP
    DNS_V6_PC2 = PC2_ETH2_IPV6[:-3]
    DNS_V6_PC3 = PC3_ETH2_IPV6[:-3]
    DNS_V6_PC4 = PC4_ETH2_IPV6[:-3]


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

dns_api = network.DnsSettingsApi(fw)
dns_proxy_api = network.DnsProxyApi(fw)
dns_policy_api = network.DnsPolicyApi(fw)
dns_rule_api = DNSRuleApi(fw)
pkg_api = PacketmonitorApi(fw)
interface_api = network.InterfaceIPv4Api(fw)
interface_v6_api = network.InterfaceIPv6Api(fw)
diagnostic_api = DiagnosticApi(fw)
log_category_api = LogCategoryApi(fw)
log_monitor_api = LogMonitorApi(fw)
accessrule_api= AccessRuleApi(fw)
setting_api = SettingApi(fw)
zone_api = network.ZoneObjectsApi(fw)
license_cli= LicenseCli(fw_cli)
dns_cli = DNSCli(fw_cli)
dns_policy_cli = DNSPolicyCli(fw_cli)

dns_dict = {
    "dns": {
        "server": {
            "inherit": False,
            "static": {
                "primary": "",
                "secondary": "",
                "tertiary": ""
            },
            "ipv6": {
                "inherit": False,
                "static": {
                    "primary": "::",
                    "secondary": "::",
                    "tertiary": "::"
                },
                "preferred": False
            }
        }
    }
}

log_group_dict = {
    "log":{
        "group":[
            {
                "id":101,
                "name":"DNS Proxy",
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

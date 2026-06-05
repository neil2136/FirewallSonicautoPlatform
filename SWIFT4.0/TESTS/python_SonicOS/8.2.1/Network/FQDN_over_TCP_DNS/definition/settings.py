import os
import sys
import re
import time
import copy
import requests
import unittest
import json
from datetime import datetime
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.log import LogAutomationApi, LogMonitorApi
from lib.modules.API.network import (
    AddressobjectsApi,
    DnsProxyApi,
    DnsSettingsApi,
    InterfaceIPv4Api,
    InterfaceIPv6Api,
    ZoneObjectsApi,
)
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.policy import NatPolicyApi
from lib.modules.API.system import (
    DiagnosticApi,
    RestartApi,
    SettingApi,
    TimeApi,
    ScheduleApi,
    PacketmonitorApi,
)
from lib.modules.CLI.network import DNSCli
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + "/Network/FQDN_over_TCP_DNS/"
sys.path.append(suite_path)
sys.path.append(suite_path + "testcases")
TESTPLAN = suite_path + "testplan/FQDN_over_TCP_DNS.json"
CONF_PATH = suite_path + "definition/config"
SCRIPTS_PATH = suite_path + "definition/scripts"
EXP_PATH = "/tmp/dns_tcp_exp"

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip("PC1", "eth1")
PC1_ETH2_IP = os_obj.get_node_interface_ip("PC1", "eth2")
PC1_ETH2_IP_V6 = "1001:1::10"
PC2_ETH1_IP = os_obj.get_node_interface_ip("PC2", "eth1")
PC2_ETH2_IP = os_obj.get_node_interface_ip("PC2", "eth2")
PC2_ETH2_IP_V6 = "1001:2::20"
PC3_ETH1_IP = os_obj.get_node_interface_ip("PC3", "eth1")
PC3_ETH2_IP = os_obj.get_node_interface_ip("PC3", "eth2")
PC3_ETH2_IP_V6 = "2001:100::169"
logger.info(
    f"\n PC1_ETH1_IP: {PC1_ETH1_IP}"
    f"\n PC1_ETH2_IP: {PC1_ETH2_IP}"
    f"\n PC1_ETH2_IP_V6: {PC1_ETH2_IP_V6}"
    f"\n PC2_ETH1_IP: {PC2_ETH1_IP}"
    f"\n PC2_ETH2_IP: {PC2_ETH2_IP}"
    f"\n PC2_ETH2_IP_V6: {PC2_ETH2_IP_V6}"
    f"\n PC3_ETH1_IP: {PC3_ETH1_IP}"
    f"\n PC3_ETH2_IP: {PC3_ETH2_IP}"
    f"\n PC3_ETH2_IP_V6: {PC3_ETH2_IP_V6}"
    f"\n FW_DNS1_IP: {Params.G_DNS1}"
    f"\n FW_DNS2_IP: {Params.G_DNS2}"
)
PC1_login = Host(PC1_ETH1_IP)
PC2_login = Host(PC2_ETH1_IP)
PC3_login = Host(PC3_ETH1_IP)


# parameters on the fw
class Parameter:
    FIREWALL = "192.168.168.168"
    X1_IP_V4 = "12.12.1.168"
    X1_SUBNET = "12.12.1.0"
    X1_GW = "12.12.1.1"
    X1_NAT = "12.12.1.0"
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_IP_V6 = "2001:100::168"
    X1_SUBNET_V6 = "2001:100::"
    X2_IP_V4 = "192.168.2.168"
    X2_SUBNET = "192.168.2.0"
    X2_GW = "192.168.2.168"
    X2_IP_V6 = "1001:2::168"
    X0_IP_V6 = "1001:1::168"
    MASK = "255.255.255.0"
    # Route 1
    RT_HOST_1 = "10.0.0.0"
    RT_MASK_1 = "255.0.0.0"
    PC1_GW = "192.168.2.1"
    # Default Route
    RT_DEF_HOST = "0.0.0.0"
    RT_DEF_MASK = "0.0.0.0"


class CaseParms:
    TEST_DOMAIN_1 = "100.dnstcp.example.com"
    TEST_DNS_AO_NAME_1 = "test_dns_tcp_ao_1"
    TEST_DOMAIN_2 = "100.tcpdns.example.com"
    TEST_DNS_AO_NAME_2 = "test_dns_tcp_ao_2"
    CUS_AG_NAME = "test_cus_ag"
    CUS_AO_NAME = "test_cus_ao"
    EXP_FILE_PATH = "/tmp/dns_tcp.exp"


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL, user="admin", password="sonicauto", supported_config_mode="api"
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user="admin",
    password="sonicauto",
    supported_config_mode="cli-ssh",
)
accessruleapi = AccessRuleIPv4Api(fw)
aoapi = AddressobjectsApi(fw)
addressobjectgroupapi = AddressObjectGroupApi(fw)
diagapi = DiagnosticApi(fw)
dnsproxyapi = DnsProxyApi(fw)
dnssettingsapi = DnsSettingsApi(fw)
interfacev4api = InterfaceIPv4Api(fw)
interfacev6api = InterfaceIPv6Api(fw)
licensecli = LicenseCli(fw_cli)
logapi = LogMonitorApi(fw)
logautoapi = LogAutomationApi(fw)
natpolicyapi = NatPolicyApi(fw)
packetmonitorapi = PacketmonitorApi(fw)
restartapi = RestartApi(fw)
scheduleapi = ScheduleApi(fw)
settingapi = SettingApi(fw)
timeapi = TimeApi(fw)
zoneapi = ZoneObjectsApi(fw)
dnscli = DNSCli(fw_cli)


# Init Settings
x1_wan_v4_dict = {
    "if": "X1",
    "zone": "WAN",
    "mode": "static",
    "ip": Parameter.X1_IP_V4,
    "netmask": Parameter.MASK,
    "gateway": Parameter.X1_GW,
    "dns1": PC2_ETH2_IP,
    "dns2": Parameter.X1_DNS2,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_snmp": True,
    "mgmt_ping": True,
    "user_https": True,
}

x1_wan_v6_dict = {
    "name": "X1",
    "mode": "static",
    "zone": "WAN",
    "ip": Parameter.X1_IP_V6,
    "prefix_length": 64,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_snmp": True,
    "mgmt_ping": True,
    "user_https": True,
}

x2_lan_v4_dict = {
    "if": "X2",
    "zone": "LAN",
    "mode": "static",
    "ip": Parameter.X2_IP_V4,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_ping": True,
    "user_https": True,
    "mgmt_snmp": True,
}

x2_lan_v6_dict = {
    "name": "X2",
    "mode": "static",
    "zone": "LAN",
    "ip": Parameter.X2_IP_V6,
    "prefix_length": 64,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_snmp": True,
    "mgmt_ping": True,
    "user_https": True,
}

ipv6_nat_dict = {
    "nat_policies": [
        {
            "ipv6": {
                "comment": "auto_test_ipv6_nat",
                "destination": {"any": True},
                "enable": True,
                "inbound": "any",
                "name": "cfs_v6_nat_rule",
                "outbound": "any",
                "priority": {"auto": True},
                "reflexive": False,
                "service": {"any": True},
                "source": {"any": True},
                "source_port_remap": True,
                "ticket": {"tag1": "", "tag2": "", "tag3": ""},
                "translated_destination": {"original": True},
                "translated_service": {"original": True},
                "translated_source": {"name": "X1 IPv6 Primary Static Address"},
            }
        }
    ]
}

fqdn_ao_1_dict = {
    "object_type": "fqdn",
    "name": CaseParms.TEST_DNS_AO_NAME_1,
    "zone": "WAN",
    "value": CaseParms.TEST_DOMAIN_1,
    "dns_ttl": 0,
}

fqdn_ao_2_dict = {
    "object_type": "fqdn",
    "name": CaseParms.TEST_DNS_AO_NAME_2,
    "zone": "WAN",
    "value": CaseParms.TEST_DOMAIN_2,
    "dns_ttl": 0,
}

dns_settings_dict = {
    "dns": {
        "server": {
            "inherit": False,
            "static": {
                "primary": PC3_ETH2_IP,
                "secondary": "0.0.0.0",
                "tertiary": "0.0.0.0",
            },
            "ipv6": {
                "inherit": False,
                "static": {
                    "primary": PC3_ETH2_IP_V6,
                    "secondary": "::",
                    "tertiary": "::",
                },
                "preferred": False,
            },
        },
        "rebinding": {
            "enable": False,
            "action": "log-attack-only",
            "allowed_domains": {},
        },
        "fqdn_binding": False,
        "split_servers": True,
        "fqdn_over_tcp_dns": True,
    }
}

dns_proxy_settings_dict = {
    "enable": True,
    "enforce_all_dns_requests": True,
    "dns_cache": True,
}

dns_split_settings_dict = {
    "domain": "*.dnstcp.example.com",
    "ipv4": {"primary": PC3_ETH2_IP},
    "ipv6": {"primary": PC3_ETH2_IP_V6},
    "local_interface": "X1",
    "manual_ttl": 0,
}

custom_acl_dict = {
    "action": "deny",
    "botnet_filter": False,
    "comment": "",
    "connection_limit": {"source": {}, "destination": {}},
    "destination": {"address": {"any": True}},
    "dpi": True,
    "dpi_ssl": {"client": True, "server": True},
    "enable": True,
    "flow_reporting": False,
    "fragments": True,
    "from": "LAN",
    "geo_ip_filter": {"enable": False},
    "h323": False,
    "logging": True,
    "management": False,
    "max_connections": 100,
    "name": "test_dns_tcp",
    "packet_monitoring": False,
    "priority": {"auto": True},
    "quality_of_service": {"class_of_service": {}, "dscp": {"preserve": True}},
    "redirect_unauthenticated_users_to_log_in": True,
    "reflexive": False,
    "schedule": {"name": "test_sched"},
    "service": {"any": True},
    "sip": False,
    "source": {"address": {"any": True}, "port": {"any": True}},
    "tcp": {"timeout": 15, "urgent": False},
    "to": "WAN",
    "udp": {"timeout": 30},
    "users": {"included": {"all": True}, "excluded": {"none": True}},
}

lan_wan_acl_dict = {"access_rules": [{"ipv4": custom_acl_dict}]}

deny_lan_to_wan_dict = {
    "name": "deny_lan_to_wan",
    "from": "LAN",
    "to": "WAN",
    "source_addr": {"group": "LAN Subnets"},
    "dst_addr": {"any": True},
    "service": {"any": True},
    "action": "deny",
    "comment": "",
}

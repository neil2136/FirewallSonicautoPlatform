import os
import sys
import re
from time import sleep
import copy
import json
import subprocess
import unittest

from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test, skip_if_fail_method, repeat_method
from runner.utils.assertion import Assertion
from runner.settings import Params, logger

# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall

# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API.log import LogSettingsApi, LogMonitorApi, SyslogSettingsApi
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.policy import NatPolicyApi
from lib.modules.CLI.system import LicenseCli

sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
suite_path = os.environ['PYTHON_SONICOS_HOME'] + '/Log/Log_For_TCP_Connection_NAT_Mapping/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/log_for_tcp_connection_nat_mapping.json'
script_path = suite_path + 'definition/script.py'

os_obj = Openstack(Params.testbed)
Console_Info = os_obj.get_console_info(dut='UTM')
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')

logger.info(f"""
PC1_ETH0_IP is: {PC1_ETH0_IP}
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH0_IP is: {PC2_ETH0_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
PC3_ETH0_IP is: {PC3_ETH0_IP}
PC3_ETH1_IP is: {PC3_ETH1_IP}
PC3_ETH2_IP is: {PC3_ETH2_IP}
""")

PC1 = Host(PC1_ETH2_IP)
PC2 = Host(PC2_ETH2_IP)
PC3 = Host(PC3_ETH2_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X2_IP = '13.13.1.168'
    X0_V6_IP = '1011::168'
    X1_V6_IP = '1012::168'
    NAT_IP_DMZ = '12.12.1.100'
    NAT_IP_LAN = '12.12.1.101'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


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

license_cli = LicenseCli(fw_cli)
iface_v4_api = network.InterfaceIPv4Api(fw)
iface_v6_api = network.InterfaceIPv6Api(fw)
time_api = system.TimeApi(fw)
settings_api = system.SettingApi(fw)
pkt_mon_api = system.PacketmonitorApi(fw)
restart_api = system.RestartApi(fw)
diag_api = system.DiagnosticApi(fw)
logset_api = LogSettingsApi(fw)
logmon_api = LogMonitorApi(fw)
acl_api = AccessRuleApi(fw)
nat_api = NatPolicyApi(fw)
ao_api = network.AddressobjectsApi(fw)
syslog_api = SyslogSettingsApi(fw)

x1_opt = {
    'if': 'X1',
    'gateway': '12.12.1.1',
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': '255.255.255.0',
    'mgmt_https': True,
    'mgmt_ping': True
}
x2_opt = {
    'if': 'X2',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': '255.255.255.0',
    'mgmt_https': True,
    'mgmt_ping': True
}

x0_v6_dict = {
    'name': 'X0',
    'mode': 'static',
    'zone': 'LAN',
    'ip': Parameter.X0_V6_IP,
    'prefix_length': 64,
    'mgmt_ping': True,
    'mgmt_https': True
}
x1_v6_dict = {
    'name': 'X1',
    'mode': 'static',
    'zone': 'WAN',
    'ip': Parameter.X1_V6_IP,
    'prefix_length': 64,
    'mgmt_ping': True,
    'mgmt_https': True
}
acl_base = {
    "enable": True,
    "name": "",
    "from": "WAN",
    "to": "DMZ",
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
    }
}

event_1197 = {
    "log":
        {"event": [{
            "id": 1197,
            "name": "Connection NAT Mapping",
            "priority_level": "notice",
            "log_email": {},
            "log_monitor": {"redundancy_interval": 0},
            "email_alert": {},
            "syslog": {"redundancy_interval": 0},
            "trap": {},
            "ipfix": {},
            "event_profile": {"syslog_server_profile": 0},
            "log_digest": False,
            "color": {"hex": "0x001E90FF"},
            "alert_email": {}
        }]
        }
}

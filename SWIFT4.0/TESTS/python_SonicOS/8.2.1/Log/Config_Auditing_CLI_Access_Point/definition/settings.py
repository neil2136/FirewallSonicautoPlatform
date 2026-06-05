import os
import sys
import re
import time
import datetime
import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from networkdevice import Host

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Access_Point/testcases")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Access_Point")
TESTPLAN = os.environ[
               "PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_CLI_Access_Point/testplan/Config_Auditing_CLI_Access_Point.json'

from lib.modules.API import log, network, system
from lib.modules.CLI.system import LicenseCli, AdminCli
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from lib.modules.CLI.dpissl import ClientSslCli

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
logger.info("\n" + "-" * 30 + "\n" \
            + "PC1_ETH0_IP(X0 PC) :" + PC1_ETH1_IP + "\n" \
            + "PC2_ETH1_IP(X1 PC) :" + PC2_ETH0_IP + "\n" \
            + "PC2_ETH1_IP :" + PC2_ETH1_IP + "\n" \
            + "-" * 30
            )
PC2_login = Host(PC2_ETH0_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    platform = os_obj.get_node_platform('UTM')


x1_static_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.DNS1,
    'dns2': Parameter.DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_https': True,
}

pc1_ao_dict = {
    "object_type": "host",
    "name": PC1_ETH1_IP,
    "zone": "LAN",
    "value": PC1_ETH1_IP,
}

syslog_param = {
    "name": PC1_ETH1_IP
}

audit_setting_dict1 = {
    "log": {
        "event": [{
            "id": 1382,
            "name": "Configuration Change Succeeded",
            "category": "Log",
            "group": "Configuration Auditing",
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
            "trap": {
                "redundancy_interval": 0
            },
            "event_profile": {
                "syslog_server_profile": 0
            },
            "ipfix": {
                "redundancy_interval": 60
            },
            "log_digest": True,
            "color": {
                "hex": "0x00FF0000"
            },
            "alert_email": {}
        }]
    }
}

audit_setting_dict2 = {
    "log": {
        "event": [{
            "id": 1383,
            "name": "Configuration Change Failed",
            "category": "Log",
            "group": "Configuration Auditing",
            "priority_level": "alert",
            "log_monitor": {
                "redundancy_interval": 0
            },
            "email_alert": {},
            "syslog": {
                "redundancy_interval": 0
            },
            "trap": {
                "redundancy_interval": 0
            },
            "event_profile": {
                "syslog_server_profile": 0
            },
            "ipfix": {
                "redundancy_interval": 60
            },
            "log_digest": False,
            "color": {
                "hex": "0x00FF0000"
            },
            "alert_email": {}
        }]
    }
}

snmp_dict = {
    "snmp": {
        "enable": True,
        "system_name": "sonicwall",
        "get_community_name": "public",
        "trap_community_name": "public",
        "host_1": PC2_ETH1_IP,
        "host_2": "",
        "host_3": "",
        "host_4": "",
        "system_contact": "",
        "system_location": "",
    }
}

x3_vlan1_dict = {
    'if': 'X3',
    'type': 'vlan',
    'vlan_tag': 15,
    'zone': 'WAN',
    'mode': 'static',
    'ip': "192.168.166.167",
    'netmask': '255.255.255.0',
    'gateway': "192.168.166.168",
    'dns1': Parameter.DNS1,
    'dns2': Parameter.DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_https': True,
}

# Instantiate objects including API,CLI
console_info = os_obj.get_console_info(dut='UTM')

fw_api = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
interface_api = network.InterfaceIPv4Api(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
license_cli = LicenseCli(fw_cli)
snmp_api = system.SNMPApi(fw_api)
logsetting_api = log.LogSettingsApi(fw_api)
log_api = log.LogMonitorApi(fw_api)
audit_log_api = log.AuditlogMonitorApi(fw_api)
ao_api = network.AddressobjectsApi(fw_api)

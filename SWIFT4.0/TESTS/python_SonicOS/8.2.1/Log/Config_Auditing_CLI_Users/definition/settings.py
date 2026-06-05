import os
import sys
import re
import time
import datetime
import unittest
import paramunittest
from networkdevice import Host
from runner.settings import Params, logger
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test, skip_if_dts, repeat_method


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Users")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Users/testcases")

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_CLI_Users/testplan/Config_Auditing_CLI_Users.json'

from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from lib.modules.CLI.dpissl import ClientSslCli
from lib.modules.API import log, network, system
from util.enhancedinfo import show_testcase_info
from lib.modules.CLI.system import LicenseCli, AdminCli

os_obj = Openstack(Params.testbed)

PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH1_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC', 'eth1')
PC2_ETH3_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC', 'eth3')

logger.info("\n" + "-" * 30 + "\n" \
            + "PC1_ETH0_IP(X0 PC) :" + PC1_ETH0_IP + "\n" \
            + "PC2_ETH1_IP(X1 PC) :" + PC2_ETH1_IP + "\n" \
            + "PC2_ETH3_IP :" + PC2_ETH3_IP + "\n" \
            + "-" * 30
            )
            
PC2_login = Host(PC2_ETH3_IP)

IP_sslvpn_ao_dict = '2.2.2.100'
IP_syslog_ao_dict = '192.168.168.100'


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    MASK = '255.255.255.0'
    PC1_GW = '192.168.2.1'
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

x2_static_dict = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': '14.1.1.1',
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_https': True,
}

lan_ao_dict = {
    "object_type": "host",
    "name": PC1_ETH0_IP,
    "zone": "LAN",
    "value": PC1_ETH0_IP,
}

sslvpn_ao_dict = {
    "object_type": "host",
    "name": "test_09",
    "zone": "SSLVPN",
    "value": IP_sslvpn_ao_dict,
}

syslog_ao_dict = {
    "object_type": "host",
    "name": 'test_syslog',
    "zone": "LAN",
    "value": IP_syslog_ao_dict
}

vpn_ao_dict = {
    "object_type": "network",
    "name": "remote_vpn_net",
    "zone": "VPN",
    "value": "22.22.22.0,255.255.255.0"
}

syslog_param = {
    "name": PC1_ETH0_IP
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

# parameters on the test case
added_radius_server = "Added 'Radius Server IP Address'"
deleted_radius_server = "Deleted 'Radius Server IP Address'"
added_ldap_server = "Added 'LDAP server name/address'"
deleted_ldap_server = "Deleted 'LDAP server name/address'"
added_sso_agent = "Added 'SSO Authentication Agent Host name / IP address'"
deleted_sso_agent = "Deleted 'SSO Authentication Agent Host name / IP address'"
added_tacacs_server = "Added 'Tacacs Server IP Address'"
deleted_tacacs_server = "Deleted 'Tacacs Server IP Address'"
added_sso_ts_agent = "Added 'SSO Terminal Service Host name / IP address'"
added_sso_ra_client = "Added 'RADIUS Accounting Host name / IP address'"
added_sso_tp_client = "Added 'Host name / IP address'"
added_radius_acct_server = "Added 'Radius Accounting Server IP Address'"
added_tacacs_acct_server = "Added 'Tacacs Accounting Server IP Address'"
added_local_user = "Added 'User Object'"
deleted_local_user = "Deleted 'User Object'"
added_local_group = "Added 'User Group Object'"
added_guest_profile = "'Name of the Guest Profile"
added_guest_accounts = "Added 'User Object'"
deleted_guest_accounts = "Deleted 'User Object'"
generate_guest_accounts = "Generate Guest Accounts"
export_guest_accounts = "Export Guest Accounts Via SCP"
logout_users = "Logout All Users"
logout_guests = "Logout All Guests"
added_auth_part = "'Auth Partition Name'"
added_part_policy = "'Authentication partition'"

# Instantiate objects including API,CLI
console_info = os_obj.get_console_info(dut='UTM')

G_NEW_PASSWORD = Params.G_NEW_PASSWORD
fw_api = Firewall(Parameter.FIREWALL, user='admin', password=G_NEW_PASSWORD, supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password=G_NEW_PASSWORD, supported_config_mode='cli-ssh')

admini_cli = AdminCli(fw_cli)
license_cli = LicenseCli(fw_cli)
snmp_api = system.SNMPApi(fw_api)
dpissl_obj = ClientSslCli(fw_cli)
log_api = log.LogMonitorApi(fw_api)
status_api = system.StatusApi(fw_api)
ao_api = network.AddressobjectsApi(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
logsetting_api = log.LogSettingsApi(fw_api)
audit_log_api = log.AuditlogMonitorApi(fw_api)
interface_api = network.InterfaceIPv4Api(fw_api)

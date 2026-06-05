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
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Selected/testcases")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Selected")
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_CLI_Selected/testplan/Config_Auditing_CLI_Selected.json'

from lib.modules.API import log,network,system
from lib.modules.CLI.system import LicenseCli,AdminCli
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from lib.modules.CLI.dpissl import ClientSslCli


os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC2_ETH1_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth1')
PC2_ETH3_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth3')
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
            "name":PC1_ETH0_IP
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
            "log_digest": False ,
            "color": {
                "hex": "0x00FF0000"
            },
            "alert_email": {}
        }]
    }
}



snmp_dict = {
            "snmp":{
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

# paramenters on the test case
check_info_dict = {
    'tc1_disablesyslog': ["'IPv6 Visibility'.*?changed from \[enabled\].*?changed to \[disabled\]",
                         "'Wireless LAN Visibility'.*?changed from \[enabled\].*?changed to \[disabled\]"],
    'tc1_disableauditlog': ["'IPv6 Visibility'.*?enabled.*?disabled",
                           "'Wireless LAN Visibility'.*?enabled.*?disabled"],
    'tc1_disablelog': ["'Wireless LAN Visibility'.*?enabled.*?disabled",
                       "'Wireless LAN Visibility'.*?enabled.*?disabled"],
    'tc1_disablesnmplog': ["'IPv6 Visibility'.*?changed from \[enabled\].*?changed to \[disabled\]",
                          "'Wireless LAN Visibility'.*?changed from \[enabled\].*?changed to \[disabled\]"],
    'tc1_enablesyslog': ["'IPv6 Visibility'.*?changed from \[disabled\].*?changed to \[enabled\]",
                         "'Wireless LAN Visibility'.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc1_enableauditlog': ["'IPv6 Visibility'.*?disabled.*?enabled",
                           "'Wireless LAN Visibility'.*?disabled.*?enabled"],
    'tc1_enablelog': ["'Wireless LAN Visibility'.*?enabled.*?disabled",
                    "'Wireless LAN Visibility'.*?enabled.*?disabled"],
    'tc1_enablesnmplog': ["'IPv6 Visibility'.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc1_2enablesnmplog': ["'Wireless LAN Visibility'.*?changed from \[disabled\].*?changed to \[enabled\]"],

    'tc2_enablesyslog': ["'Enable SSL'.*?changed from \[disabled\].*?changed to \[enabled\]",
            "'SSL Inspect Client AppFw'.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc2_enableauditlog': ["'Enable SSL'.*?disabled.*?enabled",
            "'SSL Inspect Client AppFw'.*?disabled.*?enabled"],
    'tc2_enablelog': ["'Enable SSL'.*?changed from \[disabled\].*?changed to \[enabled\]",
            "'SSL Inspect Client AppFw'.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc2_enablesnmplog': ["'Enable SSL'.*?changed from \[disabled\].*?changed to \[enabled\]",
            "'SSL Inspect Client AppFw'.*?changed from \[disabled\].*?changed to \[enabled\]"],

    'tc2_disablesyslog': ["'Enable SSL'.*?changed from \[enabled\].*?changed to \[disabled\]",
            "'SSL Inspect Client AppFw'.*?changed from \[enabled\].*?changed to \[disabled\]"],
    'tc2_disableauditlog': ["'Enable SSL'.*?enabled.*?disabled",
            "'SSL Inspect Client AppFw'.*?enabled.*?disabled"],
    'tc2_disablelog': ["'Enable SSL'.*?changed from \[enabled\].*?changed to \[disabled\]",
            "'SSL Inspect Client AppFw'.*?changed from \[enabled\].*?changed to \[disabled\]"],
    'tc2_disablesnmplog': ["'Enable SSL'.*?changed from \[enabled\].*?changed to \[disabled\]",
            "'SSL Inspect Client AppFw'.*?changed from \[enabled\].*?changed to \[disabled\]"],

    'tc3_syslog_check': ["VPNpolicy_TunnelInterPreshared"],
    'tc3_auditlog_check': ["VPN.*?VPNpolicy_TunnelInterPreshared"],
    'tc3_log_check': ["Configuration succeeded.*?VPNpolicy_TunnelInterPreshared"],
    'tc3_snmplog_check': ["IPsec Name.*?VPNpolicy_TunnelInterPreshared"],

    'tc4_syslog_check': ["VPNpolicy_AutoProvisioningClient"],
    'tc4_auditlog_check': ["VPNpolicy_AutoProvisioningClient"],
    'tc4_log_check': ["Configuration succeeded.*?VPNpolicy_AutoProvisioningClient"],
    'tc4_snmplog_check': ["IPsec Name.*?VPNpolicy_AutoProvisioningClient"],

    'tc5_syslog_check': ["Added 'Radius Server IP Address'",
                          "Deleted 'Radius Server IP Address'"],
    'tc5_auditlog_check': ["Added 'Radius Server IP Address'",
                          "Deleted 'Radius Server IP Address'"],
    'tc5_log_check': ["Added 'Radius Server IP Address'",
                          "Deleted 'Radius Server IP Address'"],
    'tc5_snmplog_check': ["Added 'Radius Server IP Address'",
                          "Deleted 'Radius Server IP Address'"],
                          
    'tc6_syslog_check': ["'Radius Server IP Address'.*changed from \[10.10.10.10\].*?changed to \[10.10.10.9\]"],
    'tc6_auditlog_check': ["'Radius Server IP Address'.*?10.10.10.10.*?10.10.10.9"],
    'tc6_log_check': ["'Radius Server IP Address'.*changed from \[10.10.10.10\].*?changed to \[10.10.10.9\]"],
    'tc6_snmplog_check': ["'Radius Server IP Address'.*changed from \[10.10.10.10\].*?changed to \[10.10.10.9\]"],

    'tc7_syslog_check': ["'Enable SSLVPN Access'.*?LAN.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc7_auditlog_check': ["LAN.*?'Enable SSLVPN Access'.*?disabled.*?enabled"],
    'tc7_log_check': ["'Enable SSLVPN Access'.*?LAN.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc7_snmplog_check': ["'Enable SSLVPN Access'.*?LAN.*?changed from \[disabled\].*?changed to \[enabled\]"],

    'tc8_syslog_check': ["'SSL VPN Bookmark Service Name'.*?test.*?changed to \[test\]",
                          "'SSL VPN RDP Server IP'.*?test.*?changed to \[10.10.10.10\]",
                          "'SSL VPN RDP Service Type'.*?test.*?changed to \[SSHv2.*?\]"],
    'tc8_auditlog_check': ["'SSL VPN Bookmark Service Name'.*?test",
                          "'SSL VPN RDP Server IP'.*?10.10.10.10",
                          "'SSL VPN RDP Service Type'.*?SSHv2"],
    'tc8_log_check': ["'SSL VPN Bookmark Service Name'.*?test.*?changed to \[test\]",
                          "'SSL VPN RDP Server IP'.*?test.*?changed to \[10.10.10.10\]",
                          "'SSL VPN RDP Service Type'.*?test.*?changed to \[SSHv2.*?\]"],
    'tc8_snmplog_check': ["'SSL VPN Bookmark Service Name'.*?test.*?changed to \[test\]",
                          "'SSL VPN RDP Server IP'.*?test.*?changed to \[10.10.10.10\]",
                          "'SSL VPN RDP Service Type'.*?test.*?changed to \[SSHv2.*?\]"],

    'tc9_syslog_check': ["Deleted 'Policy Action'.*?Deny 'Any' from 'Any' to 'Any'.*?changed from \[Deny 'Any' from 'Any' to 'Any'\]"],
    'tc9_auditlog_check': ["Deleted 'Policy Action'.*?Deny 'Any' from 'Any' to 'Any'"],
    'tc9_log_check': ["Rule Deleted.*?Deny 'Any' from 'Any' to 'Any'Security Policy deleted"],
    'tc9_snmplog_check': ["Deleted 'Policy Action'.*?Deny 'Any' from 'Any' to 'Any'.*?changed from \[Deny 'Any' from 'Any' to 'Any'\]"],

    'tc10_syslog_check': ["'Application Firewall object name'.*?testmatchobject.*?changed to \[testmatchobject\]",
                          "'Application Firewall object type'.*?testmatchobject.*?changed to \[Email To\]",
                          "'Application Firewall Object Key'.*?testmatchobject.*?changed to \[abc\]"],
    'tc10_auditlog_check': ["'Application Firewall object name'.*?testmatchobject",
                          "'Application Firewall object type'.*?Email To",
                          "'Application Firewall Object Key'.*?abc"],
    'tc10_log_check': ["'Application Firewall object name'.*?testmatchobject.*?changed to \[testmatchobject\]",
                          "'Application Firewall object type'.*?testmatchobject.*?changed to \[Email To\]",
                          "'Application Firewall Object Key'.*?testmatchobject.*?changed to \[abc\]"],
    'tc10_snmplog_check': ["'Application Firewall object name'.*?testmatchobject.*?changed to \[testmatchobject\]",
                          "'Application Firewall object type'.*?testmatchobject.*?changed to \[Email To\]",
                          "'Application Firewall Object Key'.*?testmatchobject.*?changed to \[abc\]"],

    'tc11_syslog_check': ["Added 'Schedule Object'.*?testSystemSchedules.*?changed to \[testSystemSchedules\]",
                           "'The start year for onetime schedule'.*?testSystemSchedules.*?changed to \[2024\]",
                           "'The end year for onetime schedule'.*?testSystemSchedules.*?changed to \[2024\]",
                           "The start month for onetime schedule'.*?testSystemSchedules.*?changed to \[August\]",
                           "The end month for onetime schedule'.*?testSystemSchedules.*?changed to \[August\]",
                           "'The start day for onetime schedule'.*?testSystemSchedules.*?changed to \[1\]",
                           "'The end day for onetime schedule'.*?testSystemSchedules.*?changed to \[2\]"
                           ],
    'tc11_auditlog_check': ["Added 'Schedule Object'.*?testSystemSchedules",
                           "testSystemSchedules.*?'The start year for onetime schedule'.*?2024",
                           "testSystemSchedules.*?'The end year for onetime schedule'.*?2024",
                           "testSystemSchedules.*?'The start month for onetime schedule'.*?August",
                           "testSystemSchedules.*?'The end month for onetime schedule'.*?August",                
                           "testSystemSchedules.*?'The start day for onetime schedule'.*?1",
                           "testSystemSchedules.*?'The end day for onetime schedule'.*?2",
                           ],
    'tc11_log_check': ["Added 'Schedule Object'.*?testSystemSchedules.*?changed to \[testSystemSchedules\]",
                           "'The start year for onetime schedule'.*?testSystemSchedules.*?changed to \[2024\]",
                           "'The end year for onetime schedule'.*?testSystemSchedules.*?changed to \[2024\]",
                           "The start month for onetime schedule'.*?testSystemSchedules.*?changed to \[August\]",
                           "The end month for onetime schedule'.*?testSystemSchedules.*?changed to \[August\]",
                           "'The start day for onetime schedule'.*?testSystemSchedules.*?changed to \[1\]",
                           "'The end day for onetime schedule'.*?testSystemSchedules.*?changed to \[2\]"
                           ],
    'tc11_snmplog_check': ["Added 'Schedule Object'.*?testSystemSchedules.*?changed to \[testSystemSchedules\]",
                           "'The start year for onetime schedule'.*?testSystemSchedules.*?changed to \[2024\]",
                           "'The end year for onetime schedule'.*?testSystemSchedules.*?changed to \[2024\]",
                           "The start month for onetime schedule'.*?testSystemSchedules.*?changed to \[August\]",
                           "The end month for onetime schedule'.*?testSystemSchedules.*?changed to \[August\]",
                           "'The start day for onetime schedule'.*?testSystemSchedules.*?changed to \[1\]",
                           "'The end day for onetime schedule'.*?testSystemSchedules.*?changed to \[2\]"
                           ],
    'tc12_syslog_check': ["'IP Helper Comment'.*?changed from \[new_add_policy\].*?changed to \[new_add_policy111\]"],
    'tc12_auditlog_check': ["'IP Helper Comment'.*?new_add_policy.*?new_add_policy111"],
    'tc12_log_check': ["'IP Helper Comment'.*?changed from \[new_add_policy\].*?changed to \[new_add_policy111\]"],
    'tc12_snmplog_check': ["'IP Helper Comment'.*?changed from \[new_add_policy\].*?changed to \[new_add_policy111\]"],
}

#Instantiate objects including API,CLI
console_info = os_obj.get_console_info(dut='UTM')

fw_api = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
ao_api = network.AddressobjectsApi(fw_api) 
interface_api = network.InterfaceIPv4Api(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
license_cli = LicenseCli(fw_cli)
snmp_api = system.SNMPApi(fw_api)
logsetting_api = log.LogSettingsApi(fw_api)
log_api = log.LogMonitorApi(fw_api)
audit_log_api = log.AuditlogMonitorApi(fw_api)


admini_cli = AdminCli(fw_cli)
dpissl_obj = ClientSslCli(fw_cli)
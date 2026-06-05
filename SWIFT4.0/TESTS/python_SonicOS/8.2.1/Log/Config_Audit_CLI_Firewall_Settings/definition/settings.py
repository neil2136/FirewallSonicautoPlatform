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

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall

# import form branch lib contents for test suit
from lib.modules.API.network import AddressobjectsApi, InterfaceIPv4Api
from lib.modules.API.log import SyslogSettingsApi, LogMonitorApi, AuditlogMonitorApi, LogSettingsApi
from lib.modules.API.system import SNMPApi
from lib.modules.CLI.system import LicenseCli, AdminCli
from lib.modules.CLI.firewallsettings import AdvancedCli, FloodprotectionCli, QosmappingCli, SslcontrolCli, CiphercontrolCli
from lib.modules.CLI.firewall import BandwidthObjectCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Audit_CLI_Firewall_Settings/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
CONFS_PATH = suite_path + 'definition/confs/'
TESTPLAN = suite_path + 'testplan/Config_Audit_CLI_Firewall_Settings.json'

# Instantiate objects including common_lib import
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


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    MASK = '255.255.255.0'
    PC1_GW = '192.168.2.1'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


# Instantiate objects including API,CLI
fw = Firewall(Parameter.FIREWALL, user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='cli-ssh')
ao_api = AddressobjectsApi(fw)
interface_api = InterfaceIPv4Api(fw)
syslog_api = SyslogSettingsApi(fw)
snmp_api = SNMPApi(fw)
logsetting_api = LogSettingsApi(fw)
log_api = LogMonitorApi(fw)
audit_log_api = AuditlogMonitorApi(fw)

license_cli = LicenseCli(fw_cli)
advanced_cli = AdvancedCli(fw_cli)
bwobject_cli = BandwidthObjectCli(fw_cli)
floodprotection_cli = FloodprotectionCli(fw_cli)
qosmapping_cli = QosmappingCli(fw_cli)
sslcontrol_cli = SslcontrolCli(fw_cli)
ciphercontrol_cli = CiphercontrolCli(fw_cli)

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
}

lan_ao_dict = {
    "object_type": "host",
    "name": PC1_ETH0_IP,
    "zone": "LAN",
    "value": PC1_ETH0_IP,
}
syslog_ao_dict = {
    "object_type": "host",
    "name": 'test_syslog',
    "zone": "LAN",
    "value": '192.168.168.100'
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
relay_policy_dict = {
    'name': 'auto_policy_test01',
    'protocol': 'DHCP',
    'from': 'X0',
    'to': 'name "X1 IP"',
}

# paramenters on the test case
check_info_dict = {
    'tc30_syslog_check': ["Enable UDP Flood Protection For IPv6.*?disabled.*?enabled"],
    'tc30_auditlog_check': ["Enable UDP Flood Protection For IPv6.*?disabled.*?enabled"],
    'tc30_log_check': ["Enable UDP Flood Protection For IPv6.*?disabled.*?enabled"],
    'tc30_snmplog_check': ["Enable UDP Flood Protection For IPv6.*?disabled.*?enabled"],
    'tc37_syslog_check': ["Enable ICMP Flood Protection For IPv6.*?disabled.*?enabled"],
    'tc37_auditlog_check': ["Enable ICMP Flood Protection For IPv6.*?disabled.*?enabled"],
    'tc37_log_check': ["Enable ICMP Flood Protection For IPv6.*?disabled.*?enabled"],
    'tc37_snmplog_check': ["Enable ICMP Flood Protection For IPv6.*?disabled.*?enabled"],
    'tc72_syslog_check': ["Wiremode Vlan configuration.*?X3/666/X4/777"],
    'tc72_auditlog_check': ["Wiremode Vlan configuration.*?X3/666/X4/777"],
    'tc72_log_check': ["Wiremode Vlan configuration.*?X3/666/X4/777"],
    'tc72_snmplog_check': ["Wiremode Vlan configuration.*?X3/666/X4/777"],
    'tc74_syslog_check': ["Deleted 'Wiremode Vlan configuration Source Interface.*?X3/666/X4/777"],
    'tc74_auditlog_check': ["Deleted 'Wiremode Vlan configuration Source Interface.*?X3/666/X4/777"],
    'tc74_log_check': ["Deleted 'Wiremode Vlan configuration Source Interface.*?X3/666/X4/777"],
    'tc74_snmplog_check': ["Deleted 'Wiremode Vlan configuration Source Interface.*?X3/666/X4/777"],
    'tc01_syslog_check': ["Randomize IP ID.*?disabled.*?enabled",
                          "Decrement IP TTL for forwarded traffic.*?disabled.*?enabled",
                          "'Enable Stealth Mode.*?disabled.*?enabled",
                          ],
    'tc01_auditlog_check': ["'Randomize IP ID.*?disabled.*?enabled",
                            "'Decrement IP TTL for forwarded traffic.*?disabled.*?enabled",
                            "'Enable Stealth Mode.*?disabled.*?enabled",
                            ],
    'tc01_log_check': ["'Randomize IP ID.*?disabled.*?enabled",
                       "'Decrement IP TTL for forwarded traffic.*?disabled.*?enabled",
                       "'Enable Stealth Mode.*?disabled.*?enabled",
                       ],
    'tc01_snmplog_check': ["'Randomize IP ID.*?disabled.*?enabled",
                           "'Decrement IP TTL for forwarded traffic.*?disabled.*?enabled",
                           "'Enable Stealth Mode.*?disabled.*?enabled",
                           ],
    'tc61_syslog_check': ["'Enable FTP Transformations for TCP port\(s\) in Service Object.*?FTP.*?Telnet"],
    'tc61_auditlog_check': ["'Enable FTP Transformations for TCP port\(s\) in Service Object.*?FTP.*?Telnet"],
    'tc61_log_check': ["'Enable FTP Transformations for TCP port\(s\) in Service Object.*?FTP.*?Telnet"],
    'tc61_snmplog_check': ["'Enable FTP Transformations for TCP port\(s\) in Service Object.*?FTP.*?Telnet"],
    'tc16_syslog_check': ["'Bandwidth Object Guaranteed Bandwidth.*?changed from \[0\].*?changed to \[123\]"],
    'tc16_auditlog_check': ["'Bandwidth Object Guaranteed Bandwidth.*?0.*?123"],
    'tc16_log_check': ["'Bandwidth Object Guaranteed Bandwidth.*?changed from \[0\].*?changed to \[123\]"],
    'tc16_snmplog_check': ["'Bandwidth Object Guaranteed Bandwidth.*?changed from \[0\].*?changed to \[123\]"],
    'tc18_syslog_check': ["'Bandwidth Object Maximum Bandwidth.*?changed from \[20\].*?changed to \[456\]"],
    'tc18_auditlog_check': ["'Bandwidth Object Maximum Bandwidth.*?20.*?456"],
    'tc18_log_check': ["'Bandwidth Object Maximum Bandwidth.*?changed from \[20\].*?changed to \[456\]"],
    'tc18_snmplog_check': ["'Bandwidth Object Maximum Bandwidth.*?changed from \[20\].*?changed to \[456\]"],
    'tc20_syslog_check': ["'Bandwidth Object Maximum Bandwidth.*?changed from \[20\].*?changed to \[456\]"],
    'tc20_auditlog_check': ["'Bandwidth Object Maximum Bandwidth.*?20.*?456"],
    'tc20_log_check': ["'Bandwidth Object Maximum Bandwidth.*?changed from \[20\].*?changed to \[456\]"],
    'tc20_snmplog_check': ["'Bandwidth Object Maximum Bandwidth.*?changed from \[20\].*?changed to \[456\]"],
    'tc25_syslog_check': ["Clear TCP Stats"],
    'tc25_auditlog_check': ["Clear TCP Stats"],
    'tc25_log_check': ["Clear TCP Stats"],
    'tc25_snmplog_check': ["Clear TCP Stats"],
    'tc45_syslog_check': ["'QOS DSCP priority.*?changed from \[0.*?changed to \[4",
                          "'QOS DSCP Range Begin.*?changed from \[0.*?changed to \[5",
                          "'QOS DSCP Range End.*?changed from \[7.*?changed to \[6",
                          ],
    'tc45_auditlog_check': ["'QOS DSCP priority",
                            "'QOS DSCP Range Begin",
                            "'QOS DSCP Range End",
                            ],
    'tc45_log_check': ["'QOS DSCP priority.*?changed from \[0.*?changed to \[4",
                       "'QOS DSCP Range Begin.*?changed from \[0.*?changed to \[5",
                       "'QOS DSCP Range End.*?changed from \[7.*?changed to \[6",
                       ],
    'tc45_snmplog_check': ["'QOS DSCP priority.*?changed from \[0.*?changed to \[4",
                           "'QOS DSCP Range Begin.*?changed from \[0.*?changed to \[5",
                           "'QOS DSCP Range End.*?changed from \[7.*?changed to \[6",
                           ],
    'tc47_syslog_check': ["QoS Covert To Default Settigns"],
    'tc47_auditlog_check': ["QoS Covert To Default Settigns"],
    'tc47_log_check': ["QoS Covert To Default Settigns"],
    'tc47_snmplog_check': ["QoS Covert To Default Settigns"],
    'tc48_syslog_check': ["'Enable SSL Control.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc48_auditlog_check': ["'Enable SSL Control.*?disabled.*?enabled"],
    'tc48_log_check': ["'Enable SSL Control.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc48_snmplog_check': ["'Enable SSL Control.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc49_syslog_check': ["'Action on SSL policy violation.*?changed from \[Block the connection and log the "
                          "event\].*?changed to \[Log the event\]"],
    'tc49_auditlog_check': ["'Action on SSL policy violation.*?Block the connection and log the event.*?Log the event"],
    'tc49_log_check': ["'Action on SSL policy violation.*?changed from \[Block the connection and log the "
                       "event\].*?changed to \[Log the event\]"],
    'tc49_snmplog_check': ["'Action on SSL policy violation.*?changed from \[Block the connection and log the "
                           "event\].*?changed to \[Log the event\]"],
    'tc51_syslog_check': ["'SSL Control Certificate Black List.*?changed to \[auto_black_test\]"],
    'tc51_auditlog_check': ["'SSL Control Certificate Black List.*?auto_black_test"],
    'tc51_log_check': ["'SSL Control Certificate Black List.*?changed to \[auto_black_test\]"],
    'tc51_snmplog_check': ["'SSL Control Certificate Black List.*?changed to \[auto_black_test\]"],
    'tc55_syslog_check': ["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"],
    'tc55_auditlog_check': ["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"],
    'tc55_log_check': ["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"],
    'tc55_snmplog_check': ["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"],

}

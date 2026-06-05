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
from lib.modules.CLI.network import IpHelperCli, WebproxyCli, DDNSCli, NetworkMonitorCli
from modules.CLI.objects import MatchObjectsDynamicGroupCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Audit_CLI_Network_Part2/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
CONFS_PATH = suite_path + 'definition/confs/'
TESTPLAN = suite_path + 'testplan/Config_Audit_CLI_Network_Part2.json'

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
fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
ao_api = AddressobjectsApi(fw)
interface_api = InterfaceIPv4Api(fw)
syslog_api = SyslogSettingsApi(fw)
snmp_api = SNMPApi(fw)
logsetting_api = LogSettingsApi(fw)
log_api = LogMonitorApi(fw)
audit_log_api = AuditlogMonitorApi(fw)

license_cli = LicenseCli(fw_cli)
admin_cli = AdminCli(fw_cli)
iphelper_cli = IpHelperCli(fw_cli)
webproxy_cli = WebproxyCli(fw_cli)
ddns_cli = DDNSCli(fw_cli)
networkmonitor_cli = NetworkMonitorCli(fw_cli)
MatchObjectsDynamicGroup_cli = MatchObjectsDynamicGroupCli(fw_cli)

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
    'tc01_syslog_check': ["'Enable IP Helper.*?disabled.*?enabled"],
    'tc01_auditlog_check': ["'Enable IP Helper.*?disabled.*?enabled"],
    'tc01_log_check': ["'Enable IP Helper.*?disabled.*?enabled"],
    'tc01_snmplog_check': ["'Enable IP Helper.*?disabled.*?enabled"],
    'tc02_syslog_check': ["'IP Helper Application Name.*?auto_pro_v4",
                          "'IP Helper UDP Port 1.*?auto_pro_v4.*?30",
                          "'IP Helper UDP Port 2.*?auto_pro_v4.*?40"],
    'tc02_auditlog_check': ["'IP Helper Application Name.*?auto_pro_v4",
                            "'IP Helper UDP Port 1.*?30",
                            "'IP Helper UDP Port 2.*?40"],
    'tc02_log_check': ["'IP Helper Application Name.*?auto_pro_v4",
                       "'IP Helper UDP Port 1.*?auto_pro_v4.*?30",
                       "'IP Helper UDP Port 2.*?auto_pro_v4.*?40"],
    'tc02_snmplog_check': ["'IP Helper Application Name.*?auto_pro_v4",
                           "'IP Helper UDP Port 1.*?auto_pro_v4.*?30",
                           "'IP Helper UDP Port 2.*?auto_pro_v4.*?40"],
    'tc06_syslog_check': ["'IP Helper Protocol Name.*?DHCP",
                          "'IP Helper To Address.*?X1 IP"],
    'tc06_auditlog_check': ["'IP Helper Protocol Name.*?DHCP",
                            "'IP Helper To Address.*?X1 IP"],
    'tc06_log_check': ["'IP Helper Protocol Name.*?DHCP",
                       "'IP Helper To Address.*?X1 IP"],
    'tc06_snmplog_check': ["'IP Helper Protocol Name.*?DHCP",
                           "'IP Helper To Address.*?X1 IP"],
    'tc08_syslog_check': ["'IP Helper To Address.*?X1 IP.*?X2 IP"],
    'tc08_auditlog_check': ["'IP Helper To Address.*?X1 IP.*?X2 IP"],
    'tc08_log_check': ["'IP Helper To Address.*?X1 IP.*?X2 IP"],
    'tc08_snmplog_check': ["'IP Helper To Address.*?X1 IP.*?X2 IP"],
    'tc13_syslog_check': ["'Proxy Web Server Address.*?1.1.1.1",
                          "'Proxy Web Server Port.*?3128"],
    'tc13_auditlog_check': ["'Proxy Web Server Address.*?1.1.1.1",
                            "'Proxy Web Server Port.*?3128"],
    'tc13_log_check': ["'Proxy Web Server Address.*?1.1.1.1",
                       "'Proxy Web Server Port.*?3128"],
    'tc13_snmplog_check': ["'Proxy Web Server Address.*?1.1.1.1",
                           "'Proxy Web Server Port.*?3128"],
    'tc15_syslog_check': ["Added 'Proxy server name.*?2.2.2.2"],
    'tc15_auditlog_check': ["Added 'Proxy server name.*?2.2.2.2"],
    'tc15_log_check': ["Added 'Proxy server name.*?2.2.2.2"],
    'tc15_snmplog_check': ["Added 'Proxy server name.*?2.2.2.2"],
    'tc20_syslog_check': ["'Profile Name.*?auto_test01",
                          "'Provider Name.*?dyn.com",
                          "'DDNS User Name.*?automation",
                          "'User Password.*?changed to",
                          "'Domain Name.*?test.dyn.com"],
    'tc20_auditlog_check': ["'Profile Name.*?auto_test01",
                            "'Provider Name.*?dyn.com",
                            "'DDNS User Name.*?automation",
                            "'User Password",
                            "'Domain Name.*?test.dyn.com"],
    'tc20_log_check': ["'Profile Name.*?auto_test01",
                       "'Provider Name.*?dyn.com",
                       "'DDNS User Name.*?automation",
                       "'User Password.*?changed to",
                       "'Domain Name.*?test.dyn.com"],
    'tc20_snmplog_check': ["'Profile Name.*?auto_test01",
                           "'Provider Name.*?dyn.com",
                           "'DDNS User Name.*?automation",
                           "'User Password.*?changed to",
                           "'Domain Name.*?test.dyn.com"],
    'tc24_syslog_check': ["'DDNS User Name.*?test_user01",
                          "'Domain Name.*?test.auto.com"],
    'tc24_auditlog_check': ["'DDNS User Name.*?test_user01",
                            "'Domain Name.*?test.auto.com"],
    'tc24_log_check': ["'DDNS User Name.*?test_user01",
                       "'Domain Name.*?test.auto.com"],
    'tc24_snmplog_check': ["'DDNS User Name.*?test_user01",
                           "'Domain Name.*?test.auto.com"],
    'tc27_syslog_check': ["'Profile Name.*?auto_test02",
                          "'Provider Name.*?dyn.com",
                          "'DDNS User Name.*?root02",
                          "'Domain Name.*?v6.dyn.com"],
    'tc27_auditlog_check': ["'Profile Name.*?auto_test02",
                            "'Provider Name.*?dyn.com",
                            "'DDNS User Name.*?root02",
                            "'Domain Name.*?v6.dyn.com"],
    'tc27_log_check': ["'Profile Name.*?auto_test02",
                       "'Provider Name.*?dyn.com",
                       "'DDNS User Name.*?root02",
                       "'Domain Name.*?v6.dyn.com"],
    'tc27_snmplog_check': ["'Profile Name.*?auto_test02",
                           "'Provider Name.*?dyn.com",
                           "'DDNS User Name.*?root02",
                           "'Domain Name.*?v6.dyn.com"],
    'tc36_syslog_check': ["'Probe Object.*?auto_nm_ping",
                          "'Probe Target.*?X1 IP",
                          "'Probe Gateway.*?X0 IP",
                          "'Probe Interface.*?X1",
                          "'Probe Type.*?PING"],
    'tc36_auditlog_check': ["'Probe Object.*?auto_nm_ping",
                            "'Probe Target.*?X1 IP",
                            "'Probe Gateway.*?X0 IP",
                            "'Probe Interface.*?X1",
                            "'Probe Type.*?PING"],
    'tc36_log_check': ["'Probe Object.*?auto_nm_ping",
                       "'Probe Target.*?X1 IP",
                       "'Probe Gateway.*?X0 IP",
                       "'Probe Interface.*?X1",
                       "'Probe Type.*?PING"],
    'tc36_snmplog_check': ["'Probe Object.*?auto_nm_ping",
                           "'Probe Target.*?X1 IP",
                           "'Probe Gateway.*?X0 IP",
                           "'Probe Interface.*?X1",
                           "'Probe Type.*?PING"],
    'tc43_syslog_check': ["'Probe Gateway.*?X2 IP",
                          "'Probe Type.*?TCP"],
    'tc43_auditlog_check': ["'Probe Gateway.*?X2 IP",
                            "'Probe Type.*?TCP"],
    'tc43_log_check': ["'Probe Gateway.*?X2 IP",
                       "'Probe Type.*?TCP"],
    'tc43_snmplog_check': ["'Probe Gateway.*?X2 IP",
                           "'Probe Type.*?TCP"],
    'tc46_syslog_check': ["'Probe Object.*?auto_nm_tcp_v6",
                          "'Probe Target.*?X1 IPv6 Addresses",
                          "'Probe Type.*?TCP",
                          "'Probe Port V6.*?2345"],
    'tc46_auditlog_check': ["'Probe Object.*?auto_nm_tcp_v6",
                            "'Probe Target.*?X1 IPv6 Addresses",
                            "'Probe Type.*?TCP",
                            "'Probe Port V6.*?2345"],
    'tc46_log_check': ["'Probe Object.*?auto_nm_tcp_v6",
                       "'Probe Target.*?X1 IPv6 Addresses",
                       "'Probe Type.*?TCP",
                       "'Probe Port V6.*?2345"],
    'tc46_snmplog_check': ["'Probe Object.*?auto_nm_tcp_v6",
                           "'Probe Target.*?X1 IPv6 Addresses",
                           "'Probe Type.*?TCP",
                           "'Probe Port V6.*?2345"],
    'tc52_syslog_check': ["Deleted 'Probe Object.*?auto_nm_ping",
                          "Deleted 'Probe Object.*?auto_nm_tcp_v6"],
    'tc52_auditlog_check': ["Deleted 'Probe Object.*?auto_nm_ping",
                            "Deleted 'Probe Object.*?auto_nm_tcp_v6"],
    'tc52_log_check': ["Deleted 'Probe Object.*?auto_nm_ping",
                       "Deleted 'Probe Object.*?auto_nm_tcp_v6"],
    'tc52_snmplog_check': ["Deleted 'Probe Object.*?auto_nm_ping",
                           "Deleted 'Probe Object.*?auto_nm_tcp_v6"],
    'tc63_syslog_check': ["Added 'Dynamic External Group Name.*?autotest01",
                          "'Dynamic External Group Type.*?Address Group",
                          "'Dynamic External Group Protocol.*?FTP",
                          "'Dynamic External Group FTP Server Address.*?10.11.11.11",
                          "'Dynamic External Group FTP user.*?autoroot",
                          "'Dynamic External Group FTP root directory.*?/tmp/test",
                          "'Dynamic External Group File Name.*?autofiles",
                          ],
    'tc63_auditlog_check': ["Added 'Dynamic External Group Name.*?autotest01",
                            "'Dynamic External Group Type.*?Address Group",
                            "'Dynamic External Group Protocol.*?FTP",
                            "'Dynamic External Group FTP Server Address.*?10.11.11.11",
                            "'Dynamic External Group FTP user.*?autoroot",
                            "'Dynamic External Group FTP root directory.*?/tmp/test",
                            "'Dynamic External Group File Name.*?autofiles",
                            ],
    'tc63_log_check': ["Added 'Dynamic External Group Name.*?autotest01",
                       "'Dynamic External Group Type.*?Address Group",
                       "'Dynamic External Group Protocol.*?FTP",
                       "'Dynamic External Group FTP Server Address.*?10.11.11.11",
                       "'Dynamic External Group FTP user.*?autoroot",
                       "'Dynamic External Group FTP root directory.*?/tmp/test",
                       "'Dynamic External Group File Name.*?autofiles",
                       ],
    'tc63_snmplog_check': ["Added 'Dynamic External Group Name.*?autotest01",
                           "'Dynamic External Group Type.*?Address Group",
                           "'Dynamic External Group Protocol.*?FTP",
                           "'Dynamic External Group FTP Server Address.*?10.11.11.11",
                           "'Dynamic External Group FTP user.*?autoroot",
                           "'Dynamic External Group FTP root directory.*?/tmp/test",
                           "'Dynamic External Group File Name.*?autofiles",
                           ],
    'tc64_syslog_check': ["Added 'Dynamic External Group Name.*?autotest02",
                          "'Dynamic External Group Type.*?Address Group",
                          "'Dynamic External Group URL Name.*?https://10.12.12.12",
                          ],
    'tc64_auditlog_check': ["Added 'Dynamic External Group Name.*?autotest02",
                            "'Dynamic External Group Type.*?Address Group",
                            "'Dynamic External Group URL Name.*?https://10.12.12.12",
                            ],
    'tc64_log_check': ["Added 'Dynamic External Group Name.*?autotest02",
                       "'Dynamic External Group Type.*?Address Group",
                       "'Dynamic External Group URL Name.*?https://10.12.12.12",
                       ],
    'tc64_snmplog_check': ["Added 'Dynamic External Group Name.*?autotest02",
                           "'Dynamic External Group Type.*?Address Group",
                           "'Dynamic External Group URL Name.*?https://10.12.12.12",
                           ],
}

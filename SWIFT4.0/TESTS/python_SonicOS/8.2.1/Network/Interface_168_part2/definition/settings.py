import os
import re
import sys
import copy
import time
import unittest
import paramunittest
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall

# import form branch lib contents for test suit
from lib.modules.API.network import *
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.system import *
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.users import UsersettingApi, UserLocalApi
from lib.modules.API.log import AuditlogMonitorApi
from modules.API.log import LogMonitorApi, LogSettingsApi


# import form test suite root path like definition
suite_path = (
    os.environ["PYTHON_SONICOS_HOME"] + "/Network/Interface_168_part2/"
)
sys.path.append(suite_path)
sys.path.append(suite_path + "testcases")
TESTPLAN = suite_path + "testplan/Interface.json"
SCRIPTS_PATH = suite_path + 'definition/scripts'
CONF_PATH = suite_path + 'definition/conf'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC1_ETH1_NW = os_obj.get_node_interface_network('PC1', 'eth1')
PC2_ETH1_NW = os_obj.get_node_interface_network('PC2', 'eth1')
PC4_ETH1_NW = os_obj.get_node_interface_network('PC4', 'eth1')
PC5_ETH1_NW = os_obj.get_node_interface_network('PC5', 'eth1')
PC3_ETH1_NW = os_obj.get_node_interface_network('PC3', 'eth1')
logger.info('\n' + '-' * 30 + '\n'
            + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n'
            + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n'
            + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n'
            + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n'
            + 'PC4_ETH0_IP :' + PC4_ETH0_IP + '\n'
            + 'PC4_ETH1_IP :' + PC4_ETH1_IP + '\n'
            + 'PC3_ETH0_IP :' + PC3_ETH0_IP + '\n'
            + 'PC3_ETH1_IP :' + PC3_ETH1_IP + '\n'
            + 'PC5_ETH0_IP :' + PC5_ETH0_IP + '\n'
            + 'PC5_ETH1_IP :' + PC5_ETH1_IP + '\n'
            + '-' * 30
            )
localhost = Host('localhost')
pc1_ssh = Host(PC1_ETH0_IP, user='root', password='password')
pc2_ssh = Host(PC2_ETH0_IP, user='root', password='password')
pc4_ssh = Host(PC4_ETH0_IP, user='root', password='password')
pc3_ssh = Host(PC3_ETH0_IP, user='root', password='password')
pc5_ssh = Host(PC5_ETH0_IP, user='root', password='password')

# parameters on the fw
class Parameter():
    FIREWALL = '192.168.168.168'
    fwStat_dict = {}
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '12.12.1.168'
    X1_DHCP_IP = ''
    X1_PPP_IP = ''
    X1_PPP_IP_DHCP = ''
    X1_PPPOE_IP_SERVER = '192.168.100.168'
    X1_GW = '12.12.1.1'
    X2_IP = '192.168.2.168'
    X2_GW = '192.168.2.1'
    X3_IP = '12.12.2.168'
    X3_DHCP_IP = ''
    X3_PPP_IP = ''
    X3_PPP_IP_DHCP = ''
    X3_PPPOE_IP_SERVER = '192.168.200.168'
    X3_GW = '12.12.2.1'
    X4_IP = '192.168.4.168'
    X4_GW = '192.168.4.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X0_IPv6 = '1001:1::168'
    X1_IPv6 = '2001:100::168'
    X2_IPv6 = '1001:2::168'
    PC1_ETH0 = PC1_ETH0_IP
    PC1_ETH1 = PC1_ETH1_IP
    PC2_ETH0 = PC2_ETH0_IP
    PC2_ETH1 = PC2_ETH1_IP
    PC2_ETH1_portshield = '192.168.4.20'
    PC2_ETH1_l2bridge = '12.12.2.20'
    PC4_ETH0 = PC4_ETH0_IP
    PC4_ETH1 = PC4_ETH1_IP
    PC3_ETH0 = PC3_ETH0_IP
    PC3_ETH1 = PC3_ETH1_IP
    PC3_ETH1_l2bridge = '192.168.2.211'
    PC5_ETH0 = PC5_ETH0_IP
    PC5_ETH1 = PC5_ETH1_IP
    lan_host1 = '1001:1::10'
    lan_host2 = '1001:2::20'
    lan_host1_if = 'eth1'
    wan_ip = '2001:100::40'
    wan_host1 = '2001:1::100'
    wan_host1_if = 'eth1'
    MIB_PATH = '/usr/share/snmp/'
    http_login_url = 'http://192.168.168.168/sonicui/7/login/'
    https_login_url = 'https://192.168.168.168/sonicui/7/login/'

# Instantiate objects including API,CLI import
fw = Firewall(Parameter.FIREWALL, user='admin', password='password',
              supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto',
                  supported_config_mode='cli-ssh')

license_obj = LicenseCli(fw_cli)
admin_obj = AdminApi(fw)
user_obj = UsersettingApi(fw)
failoverlb_obj = FailoverLbApi(fw)
interface_obj = InterfaceIPv4Api(fw)
interface_obj_v6 = InterfaceIPv6Api(fw)
address_obj = AddressobjectsApi(fw)
nat_obj = NatpolicyApi(fw)
restart_obj = RestartApi(fw)
setting_obj = SettingApi(fw)
interfacecli_obj = InterfaceCli(fw_cli)
packetmonitor_obj = PacketmonitorApi(fw)
diag_obj = DiagnosticApi(fw)
userlocal_obj = UserLocalApi(fw)
audit_obj = AuditlogMonitorApi(fw)
log_obj = LogMonitorApi(fw)
logsetting_obj = LogSettingsApi(fw)
snmp_obj = SNMPApi(fw)
status_obj = StatusApi(fw)
zone_obj = ZoneObjectsApi(fw)
accessrule_obj = AccessRuleIPv4Api(fw)

class PPPoeParams:
    PPPOE_IF = "eth1"
    LOCAL_IP = PC4_ETH1_IP
    PPPOE_ASSIGN = Parameter.X1_PPPOE_IP_SERVER
    PPP_SECRETS = f'{CONF_PATH}/pppoe/pap-secrets'
    PPPOE_OPTIONS = f'{CONF_PATH}/pppoe/pppoe-server-options'
    PPPOE_DOWN_IP = "0.0.0.0"

class PPPoeParams_x3:
    PPPOE_IF = "eth1"
    LOCAL_IP = PC5_ETH1_IP
    PPPOE_ASSIGN = Parameter.X3_PPPOE_IP_SERVER
    PPP_SECRETS = f'{CONF_PATH}/pppoe/pap-secrets'
    PPPOE_OPTIONS = f'{CONF_PATH}/pppoe/pppoe-server-options'
    PPPOE_DOWN_IP = "0.0.0.0"

# Init Settings
x0_lan_dict = {
    'if': 'X0',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X0_IP,
    'netmask': '255.255.255.0',
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}

x0_lan_dict_http = {
    'if': 'X0',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X0_IP,
    'netmask': '255.255.255.0',
    'mgmt_http': True,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_http': True,
    'user_https': True,
}

x0_lan_ipv6_dict = {
    'name': 'X0',
    'mode': 'static',
    'zone': 'LAN',
    'ip': Parameter.X0_IPv6,
    'mgmt_ping': True,
    'mgmt_ssh': True
}
x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': '255.255.255.0',
    'gateway': Parameter.X1_GW,
    'dns1': Params.G_DNS1,
    'dns2': Params.G_DNS2,
    'mgmt_ssh': True,
    'mgmt_https': True,
}

x1_wan_ipv6_dict = {
    'name': 'X1',
    'mode': 'static',
    'zone': 'WAN',
    'ip': Parameter.X1_IPv6,
    'mgmt_ping': True,
}

x3_wan_dict = {
    'if': 'X3',
    'zone': 'wan',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'netmask': '255.255.255.0',
    'gateway': Parameter.X3_GW,
    'dns1': Params.G_DNS1,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_http': False,
    'user_https': True,
}

x4_lan_dict = {
    'if': 'x4',
    'zone': 'lan',
    'mode': 'static',
    'ip': Parameter.X4_IP,
    'netmask': '255.255.255.0',
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    'mgmt_ping': True,
    'user_https': True,
}

icmp_drop_setting_dict1 = {
            "log": {
                "event": [{
                    "id": 38,
                    "name": "ICMP Packets Dropped",
                    "category": "Network",
                    "group": "ICMP",
                    "priority_level": "critical",
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
                    "ipfix": {},
                    "log_digest": False,
                    "color": {
                        "hex": "0x00FF0000"
                    },
                    "alert_email": {}
                }]
            }
        }

x0_lan_fqdn_dict = {
    'if': 'X0',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X0_IP,
    'netmask': '255.255.255.0',
    "fqdn_assignment": "1234567890abcd.corp.test.com",
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}

import os
import sys
import re
import time
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
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_GUI_Selected/testcases")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_GUI_Selected")
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_GUI_Selected/testplan/Config_Auditing_GUI_Selected.json'
CERT_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_GUI_Selected/definition/cert/dovecot_1k.p12'

from lib.modules.API import log,network,firewallsettings,system,\
    sslvpn,firewall,policy,sslvpn,vpn,users,dpissl,wireless,accesspoint
from lib.modules.CLI.system import LicenseCli
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall


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


# parameters on the openstack
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    platform = os_obj.get_node_platform('UTM')

# settings in TestInitConfig
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
            "value": "2.2.2.100",
        }

syslog_ao_dict = {
            "object_type": "host",
            "name": 'test_syslog',
            "zone": "LAN",
            "value": '192.168.168.100',
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
    'tc1': ["Import 3rd Cert"],
    'tc2': ["'System Name'.*?changed from \[sonicwall\].*?changed to \[test\]",
            "'System Location'.*?changed to \[test\]",
            "'System Contact' .*?changed to \[test\]",
            "'Host 2'.*?changed to \[1.1.1.1\]",
            "'Host 3'.*?changed to \[2.2.2.2\]",
            "'Host 4'.*?changed to \[3.3.3.3\]"],
    'tc3': ["LAN/DMZ/WLAN IP Address.*?X3.*?changed from \[0.0.0.0\].*?changed to \[1.1.1.1\]",
            "Interface zone.*?X3.*?changed to \[LAN\]"],
    'tc4': ["Policy Name.*?changed to \[route_policy_tc4\]",
            "The Interface for the route policy.*?changed to \[X2\]",
            "The Gateway for the route policy.*?changed to \[X2 IP\]",
            "The associated service for the route policy.*?changed to \[Ping\]"],
    'tc5': ["Inherit DNS Settings in Dynamic DHCP.*?changed to \[enabled\]",
            "DCHP Dynamic Subnet Mask.*?changed to \[255\.255\.255\.0\]",
            "Default Gateway.*?changed to \[14\.1\.1\.168\]",
            "DHCP Dynamic Range End.*?changed to \[14\.1\.1\.167\]",
            "DHCP Dynamic Range Begin.*?changed to \[14\.1\.1\.10\]"],
    'tc6': ["WLAN Ssid.*?changed to \[sonicwall_test\]",
           "Enable WLAN.*?changed to \[enabled\]"],
    'tc7': ["Modified 'SonicPointN name' , SonicWave",
            "SonicPointN SSID.*?changed to \[sonicwall_test\]"],
    'tc8': ["Added 'Virtual Access Point/Group/NAME'.*?changed to \[test\]",
            "'Virtual Access Point SSID'.*?changed to \[sonicwall\]"],
    'tc9': ["Modified 'NAC attr name'",
            'NAC attr address object.*?changed to \[test_09\]'],
    'tc10': ['RDP1', '10.5.252.115', 'HTML5-RDP', 'enabled'],
    'tc11': ["IPsec Name.*?changed to \[localvpn\]",
              "IPsec Gateway Address.*?changed to \[2\.2\.2\.2\]",
              "Type of VPN Policy.*?changed to \[Site to Site\]",
              "Authentication Method.*?changed to \[IKE using Preshared Secret\]",
              "Local Networks.*?changed to \[X0 Subnet\]",
              "Destination Networks.*?changed to \[remote_vpn_net\]",
              "Local IKE ID.*?changed to \[4\.4\.4\.4\]",
              "Peer IKE ID.*?changed to \[4\.4\.4\.4\]",
              "Encryption Key.*?changed to \[\*\*\*\*\*\*\]",
              "Enable Keep Alive.*?changed to \[enabled\]",],
    'tc12': ["Deleted 'IPsec Name'.*?localvpn",
             "Deleted 'IPsec Name'.*?localvpn2"],
    'tc13': ['2.2.2.2', 'Give bind distinguished name', 'disabled', 'testdomain1.com/users', 'testdomain1.com/groups'],
    'tc14': ["Apply password constraints.*?changed to \[password constraints for other full administrators disabled\]",
            "Apply password constraints.*?changed to \[password constraints for limited administrators disabled]",
            "Apply password constraints.*?changed to \[password constraints for local users disabled\]",
            "Apply password constraints.*?changed to \[password constraints for guest administrators disabled\]",
            "Prune Expired user accounts.*?changed to \[disabled\]",],
    'tc15': ["SSL proxy Ca cert.*?changed to \[dovecot_1k\]",],
    'tc16': ["SSL server certs config.*?changed to \[/aobj:X1 IP/certName:dovecot_1k/term:true\^]"],
    'tc17': ['FTP', 'None', 'my_access_rule1', 'enabled', '15'],
    'tc18': ["Application Firewall policy name.*?changed to \[TC18_App_Rule\]",
             "Application Firewall policy input type.*?changed to \[App Control Content\]",
             "Application Firewall policy connection.*?changed to \[Client Side\]",
             "Application Firewall policy source address.*?changed to \[Any\]",
             "Application Firewall policy destination address.*?changed to \[Any\]",
             "'Application Firewall policy exclude address.*?changed to \[None\]",
             "Application Firewall policy source service.*?changed to \[Any\]",
             "Application Firewall policy object.*?changed to \[TC18_Application_List\]",
             "Application Firewall policy object exclude.*?changed to \[None\]",
             "Application Firewall policy action.*?changed to \[Reset\]",
             "Application Firewall policy Exclude RT.*?changed to \[Any\]",
             "Application Firewall policy Include RT.*?changed to \[Any\]",
             "Application Firewall policy Exclude MF.*?changed to \[Any\]",
             "Application Firewall policy Include MF.*?changed to \[Any\]",
             "Application Firewall policy direction from.*?changed to \[Any\]",
             "Application Firewall policy direction basic.*?changed to \[Incoming\]",
             "Application Firewall direction policy.*?changed to \[Incoming\]",
             "Application Firewall policy formatted logging.*?changed to \[enabled\]",
             "Enable Application policy.*?changed to \[enabled\]",
             "Application Firewall Use global LRT.*?changed to \[enabled\]",
             "Application Firewall CFS allow object list.*?changed to \[None\]",
             "Application Firewall CFS forbid object list.*?changed to \[None\]",
             "Application Firewall policy object name.*?changed to \[TC18_Application_List\]",
             "Application Firewall policy action name.*?changed to \[Reset/Drop\]",]}

#Instantiate objects including API,CLI
console_info = os_obj.get_console_info(dut='UTM')

fw_api = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
fw_console = Firewall(Parameter.FIREWALL, console_ip=console_info[0], console_port=console_info[1], user='admin', password='password', supported_config_mode='cli-console')

interface_api = network.InterfaceIPv4Api(fw_api)
fp_api = firewallsettings.FloodprotectionApi(fw_api)
log_api = log.LogMonitorApi(fw_api)
pkg_api = system.PacketmonitorApi(fw_api)
ao_api = network.AddressobjectsApi(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
system_api = system.DiagnosticApi(fw_api)
setting_api = system.SettingApi(fw_api)
license_cli = LicenseCli(fw_cli)
log_set = log.LogCategoryApi(fw_api)
snmp_api = system.SNMPApi(fw_api)
audit_log_api = log.AuditlogMonitorApi(fw_api)
logsetting_api = log.LogSettingsApi(fw_api)
log_auto_api = log.LogAutomationApi(fw_api)
dhcp_api = network.DHCPServerApi(fw_api)
clientset_api = sslvpn.SSLVPNClientSettingsAPI(fw_api)
access_rules_api = firewall.AccessRuleApi(fw_api)
cert_api = system.CertificateApi(fw_api)
route_api = policy.RoutePolicyApi(fw_api)
virtualset_api = sslvpn.SSLVPNVirtualOfficeAPI(fw_api)
ao_api = network.AddressobjectsApi(fw_api)
vpn_api = vpn.VpnbasesettingApi(fw_api)
ldap_api = users.LdapApi(fw_api)
usersettings_api = users.UserLocalApi(fw_api)
ssl_cert_api = dpissl.ClientSslApi(fw_api)
server_ssl_api = dpissl.ServerSslApi(fw_api)
match_object_api= firewall.MatchobjectApi(fw_api)
app_rule_api = firewall.AppRuleApi(fw_api)
user_local_api = users.UserLocalApi(fw_api)
diag_api = system.DiagnosticApi(fw_api)
wireless_api = wireless.WirelessApi(fw_api)
ap_api = accesspoint.AccessPointApi(fw_api)
vap_api = accesspoint.VirtualAccessPointApi(fw_api)
pkgmonitor_api = system.PacketmonitorApi(fw_api)
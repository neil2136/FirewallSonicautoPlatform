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
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Network_Part1/testcases")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Network_Part1")
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_CLI_Network_Part1/testplan/Config_Auditing_CLI_Network_Part1.json'

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
VLAN_id_X4 = os_obj.get_node_interface_vlan_id('UTM','X4')
VLAN_id_X3 = os_obj.get_node_interface_vlan_id('UTM','X3')

logger.info("\n" + "-" * 30 + "\n" \
    + "VLAN_id_X3 :" + str(VLAN_id_X3) + "\n" \
    + "VLAN_id_X4 :" + str(VLAN_id_X4) + "\n"
)

PC2_login = Host(PC2_ETH3_IP)

IP_syslog_ao_dict = '192.168.168.100'
IP_sslvpn_ao_dict = '2.2.2.100'


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
            "value": IP_syslog_ao_dict,
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
    'tc1530910_syslog_check': ["'Interface type '.*?X3.*?changed from \[Undefined Interface\].*?changed to \[LAN\]",
                         "'LAN/DMZ/WLAN IP Address'.*?X3.*?changed from \[0.0.0.0\].*?changed to \[2.3.3.3\]"],
    'tc1530910_auditlog_check': ["X3.*?'LAN/DMZ/WLAN IP Address'.*?2.3.3.3",
                           "X3.*?'Interface type '.*?Undefined Interface LAN"],

    'tc1530911_syslog_check': ["'Interface type '.*?X3.*?changed from \[LAN\].*?changed to \[DMZ\]",
                              "'Interface zone'.*?X3.*?changed from \[LAN\].*?changed to \[DMZ\]",
                              "'Allow SSH Management on this interface'.*?X3.*?changed from \[disabled\].*?changed to \[enabled\]",
                              "'Enable PING management on this interface'.*?X3.*?changed from \[disabled\].*?changed to \[enabled\]",
                              "'LAN/DMZ/WLAN IP Address'.*?X3.*?changed from \[2.3.3.3\].*?changed to \[6.6.6.6\]"],
    'tc1530911_auditlog_check': ["X3.*?'LAN/DMZ/WLAN IP Address'.*?2.3.3.3.*?6.6.6.6",
                              "X3.*?'Enable PING management on this interface'.*?disabled.*?enabled",
                              "X3.*?'Allow SSH Management on this interface'.*?disabled.*?enabled",
                              "X3.*?'Interface zone'.*?LAN.*?DMZ",
                              "X3.*?'Interface type '.*?LAN.*?DMZ",],

    'tc1530912_syslog_check': ["'Enable Multicast Reception on the Interface'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                              "'Link Aggregate Port 2'.*?X3.*?changed from \[Any\], changed to \[X5\]",
                              "'Port Grouping'.*?X3.*?changed from \[None\], changed to \[Link Aggregation\]"],
    'tc1530912_auditlog_check': ["X3.*?'Port Grouping'.*?None.*?Link Aggregation",
                                 "X3.*?'Link Aggregate Port 2'.*?Any.*?X5",
                                 "X3.*?'Enable Multicast Reception on the Interface'.*?disabled.*?enabled"],

    'tc1530914_syslog_check': ["'IPv6 Interface Static IP'.*?X3.*?changed from \[::\], changed to \[3ffe:1900:4545::f8ff:fe21:67cf\]",
                               "'IPv6 Interface HTTPS management'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'IPv6 Interface SSH management'.*?X3.*?changed from \[disabled\], changed to \[enabled\]"],
    'tc1530914_auditlog_check': ["X3.*?'IPv6 Interface Static IP'.*?::.*?3ffe:1900:4545::f8ff:fe21:67cf",
                                 "X3.*?'IPv6 Interface HTTPS management'.*?disabled.*?enabled",
                                 "X3.*?'IPv6 Interface SSH management'.*?disabled.*?enabled"],

    'tc1530915_syslog_check': ["'IPv6 Interface Static IP'.*?X3.*?changed from \[3ffe:1900:4545::f8ff:fe21:67cf\], changed to \[3ffe:1900:4545::f8ff:fe21:67ce\]",
                               "'IPv6 Interface HTTPS user login'.*?X3.*?changed from \[disabled\], changed to \[enabled\]"],
    'tc1530915_auditlog_check': ["X3.*?'IPv6 Interface Static IP'.*?3ffe:1900:4545::f8ff:fe21:67cf.*?3ffe:1900:4545::f8ff:fe21:67ce",
                                 "X3.*?'IPv6 Interface HTTPS user login'.*?disabled.*?enabled"],
                          
    'tc1530916_syslog_check': ["'IPv6 Interface number'.*?newaddtunnelinterface.*?changed to \\[newaddtunnelinterface\\]",
                               "'IPv6 interface physical type'.*?newaddtunnelinterface.*?changed to \\[Tunnel\\]",
                               "'IPv6 Interface Tunnel GIF Destination Address'.*?newaddtunnelinterface.*?changed to \\[192.168.168.169\\]"],
    'tc1530916_auditlog_check': ["newaddtunnelinterface.*?'IPv6 Interface Tunnel GIF Destination Address'.*?192.168.168.169",
                                 "newaddtunnelinterface.*?'IPv6 interface physical type'.*?Tunnel",
                                 "newaddtunnelinterface.*?'IPv6 Interface number'.*?newaddtunnelinterface"],

    'tc1530921_syslog_check': ["'Zone Name'.*?newaddzone.*?changed to \[newaddzone\]",
                               "'Security Type'.*?newaddzone.*?changed to \[Public\]"],
    'tc1530921_auditlog_check': ["newaddzone.*?'Zone Name'.*?newaddzone",
                                "newaddzone.*?'Security Type'.*?Public "],

    'tc1530923_syslog_check': ["'Zone Name'.*?newupdatezone.*?changed to \[newupdatezone\]",
                                "'Security Type'.*?newupdatezone.*?changed to \[Trusted\]"],
    'tc1530923_auditlog_check': ["newupdatezone.*?'Zone Name'.*?newupdatezone",
                                 "newupdatezone.*?'Security Type'.*?Trusted",],

    'tc1530922_syslog_check': ["Deleted 'Zone Name'.*?newupdatezone.*?changed from \[newupdatezone\]"],
    'tc1530922_auditlog_check': ["newupdatezone.*?Deleted 'Zone Name'.*?newupdatezone"],

    'tc1530926_syslog_check': ["'Use Static DNS Servers or Inherit'.*?changed from \[Inherit DNS Settings Dynamically from WAN Zone\], changed to \[Specify DNS Servers Manually\]",
                               "'Static DNS Server One'.*?changed from \[156.154.54.200\].*?changed to \[1.1.1.1\]",
                               "'Static DNS Server Two'.*?changed from \[156.154.55.200\].*?changed to \[2.2.2.2\]",
                               "'Static DNS Server Three'.*?changed from \[8.8.8.8\].*?changed to \[3.3.3.3\]"],
    'tc1530926_auditlog_check': ["DNS Servers or Inherit' Inherit DNS Settings Dynamically from WAN ZoneSpecify DNS Servers Manually",
                                 "Server Three'.*?8.8.8.8.*?3.3.3.3",
                                "Server Two'.*?156.154.55.200.*?2.2.2.2",
                                "Server One'.*?156.154.54.200.*?1.1.1.1"],

    'tc1530927_syslog_check': ["'Split DNS Domain Name'.*?mail.126.com.*?changed to \[mail.126.com\]",
                          "'Split IPv4 Primary DNS Server'.*?mail.126.com.*?changed to \[10.8.166.239\]"],
    'tc1530927_auditlog_check': ["mail.126.com.*?'Split DNS Domain Name'.*?mail.126.com",
                                "mail.126.com.*?'Split IPv4 Primary DNS Server'.*?10.8.166.239",],

    'tc1530928_syslog_check': ["Deleted 'Split DNS Domain Name'.*?mail.126.com.*?changed from \[mail.126.com\]"],
    'tc1530928_auditlog_check': ["mail.126.com.*?Deleted 'Split DNS Domain Name'.*?mail.126.com "],

    'tc1530929_syslog_check': ["'Split DNS Domain Name'.*?mail.163.com.*?changed to \[mail.163.com\]",
                          "'Split IPv6 Primary DNS Server'.*?mail.163.com.*?changed to \[33::33\]"],
    'tc1530929_auditlog_check': ["mail.163.com.*?'Split IPv6 Primary DNS Server'.*?33::33",
                                "mail.163.com.*?'Split DNS Domain Name'.*?mail.163.com"],

    'tc1530930_syslog_check': ["Deleted 'Split DNS Domain Name'.*?mail.163.com.*?changed from \[mail.163.com\]"],
    'tc1530930_auditlog_check': ["mail.163.com.*?Deleted 'Split DNS Domain Name'.*?mail.163.com"],
    
    'tc1530931_syslog_check': ["'Enforce DNS Proxy'.*?changed from \[disabled\].*?changed to \[enabled\]",
                               "'Enforce DNS Proxy'.*?changed from \[enabled\].*?changed to \[disabled\]"],
    'tc1530931_auditlog_check': ["'Enforce DNS Proxy'.*?disabled.*?enabled",
                                  "'Enforce DNS Proxy'.*?enabled.*?disabled"],

    'tc1530932_syslog_check': ["'Enable DNS Cache'.*?changed from \[enabled\].*?changed to \[disabled\]",
                               "'Enable DNS Cache'.*?changed from \[disabled\].*?changed to \[enabled\]"],
    'tc1530932_auditlog_check': ["'Enable DNS Cache'.*?enabled.*?disabled",
                                 "'Enable DNS Cache'.*?disabled.*?enabled"],

    'tc1530933_syslog_check': ["'Static DNS Cache IP Address'.*?sonicwall.com.*?changed to \[3.3.3.3\]",
                               "'Static DNS Cache Domain Name'.*?sonicwall.com.*?changed to \[sonicwall.com\]"],
    'tc1530933_auditlog_check': ["sonicwall.com.*?'Static DNS Cache Domain Name'.*?sonicwall.com",
                               "sonicwall.com.*?'Static DNS Cache IP Address'.*?3.3.3.3"],

    'tc1530934_syslog_check': ["Deleted 'Static DNS Cache Domain Name'.*?sonicwall.com.*?changed from \[sonicwall.com\]"],
    'tc1530934_auditlog_check': ["sonicwall.com.*?Deleted 'Static DNS Cache Domain Name'.*?sonicwall.com"],    

    'tc1530935_syslog_check': ["'Custom Malicious Domain Name'.*?sonicwall.com.*?changed to \[sonicwall.com\]"],
    'tc1530935_auditlog_check': ["Custom Domain.*?sonicwall.com.*?'Custom Malicious Domain Name'.*?sonicwall.com"],  

    'tc1530936_syslog_check': ["'White Entry Name'.*?sonicwall.com.*?changed to \[sonicwall.com\]"],
    'tc1530936_auditlog_check': ["White Entry.*?sonicwall.com.*?'White Entry Name'.*?sonicwall.com"],   

    'tc1530937_syslog_check': ["'DNS Tunnel White Entry'.*?10.10.10.1.*?changed to \[10.10.10.1\]"],
    'tc1530937_auditlog_check': ["Dns Tunnel White Entry.*?10.10.10.1.*?'DNS Tunnel White Entry'.*?10.10.10.1"], 

    'tc1530938_syslog_check': ["'The Interface for the route policy'.*?changed to \[X6\]",
                               "'The Metric for the route policy'.*?changed to \[4\]",
                                "'Policy Name'.*?changed to \[Route Policy\]"],
    'tc1530938_auditlog_check': ["'The Metric for the route policy'.*?4",
                                 "'The Interface for the route policy'.*?X6",
                                "'Policy Name'.*?Route Policy"],

    'tc1530939_syslog_check': ["'The Number of the route policy nexthop'.*?changed to \[2\]",
                               "'The Metric for the route policy'.*?changed to \[3\]",
                                "'The Interface for the route policy'.*?changed to \[X0\]",
                                "'The 2nd Interface for the route policy'.*?changed to \[X2\]"],
    'tc1530939_auditlog_check': ["'The Metric for the route policy'.*?3",
                                 "'The 2nd Interface for the route policy'.*?X2",
                                "'The Interface for the route policy'.*?X0",
                                "'The Number of the route policy nexthop'.*?2"],

    'tc1530941_syslog_check': ["Deleted 'The ID of the route policy'",
                               "Deleted 'The ID of the route policy'"],
    'tc1530941_auditlog_check': ["Deleted 'The ID of the route policy'",
                                "Deleted 'The ID of the route policy'"],

    'tc1530942_auditlog_check': ["'Policy Name'.*?newaddv6policy",
                               "'IPv6 PBR Object metric'.*?3"],
    'tc1530942_syslog_check': ["'Policy Name'.*?changed to \[newaddv6policy\]",
                                "'IPv6 PBR Object metric'.*?changed to \[3\]"],  

    'tc1530943_syslog_check': ["Deleted 'IPv6 PBR Object ID'"],
    'tc1530943_auditlog_check': ["IPV6 PolicyBasedRoute.*?Deleted 'IPv6 PBR Object ID'"],  

    'tc1530948_syslog_check': [r"'NAT Policy Name'.*?changed to \[newaddnatpolicy\]",
                               r"'Destination Interface'.*?changed to \[X3\]",
                               r"'Source Interface'.*?changed to \[X2\]"],

    'tc1530948_auditlog_check': [r"'NAT Policy Name'.*?newaddnatpolicy",
                                 r"'Destination Interface'.*?X3",
                                 r"'Source Interface'.*?X2"],

    'tc1530949_syslog_check': [r"Deleted\s+'Original Source'"],
    'tc1530949_auditlog_check': [r"Deleted\s+'Original Source'\s+Orig\s+Src"],

    'tc1530950_syslog_check': [r"'IPv6 Source Interface'.*?changed to \[X2\]",
                               r"'IPv6 Destination Interface'.*?changed to \[X3\]",
                               r"'IPv6NAT Policy Name'.*?changed to \[newaddv6nat\]"],
    
    'tc1530950_auditlog_check': ["'IPv6NAT Policy Name'.*?newaddv6nat",
                                 "'IPv6 Destination Interface'.*?X3",
                                 "'IPv6 Source Interface'.*?X2"],

    'tc1530951_syslog_check': [r"Deleted 'IPv6 Original Source'\s*,"],
    'tc1530951_auditlog_check': ["newaddv6nat.*?Deleted"],

    'tc1530952_auditlog_check': ["3.3.3.3.*?'Static ARP.*?Nat ARP'",
                                 "3.3.3.3.*?'Static ARP Ethernet address'.*?00:01:02:03:04:05"],
    'tc1530952_syslog_check': ["'Static ARP IP Address'.*?3.3.3.3.*?changed to \[3.3.3.3\]",
                              "'Static ARP: Interface'.*?3.3.3.3.*?changed to \[X0\]",
                              "'Static ARP Ethernet address'.*?3.3.3.3, changed to \[00:01:02:03:04:05\]"],

    'tc1530953_auditlog_check': ["Deleted 'Static ARP IP Address' 3.3.3.3"],
    'tc1530953_syslog_check': ["Deleted 'Static ARP IP Address'.*?3.3.3.3.*?changed from \[3.3.3.3\]"],

    'tc1530954_auditlog_check': ["ARP Cache entry timeout.*?10.*?15"],
    'tc1530954_syslog_check': ["ARP Cache entry timeout.*?changed from \[10\].*?changed to \[15\]"],

    'tc1530955_auditlog_check': ["Static NDP.*?2001:10:10:10:2D0:02BB:03CC:04DD.*?'NDP static ethernet'"],
    'tc1530955_syslog_check': ["'NDP static IP'.*?2001:10:10:10:2D0:02BB:03CC:04DD.*?changed to \[2001:10:10:10:2D0:02BB:03CC:04DD\]"],

    'tc1530956_auditlog_check': ["Deleted 'NDP static IP'.*?2001:10:10:10:2d0:2bb:3cc:4dd"],
    'tc1530956_syslog_check': ["Deleted 'NDP static IP'.*?02BB03CC04DD.*?changed from \[2001:10:10:10:2d0:2bb:3cc:4dd\]"],

    'tc1530957_auditlog_check': ["'Use Static Arp Entry for Mac-IP Spoof'.*?disabled.*?enabled",
                                 "'Create cache for Mac-IP spoof'.*?disabled.*?enabled",
                                 "'Use DHCP relay's lease for Mac-IP Spoof'.*?disabled.*?enabled",
                                 "'Use DHCP server's lease for Mac-IP Spoof' disabled.*?enabled",
                                 "'Refresh Arp cache for Mac-IP Spoof' disabled.*?enabled",
                                 "'Fill Arp cache for Mac-IP Spoof' disabled.*?enabled",
                                 "'Enforce MAC-IP anti-spoofing' disabled.*?enabled",
                                 "'Enable MAC-IP anti-spoofing' disabled.*?enabled"],
    'tc1530957_syslog_check': ["'Enable MAC-IP anti-spoofing'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Enforce MAC-IP anti-spoofing'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Fill Arp cache for Mac-IP Spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Refresh Arp cache for Mac-IP Spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Use DHCP server's lease for Mac-IP Spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Use DHCP relay's lease for Mac-IP Spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Create cache for Mac-IP spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Use Static Arp Entry for Mac-IP Spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]"],

    'tc1530958_auditlog_check': ["'Mac-IP Spoof Static MAC Address'.*?00:01:02:03:04:05",
                                "'Mac-IP Spoof IP Address'.*?10.10.10.10",
                                "'Mac-IP Spoof Static Interface Index'.*?X3"],
    'tc1530958_syslog_check': ["'Mac-IP Spoof Static Interface Index'.*?X3.*?10.10.10.10.*?00:01:02:03:04:05.*?changed to \[X3\]",
                              "'Mac-IP Spoof IP Address'.*?X3.*?10.10.10.10.*?00:01:02:03:04:05.*?changed to \[10.10.10.10\]",
                               "'Mac-IP Spoof Static MAC Address'.*?X3.*?10.10.10.10.*?00:01:02:03:04:05.*?changed to \[00:01:02:03:04:05\]"],

    'tc1530959_auditlog_check': ["Deleted 'Mac-IP Spoof Static Interface Index' X3"],
    'tc1530959_syslog_check': ["Deleted 'Mac-IP Spoof Static Interface Index'.*?X3.*?10.10.10.10.*?00:01:02:03:04:05, changed from \[X3\]"],

    'tc1530960_auditlog_check': ["'Use Static Ndp Entry for IPv6 Mac-IP Spoof'.*?disabled.*?enabled",
                                 "'Create cache for IPv6 Mac-IP spoof'.*?disabled.*?enabled",
                                 "'Fill Ndp cache for IPv6 Mac-IP Spoof'.*?disabled.*?enabled",
                                 "'Enforce IPv6 Mac-IP anti-spoofing' disabled.*?enabled",
                                 "'Enable IPv6 Mac-IP anti-spoofing' disabled.*?enabled",],
    'tc1530960_syslog_check': ["'Enable IPv6 Mac-IP anti-spoofing'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Enforce IPv6 Mac-IP anti-spoofing'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Fill Ndp cache for IPv6 Mac-IP Spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Create cache for IPv6 Mac-IP spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",
                               "'Use Static Ndp Entry for IPv6 Mac-IP Spoof'.*?X3.*?changed from \[disabled\], changed to \[enabled\]",],

    'tc1530961_auditlog_check': ["'IPv6 Mac-IP Spoof Static MAC Address'.*?00:01:02:03:04:05",
                                "'IPv6 Mac-IP Spoof IP Address'.*?1030::C9B4:FF12:48AA:1A2B",
                                "'IPv6 Mac-IP Spoof Static Interface Index'.*?X3"],
    'tc1530961_syslog_check': ["'IPv6 Mac-IP Spoof IP Address'.*?00:01:02:03:04:05, changed to \[1030::C9B4:FF12:48AA:1A2B\]",
                              "'IPv6 Mac-IP Spoof Static MAC Address'.*?00:01:02:03:04:05, changed to \[00:01:02:03:04:05\]",
                               "'IPv6 Mac-IP Spoof Static Interface Index'.*?00:01:02:03:04:05, changed to \[X3\]"],

    'tc1530962_auditlog_check': ["Deleted 'IPv6 Mac-IP Spoof Static Interface Index'.*?X3",],
    'tc1530962_syslog_check': ["Deleted 'IPv6 Mac-IP Spoof Static Interface Index'.*?00:01:02:03:04:05.*?changed from \[X3\]"],

    'tc1530963_auditlog_check': ["'Enable DHCP Server'.*?disabled.*?enabled",
                                "'Enable DHCP Server'.*?enabled.*?disabled"],
    'tc1530963_syslog_check': ["'Enable DHCP Server'.*?changed from \[enabled\], changed to \[disabled\]",
                               "'Enable DHCP Server'.*?changed from \[disabled\], changed to \[enabled\]"],

    'tc1530964_auditlog_check': ["'DCHP Dynamic Subnet Mask'.*?255.255.255.0",
                                 "'DHCP Dynamic Range End'.*?6.6.6.254",
                                 "'DHCP Dynamic Range Begin'.*?6.6.6.7"],
    'tc1530964_syslog_check': ["'DHCP Dynamic Range End'.*?6.6.6.7.*?6.6.6.254.*?changed to \[6.6.6.254\]",
                               "'DCHP Dynamic Subnet Mask'.*?6.6.6.7.*?6.6.6.254.*?changed to \[255.255.255.0\]",
                               "'DHCP Dynamic Range Begin'.*?6.6.6.7.*?6.6.6.254.*?changed to \[6.6.6.7\]"],

    'tc1530965_auditlog_check': ["DHCP Dynamic Ranges.*?6.6.6.10.*?6.6.6.200.*?'Allow BOOTP'.*?disabled.*?enabled",
                                 "DHCP Dynamic Ranges.*?6.6.6.10.*?6.6.6.200.*?'DHCP Dynamic Range End'.*?6.6.6.254.*?6.6.6.200",
                                 "DHCP Dynamic Ranges.*?6.6.6.10.*?6.6.6.200.*?'DHCP Dynamic Range Begin'.*?6.6.6.7.*?6.6.6.10"],
    'tc1530965_syslog_check': ["'DHCP Dynamic Range Begin'.*?6.6.6.10.*?6.6.6.200.*?changed from \[6.6.6.7\], changed to \[6.6.6.10\]",
                               "'DHCP Dynamic Range End'.*?6.6.6.10.*?6.6.6.200.*?changed from \[6.6.6.254\], changed to \[6.6.6.200\]",
                               "'Allow BOOTP'.*?6.6.6.10.*?6.6.6.200.*?changed from \[disabled\], changed to \[enabled\]"], 

    'tc1530966_auditlog_check': ["DHCP Static Ranges.*?192.168.168.188.*?000102030405.*?'DCHP Static Subnet Mask'.*?255.255.255.0",
                                 "DHCP Static Ranges.*?192.168.168.188.*?000102030405.*?'DHCP Static Ethernet Address'.*?000102030405",
                                 "DHCP Static Ranges.*?192.168.168.188.*?000102030405.*?'DHCP Static IP'.*?192.168.168.188"],
    'tc1530966_syslog_check': ["'DHCP Static IP'.*?192.168.168.188.*?000102030405.*?changed to \[192.168.168.188\]",
                               "'DHCP Static Ethernet Address'.*?192.168.168.188.*?000102030405, changed to \[000102030405\]",
                               "'DCHP Static Subnet Mask'.*?192.168.168.188.*?000102030405, changed to \[255.255.255.0\]"],  

    'tc1530967_auditlog_check': ["DHCP Static Ranges.*?10.10.10.10.*?000102030405.*?'DCHP Static Subnet Mask'.*?255.255.255.0",
                                 "DHCP Static Ranges.*?10.10.10.10.*?000102030405.*?'DHCP Static Ethernet Address'.*?000102030405",
                                 "DHCP Static Ranges.*?10.10.10.10.*?000102030405.*?'DHCP Static IP'.*?10.10.10.10"],
    'tc1530967_syslog_check': ["'DHCP Static IP'.*?10.10.10.10.*?000102030405.*?changed to \[10.10.10.10\]",
                               "'DHCP Static Ethernet Address'.*?10.10.10.10.*?000102030405, changed to \[000102030405\]",
                               "'DCHP Static Subnet Mask'.*?10.10.10.10.*?000102030405, changed to \[255.255.255.0\]"],  

    'tc1530968_auditlog_check': ["Deleted 'DHCP Static IP'.*?10.10.10.10"],
    'tc1530968_syslog_check': ["Deleted 'DHCP Static IP'.*?10.10.10.10/000102030405.*?changed from \[10.10.10.10\]"], 

    'tc1530970_auditlog_check': ["'Enable DHCPv6'.*?enabled.*?disabled"],
    'tc1530970_syslog_check': ["'Enable DHCPv6'.*?changed from \[enabled\].*?changed to \[disabled\]"], 

    'tc1530972_auditlog_check': ["'DHCPv6 dynamic scope object send options always'.*?enabled"],
    'tc1530972_syslog_check': ["'DHCPv6 dynamic scope object send options always'.*?dyanmicScope, changed to \[enabled\]"], 

    'tc1530973_auditlog_check': ["'DHCPv6 Server static DUID'.*?29",
                                 "'DHCPv6 Server static IAID'.*?28",
                                 "'DHCPv6 Server static IP'.*?fe00::2016",
                                 "'DHCPv6 Server static prefix'.*?fe00::",
                                 "'DHCPv6 Server static type'.*?Static",
                                 "'DHCPv6 Server static entry'.*?dhcps6StaticName"],
    'tc1530973_syslog_check': ["'DHCPv6 Server static type'.*?dhcps6StaticName, changed to \[Static\]",
                               "'DHCPv6 Server static entry'.*?dhcps6StaticName, changed to \[dhcps6StaticName\]",
                               "'DHCPv6 Server static type'.*?dhcps6StaticName, changed to \[Static\]",
                               "'DHCPv6 Server static prefix'.*?dhcps6StaticName, changed to \[fe00::\]",
                               "'DHCPv6 Server static IP'.*?dhcps6StaticName, changed to \[fe00::2016\]",
                               "'DHCPv6 Server static IAID'.*?dhcps6StaticName, changed to \[28\]",
                               "'DHCPv6 Server static DUID'.*?dhcps6StaticName, changed to \[29\]"], 

    'tc1530975_auditlog_check': ["Deleted 'DHCPv6 Server static entry' dhcps6StaticName",
                                 "Deleted 'DHCPv6 dynamic scope object ID' dyanmicScope"],
    'tc1530975_syslog_check': ["Deleted 'DHCPv6 dynamic scope object ID'.*?dyanmicScope, changed from \[dyanmicScope\]",
                               "Deleted 'DHCPv6 Server static entry'.*?dhcps6StaticName, changed from \[dhcps6StaticName\]"],

    'tc1530974_auditlog_check': ["'DHCPv6 Server static option send options always'.*?enabled"],
    'tc1530974_syslog_check': ["'DHCPv6 Server static option send options always'.*?dhcps6StaticName, changed to \[enabled\]"],  

    'tc1530971_auditlog_check': ["'DHCPv6 dynamic scope object range end'.*?fe00::2014",
                                 "'DHCPv6 dynamic scope object range start'.*?fe00::1",
                                 "'DHCPv6 dynamic scope object prefix'.*?fe00::",
                                 "'DHCPv6 dynamic scope object type'.*?Dynamic",
                                 "'DHCPv6 dynamic scope object ID'.*?dyanmicScope"],
    'tc1530971_syslog_check': ["'DHCPv6 dynamic scope object ID'.*?dyanmicScope, changed to \[dyanmicScope\]",
                               "'DHCPv6 dynamic scope object type'.*?dyanmicScope, changed to \[Dynamic\]",
                               "'DHCPv6 dynamic scope object prefix'.*?dyanmicScope, changed to \[fe00::\]",
                               "'DHCPv6 dynamic scope object range start'.*?dyanmicScope, changed to \[fe00::1\]",
                               "'DHCPv6 dynamic scope object range end'.*?dyanmicScope, changed to \[fe00::2014\]",
                               ],   
    'tc1530917_auditlog_check': ["'LB-Type Member Display Name'.*?U0",
                                 "Added 'LB-Type Member Display Name'.*?U0",
                                 "U0.*?'LB-Type Member Rank'.*?2",
                                 "U0.*?'LB-Type Member Group'.*?Default LB Group"],
    'tc1530917_syslog_check': ["Added 'LB-Type Member Display Name'.*?U0, changed to \[U0\]",
                               "'LB-Type Member Display Name'.*?U0, changed to \[U0\]",
                               "'LB-Type Member Group'.*?U0, changed to \[ Default LB Group\]",
                               "'LB-Type Member Rank'.*?U0, changed to \[2\]"],

    'tc1530918_auditlog_check': ["Default LB Group.*?'LB Type'.*?Basic Failover.*?Ratio"],
    'tc1530918_syslog_check': ["'LB Type'.*?Default LB Group, changed from \[Basic Failover\], changed to \[Ratio\]"],

    'tc1530919_auditlog_check': ["Added 'LB-Type Member Display Name'.*?U0",
                                 "'LB-Type Member Display Name'.*?U0",
                                 "'LB-Type Member Group'.*?Default LB Group IPv6",
                                 "'LB-Type Member Rank'.*?2"],
    'tc1530919_syslog_check': ["Added 'LB-Type Member Display Name'.*?U0, changed to \[U0\]",
                               "'LB-Type Member Display Name'.*?U0, changed to \[U0]",
                               "'LB-Type Member Group'.*?U0, changed to \[ Default LB Group IPv6\]",
                               "'LB-Type Member Rank'.*?U0, changed to \[2\]"],

    'tc1530920_auditlog_check': ["'LB Type'.*?Ratio.*?Basic Failover"],
    'tc1530920_syslog_check': ["'LB Type'.*?Default LB Group IPv6, changed from \[Basic Failover\], changed to \[Ratio\]"], 

    'tc1530913_auditlog_check': ["X4:V{}.*?'Wire Mode Interface Zone'.*?LAN".format(VLAN_id_X4),
                                 "X4:V{}.*?'L2TP: Assigned subnet mask'.*?255.255.255.0".format(VLAN_id_X4),
                                 "X4:V{}.*?'Interface Wire Mode Type'.*?Network Tap".format(VLAN_id_X4),
                                 "X4:V{}.*?'VLAN Tag'.*?{}".format(VLAN_id_X4,VLAN_id_X4)],
    'tc1530913_syslog_check': [r"'Name of the Interface'\s*,\s*X4:V{}\s*,\s*changed to \[X4:V{}\]".format(VLAN_id_X4, VLAN_id_X4),
                               r"'Type of interface'\s*,\s*X4:V{}\s*,\s*changed to \[VLAN\]".format(VLAN_id_X4),
                               r"'Interface zone'\s*,\s*X4:V{}\s*,\s*changed to \[LAN\]".format(VLAN_id_X4),
                               r"Added 'Index of the interface'\s*,\s*X4:V{}\s*,\s*changed to \[Any\]".format(VLAN_id_X4)]                                                       
}  

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
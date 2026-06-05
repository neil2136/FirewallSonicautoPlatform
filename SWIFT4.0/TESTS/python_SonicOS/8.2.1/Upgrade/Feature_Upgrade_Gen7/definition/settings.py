import os
import sys
import re
import time
import copy
import requests
import unittest
import json
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
from lib.modules.API import network
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.API import dpissl
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import securityservices
from lib.modules.API import policy
from lib.modules.API import log
from lib.modules.API import object

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Upgrade/Feature_Upgrade_Gen7/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/Feature_Upgrade_Gen7.json'
CONF_PATH = suite_path + 'definition/config'
HTTPS_SERVER_PATH = CONF_PATH + '/httpserver'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
configPath = os.environ["PYTHON_SONICOS_HOME"] + '/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X2_IP = '192.168.2.168'
    X2_SUBNET = '192.168.2.0'
    VALID_DNS = PC4_ETH1_IP
    FAKE_DNS1 = '2.2.2.2'
    FAKE_DNS2 = '3.3.3.3'

    prebuild = Params.prebuild
    testbuild = Params.build


class CaseParams:
    fw_setting_res = []
    fw_function_res = []
    custom_zone_name = 'auto_test01'
    custom_nat_name = 'auto_wan_to_lan_nat'
    custom_route_name = 'auto_x2_to_x1_route'
    custom_access_name = 'auto_wan_to_lan_acl'
    custom_march_name = 'auto_match_test1'
    custom_apprule_name = 'auto_apprule_test1'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

interfaceapi = network.InterfaceIPv4Api(fw)
licensecli = LicenseCli(fw_cli)
aoapi = network.AddressobjectsApi(fw)
cfoobjectapi = firewall.CfoObjectApi(fw)
cfoprofileapi = firewall.CfoProfilesApi(fw)
fwupgradeapi = system.SettingApi(fw)
statusapi = system.StatusApi(fw)
clientsslapi = dpissl.ClientSslApi(fw)
restartapi = system.RestartApi(fw)
diagapi = system.DiagnosticApi(fw)
snmpapi = system.SNMPApi(fw)
spywareapi = securityservices.AntiSpywareApi(fw)
gavapi = securityservices.GAV(fw)
ipsapi = securityservices.IPSApi(fw)
zonesapi = network.ZoneObjectsApi(fw)
natpolicyapi = network.NatpolicyApi(fw)
accessruleapi = firewall.AccessRuleApi(fw)
routepolicyapi = policy.RoutePolicyApi(fw)
matchobjectapi = firewall.MatchobjectApi(fw)
appruleapi = firewall.AppRuleApi(fw)
dnssettingapi = network.DnsSettingsApi(fw)
syslogsettingsapi = log.SyslogSettingsApi(fw)
logmonitorapi = log.LogMonitorApi(fw)
logsettingsapi = log.LogSettingsApi(fw)
timeapi = system.TimeApi(fw)
dosactionprofilesapi = object.DosActionProfilesApi(fw)
dhcpserverapi = network.DHCPServerApi(fw)


x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
x1_dhcp_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'dhcp',
    'mgmt_https': True,
    'mgmt_ping': True,
}
x2_dmz_dict = {
    'if': 'X2',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}
x2_transparent_dict = {
    'if': 'X2',
    'comment': 'auto_transmode_test_x2',
    'zone': 'LAN',
    'mode': 'transparent',
    'transparent_range': {'name': PC4_ETH1_IP},
    'gratuitous_arp_wan_forwarding': False,
    'gratuitous_arp_wan_generation': False,
    'mgmt_https': True,
    'mgmt_ping': True,
    'user_https': True,
}
dhcp_seting_dict = {
    "dhcp_server": {
        "ipv4": {
            "enable": False,
            "conflict_detection": True,
            "persistence": False,
            "persistence_monitoring_interval": 30,
            "trusted_relay_agents": "",
            "recycle_expired_lease": 0
        }
    }
}
cfs_filter_dict = {
    "content_filter": {
        "profile": [
            {
                "bing_force_safe_search": False,
                "categories": "block",
                "consent": {
                    "required": False
                },
                "custom_header": {
                    "insertion": False
                },
                "google_force_safe_search": False,
                "https_filtering": False,
                "name": "CFS Default Profile",
                "reputation": {
                    "active": False
                },
                "safe_search": False,
                "smart_filter": False,
                "threat_api": False,
                "uri_list": {
                    "forbidden_operation": "block",
                    "search_order": "allowed-first"
                },
                "youtube_restrict_mode": False
            }
        ]
    }
}
route_base_dict = {
    "name": CaseParams.custom_route_name,
    "comment": "",
    "interface": "X1",
    "metric": 8,
    "service": {
        "any": True
    },
    "gateway": {
        "name": "X1 Default Gateway"
    },
    "source": {
        "name": "X2 Subnet"
    },
    "destination": {
        "name": PC4_ETH1_IP
    },
    "disable_on_interface_down": True,
    "vpn_precedence": False,
    "probe": "",
    "distance": {
        "auto": True
    },
    "tos": "0x00",
    "mask": "0x00",
    "type": "standard"
}
org_base_dict = copy.deepcopy(route_base_dict)
route_policy_dict = {"route_policies": [{"ipv4": route_base_dict}]}
default_acl_dict = {
    # "uuid": '',
    "name": "Default Access Rule",
    "enable": True,
    "from": "LAN",
    "to": "WAN",
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
            'all': True
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
    "block": {
        "countries": {
            "unknown": False
        }
    },
    "packet_monitoring": False,
    "management": False,
    "max_connections": 100,
    "priority": {
        "manual": {
            "value": 13
        }
    },
    "tcp": {
        "timeout": 15,
        "urgent": False
    },
    "udp": {
        "timeout": 30
    },
    "connection_limit": {
        "source": {},
        "destination": {}
    },
    "dpi": True,
    "dpi_ssl": {
        "client": True,
        "server": True
    },
    "redirect_unauthenticated_users_to_log_in": True,
    "quality_of_service": {
        "class_of_service": {},
        "dscp": {
            "preserve": True
        }
    }
}
custom_acl_dict = {
    "action": "allow",
    "botnet_filter": False,
    "comment": "",
    "connection_limit": {
        "destination": {},
        "source": {}
    },
    "destination": {
        "address": {
            "name": "X1 IP"
        }
    },
    "dpi": True,
    "dpi_ssl": {
        "client": True,
        "server": True
    },
    "enable": True,
    "flow_reporting": False,
    "fragments": True,
    "from": "WAN",
    "geo_ip_filter": {
        "enable": False
    },
    "h323": False,
    "logging": True,
    "management": False,
    "max_connections": 100,
    "name": CaseParams.custom_access_name,
    "packet_monitoring": False,
    "priority": {
        "auto": True
    },
    "quality_of_service": {
        "class_of_service": {},
        "dscp": {
            "preserve": True
        }
    },
    "reflexive": False,
    "service": {
        "any": True
    },
    "sip": False,
    "source": {
        "address": {
            "any": True
        },
        "port": {
            "any": True
        }
    },
    "tcp": {
        "timeout": 15,
        "urgent": True
    },
    "to": "LAN",
    "udp": {
        "timeout": 30
    },
    "users": {
        "excluded": {
            "none": True
        },
        "included": {
            "all": True
        }
    }
}
org_acl_dict = copy.deepcopy(custom_acl_dict)
wan_lan_acl_dict = {"access_rules": [{"ipv4": custom_acl_dict}]}

cfs_profile_dict = {
    "content_filter": {
        "profile": [
            {
                "name": "CFS Default Profile",
                "uri_list": {
                    "allowed": [
                        {
                            "name": "auto_test"
                        }
                    ],
                    "search_order": "allowed-first",
                    "forbidden_operation": "block"
                },
                "https_filtering": False,
                "smart_filter": False,
                "safe_search": False,
                "threat_api": False,
                "google_force_safe_search": False,
                "youtube_restrict_mode": False,
                "bing_force_safe_search": False,
                "consent": {
                    "required": False
                },
                "custom_header": {
                    "insertion": False
                },
                "reputation": {
                    "active": False
                },
                "category": [
                    {
                        "name": "52. Keyloggers and Monitoring",
                        "operation": "allow"
                    },
                    {
                        "name": "59. Malware",
                        "operation": "allow"
                    },
                    {
                        "name": "86. Phishing and Other Frauds",
                        "operation": "allow"
                    },
                    {
                        "name": "63. Proxy Avoidance and Anonymizers",
                        "operation": "allow"
                    },
                    {
                        "name": "65. Spyware and Adware",
                        "operation": "allow"
                    },
                    {
                        "name": "87. Bot Nets",
                        "operation": "allow"
                    },
                    {
                        "name": "88. SPAM URLs",
                        "operation": "allow"
                    },
                    {
                        "name": "82. Open HTTP Proxies",
                        "operation": "allow"
                    },
                    {
                        "name": "8. Drugs/Illegal Drugs",
                        "operation": "allow"
                    },
                    {
                        "name": "4. Pornography",
                        "operation": "allow"
                    },
                    {
                        "name": "10. Sex Education",
                        "operation": "allow"
                    },
                    {
                        "name": "2. Intimate Apparel/Swimsuit",
                        "operation": "allow"
                    },
                    {
                        "name": "85. Gross",
                        "operation": "allow"
                    },
                    {
                        "name": "3. Nudism",
                        "operation": "allow"
                    },
                    {
                        "name": "12. Alcohol/Tobacco",
                        "operation": "allow"
                    },
                    {
                        "name": "6. Adult/Mature Content",
                        "operation": "allow"
                    },
                    {
                        "name": "34. Personals and Dating",
                        "operation": "allow"
                    },
                    {
                        "name": "57. Internet Watch Foundation CAIC",
                        "operation": "allow"
                    },
                    {
                        "name": "7. Cult/Occult",
                        "operation": "allow"
                    },
                    {
                        "name": "11. Gambling",
                        "operation": "allow"
                    },
                    {
                        "name": "83. Marijuana",
                        "operation": "allow"
                    },
                    {
                        "name": "28. Hacking",
                        "operation": "allow"
                    },
                    {
                        "name": "5. Weapons",
                        "operation": "allow"
                    },
                    {
                        "name": "50. Pay to Surf Sites",
                        "operation": "allow"
                    },
                    {
                        "name": "62. Questionable",
                        "operation": "allow"
                    },
                    {
                        "name": "61. Hate and Racism",
                        "operation": "allow"
                    },
                    {
                        "name": "1. Violence",
                        "operation": "allow"
                    },
                    {
                        "name": "84. Cheating",
                        "operation": "allow"
                    },
                    {
                        "name": "9. Illegal Skills/Questionable Skills",
                        "operation": "allow"
                    },
                    {
                        "name": "16. Abortion/Advocacy Groups",
                        "operation": "allow"
                    },
                    {
                        "name": "60. Radicalization and Extremism",
                        "operation": "allow"
                    },
                    {
                        "name": "58. Social Networking",
                        "operation": "allow"
                    },
                    {
                        "name": "72. Personal Sites and Blogs",
                        "operation": "allow"
                    },
                    {
                        "name": "68. Online Greeting Cards",
                        "operation": "allow"
                    },
                    {
                        "name": "29. Search Engines and Portals",
                        "operation": "block"
                    },
                    {
                        "name": "54. Advertisement",
                        "operation": "allow"
                    },
                    {
                        "name": "30. E-Mail",
                        "operation": "allow"
                    },
                    {
                        "name": "31. Web Communications",
                        "operation": "allow"
                    },
                    {
                        "name": "80. Dynamic Content",
                        "operation": "allow"
                    },
                    {
                        "name": "13. Chat/Instant Messaging (IM)",
                        "operation": "allow"
                    },
                    {
                        "name": "35. Usenet News Groups",
                        "operation": "allow"
                    },
                    {
                        "name": "39. Internet Auctions",
                        "operation": "allow"
                    },
                    {
                        "name": "38. Shopping",
                        "operation": "allow"
                    },
                    {
                        "name": "49. Freeware/Software Downloads",
                        "operation": "allow"
                    },
                    {
                        "name": "14. Arts/Entertainment",
                        "operation": "allow"
                    },
                    {
                        "name": "48. Multimedia",
                        "operation": "allow"
                    },
                    {
                        "name": "81. P2P",
                        "operation": "allow"
                    },
                    {
                        "name": "22. Games",
                        "operation": "allow"
                    },
                    {
                        "name": "75. Music",
                        "operation": "allow"
                    },
                    {
                        "name": "45. Travel",
                        "operation": "allow"
                    },
                    {
                        "name": "70. Home and Garden",
                        "operation": "allow"
                    },
                    {
                        "name": "37. Religion",
                        "operation": "allow"
                    },
                    {
                        "name": "67. Hunting and Fishing",
                        "operation": "allow"
                    },
                    {
                        "name": "41. Society and Lifestyle",
                        "operation": "allow"
                    },
                    {
                        "name": "44. Sports",
                        "operation": "allow"
                    },
                    {
                        "name": "71. Fashion and Beauty",
                        "operation": "allow"
                    },
                    {
                        "name": "69. Recreation and Hobbies",
                        "operation": "allow"
                    },
                    {
                        "name": "47. Humor/Jokes",
                        "operation": "allow"
                    },
                    {
                        "name": "40. Real Estate",
                        "operation": "allow"
                    },
                    {
                        "name": "76. Computer and Internet Security",
                        "operation": "allow"
                    },
                    {
                        "name": "20. Online Banking",
                        "operation": "allow"
                    },
                    {
                        "name": "15. Business and Economy",
                        "operation": "allow"
                    },
                    {
                        "name": "27. Information Technology/Computers",
                        "operation": "allow"
                    },
                    {
                        "name": "24. Military",
                        "operation": "allow"
                    },
                    {
                        "name": "21. Online Brokerage and Trading",
                        "operation": "allow"
                    },
                    {
                        "name": "18. Training and Tools",
                        "operation": "allow"
                    },
                    {
                        "name": "77. Online Personal Storage",
                        "operation": "allow"
                    },
                    {
                        "name": "23. Government",
                        "operation": "allow"
                    },
                    {
                        "name": "78. Content Delivery Networks",
                        "operation": "allow"
                    },
                    {
                        "name": "46. Vehicles",
                        "operation": "allow"
                    },
                    {
                        "name": "55. Web Hosting",
                        "operation": "allow"
                    },
                    {
                        "name": "43. Restaurants and Dining",
                        "operation": "allow"
                    },
                    {
                        "name": "66. Legal",
                        "operation": "allow"
                    },
                    {
                        "name": "73. Local Information",
                        "operation": "allow"
                    },
                    {
                        "name": "32. Job Search",
                        "operation": "allow"
                    },
                    {
                        "name": "74. Translation",
                        "operation": "allow"
                    },
                    {
                        "name": "36. Reference",
                        "operation": "allow"
                    },
                    {
                        "name": "25. Political/Advocacy Groups",
                        "operation": "allow"
                    },
                    {
                        "name": "17. Education",
                        "operation": "allow"
                    },
                    {
                        "name": "53. Kid Friendly",
                        "operation": "allow"
                    },
                    {
                        "name": "33. News and Media",
                        "operation": "allow"
                    },
                    {
                        "name": "26. Health",
                        "operation": "allow"
                    },
                    {
                        "name": "79. Image and Video Search",
                        "operation": "allow"
                    },
                    {
                        "name": "19. Cultural Institutions",
                        "operation": "allow"
                    },
                    {
                        "name": "56. Other",
                        "operation": "allow"
                    },
                    {
                        "name": "64. Not Rated",
                        "operation": "allow"
                    },
                    {
                        "name": "92. Dead Sites",
                        "operation": "allow"
                    },
                    {
                        "name": "91. Parked Domains",
                        "operation": "allow"
                    },
                    {
                        "name": "93. Private IP Addresses",
                        "operation": "allow"
                    }
                ]
            }
        ]
    }
}

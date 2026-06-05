import os
import sys
import re
import time
import copy
import requests
import unittest
import json
from datetime import datetime
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
from lib.modules.API.firewall import CfoActionApi, CfoObjectApi, CfoProfilesApi
from lib.modules.API.log import LogAutomationApi
from lib.modules.API.network import (
    AddressobjectsApi,
    InterfaceIPv4Api,
    InterfaceIPv6Api,
    ZoneObjectsApi,
)
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.policy import NatPolicyApi
from lib.modules.API.securityservices import (
    CFSCustomCategoryApi,
    ContentFilterApi,
    ContentFilterPolicyApi,
)
from lib.modules.API.system import RestartApi, SettingApi, TimeApi, ScheduleApi
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.users import UserLocalApi

# import form test suite root path like definition
suite_path = (
    os.environ["PYTHON_SONICOS_HOME"] + "/User/CFS_with_User/"
)
sys.path.append(suite_path)
sys.path.append(suite_path + "testcases")
TESTPLAN = suite_path + "testplan/CFS_Policy_Function.json"
CONF_PATH = suite_path + "definition/config"
BIN_PATH = suite_path + "definition/bin"
EXP_PATH = "/tmp/schedule_exp"
HTTPS_SERVER_PATH = CONF_PATH + "/httpserver"
HTTP_CERT_PATH = os.environ["PYTHON_COMMON_HOME"] + "/util/dpissl/cert"
HTTP_CFG_PATH = (
    os.environ["PYTHON_SONICOS_HOME"] + "/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/"
)

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip("PC1", "eth1")
PC1_ETH2_IP = os_obj.get_node_interface_ip("PC1", "eth2")
PC1_ETH2_IP_V6 = "1001:1::10"
PC2_ETH1_IP = os_obj.get_node_interface_ip("PC2", "eth1")
PC2_ETH2_IP = os_obj.get_node_interface_ip("PC2", "eth2")
PC2_ETH2_IP_V6 = "1001:2::20"
PC3_ETH1_IP = os_obj.get_node_interface_ip("PC3", "eth1")
PC3_ETH2_IP = os_obj.get_node_interface_ip("PC3", "eth2")
PC3_ETH2_IP_V6 = "1001:3::30"
PC4_ETH1_IP = os_obj.get_node_interface_ip("PC4", "eth1")
PC4_ETH2_IP = os_obj.get_node_interface_ip("PC4", "eth2")
PC4_ETH2_IP_V6 = "2001:100::169"
logger.info(
    f"\n PC1_ETH1_IP: {PC1_ETH1_IP}"
    f"\n PC1_ETH2_IP: {PC1_ETH2_IP}"
    f"\n PC1_ETH2_IP_V6: {PC1_ETH2_IP_V6}"
    f"\n PC2_ETH1_IP: {PC2_ETH1_IP}"
    f"\n PC2_ETH2_IP: {PC2_ETH2_IP}"
    f"\n PC2_ETH2_IP_V6: {PC2_ETH2_IP_V6}"
    f"\n PC3_ETH1_IP: {PC3_ETH1_IP}"
    f"\n PC3_ETH2_IP: {PC3_ETH2_IP}"
    f"\n PC3_ETH2_IP_V6: {PC3_ETH2_IP_V6}"
    f"\n PC4_ETH1_IP: {PC4_ETH1_IP}"
    f"\n PC4_ETH2_IP: {PC4_ETH2_IP}"
    f"\n PC4_ETH2_IP_V6: {PC4_ETH2_IP_V6}"
    f"\n FW_DNS1_IP: {Params.G_DNS1}"
    f"\n FW_DNS2_IP: {Params.G_DNS2}"
)
PC1_login = Host(PC1_ETH1_IP)
PC2_login = Host(PC2_ETH1_IP)
PC3_login = Host(PC3_ETH1_IP)
PC4_login = Host(PC4_ETH1_IP)


# parameters on the fw
class Parameter:
    FIREWALL = "192.168.168.168"
    X1_IP_V4 = "12.12.1.168"
    X1_SUBNET = "12.12.1.0"
    X1_GW = "12.12.1.1"
    X1_NAT = "12.12.1.0"
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_IP_V6 = "2001:100::168"
    X1_SUBNET_V6 = "2001:100::"
    X2_IP_V4 = "192.168.2.168"
    X2_SUBNET = "192.168.2.0"
    X2_GW = "192.168.2.168"
    X2_IP_V6 = "1001:2::168"
    X3_IP_V4 = "192.168.3.168"
    X3_SUBNET = "192.168.3.0"
    X3_GW = "192.168.3.168"
    X3_IP_V6 = "1001:3::168"
    X0_IP_V6 = "1001:1::168"
    MASK = "255.255.255.0"
    # Route 1
    RT_HOST_1 = "10.0.0.0"
    RT_MASK_1 = "255.0.0.0"
    PC1_GW = "192.168.2.1"
    # Default Route
    RT_DEF_HOST = "0.0.0.0"
    RT_DEF_MASK = "0.0.0.0"


class CaseParms:
    CUS_AG_NAME = "test_cus_ag"
    CUS_AO_NAME = "test_cus_ao"
    RANGE_AO_NAME = "test_range_ao"
    RANGE_VALUE = "192.168.2.10,192.168.2.30"
    NETWORK_AO_NAME = "test_network_ao"
    NETWORK_VALUE = f"{Parameter.X2_SUBNET},{Parameter.MASK}"
    HOST_V4_AO_NAME = "test_host_v4_ao"
    HOST_V6_AO_NAME = "test_host_v6_ao"
    CUS_CFS_PROFILE_NAME = "test_cus_cfs_profile_unblock_search"
    URI_OBJ_NAME_1 = "test_uri_obj_1"
    CFS_TEST_URL_1 = "pc3.baidu.com"
    URI_OBJ_NAME_2 = "test_uri_obj_2"
    CFS_TEST_URL_2 = "pc4.baidu.com"
    URI_OBJ_NAME_3 = "test_uri_obj_3"
    CFS_TEST_URL_3 = "pc2.google.co.jp"
    CUS_CFS_ACT_NAME = "test_cus_cfs_action"
    URI_OBJ_NAME_4 = "test_uri_obj_4"
    CFS_TEST_URL_4 = PC4_ETH2_IP
    URI_OBJ_NAME_5 = "test_uri_obj_5"
    CFS_TEST_URL_5 = f"{PC4_ETH2_IP}/test_001.txt"
    URI_OBJ_NAME_6 = "test_uri_obj_6"
    CFS_TEST_URL_6 = "pc3.baidu.com/test_001.txt"
    LOCAL_USER_1 = "local_user_1"
    LOCAL_USER_2 = "local_user_2"
    USER_GROUP_1 = "test_group_1"
    USER_GROUP_2 = "test_group_2"
    GUEST_USER = "guest_user_1"


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user="admin",
    password=Params.G_NEW_PASSWORD,
    supported_config_mode="api",
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user="admin",
    password=Params.G_NEW_PASSWORD,
    supported_config_mode="cli-ssh",
)
addressobjectsapi = AddressobjectsApi(fw)
addressobjectgroupapi = AddressObjectGroupApi(fw)
cfsactionapi = CfoActionApi(fw)
cfsapi = ContentFilterApi(fw)
cfscuscateapi = CFSCustomCategoryApi(fw)
cfsobjectapi = CfoObjectApi(fw)
cfspolicyapi = ContentFilterPolicyApi(fw)
cfsprofileapi = CfoProfilesApi(fw)
interfacev4api = InterfaceIPv4Api(fw)
interfacev6api = InterfaceIPv6Api(fw)
licensecli = LicenseCli(fw_cli)
logautoapi = LogAutomationApi(fw)
natpolicyapi = NatPolicyApi(fw)
restartapi = RestartApi(fw)
scheduleapi = ScheduleApi(fw)
settingapi = SettingApi(fw)
timeapi = TimeApi(fw)
userlocalapi = UserLocalApi(fw)
zoneapi = ZoneObjectsApi(fw)


# Init Settings
x1_wan_v4_dict = {
    "if": "X1",
    "zone": "WAN",
    "mode": "static",
    "ip": Parameter.X1_IP_V4,
    "netmask": Parameter.MASK,
    "gateway": Parameter.X1_GW,
    "dns1": PC2_ETH2_IP,
    "dns2": Parameter.X1_DNS2,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_snmp": True,
    "mgmt_ping": True,
    "user_https": True,
}

x1_wan_v6_dict = {
    "name": "X1",
    "mode": "static",
    "zone": "WAN",
    "ip": Parameter.X1_IP_V6,
    "prefix_length": 64,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_snmp": True,
    "mgmt_ping": True,
    "user_https": True,
}

x2_lan_v4_dict = {
    "if": "X2",
    "zone": "LAN",
    "mode": "static",
    "ip": Parameter.X2_IP_V4,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_ping": True,
    "user_https": True,
    "mgmt_snmp": True,
}

x2_lan_v6_dict = {
    "name": "X2",
    "mode": "static",
    "zone": "LAN",
    "ip": Parameter.X2_IP_V6,
    "prefix_length": 64,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_snmp": True,
    "mgmt_ping": True,
    "user_https": True,
}

x3_lan_v4_dict = {
    "if": "X3",
    "zone": "LAN",
    "mode": "static",
    "ip": Parameter.X3_IP_V4,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_ping": True,
    "user_https": True,
    "mgmt_snmp": True,
}

x3_lan_v6_dict = {
    "name": "X3",
    "mode": "static",
    "zone": "LAN",
    "ip": Parameter.X3_IP_V6,
    "prefix_length": 64,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_snmp": True,
    "mgmt_ping": True,
    "user_https": True,
}

ipv6_nat_dict = {
    "nat_policies": [
        {
            "ipv6": {
                "comment": "auto_test_ipv6_nat",
                "destination": {"any": True},
                "enable": True,
                "inbound": "any",
                "name": "cfs_v6_nat_rule",
                "outbound": "any",
                "priority": {"auto": True},
                "reflexive": False,
                "service": {"any": True},
                "source": {"any": True},
                "source_port_remap": True,
                "ticket": {"tag1": "", "tag2": "", "tag3": ""},
                "translated_destination": {"original": True},
                "translated_service": {"original": True},
                "translated_source": {"name": "X1 IPv6 Primary Static Address"},
            }
        }
    ]
}

cfs_service_dict = {
    "content_filter": {
        "filter_type": "cfs",
        "cfs": {
            "enable": True,
            "exclude": {
                "administrator": False,
                "address": {},
            },
        },
    }
}

cfs_def_policy_dict = {
    "content_filter": {
        "cfs": {
            "policy": [
                {
                    "name": "CFS Default Policy",
                    "source": {
                        "zone": "LAN",
                        "address": {
                            "included": {"any": True},
                            "excluded": {"none": True},
                        },
                    },
                    "destination": {"zone": "WAN"},
                    "user": {"included": {"all": True}, "excluded": {"none": True}},
                    "schedule": {"always_on": True},
                    "profile": "CFS Default Profile",
                    "action": "CFS Default Action",
                    "enable": True,
                    "priority": {"value": 1},
                }
            ]
        }
    }
}

cfs_def_profile_dict = {
    "content_filter": {
        "profile": [
            {
                "name": "CFS Default Profile",
                "threat_api": False,
                "bing_force_safe_search": False,
                "consent": {"required": False},
                "custom_header": {"insertion": False},
                "google_force_safe_search": False,
                "https_filtering": False,
                "reputation": {"active": False},
                "safe_search": False,
                "smart_filter": False,
                "uri_list": {
                    "forbidden_operation": "block",
                    "search_order": "allowed-first",
                },
                "youtube_restrict_mode": False,
                "category": [
                    {"name": "52. Keyloggers and Monitoring", "operation": "block"},
                    {"name": "59. Malware", "operation": "block"},
                    {"name": "86. Phishing and Other Frauds", "operation": "block"},
                    {
                        "name": "63. Proxy Avoidance and Anonymizers",
                        "operation": "block",
                    },
                    {"name": "65. Spyware and Adware", "operation": "block"},
                    {"name": "87. Bot Nets", "operation": "block"},
                    {"name": "88. SPAM URLs", "operation": "block"},
                    {"name": "82. Open HTTP Proxies", "operation": "block"},
                    {"name": "8. Drugs/Illegal Drugs", "operation": "block"},
                    {"name": "4. Pornography", "operation": "block"},
                    {"name": "10. Sex Education", "operation": "block"},
                    {"name": "2. Intimate Apparel/Swimsuit", "operation": "block"},
                    {"name": "85. Gross", "operation": "block"},
                    {"name": "3. Nudism", "operation": "block"},
                    {"name": "12. Alcohol/Tobacco", "operation": "block"},
                    {"name": "6. Adult/Mature Content", "operation": "block"},
                    {"name": "34. Personals and Dating", "operation": "allow"},
                    {
                        "name": "57. Internet Watch Foundation CAIC",
                        "operation": "block",
                    },
                    {"name": "7. Cult/Occult", "operation": "block"},
                    {"name": "11. Gambling", "operation": "block"},
                    {"name": "83. Marijuana", "operation": "block"},
                    {"name": "28. Hacking", "operation": "block"},
                    {"name": "5. Weapons", "operation": "block"},
                    {"name": "50. Pay to Surf Sites", "operation": "allow"},
                    {"name": "62. Questionable", "operation": "block"},
                    {"name": "61. Hate and Racism", "operation": "block"},
                    {"name": "1. Violence", "operation": "block"},
                    {"name": "84. Cheating", "operation": "block"},
                    {
                        "name": "9. Illegal Skills/Questionable Skills",
                        "operation": "block",
                    },
                    {"name": "16. Abortion/Advocacy Groups", "operation": "block"},
                    {"name": "60. Radicalization and Extremism", "operation": "block"},
                    {"name": "58. Social Networking", "operation": "allow"},
                    {"name": "72. Personal Sites and Blogs", "operation": "allow"},
                    {"name": "68. Online Greeting Cards", "operation": "allow"},
                    {"name": "29. Search Engines and Portals", "operation": "block"},
                    {"name": "54. Advertisement", "operation": "allow"},
                    {"name": "30. E-Mail", "operation": "allow"},
                    {"name": "31. Web Communications", "operation": "allow"},
                    {"name": "80. Dynamic Content", "operation": "allow"},
                    {"name": "13. Chat/Instant Messaging (IM)", "operation": "allow"},
                    {"name": "35. Usenet News Groups", "operation": "allow"},
                    {"name": "39. Internet Auctions", "operation": "allow"},
                    {"name": "38. Shopping", "operation": "allow"},
                    {"name": "49. Freeware/Software Downloads", "operation": "allow"},
                    {"name": "14. Arts/Entertainment", "operation": "allow"},
                    {"name": "48. Multimedia", "operation": "allow"},
                    {"name": "81. P2P", "operation": "allow"},
                    {"name": "22. Games", "operation": "allow"},
                    {"name": "75. Music", "operation": "allow"},
                    {"name": "45. Travel", "operation": "allow"},
                    {"name": "70. Home and Garden", "operation": "allow"},
                    {"name": "37. Religion", "operation": "allow"},
                    {"name": "67. Hunting and Fishing", "operation": "allow"},
                    {"name": "41. Society and Lifestyle", "operation": "allow"},
                    {"name": "44. Sports", "operation": "allow"},
                    {"name": "71. Fashion and Beauty", "operation": "allow"},
                    {"name": "69. Recreation and Hobbies", "operation": "allow"},
                    {"name": "47. Humor/Jokes", "operation": "allow"},
                    {"name": "40. Real Estate", "operation": "allow"},
                    {
                        "name": "76. Computer and Internet Security",
                        "operation": "allow",
                    },
                    {"name": "20. Online Banking", "operation": "allow"},
                    {"name": "15. Business and Economy", "operation": "allow"},
                    {
                        "name": "27. Information Technology/Computers",
                        "operation": "allow",
                    },
                    {"name": "24. Military", "operation": "allow"},
                    {"name": "21. Online Brokerage and Trading", "operation": "allow"},
                    {"name": "18. Training and Tools", "operation": "allow"},
                    {"name": "77. Online Personal Storage", "operation": "allow"},
                    {"name": "23. Government", "operation": "allow"},
                    {"name": "78. Content Delivery Networks", "operation": "allow"},
                    {"name": "46. Vehicles", "operation": "allow"},
                    {"name": "55. Web Hosting", "operation": "allow"},
                    {"name": "43. Restaurants and Dining", "operation": "allow"},
                    {"name": "66. Legal", "operation": "allow"},
                    {"name": "73. Local Information", "operation": "allow"},
                    {"name": "32. Job Search", "operation": "allow"},
                    {"name": "74. Translation", "operation": "allow"},
                    {"name": "36. Reference", "operation": "allow"},
                    {"name": "25. Political/Advocacy Groups", "operation": "allow"},
                    {"name": "17. Education", "operation": "allow"},
                    {"name": "53. Kid Friendly", "operation": "allow"},
                    {"name": "33. News and Media", "operation": "allow"},
                    {"name": "26. Health", "operation": "allow"},
                    {"name": "79. Image and Video Search", "operation": "allow"},
                    {"name": "19. Cultural Institutions", "operation": "allow"},
                    {"name": "56. Other", "operation": "allow"},
                    {"name": "64. Not Rated", "operation": "allow"},
                    {"name": "92. Dead Sites", "operation": "allow"},
                    {"name": "91. Parked Domains", "operation": "allow"},
                    {"name": "93. Private IP Addresses", "operation": "allow"},
                ],
            }
        ]
    }
}

cfs_def_action_dict = {
    "content_filter": {
        "action": [
            {
                "name": "CFS Default Action",
                "wipe_cookies": False,
                "flow_reporting": False,
                "block": {"page": {"default": True}},
                "passphrase": {
                    "page": {"default": True},
                    "password": "",
                    "active_time": 60,
                },
                "confirm": {"page": {"default": True}, "active_time": 60},
                "bandwidth_management": {
                    "aggregation_method": "policy",
                    "usage_tracking": False,
                    "egress": {},
                    "ingress": {},
                },
            }
        ]
    }
}

uri_list_obj_dict = {
    "content_filter": {
        "uri_list_object": [
            {
                "name": "obj_name",
                "type": "uri",
                "uri": [{"uri": "uri_path"}],
            }
        ]
    }
}

uri_list_kw_obj_dict = {
    "content_filter": {
        "uri_list_object": [
            {
                "name": "obj_name",
                "type": "uri",
                "keyword": [{"keyword": "uri_path"}],
            }
        ]
    }
}

guest_user = {
    "action": "add",
    "username": CaseParms.GUEST_USER,
    "userpassword": Params.G_NEW_PASSWORD,
    "member_of": ["Guest Administrators"],
}

local_user_1 = {
    "action": "add",
    "username": CaseParms.LOCAL_USER_1,
    "userpassword": Params.G_NEW_PASSWORD,
    "member_of": ["SonicWALL Administrators"],
}

local_user_2 = {
    "action": "add",
    "username": CaseParms.LOCAL_USER_2,
    "userpassword": Params.G_NEW_PASSWORD,
    "member_of": ["SonicWALL Administrators"],
}

user_group_1 = {
    "user": {
        "local": {
            "group": [
                {
                    "name": CaseParms.USER_GROUP_1,
                    "member": [{"name": CaseParms.LOCAL_USER_1}],
                }
            ]
        }
    }
}

user_group_2 = {
    "user": {
        "local": {
            "group": [
                {
                    "name": CaseParms.USER_GROUP_2,
                    "member": [{"name": CaseParms.LOCAL_USER_2}],
                }
            ]
        }
    }
}

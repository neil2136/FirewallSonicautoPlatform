import os
import sys
import copy
import ast
import re
import time
import json
import requests
import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, FirewallCLI
from util.enhancedinfo import show_testcase_info

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api, AddressobjectsApi, IpHelperApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.CLI.system import LicenseCli,AdminCli
from lib.modules.API.system import RestartApi, SettingApi
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.API.securityservices import ContentFilterPolicyApi
from lib.modules.API.firewall import CfoProfilesApi
from lib.modules.CLI.network import InterfaceCli
from lib.modules.ui.fw_page import FWPage

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Address_Objects_TP158_part2'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/address_objects_tp158_part2.json'
CONF_PATH = suite_path + '/definition/config'

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

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            f"\n PC4_ETH0_IP : {PC4_ETH0_IP}"
            f"\n PC4_ETH1_IP : {PC4_ETH1_IP}"
            )

console_info_UTM = os_obj.get_console_info('UTM')
logger.info(console_info_UTM)
if console_info_UTM:
    consvr_UTM = console_info_UTM[0]
    conport_UTM = console_info_UTM[1]

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)
PC4_Login = Host(PC4_ETH0_IP)


#################################################################################################################
#
#                                                                                                              #
#  PC1(eth1)---------(192.168.168.168 x0)DUT x1(12.12.1.168)---------PC4 eth1 (12.12.1.30)                         #
#  PC2(eth1)----------(192.168.2.168 x2)|                           DNS server,http server(eth1)
#  PC3(eth1)----------(192.168.2.168 x2)|
#                                                                                                              #
#
#################################################################################################################


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_NET = '12.12.1.0'
    MASK = '255.255.255.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X2_IP = '192.168.2.168'
    X2_SUBNET = '192.168.2.0'
    X1_REMOTE_IP = '12.12.1.201'
    FQDN_Hostname = 'pc4.baidu.com'
    # below are new added for new cases
    X0_V6_IP = '1001:1::168'
    X0_V6_PREFIX = '1001:1::'
    PREFIX_LENGTH = 64

class ParamCases:
    tc01_x0linklocal = ''

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='cli-ssh')
utm_fw_console = Firewall(
    ip=Parameter.FIREWALL,
    console_ip=consvr_UTM,
    console_port=conport_UTM,
    user='admin',
    password='password',
    supported_config_mode='cli-console'
)
fwpageui = FWPage(ip, user='admin',password='S0nic@uto')


interfacev4api = InterfaceIPv4Api(fw_api)
interfaceipv6api = InterfaceIPv6Api(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
addressobjectgroupapi = AddressObjectGroupApi(fw_cli)
settingapi = SettingApi(fw_api)
vpnbasesettingapi = VpnbasesettingApi(fw_api)
contentfilterpolicyapi = ContentFilterPolicyApi(fw_api)
licensecli = LicenseCli(fw_cli)
cfoprofilesapi = CfoProfilesApi(fw_api)
iphelperapi = IpHelperApi(fw_api)
utm_adminconsole = AdminCli(utm_fw_console)
utm_interfaceconsole = InterfaceCli(utm_fw_console)

edit_cfs_default_policy_dict = {
    "content_filter": {
        "cfs": {
            "policy": [
                {
                    "name": "CFS Default Policy",
                    "source": {
                        "zone": "LAN",
                        "address": {
                            "included": {
                                "any": True
                            },
                            "excluded": {
                                "none": True
                            }
                        }
                    },
                    "destination": {
                        "zone": "WAN"
                    },
                    "user": {
                        "included": {
                            "all": True
                        },
                        "excluded": {
                            "none": True
                        }
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "profile": "CFS Default Profile",
                    "action": "CFS Default Action",
                    "priority": {
                        "value": 1
                    }
                }
            ]
        }
    }
}

edit_cfs_profile_dict = {
    "content_filter": {
        "profile": [
            {
                "name": "CFS Default Profile",
                "uri_list": {
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
                        "operation": "block"
                    },
                    {
                        "name": "59. Malware",
                        "operation": "block"
                    },
                    {
                        "name": "86. Phishing and Other Frauds",
                        "operation": "block"
                    },
                    {
                        "name": "63. Proxy Avoidance and Anonymizers",
                        "operation": "block"
                    },
                    {
                        "name": "65. Spyware and Adware",
                        "operation": "block"
                    },
                    {
                        "name": "87. Bot Nets",
                        "operation": "block"
                    },
                    {
                        "name": "88. SPAM URLs",
                        "operation": "block"
                    },
                    {
                        "name": "82. Open HTTP Proxies",
                        "operation": "block"
                    },
                    {
                        "name": "8. Drugs/Illegal Drugs",
                        "operation": "block"
                    },
                    {
                        "name": "4. Pornography",
                        "operation": "block"
                    },
                    {
                        "name": "10. Sex Education",
                        "operation": "block"
                    },
                    {
                        "name": "2. Intimate Apparel/Swimsuit",
                        "operation": "block"
                    },
                    {
                        "name": "85. Gross",
                        "operation": "block"
                    },
                    {
                        "name": "3. Nudism",
                        "operation": "block"
                    },
                    {
                        "name": "12. Alcohol/Tobacco",
                        "operation": "block"
                    },
                    {
                        "name": "6. Adult/Mature Content",
                        "operation": "block"
                    },
                    {
                        "name": "34. Personals and Dating",
                        "operation": "allow"
                    },
                    {
                        "name": "57. Internet Watch Foundation CAIC",
                        "operation": "block"
                    },
                    {
                        "name": "7. Cult/Occult",
                        "operation": "block"
                    },
                    {
                        "name": "11. Gambling",
                        "operation": "block"
                    },
                    {
                        "name": "83. Marijuana",
                        "operation": "block"
                    },
                    {
                        "name": "28. Hacking",
                        "operation": "block"
                    },
                    {
                        "name": "5. Weapons",
                        "operation": "block"
                    },
                    {
                        "name": "50. Pay to Surf Sites",
                        "operation": "allow"
                    },
                    {
                        "name": "62. Questionable",
                        "operation": "block"
                    },
                    {
                        "name": "61. Hate and Racism",
                        "operation": "block"
                    },
                    {
                        "name": "1. Violence",
                        "operation": "block"
                    },
                    {
                        "name": "84. Cheating",
                        "operation": "block"
                    },
                    {
                        "name": "9. Illegal Skills/Questionable Skills",
                        "operation": "block"
                    },
                    {
                        "name": "16. Abortion/Advocacy Groups",
                        "operation": "block"
                    },
                    {
                        "name": "60. Radicalization and Extremism",
                        "operation": "block"
                    },
                    {
                        "name": "58. Social Networking",
                        "operation": "block"
                    },
                    {
                        "name": "72. Personal Sites and Blogs",
                        "operation": "block"
                    },
                    {
                        "name": "68. Online Greeting Cards",
                        "operation": "block"
                    },
                    {
                        "name": "29. Search Engines and Portals",
                        "operation": "block"
                    },
                    {
                        "name": "54. Advertisement",
                        "operation": "block"
                    },
                    {
                        "name": "30. E-Mail",
                        "operation": "block"
                    },
                    {
                        "name": "31. Web Communications",
                        "operation": "block"
                    },
                    {
                        "name": "80. Dynamic Content",
                        "operation": "block"
                    },
                    {
                        "name": "13. Chat/Instant Messaging (IM)",
                        "operation": "block"
                    },
                    {
                        "name": "35. Usenet News Groups",
                        "operation": "block"
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

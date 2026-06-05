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

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, FirewallCLI
from util.enhancedinfo import show_testcase_info

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, InterfaceIPv6Api, AddressobjectsApi, NetworkMonitorApi, \
    ZoneObjectsApi, DnsSettingsApi, DnsProxyApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.CLI.network import NetworkMonitorCli, RouteCli
from lib.modules.API.system import DiagnosticApi, PacketmonitorApi, RestartApi, SettingApi
from lib.modules.API.policy import NatPolicyApi, RoutePolicyApi
from lib.modules.API.diag import DiagApi
from lib.modules.API.log import LogSettingsApi, LogCategoryApi, LogMonitorApi
# from lib.modules.API.firewall import AccessRuleIPv6Api
from lib.modules.API.accessrule import Access_Rule
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_FQDN_Object'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/ipv6_fqdn_object.json'
CONF_PATH = suite_path + '/definition/config'
HTTPS_SERVER_PATH = CONF_PATH + '/httpserver'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC2_ETH1_IPv6 = '1001:2::20'
PC3_ETH1_IPv6 = '2001:20::30'


logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            f"\n PC2_ETH2_IP : {PC2_ETH2_IP}"
            f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            )

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)


#################################################################################################################
#
#                                                                                                              #
#  PC1(eth1)---------(192.168.168.168 x0)DUT x1(2001:20::168)---------pc3(2001:20::30)                         #
#  PC2(eth1)----------(1001:2::168 x2)|                              DNS server(eth1)                          #
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
    X2_GW = '192.168.2.1'

    X0_IPv6 = '1001:1::168'
    X1_IPv6 = '2001:20::168'
    X1_IPv6_SUBNET = '2001:20::'
    X2_IPv6 = '1001:2::168'
    FQDN_Hostname_one_ipv6 = '1ipv6pc3.baidu.com'
    FQDN_Hostname_one_ipv6_not_pc3 = '1ipv6notpc3.baidu.com'
    FQDN_Hostname_four_ipv6 = '4ipv6pc3.baidu.com'
    FQDN_Mixed_Hostname = 'pc3mix.baidu.com'
    FQDN_Wildcard_Hostname = '*.baidu.com'
    IPv6_Accessrule_Name = 'ipv6testrule'
    IPv6_Routepolicy_Name = 'ipv6routetest'


class ParamCases:
    tc10result = False
    tc28result = False
    tc25result = []


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

interfacev4api = InterfaceIPv4Api(fw_api)
interfaceipv6api = InterfaceIPv6Api(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
routepolicyapi = RoutePolicyApi(fw_api)
ne_routepolicyapi = RoutePolicyApi(fw_api)
networkmonitorapi = NetworkMonitorApi(fw_api)
networkmonitorcli = NetworkMonitorCli(fw_cli)
routecli = RouteCli(fw_cli)
addressobjectgroupapi = AddressObjectGroupApi(fw_cli)
natpolicyapi = NatPolicyApi(fw_api)
diagnosticapi = DiagnosticApi(fw_api)
diagapi = DiagApi(fw_api)
packetmonitorapi = PacketmonitorApi(fw_api)
logcategapi = LogCategoryApi(fw_api)
logmonitorapi = LogMonitorApi(fw_api)
accessrule = Access_Rule(fw_api)
zoneobjectsapi = ZoneObjectsApi(fw_api)
dnssettingsapi = DnsSettingsApi(fw_api)
# accessruleipv6api = AccessRuleIPv6Api(fw_api)
restartapi = RestartApi(fw_api)
settingapi = SettingApi(fw_api)
licensecli = LicenseCli(fw_cli)
dnsproxyapi = DnsProxyApi(fw_api)

ipv6_nm_ping_non_explicit_with_fqdn_target_dict = {
    "network_monitors": [
        {
            "policy": {
                "ipv6": {
                    "name": "ipv6pingprobe",
                    "probe": {
                        "target": {
                            "name": "tc25.baidu.com"
                        },
                        "type": {
                            "ping": "non-explicit"
                        },
                        "interval": 5
                    },
                    "reply_timeout": 1,
                    "interval": {
                        "missed": 3,
                        "successful": 3
                    },
                    "must_respond": False,
                    "comment": ""
                }
            }
        }
    ]
}

route_policy_with_probe_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "pbr_with_probe",
                "comment": "",
                "interface": "X1",
                "metric": 20,
                "service": {
                    "any": True
                },
                "gateway": {
                    "name": "X1 Default Gateway"
                },
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "10.103.202.200"
                },
                "disable_on_interface_down": False,
                "vpn_precedence": False,
                "probe": "nm_ping_non_explicit",
                "distance": {
                    "auto": True
                },
                "disable_when_probes_succeed": True,
                "default_probe_state_up": False,
                "tos": "0x00",
                "mask": "0x00",
                "type": "standard"
            }
        }
    ]
}

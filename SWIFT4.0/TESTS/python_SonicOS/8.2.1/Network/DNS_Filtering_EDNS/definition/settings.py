import os
import sys
import re
import time
import copy


from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test, skip_if_fail_method, repeat_method
from runner.utils.assertion import Assertion
from runner.settings import Params, logger


# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.enhancedinfo import show_testcase_info
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall


# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import DnsSettingsApi, DnsProxyApi
from lib.modules.API.system import PacketmonitorApi
from lib.modules.API.firewall import DNSRuleApi
from lib.modules.CLI.system import LicenseCli


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_EDNS/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/DNS_Filtering_EDNS.json'

# PC addresses
OpenS = Openstack(Params.testbed)
PC1_ETH0_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}')
PC1_LOGIN = Host(PC1_ETH0_IP)


# parameters on the firewall
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    Route_Host_1 = '10.0.0.0'
    Route_Mask_1 = '255.0.0.0'
    Route_Mask_2 = '0.0.0.0'
    PC1_GW = '16.16.1.1'
    Route_Host_2 = '0.0.0.0'
    Neustar_server = '156.154.54.200'


# parameters used by suite cases
class CParam:
    EDNS_Flag_On = 'Additional RRs: 1'
    EDNS_Flag_Off = 'Additional RRs: 0'
    EDNS_Record = 'OPT=15: cf 02'
    Pkt_EDNS = 'Option Code: Unknown (15)'
    Pkt_Category = 'Option Data: cf02'
    Domain = 'www.ea.com'


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_api = InterfaceIPv4Api(fw)
dnsRule_api = DNSRuleApi(fw)
dnsSett_api = DnsSettingsApi(fw)
dnspxy_api = DnsProxyApi(fw)
license_cli = LicenseCli(fw_cli)
packet_api = PacketmonitorApi(fw)


# parameters on the test cases
X1_static_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
}
filter_rule_dict = {
    "dns_policies": [
        {
            "name": "Filter",
            "priority": {
                "manual": 1
            },
            "enable": True,
            "source": {
                "address": {
                    "any": True
                }
            },
            "service": {
                "name": "DNS (Name Service) UDP"
            },
            "from": "X0",
            "action": {
                "filter_profile": "Default Profile"
            }
        }
    ]
}
proxy_rule_dict = {
    "dns_policies": [
        {
            "name": "Proxy",
            "priority": {
                "manual": 2
            },
            "enable": True,
            "source": {
                "address": {
                    "any": True
                }
            },
            "service": {
                "name": "DNS (Name Service) UDP"
            },
            "from": "X0",
            "action": {
                "proxy":True
            },
            "proxy_mode":"ipv4-ipv4"
        }
    ]
}

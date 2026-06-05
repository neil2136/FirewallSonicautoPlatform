import os
import sys
import re
import time
import copy
import json


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
from modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import DNSSecurityApi, DnsFilteringApi, DnsSettingsApi, DnsProxyApi
from modules.API.firewall import DNSRuleApi
from modules.CLI.network import DNSfilteringCli
from modules.CLI.system import LicenseCli
from modules.API.system import DiagnosticApi


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Cache/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/DNS_Filtering_Cache.json'

# PC addresses
OpenS = Openstack(Params.testbed)
PC1_ETH0_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}')
PC1_LOGIN = Host(PC1_ETH0_IP)


# parameters on the firewall
class Parameter():
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
    Filtering_server = '156.154.54.200'


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_api = InterfaceIPv4Api(fw)
dnsSec_api = DNSSecurityApi(fw)
dnsRule_api = DNSRuleApi(fw)
dnsFilter_api = DnsFilteringApi(fw)
dnsSett_api = DnsSettingsApi(fw)
dnspxy_api = DnsProxyApi(fw)
dnsSec_cli = DNSfilteringCli(fw_cli)
license_cli = LicenseCli(fw_cli)
diag_api = DiagnosticApi(fw)


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
add_rule_dict = {
    "dns_policies": [
        {
            "name": "test",
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
categorized_domains = {
    'adultswim.com': 'Adult',
    'www.ea.com': 'Gaming',
    'www.gamblingsites.org': 'Gambling',
    'theonlygames.com': 'Malware',
    'shibaswap.com': 'Phishing',
    'sitenable.ch': 'Anonymous Proxies',
    'loveread.me': 'Social',
    'bleacherreport.com': 'Sports',
    'doramy.club': 'Hacking/Warez/P2P',
    'grabagun.com': 'Violence',
    'www.jiayuan.com': 'Dating',
    'heavengifts.com': 'Drugs',
    'jiushang.cn': 'Alcohol',
    'henrymakow.com': 'Discrimination/Hate',
    'ithome.com': 'Spyware',
    'myfreecams.com': 'Pornography',
    'baidu.com':' '
}
categorized_domains_backup = {
    'Adult': ['onlyfans.com', 'seedit.com', '9gag.com'],
    'Gaming': ['ubisoft.com', 'nintendo.com', 'ign.com'],
    'Gambling': ['bet365.com', 'bet9ja.com', 'flashscore.com'],
    'Malware': ['chinadd.cn', 'chinaznj.com', 'yxdown.com'],
    'Phishing': ['adskeeper.co.uk'], 
    'Anonymous Proxies': ['nordvpn.com', 'ppvpn.net', 'proxysite.com'],
    'Social': ['facebook.com', 'douban.com', 'zhihu.com'],
    'Sports': ['goal.com', 'nba.com', 'cbssports.com'],
    'Hacking/Warez/P2P': ['thepiratebay.org', 'utorrent.com', 'cn163.ne'],
    'Violence': ['sportsmansoutdoorsuperstore.com', 'waffenbude.de', 'arms24.com'],
    'Dating': ['tinder.com', 'seeking.com', 'muslima.com'],
    'Drugs': ['leafly.com', 'marijuana.com'],
    'Alcohol': ['fairesagnole.eu', 'totalwine.com', 'birraichnusa.it'],
    'Discrimination/Hate': ['palinfo.com'], 
    'Spyware': ['doyo.cn'],
    'Pornography': ['playboy.com', 'pornhub.com', 'xnxx.com', 'sex.com'],
    'No Category': ['bing.com']
}
re_test_category_list = []
cache_result_dict = {
    'Adult': False,
    'Gaming': False,
    'Gambling': False,
    'Malware': False,
    'Phishing': False,
    'Anonymous Proxies': False,
    'Social': False,
    'Sports': False,
    'Hacking/Warez/P2P': False,
    'Violence': False,
    'Dating': False,
    'Drugs': False,
    'Alcohol': False,
    'Discrimination/Hate': False,
    'Spyware': False,
    'Pornography': False,
    'No Category': False
}
ipv6_domain = "playboy.com"
ipv6_category = "Pornography"

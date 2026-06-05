import os
import sys
import unittest
from time import sleep
import paramunittest
import copy


sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Whitelist')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from utm import Firewall,FirewallAPI
from runner.unittest.setup import Test, repeat_method
from runner.settings import Params, logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from lib.modules.API import network, system
from networkdevice import Host
from lib.modules.CLI.system import LicenseCli


TEST_PATH = os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Whitelist'


class Parameter():
    FIREWALL = '192.168.168.168'

    TESTPLAN = TEST_PATH + '/testplan/dns_filtering_whitelist.json'

    white_list = 'www.ea.com'
    whitelists = ['www.123.com', 'ppp.com', 'hello.com', 'ios.org', '886']

    dns_policy_dict = {
        "dns_policies":[{
            "action":{
                "filter_profile": "Default Profile"
            },
            "comment":"",
            "connection_limit":{
                "source":{
                    "enable":False, 
                    "threshold": {"value":128}
                }
            },
            "enable":True,
            "from":"X0",
            "max_connections":100,
            "name":"my dns rule",
            "priority":{"manual":1},
            "schedule":{"always_on":True},
            "service":{"name":"DNS (Name Service) UDP"},
            "source":{
                "address":{"any":True}
            },
            "ticket":{"tag1":"","tag2":"","tag3":""},
            "uuid":""
        }]
    }

    settings_dict = {
        "dns_security":{
            "dns_filtering":{
                "forged_ip":{
                    "ipv4":"127.0.0.1",
                    "ipv6":"::1"
                },
            }
        }
    }


fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
interface_v4 = network.InterfaceIPv4Api(fw)
tsr = system.DiagnosticApi(fw)
localhost = Host('localhost')
dnsfilter = network.DnsFilteringApi(fw)
dnspolicy = network.DnsPolicyApi(fw)
opt = copy.deepcopy(Parameter.settings_dict)


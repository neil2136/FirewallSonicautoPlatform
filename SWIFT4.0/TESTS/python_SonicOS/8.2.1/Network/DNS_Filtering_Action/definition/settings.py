import sys
import re
import os
import time
import unittest
from nose_parameterized import parameterized
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Action')
from runner.unittest.setup import Test, repeat_method
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import firewall
from utm import Firewall
from lib.modules.API.network import DnsFilteringApi
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from lib.modules.API.system import PacketmonitorApi
from networkdevice import Host
from util.openstack import Openstack
from lib.modules.CLI.network import DNSfilteringCli
from util.enhancedinfo import show_testcase_info
from lib.modules.API.system import PacketmonitorApi
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.log import LogSettingsApi,LogCategoryApi,LogMonitorApi


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
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/DNS_Filtering_Action/testplan/DNS_Filtering_Action.json"


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
zone_api = network.ZoneObjectsApi(fw)
interface_api = network.InterfaceIPv4Api(fw)
dnssec_obj = network.DNSSecurityApi(fw)
dnsrule_obj = firewall.DNSRuleApi(fw)
dns_filtering_obj = DnsFilteringApi(fw)
down_tsr_obj = system.DiagnosticApi(fw)
forged_ip_cli = DNSfilteringCli(fw)
packet_obj = PacketmonitorApi(fw)
log_set = LogSettingsApi(fw)
log_cata = LogCategoryApi(fw)
log_monitor = LogMonitorApi(fw)

add_file = {  
    "dns_security": {
        "dns_filtering": {
            "profile": [
                {
                    "name": "test2",
                    "actions": "{\"1\":0,\"2\":0,\"3\":0,\"4\":0}"
                }
            ]
        }
    }
}

add_rule = {
    "dns_policies": [
        {
            "name": "test2",
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
                "filter_profile": "test2"
            }
        }
    ]
}

add_file_003 = {  
    "dns_security": {
        "dns_filtering": {
            "profile": [
                {
                    "name": "test3",
                    "actions": "{\"5\":1,\"6\":1,\"7\":1,\"8\":1,\"11\":1,\"12\":1,\"13\":1,\"14\":1,\"15\":1,\"17\":1,\"18\":1,\"19\":1}"
                }
            ]
        }
    }
}

add_rule_003 = {
    "dns_policies": [
        {
            "name": "test3",
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
                "filter_profile": "test3"
            }
        }
    ]
}

add_file_004 = {  
    "dns_security": {
        "dns_filtering": {
            "profile": [
                {
                    "name": "test4",
                    "actions": "{\"1\":2,\"2\":2,\"3\":2,\"4\":2,\"5\":2,\"6\":2,\"7\":2,\"8\":2,\"9\":2,\"10\":2,\"11\":2,\"12\":2,\"13\":2,\"14\":2,\"15\":2,\"16\":2,\"17\":2,\"18\":2,\"19\":2}"
                }
            ]
        }
    }
}

add_rule_004 = {
    "dns_policies": [
        {
            "name": "test4",
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
                "filter_profile": "test4"
            }
        }
    ]
}

add_file_005 = {  
    "dns_security": {
        "dns_filtering": {
            "profile": [
                {
                    "name": "test5",
                    "actions": "{\"5\":3,\"6\":3,\"7\":3,\"8\":3,\"9\":3,\"10\":3,\"11\":3,\"12\":3,\"13\":3,\"14\":3,\"15\":3,\"16\":3,\"17\":3,\"18\":3}"                       
                }
            ]
        }
    }
}

add_rule_005 = {
    "dns_policies": [
        {
            "name": "test5",
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
                "filter_profile": "test5"
            }
        }
    ]
}

fored_ip_settings = {
    "dns_security": {
        "dns_filtering": {
            "useWhiteList": True,
            "forged_ip": {
                "ipv4": "127.0.0.2",
                "ipv6": "1001::2"
            }
        }
    }
}
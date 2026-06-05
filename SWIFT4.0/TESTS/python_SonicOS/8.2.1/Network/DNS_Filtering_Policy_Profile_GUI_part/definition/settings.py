import os
import sys
import re
import time
import copy
import json
import string
import random


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
from lib.modules.API.network import InterfaceIPv4Api, DnsProxyApi, ZoneObjectsApi, AddressobjectsApi, DnsFilteringApi
from lib.modules.API.system import PacketmonitorApi, ScheduleApi, DiagnosticApi
from lib.modules.API.firewall import DNSRuleApi
from lib.modules.API.log import LogMonitorApi, AuditlogMonitorApi
from lib.modules.CLI.network import DNSPolicyCli, DNSfilteringCli
from lib.modules.CLI.system import LicenseCli


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Policy_Profile_GUI_part/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/DNS_Filtering_Policy_Profile_GUI_part.json'

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
    Filtering_server = '156.154.54.200'
    PLATFORM = str(OpenS.get_node_platform('UTM')).upper()

class CParam:
    Log_id = 1687
    Name = "test"
    Max_count = 0
    Profile = "Default Profile"


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_api = InterfaceIPv4Api(fw)
dnsProxy_api = DnsProxyApi(fw)
dnsRule_api = DNSRuleApi(fw)
dnsFilter_api = DnsFilteringApi(fw)
packet_api = PacketmonitorApi(fw)
logMonitor_api = LogMonitorApi(fw)
audit_api = AuditlogMonitorApi(fw)
diag_api = DiagnosticApi(fw)
schedule_api = ScheduleApi(fw)
zone_api = ZoneObjectsApi(fw)
ao_api = AddressobjectsApi(fw)
dnsPolicy_cli = DNSPolicyCli(fw_cli)
dnsFilter_cli = DNSfilteringCli(fw_cli)
license_cli = LicenseCli(fw_cli)


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
dns_proxy_dict = {
    "dns_policies": [
        {
            "name": CParam.Name,
            "enable": True,
            "source": {
                "address": {
                    "any": True
                }
            },
            "from": "LAN",
            "action": {
                "proxy": True
            }
        }
    ]
}
dns_filter_dict = {
    "dns_policies": [
        {
            "name": CParam.Name,
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
            "from": "LAN",
            "action": {
                "filter_profile": "Default Profile"
            }
        }
    ]
}
max_count_dict = {
    32: (
        'TZ370-PROTOTYPE', 'TZ370W-PROTOTYPE', 'TZ370', 'TZ370W', 'TZ370P',
        'TZ270W-PROTOTYPE', 'TZ270-PROTOTYPE', 'TZ270', 'TZ270W', 'TZ270P',
        'TZ470-PROTOTYPE', 'TZ470W-PROTOTYPE', 'TZ470', 'TZ470W', 'TZ470P',
        'TZ570-PROTOTYPE', 'TZ570W-PROTOTYPE', 'TZ570', 'TZ570P', 'TZ570W',
        'TZ670-PROTOTYPE', 'TZ670W-PROTOTYPE', 'TZ670', 'TZ670P', 'TZ670W',
        'NSA2700', 'NSA2700-PROTOTYPE', 'NSA3700', 'NSA3700-PROTOTYPE'
        ),
    128: (
        'NSA4700', 'NSA4700-PROTOTYPE', 'NSA5700', 'NSA5700-PROTOTYPE',
        'NSA6700', 'NSA6700-PROTOTYPE', 'NSSP10700', 'NSSP10700-PROTOTYPE', 
        'NSSP11700', 'NSSP11700-PROTOTYPE', 'NSSP13700', 'NSSP13700-PROTOTYPE', 
        '14700', '14700-PROTOTYPE', '15700', '15700-TENANT', 'NSV-VM', 'NSV-NG'
        ),
    64: ()
}
pattern_target_dict = (
    dns_filter_dict["dns_policies"][0]["name"],
    "DNS_POL_ACTION_FILTER",
    "Profile ID            : 0",
    "Enabled               : Yes",
)
ao_dict ={
    "object_type": "host",
    "name": "my_address_object",
    "zone": "LAN",
    "value": PC1_ETH0_IP
}
schedule_dict = {
    "name": "my_schedule", 
    "occurs": {
        "recurring": {
            "recurring": [
                {
                    "sun": True, "mon": False, "tue": False, "wed": False, 
                    "thu": False, "fri": False, "sat": False,
                    "start": "02:00", "end": "23:00"
                }
            ]
        }
    }
}
custom_zone_dict = {
    "zones": [
        {
            "name": "my_zone", 
            "security_type": "trusted", 
            "interface_trust": False, 
            "auto_generate_access_rules": {
                "allow_from_to_equal": True, 
                "allow_to_lower": True, 
                "allow_from_higher": True, 
                "deny_from_lower": True
            }
        }
    ]
}
profile_dict = {
    "dns_security":{
        "dns_filtering":{
            "profile":[
                {
                    "name":CParam.Name
                }
            ]
        }
    }
}

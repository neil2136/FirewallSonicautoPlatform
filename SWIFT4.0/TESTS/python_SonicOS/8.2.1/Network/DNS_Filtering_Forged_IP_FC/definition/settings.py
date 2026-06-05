import sys
import re
import os
import time
import unittest
from nose_parameterized import parameterized
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Forged_IP_FC')
from runner.unittest.setup import Test, repeat_method
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import firewall
from utm import Firewall
from lib.modules.API.network import DnsFilteringApi
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from networkdevice import Host
from util.openstack import Openstack
from lib.modules.CLI.network import DNSfilteringCli
from util.enhancedinfo import show_testcase_info
from lib.modules.CLI.system import LicenseCli


class Parameter():
    DUT_X0_IP = "192.168.168.168"    
    DUT_X1_IP="11.11.11.168"
    Forged_ip_ipv4 = "10.0.0.1"
    New_forged_ip_ipv4= '10.0.0.6'
    Forged_ip_ipv6="1001::1"
    Forged_ip_ipv6_in_tsr = '1001:0:0:0:0:0:0:1'
    ea_domain = 'ea5.com.edgekey.net'
    DUT_X1_GW="11.11.11.1"
    DESTINATION = "10.190.202.200"
    MY_WAN_PC_IP="11.11.11.169"
    PC1_GW = '192.168.2.1'
    Route_Mask_1 = '255.0.0.0'
    Route_Host_1 = '10.0.0.0'
    Route_Host_2 = '0.0.0.0'
    Route_Mask_2 = '0.0.0.0'
    DNS_SERVER = MY_WAN_PC_IP
    REACH_WEB = "www.baidu.com"
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/DNS_Filtering_Forged_IP_FC/testplan/DNS_Filtering_Forged_IP_FC.json"


ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password')
fw_cli = fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

zone_api = network.ZoneObjectsApi(fw)
interface_api = network.InterfaceIPv4Api(fw)
dnssec_obj = network.DNSSecurityApi(fw)
dnsrule_obj = firewall.DNSRuleApi(fw)
config_forged_ip_obj = DnsFilteringApi(fw)
down_tsr_obj = system.DiagnosticApi(fw)
forged_ip_cli = DNSfilteringCli(fw)
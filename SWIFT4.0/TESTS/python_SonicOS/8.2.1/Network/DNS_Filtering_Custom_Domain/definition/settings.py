import sys
import re
import os
import time
from nose_parameterized import parameterized
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Custom_Domain')
from runner.unittest.setup import Test, repeat_method
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import firewall
from utm import Firewall
from lib.modules.API.network import DnsFilteringApi,DNSSecurityApi,DnsProxyApi
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API.system import PacketmonitorApi
from lib.modules.API.log import LogSettingsApi,LogCategoryApi,LogMonitorApi
from lib.modules.CLI.system import LicenseCli


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
    TEST_Path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Filtering_Custom_Domain'
    TESTPLAN = TEST_Path + '/testplan/DNS_Filtering_Custom_Domain.json'

domain1 = "*.e-a.com"
domain2 = "test.com"
domain3 = 'www.ea.com'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='sonicauto')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

zone_api = network.ZoneObjectsApi(fw)
interface_api = network.InterfaceIPv4Api(fw)
dnssec_obj = DNSSecurityApi(fw)
dns_filtering_obj = DnsFilteringApi(fw)
down_tsr_obj = system.DiagnosticApi(fw)
log_set = LogSettingsApi(fw)
log_cata = LogCategoryApi(fw)
log_monitor = LogMonitorApi(fw)
dnsrule_obj = firewall.DNSRuleApi(fw)
dnspxy_api = DnsProxyApi(fw)
packet_obj = PacketmonitorApi(fw)



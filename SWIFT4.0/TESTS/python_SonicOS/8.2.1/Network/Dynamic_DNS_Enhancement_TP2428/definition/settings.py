import os
import re
import sys
import copy
import time

import unittest
import paramunittest
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from nose_parameterized import parameterized

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Dynamic_DNS_Enhancement_TP2428')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Dynamic_DNS_Enhancement_TP2428/testcases')

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.system import TimeApi
from lib.modules.API.log import LogMonitorApi
from lib.modules.API.network import InterfaceIPv4Api,DDNSApi

class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    MASK = '255.255.255.0'
    PC1_GW = '192.168.2.1'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    TEST_Path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Dynamic_DNS_Enhancement_TP2428'
    TESTPLAN = TEST_Path + '/testplan/Dynamic_DNS_Enhancement_TP2428.json'


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cgi = Firewall(ip, user='admin', password='password', supported_config_mode='cgi')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

License_obj = LicenseCli(fw_cli)
interface_obj = InterfaceIPv4Api(fw_api)
ddns_obj = DDNSApi(fw_api)
time_obj = TimeApi(fw_api)
log_obj = LogMonitorApi(fw_api)


ddns_dyn_profile = {
    'version':'ipv4', # ipv4,ipv6
    'profile_name': 'newv4ddnsprofile',
    'enable': True,
    'use_online': True,
    'provider': 'dyn',#dyn,changeip,noip
    'user_name':'shsonicwall',
    'password':'SnWl001',
    'domain':'shqasonicwall.dyndns.org',
    'service_type':'dynamic',
    'bound_to': {'any':True},
    'online_settings':{'set_to_wan': True},#detect:true,set_to_wan:true,manual:1.1.1.1
    'offline_settings':{'do_nothing': True}#do_nothing:true,use_previous:true,make_host_unknown:true,manual:1.1.1.1
}
ddns_changeip_profile = {
    'version':'ipv4', # ipv4,ipv6
    'profile_name': 'test2',
    'enable': True,
    'use_online': False,
    'provider': 'changeip',#dyn,changeip,noip
    'user_name':'shautomation',
    'password':'password',
    'domain':'shautomation.changeip.net',
    # 'service_type':'dynamic',
    'bound_to': {'interface':'X1'},#
    'online_settings':{'set_to_wan':True},#detect:true,set_to_wan:true,manual:1.1.1.1
    'offline_settings':{'do_nothing': True}#do_nothing:true,use_previous:true,make_host_unknown:true,manual:1.1.1.1
}
ddns_noip_profile = {
    'version':'ipv4', # ipv4,ipv6
    'profile_name': 'test3',
    'enable': True,
    'use_online': False,
    'provider': 'noip',#dyn,changeip,noip
    'user_name':'wegu@sonicwall.com',
    'password':'password',
    'domain':'wegu.hopto.org',
    # 'service_type':'dynamic',
    'bound_to': {'interface':'X1'},#
    'online_settings':{'set_to_wan':True},#detect:true,set_to_wan:true,manual:1.1.1.1
    'offline_settings':{'do_nothing': True}#do_nothing:true,use_previous:true,make_host_unknown:true,manual:1.1.1.1
}

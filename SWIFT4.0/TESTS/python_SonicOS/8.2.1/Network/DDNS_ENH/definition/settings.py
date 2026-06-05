import os
import sys
import re
import time
import copy
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from runner.settings import logger,Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.setup import Test, repeat_method
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from utm import Firewall
from modules.API.network import DDNSApi,InterfaceIPv4Api
from modules.API.log import LogMonitorApi
from modules.CLI.system import LicenseCli
from networkdevice import Host
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DDNS_ENH')


class Parameter():
    FIREWALL = '192.168.168.168'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Network/DDNS_ENH/testplan/DDNS_ENH.json'
    x1_static_opt={
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': '13.0.0.168',
    'netmask': '255.255.255.0',
    'gateway': '13.0.0.1',
    'dns1': Params.G_DNS1,
    'dns2': Params.G_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    'mgmt_ping': True,
    'user_https':True,
    }
    ddns_dyn_profile = {
        'version':'ipv4', # ipv4,ipv6
        'profile_name': 'test1',
        'enable': True,
        'use_online': True,
        'provider': 'dyn',#dyn,changeip,noip
        'user_name':'shsonicwall',
        'password':'SnWl001',
        'domain':'shqasonicwall.dyndns.org',
        # 'service_type':'dynamic',
        'bound_to': {'interface':'X1'},#
        'online_settings':{'set_to_wan':True},#detect:true,set_to_wan:true,manual:1.1.1.1
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
           
fw = Firewall(Parameter.FIREWALL, user='admin',password='password',supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
ddnsApi = DDNSApi(fw)
interface = InterfaceIPv4Api(fw)
PC1 = Host(Params.testbed + '-PC1')
# WAN_IP = interface.get_interface_ip('X1') 
license_obj = LicenseCli(fw_cli)
log_obj = LogMonitorApi(fw)



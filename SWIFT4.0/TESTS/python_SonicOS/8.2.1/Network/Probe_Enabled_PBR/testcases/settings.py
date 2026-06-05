import sys
import re
import os
import time
import paramunittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Probe_Enabled_PBR')
from runner.unittest.setup import Test, repeat_method
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import policy
from lib.modules.API import log
from utm import Firewall
from runner.utils.assertion import Assertion
from runner.settings import Params, logger, LOG_DIR
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from tools import trafficGen,cdrouter_test


class Parameter():
    DUT_X0_IP = "192.168.168.168" 
    DUT_X1_IP = "192.168.120.20"  
    DUT_X1_GW = "192.168.120.10"  
    DUT_X2_IP = "192.168.100.20"    
    DUT_X2_GW = "192.168.100.10" 
    WAN_GW = DUT_X1_GW   
    REMOTE_HOST = '3.3.3.3' 
    NETMASK = '255.255.255.0'
    CDROUTER = '192.168.200.100'
    TESTPATH = '/usr/share/doc/cdrouter'
    TCP_PORT ='1234'
    CONF = os.environ['PYTHON_SONICOS_HOME'] + "/Network/Probe_Enabled_PBR/confs/local.conf"
    CASE = 'swl_hosts_1'
    LOG = LOG_DIR + '/capture_files'
    OS_STACK=Openstack(Params.testbed)
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/Probe_Enabled_PBR/testplan/probe_pbr.json"

ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface = network.InterfaceIPv4Api(fw)
route = network.RoutePolicyApi(fw)
ao = network.AddressobjectsApi(fw)
nm = network.NetworkMonitorApi(fw)
nat = network.NatpolicyApi(fw)
tsr = system.DiagnosticApi(fw)
route = policy.RoutePolicyApi(fw)
diag = system.DiagnosticPingApi(fw)
setting = system.SettingApi(fw)
log_monitor = log.LogMonitorApi(fw)
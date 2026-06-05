import sys
import re
import os
import time
from nose_parameterized import parameterized
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_Network_Monitor')
from runner.unittest.setup import Test, repeat_method, skip_if_fail_method
from lib.modules.API import network
from lib.modules.API import system
from utm import Firewall
from runner.utils.assertion import Assertion
from runner.settings import Params, logger, LOG_DIR
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from tools import cdrouter_test


class Parameter():
    DUT_X0_IP = "192.168.168.168" 
    DUT_X0_IPv6 = '2004::10'
    DUT_X0_PREFIX = '2004::'
    DUT_X1_IP = '100.10.0.10'
    DUT_X1_GW = '100.10.0.11'
    DUT_X1_IPV6 = '3001::100'
    NETMASK = '255.255.255.0'
    PROBE_REMOTE = '3001:051a:cafe::1' # same with ipv6RemoteHost in nm.conf
    PROBE_GW = '3001::200' # same with ipv6WanIspIp in nm.conf
    PROBE_GW_2 = 'fe80::1'
    PORT = 80
    PC1_IP = '3001::200'
    PC1_PREFIX = '64'
    PC1_INTERFACE='eth1'
    # DUT_X2_IPV6=
    DNS = '1.1.1.1'
    DHCP_SCOPE = ['2004::11', '2004::100']
    NTA1000= '192.168.200.100'
    CONF = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_Network_Monitor/confs/nm.conf'
    TESTPATH = os.environ['PYTHON_COMMON_HOME'] + '/tools/nta1000'
    CASE1 = 'swl_network_monitor_1'
    LOG = LOG_DIR + '/capture_files'
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/IPv6_Network_Monitor/testplan/ipv6_network_monitor.json"
    fw = Firewall(DUT_X0_IP, user='admin', password='password', supported_config_mode='api')
    interface = network.InterfaceIPv4Api(fw)
    inter_v6_obj = network.InterfaceIPv6Api(fw)
    route_obj = network.RoutePolicyApi(fw)
    ao_obj = network.AddressobjectsApi(fw)


import sys
import re
import os
import time
from nose_parameterized import parameterized
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Client_Prefix_Delegation')
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
    DUT_X2_IP = '100.10.0.10'
    DUT_X2_GW = '100.10.0.11'
    DUT_X3_IP = '110.10.0.10'
    DUT_X3_GW = '110.10.0.11'
    NETMASK = '255.255.255.0'
    # DUT_X2_IPV6=
    DNS = '1.1.1.1'
    DHCP_SCOPE = ['2004::11', '2004::100']
    PD_PREFIX = '3001:dddd'
    PD_PREFIX_NEW = '3002:dddd'
    PD_PREFIX_LEN = 48#same as dhcpv6WanAssignPrefixLen in dhcp.conf
    EXTRA_IP = '::1:2:3:4'
    NTA1000= '192.168.200.100'
    CONF = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_Prefix_Delegation/confs/dhcp.conf'
    CONF_NEW = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_Prefix_Delegation/confs/dhcp_new.conf'
    TESTPATH = os.environ['PYTHON_COMMON_HOME'] + '/tools/nta1000'
    CASE1 = 'swl_dhcpv6_pd_1'
    CASE2 = 'swl_dhcpv6_pd_2'
    LOG = LOG_DIR + '/capture_files'
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/IPv6_DHCP_Client_Prefix_Delegation/testplan/ipv6_dhcp_pd.json"
    fw = Firewall(DUT_X0_IP, user='admin', password='password', supported_config_mode='api')
    interface = network.InterfaceIPv4Api(fw)
    inter_v6_obj = network.InterfaceIPv6Api(fw)
    route_obj = network.RoutePolicyApi(fw)
    ao_obj = network.AddressobjectsApi(fw)


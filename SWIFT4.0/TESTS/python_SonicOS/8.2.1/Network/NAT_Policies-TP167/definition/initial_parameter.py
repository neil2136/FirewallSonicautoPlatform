import os
import sys
import re
import copy
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest

from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import firewall

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/NAT_Policies-TP167/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/NAT_Policies-TP167')

os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
pc1_defaultgw = os_obj.get_pc_default_gw_ip('PC1')

PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
tc_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/NAT_Policies-TP167/testcases'
lib_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/NAT_Policies-TP167/lib'

logger.info("\n" + "-" * 30 + "\n" \
    + "PC1_ETH0_IP :" + PC1_ETH0_IP + "\n" \
    + "PC1_ETH1_IP :" + PC1_ETH1_IP + "\n" \
    + "-" * 30
)



class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    X1_DNS_1 = '10.190.202.200'
    X1_DNS_2 = '10.50.129.148'
    HTTP_SERVER_IP = '13.0.0.5'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/NAT_Policies-TP167/testplan/NAT_Policies-TP167.json'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

interface_ipv4 = network.InterfaceIPv4Api(fw)
ao_obj = network.AddressobjectsApi(fw)
access_rules_obj = firewall.AccessRuleApi(fw)
service_obj = network.ServiceObjectApi(fw)
natpolicy_obj = network.NatpolicyApi(fw)
localhost = Host('localhost')
httpserver = Host(httpserver_pc)



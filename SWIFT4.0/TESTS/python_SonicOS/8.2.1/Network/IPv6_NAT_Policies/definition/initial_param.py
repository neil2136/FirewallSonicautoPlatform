import os
import sys
import unittest
import re
from time import sleep
import subprocess


sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_NAT_Policies')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_NAT_Policies/lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from utm import Firewall, FirewallAPI, enable_ssh
from runner.unittest.setup import Test
from runner.settings import Params, logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from lib.modules.API import network, system
from networkdevice import Host
from lib.modules.CLI.system import AdminCli


TEST_PATH = os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_NAT_Policies'


class Parameter:
    # PC1(eth1) -- (X0)UTM ; PC1(eth3) -- (X2)UTM
    # PC2(eth1) __ (X1)UTM ; PC2(eth3) -- (X3)UTM
    FIREWALL = '192.168.168.168'
    TESTPLAN = TEST_PATH + '/testplan/ipv6_nat_policies.json'

    lan_host1 = '2001::100'
    lan_host2 = '2001::110'
    lan_host1_if = 'eth1'

    wan_ip = '2001:1::20'
    wan_host1 = '2001:1::100'
    wan_host2 = '2001:1::101'
    wan_host3 = '2001:1::102'
    wan_host4 = '2001:1::103'
    wan_host1_if = 'eth1'

    dmz_host1 = '2001:2::100'
    dmz_host1_if = 'eth3'

    x3_host = '2001:3::100'
    x3_host_if = 'eth3'

    translated_ips = ['2001:1::20', '2001:1::25', '2001:1::30']
    wan_ip_pool = [wan_host1, wan_host2, wan_host3, wan_host4]

    X0_IP = '2001::10'
    X1_IP = '2001:1::10'
    X2_IP = '2001:2::10'
    X2_v4_IP = '3.3.3.168'
    X3_IP = '2001:3::10'
    X3_v4_IP = '4.4.4.168'


fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
address_obj = network.AddressobjectsApi(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
interface_v4 = network.InterfaceIPv4Api(fw)
natpolicy_obj = network.NatpolicyApi(fw)
setting = system.SettingApi(fw)
admin = AdminCli(fw_cli)
boot = system.SettingApi(fw)


localhost = Host('localhost')
pc2_ssh = Host(Params.testbed + '-PC2')
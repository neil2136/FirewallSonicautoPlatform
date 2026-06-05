import os
import sys
import unittest
from time import sleep

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/NAT64_Policies')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from utm import Firewall, FirewallAPI
from util.openstack import Openstack
from runner.unittest.setup import Test
from runner.settings import logger, Params
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from networkdevice import Host
from lib.modules.API import network, policy, accessrule
from lib.modules.CLI.system import LicenseCli

os_obj = Openstack(Params.testbed)
localhost = Host('localhost')
pc2_ssh = Host(Params.testbed + '-PC2')
pc3_ssh = Host(Params.testbed + '-PC3')

class Parameter():
    FIREWALL = '192.168.168.168'
    FIREWALL_IPV6 = '2001:db0::196'
    MASK = '255.255.255.0'
    DNS_1 = '10.190.202.200'
    IPV6_PREFIXLEN = 96
    DMZ_IPV6_PREFIXLEN = 64
    DMZ_DESTINATION = '64:9999::1402:2f4'

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Network/NAT64_Policies/testplan/nat64_policies.json'
    # PC
    PC1_IF = 'eth0'
    PC2_IF = 'eth1'
    PC3_IF = 'eth1'
    DEST_NETWORK = '64:ff9b::'
    DMZ_PREFIX = '64:9999::'


    # DUT
    X1_IP = '23.0.0.10'
    X1_IPV6 = '2001:480:1:1::100'
    X1_GW = '23.0.0.1'
    X2_IP = '20.2.2.22'
    X2_IPV6 = '2001:1100::193'



fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
license_cli = LicenseCli(fw_cli)

interface_v4 = network.InterfaceIPv4Api(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
address_obj = network.AddressobjectsApi(fw)
nat64_opt = policy.NatPolicyApi(fw)
accessrule_opt = accessrule.Access_Rule(fw)




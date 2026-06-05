import os
import sys
import unittest
import time
import re
from time import sleep

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

testplan = os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/testplan/Interface_168.json'
class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.200'
    X2_IP = '192.168.10.200'
    X4_IP = '192.168.4.200'
    X6_IP = '192.168.6.200'
    MGMT_SSH = True
    MGMT_HTTP = True
    MGMT_HTTPS = True
    MGMT_Ping = True
    MGMT_SNMP = True
    Mask = '255.255.255.0'
    TESTPLAN = testplan

from utm import Firewall,FirewallAPI
from util.openstack import Openstack
from modules.API.network import InterfaceIPv4Api
from modules.API.network import AddressobjectsApi
from runner.unittest.setup import Test, skip_if_fail_method, repeat_method, repeat_class
from modules.API import network, firewall, dpissl, system, policy, log
from runner.settings import logger, Params
from runner.utils.assertion import Assertion
from testcases.settings import Parameter
from runner.settings import logger
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from lib import utils,setup
from modules.API.users import UserLocalApi, UsersettingApi
from tools.trafficGen import ping
from modules.API.log import LogMonitorApi
from modules.API.firewall import AccessRuleApi
from networkdevice import Host
from lib.modules.CLI.system import PacketmonitorCli, AdminCli




os_obj = Openstack(Params.testbed)
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')



fw = Firewall(Parameter.FIREWALL, user= 'admin', password= 'password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
interface = InterfaceIPv4Api(fw)
userLocal = UserLocalApi(fw)
userSetting = UsersettingApi(fw)
AddressObject = AddressobjectsApi(fw)
Log = LogMonitorApi(fw)
accessrule = AccessRuleApi(fw)
acrObj = firewall.AccessRuleApi(fw)
interface_ipv4 = network.InterfaceIPv4Api(fw)
interface_obj = network.InterfaceIPv4Api(fw)
package_monitor=PacketmonitorCli(fw_cli)
package_cap=system.PacketmonitorApi(fw)
log_obj = log.LogMonitorApi(fw)
sonic_api=AdminCli(fw_cli)
localhost = Host('localhost')
pc2 = Host(PC2_ETH1_IP)
snmp_obj = system.SNMPApi(fw)

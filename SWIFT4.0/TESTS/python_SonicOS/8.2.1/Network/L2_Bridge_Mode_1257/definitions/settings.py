import os
import sys
import re
import copy
import time

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network,system,firewall,users
from lib.modules.CLI.system import LicenseCli

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/L2_Bridge_Mode_1257/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/L2_Bridge_Mode_1257')

ip = "192.168.168.168"
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_obj = network.InterfaceIPv4Api(fw_api)
lb_obj = network.FailoverLbApi(fw_api)
lc = LicenseCli(fw_cli)
ao_obj = network.AddressobjectsApi(fw_api)
dhcp_server_obj = network.DHCPServerApi(fw_api)
setting_obj = system.SettingApi(fw_api)
access_rules_obj = firewall.AccessRuleApi(fw_api)
user_obj = users.UsersettingApi(fw_api)
radius_obj = users.RadiusApi(fw_api)
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/L2_Bridge_Mode_1257/testplan/L2_Bridge_Mode_1257.json'

X1_IP = '8.0.0.5'
X1_GW = '8.0.0.3'
X1_DNS1 = Params.G_DNS1
X1_DNS2 = Params.G_DNS2
MASK = '255.255.255.0'
PC3_ETH0_IP='8.0.0.3'
X2_IP = '2.2.2.168'
RADIUS_SERVER_IP = PC3_ETH0_IP
RADIUS_PASS = 'password'
RADIUS_USER= 'TB32PC1ETH0'
RADIUS_PASSWD='password'

localhost = Host(Params.testbed + '-PC1')
PC2_login = Host(Params.testbed + '-PC2', user='root', password='password')
PC3_login = Host(Params.testbed + '-PC3', user='root', password='password')

fw_api_radius = Firewall(ip, user=RADIUS_USER, password=RADIUS_PASSWD, supported_config_mode='api')

my_topo = {'TOPO':Params.product + '_l2bridgemode_1', 'ACTION': 'add', 'SPECFILE': '/SWIFT4.0/COMMON/data/switches/' + Params.testbed + '.yaml'}
logger.info(' {} '.center(20,'-').format(my_topo))

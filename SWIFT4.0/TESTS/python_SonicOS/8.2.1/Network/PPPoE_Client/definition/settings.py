import os
import sys
import re
import unittest
import time
from dateutil.parser import parse
from networkdevice import Host
from runner.unittest.setup import Test, skip_if_fail_method, repeat_method
from runner.settings import logger, Params
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/PPPoE_Client')
setup_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/PPPoE_Client/definition/pppoe_confs'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/PPPoE_Client/testplan/pppoe_client.json'


from util.enhancedinfo import show_testcase_info
from utm import Firewall, FirewallAPI
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.log import LogMonitorApi, LogCategoryApi
from lib.modules.CLI.system import LicenseCli


# parameters on the openstack
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2

    PC1_IP = '192.168.168.202'
    Mask = '255.255.255.0'
    X2_IP = '172.16.1.200'
    PC2_IP = '172.100.1.12'
    PC2_SERVER_X2 = '172.20.1.122'
    PC2_X2_SUB = '172.20.1.0'
    ADD_PC2_X2_ROUTE = f'{PC2_X2_SUB} gw {FIREWALL} netmask {Mask}'
    CHECK_X2_ROUTE = f'{PC2_X2_SUB}/24 via {FIREWALL}'
    PC2_SERVER_X3 = '172.30.1.124'
    PC2_X3_SUB = '172.30.1.0'
    ADD_PC2_X3_ROUTE = f'{PC2_X3_SUB} gw {FIREWALL} netmask {Mask}'
    CHECK_X3_ROUTE = f'{PC2_X3_SUB}/24 via {FIREWALL}'
    ip_pool_start_X2 = '172.20.1.100'
    ip_pool_end_X2 = '172.20.1.110'
    ip_pool_start_X3 = '172.30.1.100'
    ip_pool_end_X3 = '172.30.1.110'
    disconnected_IP = '0.0.0.0'
    MGMT_SSH = True
    MGMT_HTTP = True
    MGMT_HTTPS = True
    MGMT_Ping = True
    MGMT_SNMP = True


# parameters on the test case
X1_static_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
}
# case 12, 14, 19, 39
x2_pppoe_opt_dynamic_dict = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': 'pppoe',
    'pppoe_servicename': '',
    'pppoe_passwd': 'password',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': True,
    'pppoe_inactivity': 2,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,
    'mgmt_ping': True,
    'mgmt_https': True,
    'mgmt_ssh': True
}
# case 13, 14
x3_pppoe_opt_dynamic_dict = {
    'if': 'x3',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': 'pppoe',
    'pppoe_servicename': '',
    'pppoe_passwd': 'password',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': True,
    'pppoe_inactivity': 0,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,
    'mgmt_ping': True,
    'mgmt_https': True,
    'mgmt_ssh': True
}
# case 13
x2_static_opt_dynamic_dict = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': '12.12.12.12',
    'netmask': '255.255.255.0',
    'gateway': '12.12.12.1'
}


fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')
interfaceapi = InterfaceIPv4Api(fw)
logmonitorapi = LogMonitorApi(fw)
logcategoryapi = LogCategoryApi(fw)
license_cli = LicenseCli(fw_cli)
localhost = Host('localhost')
PC2_login = Host(Parameter.PC2_IP, user='root', password='password')

import os
import sys
import json
import paramunittest
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import contents from common_lib path
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import AddressobjectsApi, ZoneObjectsApi, InterfaceIPv4Api
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.API.system import SettingApi

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
           '/Network/IPv6_Address_Objects_TP2508_Part2/testplan/ipv6_address_objects_tp2508.json'


class Parameter:
    FIREWALL = '192.168.168.168'


# parameters on the test case
Default_Interface_Ao_list = [
    "X2 IP",
    "X2 Subnet",
    "X2 IPv6 Link-Local Address",
    "X2 IPv6 Primary Dynamic Address",
    "X2 IPv6 Primary Dynamic Address Subnet",
    "X2 IPv6 Primary Static Address",
    "X2 IPv6 Primary Static Address Subnet"
]
WAN_Interface_Ao_list = [
    "X2 IP",
    "X2 Subnet",
    "X2 IPv6 Link-Local Address",
    "X2 IPv6 Primary Dynamic Address",
    "X2 IPv6 Primary Dynamic Address Subnet",
    "X2 IPv6 Primary Static Address",
    "X2 IPv6 Primary Static Address Subnet",
    "X2 Default Gateway",
    "X2 IPv6 Default Gateway"
]

# Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')

addressobj_api = AddressobjectsApi(fw)
interface_api = InterfaceIPv4Api(fw)
zoneobj_api = ZoneObjectsApi(fw)
route_api = RoutePolicyApi(fw)
setting_api = SettingApi(fw)

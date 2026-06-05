import os
import sys
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]
                + '/Network/API_Version2_Interface_IPv6')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]
                + '/Network/API_Version2_Interface_IPv6/testcases')
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')

from utm import Firewall
from runner.unittest.setup import Test
from runner.settings import logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import InterfaceIPv6Api

testplan = os.environ["PYTHON_SONICOS_HOME"]

class Parameter():
    FIREWALL = '192.168.168.168'
    X2_IP = '172.16.1.168'
    TESTPLAN = testplan + '/Network/API_Version2_Interface_IPv6/testplan/api_interface_ipv6.json'

fw_api = Firewall(Parameter.FIREWALL,
                  user='admin',
                  password='password',
                  supported_config_mode='api')

interface_ipv6 = InterfaceIPv6Api(fw_api)
interface_ipv4 = InterfaceIPv4Api(fw_api)

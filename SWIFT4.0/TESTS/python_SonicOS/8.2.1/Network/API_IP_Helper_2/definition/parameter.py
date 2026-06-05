import sys
import os
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
from utm import Firewall
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from lib.modules.API.network import AddressobjectsApi
from lib.modules.API.network import IpHelperApi
from util.enhancedinfo import show_testcase_info
from lib.modules.API.network import InterfaceIPv4Api
from runner.settings import logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
testplan = os.environ["PYTHON_SONICOS_HOME"]


class Parameter:
    FIREWALL = '192.168.168.168'
    X2_IP = '172.16.1.168'
    TESTPLAN = testplan + '/Network/API_IP_Helper_2/testplan/api_iphelper.json'



fw_api = Firewall(Parameter.FIREWALL,user='admin',password='sonicauto',supported_config_mode='api')

iphelperApi = IpHelperApi(fw_api)
addressObjectsApi = AddressobjectsApi(fw_api)
interface_ipv4 = InterfaceIPv4Api(fw_api)

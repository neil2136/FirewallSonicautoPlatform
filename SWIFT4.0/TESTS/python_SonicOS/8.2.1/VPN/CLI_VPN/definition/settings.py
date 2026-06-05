import os
import sys
import re
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/CLI_VPN')

from runner.settings import Params, logger
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test
from utm import Firewall
from util.enhancedinfo import show_testcase_info

class Parameter():
    FIREWALL = '192.168.168.168'
    X2_IP = '172.168.168.168'
    X2_GW = '172.168.168.1'
    X2_DNS = '10.9.1.40'
    MASK = '255.255.255.0'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/CLI_VPN/testplan/CLI_VPN.json'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

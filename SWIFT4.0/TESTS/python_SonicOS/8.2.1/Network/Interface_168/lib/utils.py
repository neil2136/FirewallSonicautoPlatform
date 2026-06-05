import os
import sys
import re
import json as js
import urllib3
import requests
import time

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from utm import Firewall
from lib.modules.API.network import InterfaceIPv4Api
from runner.unittest.setup import Test
from runner.settings import logger
from runner.utils.assertion import Assertion
from testcases.settings import Parameter
from runner.settings import logger
from util.enhancedinfo import show_testcase_info
from modules.API.policy import SecurityPolicyApi
from modules.API.log import LogMonitorApi

interface_management_path = '/SWIFT4.0/COMMON/bin/interface_management.pl'
fw = Firewall(Parameter.FIREWALL, user= 'admin', password= 'password', supported_config_mode='api')
interface = InterfaceIPv4Api(fw)
log = LogMonitorApi(fw)




def log_testplan(case_id):
    description = show_testcase_info(Parameter.TESTPLAN,
                                     case_id, description=True)['title']
    testplan = show_testcase_info(Parameter.TESTPLAN, case_id, description=True)
    logger.info(testplan)
    logger.info('*' * 8 + ' title ' + '*' * 8)
    logger.info(testplan['title'])
    logger.info('*' * 8 + ' steps ' + '*' * 8)
    for item in testplan['steps'].split('&'):
        logger.info(item)
    logger.info('*' * 8 + ' result ' + '*' * 8)
    for item in testplan['result'].split('&'):
        logger.info(item)

def test_management_function(function, action):
    success_flag = False
    failed_flag = False
    cmd = 'perl {} -m {} -a '.format(interface_management_path, Parameter.X2_IP) + function
    out = ''.join(os.popen(cmd))
    logger.info(out)
    if 'successfully' in out:
        success_flag = True
    if 'failed' in out:
        failed_flag = True
    # test auto added -> action = 'on' ; auto deleted -> action -> 'off'
    if action == 'on':
        return success_flag
    if action == 'off':
        return failed_flag

def VerifyL2bridgeMode(interface_name, l2_to_name):
    x_dict = interface.get_interface_status(interface_name)  ## type(x_dict) = dict
    l2bridge_interface = x_dict['interfaces'][0]['ipv4']['ip_assignment']['mode']['l2bridge']['bridge_to']
    logger.info(l2bridge_interface)
    if l2_to_name == l2bridge_interface:
        return True
    else:
        return  False

def VerifyLog(message):
    list = log.show_log()
    result = False
    for item in list:
        out = str(item)
        pattern = ''.join(re.findall('{}'.format(message),out))
        if message == pattern:
            result = True
            break
    return result

def User_http_Check():
    url = 'api/sonicos/interfaces/ipv4/name/X2'
    json = fw.api_get(url)
    output = json['interfaces'][0]['ipv4']['user_login'].get('http')
    if output == None:
        return True
    return False

def User_authen(method):
    url = 'api/sonicos/user/authentication/methods'
    json = fw.api_get(url)
    json['user']['auth']['auth_method'] = method
    out = fw.api_put(url, data=json)
    logger.info(json)
    if out:
        return True
    return False

def GetPPPoEIP():
    time.sleep(5)
    list = log.show_log()
    list_reverse = list[::-1]
    ip = '0.0.0.0'
    out = str(list_reverse)
    pattern = re.findall("10.10.0.1\d{2}", out)
    logger.info("-----------------------------PPPoE-------IP--------------------------")
    logger.info(pattern[0])
    ip = pattern[0]
    return ip

def GetPPPIP():
    time.sleep(5)
    list = log.show_log()
    list_reverse = list[::-1]
    ip = '0.0.0.0'
    out = str(list_reverse)
    pattern = re.findall("13.0.11.1\d{2}", out)
    logger.info("-------------------------PPTP-----------IP--------------------------")
    logger.info(pattern[0])
    ip = pattern[0]
    return ip
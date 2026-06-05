import os
import re
import sys
import copy
import time
import unittest
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts
from util.enhancedinfo import show_testcase_info
import paramunittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Radius_Users_api')



from lib.modules.API import network
#from modules.API import firewallsettings
from lib.modules.API import users


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = '10.50.129.149'
    X1_DNS2 = '10.50.129.148'
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Radius_Users_api/testplan/testplan.json'   


ip = '192.168.168.168'
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cgi = Firewall(ip, user='admin', password='password', supported_config_mode='cgi')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

Radius_user = users.RadiusApi(fw_api)
interface_obj = network.InterfaceIPv4Api(fw_api)






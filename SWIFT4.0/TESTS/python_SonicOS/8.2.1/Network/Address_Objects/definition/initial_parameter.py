import os
import sys
import re

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
import unittest
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import object

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Address_Objects/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Address_Objects')


class Parameter():
    FIREWALL = '192.168.168.168'
    #X1_IP = '172.17.1.168'
    #X1_GW = '172.17.1.1'
    #X1_DNS = '10.9.1.40'
    #X2_IP = '14.1.1.168'
    #MASK = '255.255.255.0'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Address_Objects/testplan/Address_Objects.json'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
address_obj       = network.AddressobjectsApi(fw)
address_gro       = network.AddressgroupsApi(fw)
address_group_obj = object.AddressObjectGroupApi(fw)

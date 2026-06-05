import os
import re
import sys
import copy
import time
import unittest
import time
from datetime import datetime, timedelta

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest
import requests
from lib.modules.API.system import DiagnosticApi

sys.path.append(os.environ["PYTHON_COMMON_HOME"])

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.CLI.system import LicenseCli

from util.openstack import Openstack

from networkdevice import Host

from lib.modules.API.network import InterfaceIPv4Api

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Static_Interfaces')


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Static_Interfaces/testplan/static_interface.json'


os_obj = Openstack(Params.testbed)
ip = '192.168.168.168'
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
diag_api = DiagnosticApi(fw_api)
os_obj = Openstack(Params.testbed)

PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')

localhost = Host('localhost')
PC1_login = Host(PC1_ETH1_IP, user='root', password='password')
local_host = Host('localhost')

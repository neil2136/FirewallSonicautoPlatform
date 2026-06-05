import imp
import os
import re
import sys
import copy
import time
import unittest

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from networkdevice import Host
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts
from util.enhancedinfo import show_testcase_info
import paramunittest
import subprocess

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_BVT')

from modules.CLI.users import UsersStatusCli
from modules.API.users import SSOApi
from modules.API.users import UserStatusApi
from modules.API.users import UsersettingApi


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = '10.102.1.60'
    X1_DNS2 = '10.50.129.148'
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_BVT/testplan/testplan.json'


ip = '192.168.168.168'
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

static_pc = Params.testbed + '-PC1'
static_client = Host(static_pc)

userstatus = UserStatusApi(fw_api)
sso_client = SSOApi(fw_api)
usersetting = UsersettingApi(fw_api)

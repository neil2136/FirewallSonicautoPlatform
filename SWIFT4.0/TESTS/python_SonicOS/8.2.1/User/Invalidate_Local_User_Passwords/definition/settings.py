import os
import sys
import re
import time
import copy
import requests
from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Invalidate_Local_User_Passwords/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Invalidate_Local_User_Passwords')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Invalidate_Local_User_Passwords/testplan/testplan.json'

from util.openstack import Openstack
from pexpect import pxssh
from networkdevice import Host

from lib.modules.CLI import network
from utm import Firewall
from lib.modules.API.firewall import CfoProfilesApi
from lib.modules.API.firewall import CfoObjectApi
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from lib.modules.API.users import UserLocalApi
from runner.unittest.setup import Test, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest

logger.info(sys.path)

from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.CLI.firewall import AccessRuleCli


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Invalidate_Local_User_Passwords/testplan/testplan.json'

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')

interface = InterfaceIPv4Api(fw_api)
license = LicenseCli(fw_cli)
configinterfacecli = InterfaceCli(fw_cli)
cfs_profiles = CfoProfilesApi(fw_api)
cfs_uri_object = CfoObjectApi(fw_api)

user_local = UserLocalApi(fw_api)
access_rules = AccessRuleIPv4Api(fw_api)
accessrulecli = AccessRuleCli(fw_cli)

logger.info("The Firewall LAN IP is {}".format(ip))
static_pc = Params.testbed + '-PC1'
static_client = Host(static_pc)
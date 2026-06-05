import os
import sys
import json
from collections import OrderedDict
import pexpect
from pexpect import pxssh
import time
import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import securityservices
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import log
from modules.API import users
from lib.modules.API import network, firewall, system, users, log
from lib.modules.API.users import LdapApi
from lib.modules.API.users import UserLocalApi
from lib.modules.API.network import AddressobjectsApi
from modules.API.users import AuthPartitionsApi

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Partitions_GUI/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Partitions_GUI')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Partitions_GUI/definition')


local_host = Host('localhost')

FIREWALL = '192.168.168.168'
X1_IP = '10.10.0.30'
X1_GW = '10.10.0.1'
X1_DNS1 = '10.9.1.40'
X1_DNS2 = '10.190.202.200'
MASK = '255.255.255.0'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Partitions_GUI/testplan/Auth_Partitions_GUI.json'
ip = FIREWALL
fw = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
interface_obj = network.InterfaceIPv4Api(fw)
lc = LicenseCli(fw_cli)
user_auth_partition = AuthPartitionsApi(fw)
localusers = UserLocalApi(fw)
local_user = users.UserLocalApi(fw)
user_ldap = LdapApi(fw)
address_objects = AddressobjectsApi(fw)


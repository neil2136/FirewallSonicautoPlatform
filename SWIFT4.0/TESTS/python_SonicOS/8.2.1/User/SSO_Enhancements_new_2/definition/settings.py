import os
import re
import sys
import copy
import json
import time
import unittest
import urllib3
import requests
import paramiko

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enhancements_new_2')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enhancements_new_2/definition')

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, ServiceObjectApi, ServiceGroupApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.policy import NatPolicyApi
from lib.modules.API.system import SettingApi
from lib.modules.API.users import SSOApi, UsersettingApi, UserStatusApi, UserLocalApi, LdapApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


class Parameter():
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.168'
    X1_GW = '13.0.0.1'
    X2_IP = '192.168.3.168'
    X2_GW = '192.168.3.1'
    MASK = '255.255.255.0'
    SSO_SERV = '192.168.168.65'
    DMZ_SERV = '192.168.3.65'

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_Enhancements_new_2/testplan/testplan.json'

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

os_obj = Openstack(Params.testbed)
pc1 = Host('localhost')

license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
user_sso = SSOApi(fw_api)
user_setting = UsersettingApi(fw_api)
accessrule = AccessRuleIPv4Api(fw_api)
nat_policy = NatPolicyApi(fw_api)
user_ldap = LdapApi(fw_api)
user_local = UserLocalApi(fw_api)
addr_object = AddressobjectsApi(fw_api)
addr_group = AddressObjectGroupApi(fw_api)
service_Group = ServiceGroupApi(fw_api)
service_object = ServiceObjectApi(fw_api)
settings_obj = SettingApi(fw_api)

sso_agent = {
 "user": {
  "sso": {
   "agent": [
    {
     "host": {Parameter.SSO_SERV},
     "enable": True,
     "port": 2258,
     "timeout": 5,
     "retries": 3,
     "max_requests": 3,
     "shared_key": "225abc"
    }
   ]
  }
 }
}

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

sys.path.append(os.environ["PYTHON_COMMON_HOME"])

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.CLI.system import LicenseCli

from util.openstack import Openstack

from networkdevice import Host

from lib.modules.API.diag import DiagApi
from lib.modules.API.firewall import MatchobjectApi
from lib.modules.API.network import AddressobjectsApi
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.object import CountryApi
from lib.modules.API.network import ServiceGroupApi,ServiceObjectApi
from lib.modules.ui.fw_page import FWPage
from lib.modules.API.system import AdminApi
from lib.modules.API.users import UserLocalApi
from lib.modules.API.policy import  SecurityPolicyApi
from lib.modules.API.object import SecurityActionProfilesApi
from lib.modules.API.system import PacketmonitorApi
from lib.modules.API.system import  RestartApi, DiagnosticApi,SettingApi
from lib.modules.API.users import LdapApi
from lib.modules.API.object import DosActionProfilesApi
from lib.modules.API import network, object, policy, log, system

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Routing_Policies')
class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Routing_Policies/testplan/routing_policies.json'

os_obj = Openstack(Params.testbed)
ip = '192.168.168.168'
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
os_obj = Openstack(Params.testbed)

PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
ui_obj = FWPage()
userapi = UserLocalApi(fw_api)
country_obj = CountryApi(fw_api)
security_policy = SecurityPolicyApi(fw_api)
SecurityAction_profiles_api=SecurityActionProfilesApi(fw_api)
pocket_monitor = PacketmonitorApi(fw_api)
diag_api=DiagApi(fw_api)
fw_boot = SettingApi(fw_api)
reboot_obj = RestartApi(fw_api)
dos_policy_obj = policy.DosPolicyApi(fw_api)
routing_policies_obj = policy.RoutePolicyApi(fw_api)
address_objects = network.AddressobjectsApi(fw_api)
dos_action_profile = object.DosActionProfilesApi(fw_api)
schedules_obj = object.ScheduleObjectApi(fw_api)
time_obj = system.TimeApi(fw_api)
localhost = Host('localhost')
PC1_login = Host(PC1_ETH1_IP, user='root', password='password')
local_host = Host('localhost')
log_obj = log.LogMonitorApi(fw_api)

service_group_obj = ServiceGroupApi(fw_api)
service_obj = ServiceObjectApi(fw_api)
add_group= object.AddressObjectGroupApi(fw_api)

ldap = LdapApi(fw_api)

dos_action_profile_api = DosActionProfilesApi(fw_api)

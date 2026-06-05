import os
import re
import sys
import copy
import time
import unittest
import json
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, repeat_method
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network, firewall, system, users, log, accessrule
import paramunittest
import paramiko

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_using_TLS/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/sslvpn')
print(sys.path)
import ui_user

from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.network import AddressobjectsApi
from lib.modules.CLI.users import UsersStatusCli
from lib.modules.API.users import UserLocalApi
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from lib.modules.API.sslvpn import SSLVPNClientSettingsAPI
from lib.modules.API.sslvpn import SSLVPNPortalSettingsAPI
from lib.modules.API.users import LdapApi
from lib.modules.API.users import UsersettingApi
from lib.modules.API.users import RadiusApi
from lib.modules.API.system import AdminApi
from lib.modules.API.system import CertificateApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.CLI.system import LicenseCli

from sslvpn.common_lib import netextender
from pexpect import pxssh

class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    ETH0_IP = '192.168.168.3'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_using_TLS/testplan/testplan_ldap_using_tls.json'

ca_cert = os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_using_TLS/definition/root_cert.cer'

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

os_obj = Openstack(Params.testbed)
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
PC2_login = Host(PC2_ETH1_IP)
PC3_login = Host(PC3_ETH2_IP)

interface = InterfaceIPv4Api(fw_api)

cp_nx = netextender.InstallNX()
nx = netextender.NetextenderConnect(fw_api)
dnssettingapi = network.DnsSettingsApi(fw_api)
certobj = CertificateApi(fw_api)
access_rules = AccessRuleIPv4Api(fw_api)

address_objects = AddressobjectsApi(fw_api)

admin_obj = AdminApi(fw_api)
sslvpnserver = SSLVPNServerSettingsAPI(fw_api)
clientsetobj = SSLVPNClientSettingsAPI(fw_api)
portalsetobj = SSLVPNPortalSettingsAPI(fw_api)
userstatus1 = UsersStatusCli(fw_cli)

user_setting = UsersettingApi(fw_api)
user_local = UserLocalApi(fw_api)
ldap = LdapApi(fw_api)
radius_user = RadiusApi(fw_api)
user_status = users.UserStatusApi(fw_api)
license = LicenseCli(fw_cli)

# Parameter assigned to be used through out.
logger.info("The Firewall LAN IP is {}".format(ip))
WAN_IP = Parameter.X1_IP
logger.info("Wan IP is {}".format(WAN_IP))
localhost = Host('localhost')
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)

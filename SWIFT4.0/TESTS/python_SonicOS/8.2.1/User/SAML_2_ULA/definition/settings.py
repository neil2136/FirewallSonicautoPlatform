import os
import sys
import copy
import re
import time
import json
import requests
import subprocess
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from bs4 import BeautifulSoup

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API.log import LogMonitorApi
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.users import UserLocalApi, SAMLApi, UsersettingApi
from lib.modules.API.firewall import AccessRuleApi, CfoProfilesApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.securityservices import ContentFilterPolicyApi
from modules.ui.fw_page import FWPage
from modules.ui.ui_wrapper import Browser

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_2_ULA'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/saml_2_ula.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')
logger.info(f"""
PC1_ETH0_IP : {PC1_ETH0_IP}
PC1_ETH1_IP : {PC1_ETH1_IP}
PC1_ETH2_IP : {PC1_ETH2_IP}
PC2_ETH0_IP : {PC2_ETH0_IP}
PC2_ETH1_IP : {PC2_ETH1_IP}
PC2_ETH2_IP : {PC2_ETH2_IP}
PC3_ETH0_IP : {PC3_ETH0_IP}
PC3_ETH1_IP : {PC3_ETH1_IP}
PC3_ETH2_IP : {PC3_ETH2_IP}
""")

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X2_IP = '13.13.1.168'
    X1_DNS_1 = Params.G_DNS1
    X1_DNS_2 = Params.G_DNS2
    USER1 = 'sonicauto@lusunshine1314163.onmicrosoft.com'
    USER2 = 'cyuan@lusunshine1314163.onmicrosoft.com'
    PWD = 'fxhWAN$246'



fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)
fw_page_ui = FWPage(password=Params.G_NEW_PASSWORD)
ula_ui = Browser()

if_v4_api = network.InterfaceIPv4Api(fw)
time_api = system.TimeApi(fw)
pkt_mon_api = system.PacketmonitorApi(fw)
log_api = LogMonitorApi(fw)
licensecli = LicenseCli(fw_cli)
user_local = UserLocalApi(fw)
acl = AccessRuleApi(fw)
ca = system.CertificateApi(fw)
saml_api = SAMLApi(fw)
ao_api = network.AddressobjectsApi(fw)
ag_api = AddressObjectGroupApi(fw)
setting_api = system.SettingApi(fw)
diag_api = system.DiagnosticApi(fw)
log_mon_api = LogMonitorApi(fw)
restart_api = system.RestartApi(fw)
ca_api = system.CertificateApi(fw)
local_user_api = UserLocalApi(fw)
user_setting_api = UsersettingApi(fw)
zone_api = network.ZoneObjectsApi(fw)
admin_api = system.AdminApi(fw)
cfo_profile_api = CfoProfilesApi(fw)
cfs_api = ContentFilterPolicyApi(fw)

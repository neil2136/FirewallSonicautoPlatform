import os
import sys
import re
import time
import copy
import json
import subprocess
import random
import unittest
import string
import urllib3
from collections import OrderedDict
import requests

from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test, skip_if_fail_method, repeat_method
from runner.utils.assertion import Assertion
from runner.settings import Params, logger

# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall

# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.users import SAMLApi
from lib.modules.CLI.users import SAMLCli
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from modules.ui.fw_page import FWPage
from modules.ui.ui_wrapper import Browser


sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
suite_path = os.environ['PYTHON_SONICOS_HOME'] + '/User/SAML_SSLVPN_UI_Part/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/saml_sslvpn.json'


os_obj = Openstack(Params.testbed)
Console_Info = os_obj.get_console_info(dut='UTM')
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
PC1_ETH0_IP is: {PC1_ETH0_IP}
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH0_IP is: {PC2_ETH0_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
PC3_ETH0_IP is: {PC3_ETH0_IP}
PC3_ETH1_IP is: {PC3_ETH1_IP}
PC3_ETH2_IP is: {PC3_ETH2_IP}
""")

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)
pc3_login = Host(PC3_ETH2_IP)


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2



fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)
fw_page_ui = FWPage(password=Params.G_NEW_PASSWORD)


if_v4_api = network.InterfaceIPv4Api(fw)
time_api = system.TimeApi(fw)
settings_api = system.SettingApi(fw)
pkt_mon_api = system.PacketmonitorApi(fw)
restart_api = system.RestartApi(fw)
diag_api = system.DiagnosticApi(fw)
license_cli = LicenseCli(fw_cli)
saml_api = SAMLApi(fw)
saml_cli = SAMLCli(fw_cli)
ca_api = system.CertificateApi(fw)
acl_api = AccessRuleApi(fw)
sslvpn_api = SSLVPNServerSettingsAPI(fw)
setting_api = system.SettingApi(fw)

idp_add = {
    "authentication_url": "test.com",
    "group_name_attribute": "sonicauto",
    "logout_url": "test.com",
    'name': "idp",
    'server_id': "11",
    'trusted_certificate': "OneLogin Account  (0482EEBEB71556A11F5D8252B9F5F754A21AF08F)",
    'user_name_attribute': "sonicauto"
}
idp_import = {
    "authentication_url": "",
    "group_name_attribute": "sonicauto",
    "logout_url": "",
    'name': "idp_import",
    'server_id': "",
    'trusted_certificate': "Microsoft Azure Federated SSO Certificate (15F23AEA1860B094449084CD5088F2F0)",
    'user_name_attribute': "sonicauto"
}
svc_provider = {
    'address_object': "X1 IP",
    'name': "sp_tc25",
    'service': {'https': True},
    'type': "ip"
}
saml_profile = {
    'identity_provider': "idp_tc25",
    'management': True,
    'name': "profile_tc25",
    'service_provider': "sp_tc25",
    'single_sign_off': False,
    'sslvpn': False,
    'use_certificate_sign_sp_request': False
}
idp_cli = {
    'idp_name': 'idp_tc20',
    'auth_url': 'test.com',
    'group-name-attribute': 'idp_tc20',
    'logout-url': 'test.com',
    'server-id': 'idp_tc20',
    'trusted-certificate': 'OneLogin\ Account\ \ (0482EEBEB71556A11F5D8252B9F5F754A21AF08F)',
    'user-name-attribute': 'idp_tc20'
}

locate_profile_https = ['xpath', '//*[text()="profile_https"]']
locate_profile_sslvpn = ['xpath', '//*[text()="profile_sslvpn"]']
locate_apply = ['xpath','//*[text()="Apply"]']
locate_profile_expand = ['xpath',
                                 '//*[text()="profile_sslvpn"]/parent::*/preceding-sibling::div[contains(@class, "sw-table-row__cell--typed-col")]']
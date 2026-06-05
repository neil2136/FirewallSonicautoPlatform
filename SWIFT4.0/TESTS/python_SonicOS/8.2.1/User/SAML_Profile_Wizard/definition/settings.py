import os
import sys
import re
from datetime import datetime, timedelta
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
# from modules.API.object import ServicesApi
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.users import SAMLApi
from lib.modules.CLI.users import SAMLCli
from modules.ui.fw_page import FWPage

sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
suite_path = os.environ['PYTHON_SONICOS_HOME'] + '/User/SAML_Profile_Wizard/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/saml_profile_settings.json'
cert_file = suite_path + 'definition/sonicauto.cer'

# xml_file = suite_path + 'definition/file/SAML.xml'

os_obj = Openstack(Params.testbed)
Console_Info = os_obj.get_console_info(dut='UTM')
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')

logger.info(f"""
PC1_ETH0_IP is: {PC1_ETH0_IP}
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH1_IP is: {PC1_ETH2_IP}
PC2_ETH0_IP is: {PC2_ETH0_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH1_IP is: {PC2_ETH2_IP}
""")

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)


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
fw_page_ui = FWPage(password='S0nic@uto')

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
svc_obj = network.ServiceObjectApi(fw)
base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
url = base_url + 'users/users-settings'

idp_add = {
    'name': "idp_azure",
    "authentication_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
    "group_name_attribute": "department",
    "logout_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
    'server_id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/",
    'trusted_certificate': "Microsoft Azure Federated SSO Certificate (673F596265895E9643B1FD8B785D1EA4)",
    'user_name_attribute': "displayname"
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
    "domain_name": "shanghaiqa.com",
    'name': "sp_azure",
    'service': {'https': True},
    'type': "domain"
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
    'auth_url': 'https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2',
    'group-name-attribute': 'idp_tc20',
    'logout-url': "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
    'server-id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/",
    # 'trusted-certificate': "Microsoft Azure Federated SSO Certificate (673F596265895E9643B1FD8B785D1EA4)",
    'trusted-certificate': "Microsoft\ Azure\ Federated\ SSO\ Certificate\ (673F596265895E9643B1FD8B785D1EA4)",
    'user-name-attribute': 'idp_tc20'
}

next_button_xpath = '//*[text()="Next"]'
apply_xpath = '//button[text()="Apply"]'
close_xpath = '(//button[text()="Close"])[2]'
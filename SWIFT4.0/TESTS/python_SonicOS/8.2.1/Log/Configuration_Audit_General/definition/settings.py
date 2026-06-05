import os
import sys
import re
import time
import json

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from tools.send_fetch_email import Email
from util.dpissl.lib.mail_server import StartMailServer

# import form branch lib contents for test suit
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.system import RestartApi, SettingApi
from lib.modules.API.diag import DiagApi
from lib.modules.API.log import AuditlogMonitorApi, LogAutomationApi
from lib.modules.CLI.log import AuditLogsCli
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Configuration_Audit_General/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/Configuration_Audit_General.json'

common_dpissl_path = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/'
common_cert_path = '/util/dpissl/config/server_imaps/'
postfix_2k_path = common_dpissl_path + 'config/server_imaps/postfix_2k/'
dovecot_2k_path = common_dpissl_path + 'config/server_imaps/dovecot_2k/'
mail_server_path = common_dpissl_path + 'cert/'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
mail_server_ip = PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
setup_mail_server = StartMailServer(
    PC3_login,
    postfix_2k_path,
    dovecot_2k_path,
    mail_server_path + 'vsftpd_2k.key',
    mail_server_path + 'vsftpd_2k.crt')
mail = Email(mail_server_ip, 'test', 'password', use_ssl=False)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.168'
    X1_GW = '172.16.1.1'
    X1_SUBNET = '172.16.1.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    X2_IP = '192.168.20.168'
    MASK = '255.255.255.0'
    X4_IP = '192.168.40.168'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)
interfacev4api = InterfaceIPv4Api(fw)
diagapi = DiagApi(fw)
restartapi = RestartApi(fw)
auditapi = AuditlogMonitorApi(fw)
logautomationapi = LogAutomationApi(fw)
auditlogscli = AuditLogsCli(fw_cli)
settingapi = SettingApi(fw)


# parameters on the test cases
audit_contain_dict = {
    'group_name': 'Network Interfaces',
    'group_index': 'X2',
    'description': " 'LAN/DMZ/WLAN IP Address' ",
    'old_value': '0.0.0.0',
    'new_value': '192.168.20.168',
    'user': 'admin',
    'status': 'Succeeded',
    'destination': '192.168.168.168 (443)',
    'interface': 'X0',
}

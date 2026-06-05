import os
import re
import sys
import copy
import time
import unittest
import paramunittest
import json

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar
import re

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suite
from lib.modules.API import network
from lib.modules.API.users import UserLocalApi
from lib.modules.API.network import DHCPServerApi, AddressobjectsApi
from lib.modules.API.users import UserGuestApi
from lib.modules.API.log import LogMonitorApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.log import LogSettingsApi
from lib.modules.API.system import SettingApi, DiagnosticApi
from lib.modules.CLI.system import LicenseCli
from util.dpissl.lib.mail_server import StartMailServer
from lib.modules.API.system import PacketmonitorApi

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Guest_Services_For_Non_Wireless_Zones_TP2379/'
TESTPLAN = suite_path + 'testplan/Guest_Service_TP2379.json'
defi_path = suite_path + 'definition'
mail_path = defi_path + '/conf_files/mail'
cert_path = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert/'
cert_1K_path = cert_path + 'vsftpd_1k.p12'
cert_2K_path = cert_path + 'vsftpd_2k.p12'
cert_4K_path = cert_path + 'vsftpd_4k.p12'
cert_self_2K_path = cert_path + 'key2048_dell_123456.p12'
common_cert_path = '/util/dpissl/config/server_imaps/'
postfix_1k_path = os.environ["PYTHON_COMMON_HOME"] + common_cert_path + 'postfix_1k/'
dovecot_1k_path = os.environ["PYTHON_COMMON_HOME"] + common_cert_path + 'dovecot_1k/'
postfix_2k_path = os.environ["PYTHON_COMMON_HOME"] + common_cert_path + 'postfix_2k/'
dovecot_2k_path = os.environ["PYTHON_COMMON_HOME"] + common_cert_path + 'dovecot_2k/'
postfix_4k_path = os.environ["PYTHON_COMMON_HOME"] + common_cert_path + 'postfix_4k/'
dovecot_4k_path = os.environ["PYTHON_COMMON_HOME"] + common_cert_path + 'dovecot_4k/'
mail_server_path = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert/'

from definition.send_mail import Email

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')

logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC5_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_host = Host(PC1_ETH0_IP)
PC2_host = Host(PC2_ETH0_IP)
PC3_host = Host(PC3_ETH0_IP)
PC4_host = Host(PC4_ETH0_IP)
PC5_host = Host(PC5_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_SUBNET = '172.17.1.0'
    X1_GW = '172.17.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X2_IP = '192.168.2.168'
    X2_SUBNET = '192.168.2.0'
    X3_IP = '192.168.3.168'
    X3_SUBNET = '192.168.3.0'
    X4_IP = '192.168.4.168'
    X4_SUBNET = '192.168.4.0'
    https_server_ip = "10.6.0.69"
    https_server = f"https://{https_server_ip}"
    http_server = f"http://{https_server_ip}"
    custom_admin_name = "test_user1"
    custom_admin_password = 'S0nic@uto'
    pc4eth1_ip = PC4_ETH1_IP
    PC2_ETH1_MAC = ''
    PC3_ETH1_MAC = ''
    PC4_ETH1_MAC = ''
    PC5_ETH1_MAC = ''

    MAIL_USER1 = 'test1'
    MAIL_USER_PWD = 'password'
    MAIL_SERVER = PC1_ETH2_IP
    MAIL_DOMAIN = 'guest.com'
    ACCOUNT_From = 'test1@guest.com'
    ACCOUNT_To = 'test2@guest.com'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
interface_api = network.InterfaceIPv4Api(fw)
ao_api = network.AddressobjectsApi(fw)
zone_api = network.ZoneObjectsApi(fw)
guest_api = UserGuestApi(fw)
log_api = LogMonitorApi(fw)
localuser_api = UserLocalApi(fw)
dhcpserver_api = DHCPServerApi(fw)
addressobjects_api = AddressobjectsApi(fw)
addressobjectgroup_api = AddressObjectGroupApi(fw)
logsettings_api = LogSettingsApi(fw)
setting_api = SettingApi(fw)
diag_api = DiagnosticApi(fw)
packetobj = PacketmonitorApi(fw)
licensecli = LicenseCli(fw_cli)
mail_server_ip = PC1_ETH2_IP
tb_hostname = PC1_host.send_command('hostname')
start_mail_server = StartMailServer(PC1_host, postfix_2k_path, dovecot_2k_path, mail_server_path + 'vsftpd_2k.key',
                                    mail_server_path + 'vsftpd_2k.crt')

fwcus = Firewall(
    Parameter.FIREWALL,
    user=Parameter.custom_admin_name,
    password=Parameter.custom_admin_password,
    supported_config_mode='api')

zonecusadmin_api = network.ZoneObjectsApi(fwcus)

x2_dict = {
    'if': 'X2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
x3_dict = {
    'if': 'X3',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
x4_dict = {
    'if': 'X4',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X4_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}

zoneedit_dict = {
    "zones": [
        {
            "name": "LAN",
            "guest_services": {
                "enable": True
            }
        }
    ]
}

import os
import re
import sys
import time
import unittest
from runner.settings import logger, Params
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, repeat_method


# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from networkdevice import Host


# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI, SSLVPNClientSettingsAPI
from lib.modules.API.users import UserLocalApi
from lib.modules.API.system import AdminApi
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, FailoverLbApi
from lib.modules.CLI.system import LicenseCli

from sslvpn.common_lib import netextender
from VPN.bin.global_settings import *


# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/CLI/SSH_With_ECLI/'
sys.path.append(suite_path)
from utm import Firewall, FirewallCLI
from definition.utm_new import Firewall_new

TESTPLAN = suite_path + 'testplan/SSH_With_ECLI.json'
SCRIPTS_PATH = suite_path + 'definition/scripts/'


# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
# PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
# PC3_Login = Host(PC3_ETH1_IP)

# Instantiate objects including common_lib import
class Parameter_SSH:
    WANIP = "11.11.11.200"
    platform = os_obj.get_node_platform('UTM')


# Instantiate objects including API,CLI import
ip = Parameter.FIREWALL
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli_1 = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli_2 = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli_3 = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli_4 = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli_p = Firewall(ip, user='admin', password='sonicauto', cli_port='54022', supported_config_mode='cli-ssh')

console_info = os_obj.get_console_info(dut='UTM')
fw_console_login = Firewall(
    ip,
    console_ip=console_info[0],
    console_port=console_info[1],
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-console')

licensecli = LicenseCli(fw_cli)
failoverapi = FailoverLbApi(fw)
interfacecfgapi = InterfaceIPv4Api(fw)

if_api = InterfaceIPv4Api(fw)
admin_api = AdminApi(fw)
ao_api = AddressobjectsApi(fw)
user_api = UserLocalApi(fw)
sslvpn_client_api = SSLVPNClientSettingsAPI(fw)
sslvpn_server_api = SSLVPNServerSettingsAPI(fw)
nx_install = netextender.InstallNX()
nx = netextender.NetextenderConnect(fw)
installnx = netextender.InstallNX()
Rvpn_api = VpnbasesettingApi(rt)
Lvpn_api = VpnbasesettingApi(fw)
RAddr_api = AddressobjectsApi(rt)

# parameters on the test cases
if_x0_dict = {
    'if': 'x0',
    'zone': 'LAN',
    'mode': 'static',
    'ip': ip,
    'netmask': '255.255.255.0',
    'mgmt_ssh': True,
    'mgmt_https': True,
    'mgmt_ping': True
}

SSH_default_Port_dict = {
    "ssh": {
        "port": 22
    }
}

add_ao_cli = [
    'configure',
    'address-object ipv4 test host 192.168.168.11 zone LAN',
    'commit',
    'end',
    'show address-object ipv4 test']

del_ao_dict = {
    'ip_type': 'ipv4',
    'name': 'test'
}

ao_dict_tc11 = {
    "object_type": "host",
    "ip_type": "ipv4",
    "name": '1.1.1.1',
    "zone": "LAN",
    "value": '1.1.1.1',
}

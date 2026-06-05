import os
import sys
import re
import time
import copy
import requests
from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + 'Upgrade/Platform_Upgrade_Via_UI/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + 'Upgrade/Platform_Upgrade_Via_UI')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
           '/Upgrade/Platform_Upgrade_Via_UI/testplan/platform_upgrade.json'

from utm import Firewall
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from util.openstack import Openstack
from lib.modules.API.network import AddressobjectsApi, InterfaceIPv4Api
from lib.modules.API.securityservices import ContentFilterPolicyApi
from lib.modules.CLI.system import LicenseCli, AdminCli
from lib.modules.API.system import SettingApi
from lib.modules.CLI.system import SettingCli
from lib.modules.API.policy import NatPolicyApi, SecurityPolicyApi


os_obj = Openstack(Params.testbed)
platform_name = os_obj.get_node_platform('UTM')


# parameters on the openstack
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0/24'
    X1_IP = '12.12.1.200'
    X1_NAT_IP = '12.12.1.201'
    MASK = '255.255.255.0'
    X1_SUBNET = '12.12.1.0/24'
    X1_GW = '12.12.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2

    PC1_ETH0 = '192.168.168.169'
    PC2_ETH0 = '12.12.1.210'
    PC2_ETH1 = '10.20.1.210'

    prebuild = Params.prebuild
    testbuild = Params.build


uuid_dict = {
    'TZ370-PROTOTYPE': '1523729', # troubleshooting needed
    'TZ270': '1523729',
    'TZ270W': '1523732',
    'TZ270W-PROTOTYPE': '1523732',
    'TZ370': '1523735',
    'TZ370W': '1523738',
    'TZ470': '1523741',
    'TZ470W': '1523744',
    'TZ570': '1523714',
    'TZ570P': '1523716',
    'TZ570W': '1523721',
    'TZ670': '1523723',
    'NSA2700': '1523747',
    'NSA3700': '1523753',
    'NSA4700-PROTOTYPE': '1529199',
    'NSA5700-PROTOTYPE': '1529201',
    'NSA6700-PROTOTYPE': '1529203',
    'NSSP 10700-PROTOTYPE': '1529205',
    'NSSP 11700-PROTOTYPE': '1529207',
    'NSSP 13700-PROTOTYPE': '1529209',
}
import_dict = {
   'protocol': 'scp',
   'passwd': 'password',
   'server': '192.168.168.169',
   'user': 'root',
   'file': Parameter.prebuild
}
# paramenters on the test case
nat_ipv4_dict = {
    "nat_policies": [
        {
            "ipv4": {
                "comment": 'autoadd01',
                "destination": {
                    "name": Parameter.X1_NAT_IP
                },
                "enable": True,
                "inbound": "X1",
                "name": "AutoAddRule",
                "outbound": "any",
                "service": {
                    "group": "ICMP"
                },
                "translated_destination": {
                    "name": Parameter.PC1_ETH0
                },
                "source": {
                    "any": True
                }
            }
        }
    ]
}


# generate object names including API,CLI
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
# config FW and PC
admincli = AdminCli(fw_cli)
licensecli = LicenseCli(fw_cli)
localaoapi = AddressobjectsApi(fw)
interfacecfgapi = InterfaceIPv4Api(fw)
# generate object name for test cases
fwupgradeapi = SettingApi(fw)
fwupgradecli = SettingCli(fw_cli)
natpolicyconfapi = NatPolicyApi(fw)
hostconf = Host('localhost')


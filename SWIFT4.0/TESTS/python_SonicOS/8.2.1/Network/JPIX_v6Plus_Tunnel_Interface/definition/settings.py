import os
import sys
import re
from datetime import datetime, timedelta
from time import sleep
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

from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall

# import form branch lib contents for test suite
# sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.CLI.system import TimeCli, AdminCli, LicenseCli, SettingCli
from lib.modules.API.log import LogSettingsApi, LogMonitorApi
from lib.modules.CLI.vpn import VpnBaseSettingsCli, VpnAdvancedSettingsCli
from lib.modules.CLI.network import RouteCli, InterfaceCli
from lib.modules.CLI.firewallsettings import CiphercontrolCli
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.network import AddressobjectsApi

## register root path for suite
suite_path = os.environ["PYTHON_SONICOS_HOME"]+ "/Network/JPIX_v6Plus_Tunnel_Interface/"
TESTPLAN = suite_path + "testplan/JPIX_v6Plus_tunnel_interface.json"


# os_obj = Openstack(Params.testbed)
# Console_Info = os_obj.get_console_info(dut='UTM')
# PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
# PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
# PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')

# PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
# PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
# PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')

# logger.info(f'\n PC1_ETH0_IP is: {PC1_ETH0_IP}'
#             f'\n PC1_ETH1_IP is: {PC1_ETH1_IP}'
#             f'\n PC1_ETH2_IP is: {PC1_ETH2_IP}'
#             f'\n PC2_ETH0_IP is: {PC2_ETH0_IP}'
#             f'\n PC2_ETH1_IP is: {PC2_ETH1_IP}'
#             f'\n PC2_ETH2_IP is: {PC2_ETH2_IP}')

# passwords = os_obj.get_image_pw(["PC1","PC2"])
# PC1_login = Host(PC1_ETH2_IP, password=passwords["PC1"])
# PC2_login = Host(PC2_ETH2_IP, password=passwords['PC2'])
PC1_ETH0_IP = '192.168.168.65'
PC1_login = Host(PC1_ETH0_IP, password='sonicauto')

## parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    x1_v6_static = '2001:1:2:3::100'
    

fw = Firewall(Parameter.FIREWALL,user='admin',password='password',supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL,user='admin',password='password',supported_config_mode='cli-ssh')

if_v4_api = network.InterfaceIPv4Api(fw)
if_v6_api = network.InterfaceIPv6Api(fw)
ao_api = network.AddressobjectsApi(fw)
acl_api = AccessRuleApi(fw)
nat_api = network.NatpolicyApi(fw)
route_api = network.RoutePolicyApi(fw)
pkt_api = system.PacketmonitorApi(fw)
setting_api = system.SettingApi(fw)
license_cli = LicenseCli(fw_cli)
restart_api = system.RestartApi(fw)
interface_cli = InterfaceCli(fw_cli)
diagnostic_api = system.DiagnosticApi(fw)


route_base = {
    "comment": "",
    "destination": {"name": "12.12.3.0/24"},
    "disable_on_interface_down": True,
    "distance": {"auto": True},
    "gateway": {"default": True},
    "interface": "t1",
    "mask": "0x00",
    "metric": 6,
    "name": "My Rule",
    "probe": "",
    "service": {"any": True},
    "source": {"name": "X0 Subnet"},
    "tos": "0x00",
    "type": "standard",
    "vpn_precedence": False,
    "ticket": {"tag1": "", "tag2": "", "tag3": ""},
    "priority": 1
}
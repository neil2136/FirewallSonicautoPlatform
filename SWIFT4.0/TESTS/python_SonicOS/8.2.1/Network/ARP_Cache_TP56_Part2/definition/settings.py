import os
import sys
import re
import copy
import time
from contextvars import ContextVar

from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from nose_parameterized import parameterized
import paramunittest

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import AddressobjectsApi, InterfaceIPv4Api, ArpApi, NatpolicyApi, RoutePolicyApi
from lib.modules.API.system import PacketmonitorApi, SettingApi,TimeApi, DiagnosticApi
from lib.modules.CLI.network import InterfaceCli, RouteCli,ARPCli
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Network/ARP_Cache_TP56_Part2/'
sys.path.append(suite_path)
defi_path = suite_path + 'definition'
TESTPLAN = suite_path + 'testplan/arp.json'
scripts_path = suite_path + 'definition/scripts'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
logger.info(
    f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
    f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
    f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
    f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
    f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
    f'\n PC2_ETH2_IP: {PC2_ETH2_IP}'
)
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH1_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    X1_IP = '13.0.0.168'
    X1_GW = '13.0.0.1'
    X1_DNS1 = '10.103.202.200'
    X2_IP = '172.16.1.168'
    LAN_PC = PC1_ETH0_IP
    DMZ_PC = PC2_ETH0_IP
    WAN_PC = PC2_ETH2_IP

    X0_PC_MAC = ''
    X1_PC_MAC = ''
    X2_PC_MAC = ''
    DUT_X0_MAC = ''
    DUT_X1_MAC = ''
    DUT_X2_MAC = ''
    FAKE_MAC = 'FA:16:3E:AA:12:18'
    FAKE_IP = '172.16.1.200'
    FAKE_WAN_IP = '13.0.0.200'
    SECONDARY_IP = '172.18.1.168'
    SECONDARY_PC = '172.18.1.200'
    SECONDARY_NETWORK = '172.18.1.0'


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api'
)

fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh'
)

interfaceapi = InterfaceIPv4Api(fw)
arpapi = ArpApi(fw)
pkgapi = PacketmonitorApi(fw)
interfacecli = InterfaceCli(fw_cli)
diagapi = DiagnosticApi(fw)
natpolicyapi = NatpolicyApi(fw)
aoapi = AddressobjectsApi(fw)
accessruleapi = AccessRuleIPv4Api(fw)
settingapi = SettingApi(fw)
routeapi = RoutePolicyApi(fw)
arpcli = ARPCli(fw_cli)
licensecli = LicenseCli(fw_cli)

static_arp_dict = {
    'ip': '',
    'mac': '',
    'interface': 'X2',
    'publish': False,
    'bind_mac': False,
    'dynamic': False
}

nat_base_dict = {
    "name": '',
    "enable": True,
    "comment": "test for add a nat policy",
    "inbound": "any",
    "outbound": "any",
    "source": {
        "any": True
    },
    "translated_source": {
        "original": True
    },
    "destination": {
        "any": True
    },
    "translated_destination": {
        "original": True
    },
    "service": {
        "any": True
    },
    "translated_service": {
        "original": True
    },
    "ticket": {
        "tag1": "",
        "tag2": "",
        "tag3": ""
    }
}

wan_to_dmz_dict = {
    'name': 'Default Access Rule',
    'from': 'WAN',
    'to': 'DMZ',
    'source_addr': {'any': True},
    'dst_addr': {'any': True},
    'service': {'any': True},
    'action': 'allow',
    'comment': '',
}

route_base_dict = {
    "interface": "",
    "metric": 1,
    "source": {"any": True},
    'destination': {'any': True},
    'service': {'any': True},
    'gateway': {'name': ''},
    "tos": "0x00",
    "mask": "0x00",
            "distance": {"auto": True},
            "name": 'test_route',
            "type": "standard",
            "priority": 1,
            "comment": "",
            "disable_on_interface_down": False,
            "vpn_precedence": False,
            "probe": "",
            "ticket": {"tag1": "", "tag2": "", "tag3": ""}
}

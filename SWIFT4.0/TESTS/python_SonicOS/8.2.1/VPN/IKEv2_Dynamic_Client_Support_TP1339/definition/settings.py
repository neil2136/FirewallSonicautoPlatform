import os
import sys
import copy
import ast
import re
import time
import json
import winrm
import requests
import unittest
import paramunittest
from nose_parameterized import parameterized
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, FirewallCLI
from util.enhancedinfo import show_testcase_info
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi
from lib.modules.API.vpn import VpnbasesettingApi, VpnAdvancedsettingApi
from lib.modules.CLI.vpn import VpnAdvancedSettingsCli, VpnBaseSettingsCli
from lib.modules.API.system import DiagnosticApi, RestartApi, CertificateApi, SettingApi
from lib.modules.API.log import LogMonitorApi, LogCategoryApi
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IKEv2_Dynamic_Client_Support_TP1339'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/ikev2_dynamic_client_support_tp1339.json'
SCRIPTS_PATH = suite_path + '/definition/scripts'
CERT4k_PATH = suite_path + '/definition/cert/rsa4k.pfx'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            )

PC1_Login = Host(PC1_ETH0_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)


#################################################################################################################
#
#
#  PC1(eth1)--------x0(192.168.168.168)DUT x1(12.12.1.101)---------(12.12.1.201) X1 remote DUT(X3)---------PC3
#  PC2(eth1)--------x2(193.168.1.168) |
#
#
#
#################################################################################################################


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X2_NET = '193.168.1.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X2_IP = '193.168.1.168'
    X0_REMOTE_IP = '172.16.1.101'
    X1_REMOTE_IP = '12.12.1.201'
    X3_REMOTE_IP = '12.12.3.201'
    X3_REMOTE_NET = '12.12.3.0'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


class ParamCases:
    tc01ikev2settings = False


ip = Parameter.FIREWALL
r_ip = Parameter.X0_REMOTE_IP
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
r_fw_api = Firewall(r_ip, user='admin', password='sonicauto', supported_config_mode='api')

interfacev4api = InterfaceIPv4Api(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
vpnbasesettingapi = VpnbasesettingApi(fw_api)
r_vpnbasesettingapi = VpnbasesettingApi(r_fw_api)
r_interfacev4api = InterfaceIPv4Api(r_fw_api)
r_addressobjectsapi = AddressobjectsApi(r_fw_api)
diagnosticapi = DiagnosticApi(fw_api)
vpnadvancedsettingapi = VpnAdvancedsettingApi(fw_api)
vpnadvancedsettingscli = VpnAdvancedSettingsCli(fw_cli)
vpnbasesettingscli = VpnBaseSettingsCli(fw_cli)
restartapi = RestartApi(fw_api)
settingapi = SettingApi(fw_api)
locertificateapi = CertificateApi(fw_api)
recertificateapi = CertificateApi(r_fw_api)
logmonitorapi = LogMonitorApi(fw_api)
logcategoryapi = LogCategoryApi(fw_api)
routepolicyapi = RoutePolicyApi(fw_api)
r_routepolicyapi = RoutePolicyApi(r_fw_api)
licensecli = LicenseCli(fw_cli)


modify_vpn_advanced_dict = {
    "vpn": {
        "enable": True,
        "firewall_identifier": "2CB8ED6F9ED0",
        "cleanup_tunnels": True,
        "preserve_ike_port": False,
        "traps_on_change": False,
        "nat_traversal": True,
        "ocsp_checking": False,
        "responder_url": "",
        "frag_packets": {
            "enable": True,
            "ignore_df_bit": False
        },
        "ike_dpd": {
            "enable": True,
            "interval": 60,
            "trigger": 3,
            "idle_dpd": False,
            "idle_dpd_interval": 600
        },
        "dns": {
            "server": {
                "inherit": True
            }
        },
        "wins": {
            "primary": "0.0.0.0",
            "secondary": "0.0.0.0"
        },
        "ikev2": {
            "send_cookie": False,
            "send_invalid_spi": True,
            "proposal": {
                "dh_group": "2",
                "encryption": "aes-gcm16-128",
                "prf": "hmac-sha-256"
            }
        }
    }
}

initial_pbr_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "test",
                "comment": "",
                "interface": "Nii",
                "metric": 20,
                "service": {
                    "any": True
                },
                "gateway": {
                    "default": True
                },
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "130.1.1.0"
                },
                "disable_on_interface_down": True,
                "probe": "",
                "distance": {
                    "auto": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "type": "standard",
                "auto_add_access_rules": True
            }
        }
    ]
}

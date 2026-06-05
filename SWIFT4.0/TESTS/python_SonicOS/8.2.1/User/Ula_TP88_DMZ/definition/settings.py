import os
import sys
import re
import time
import copy
import requests
import asyncio
import unittest
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack

# import form branch lib contents for test suit
from lib.modules.API import network
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import policy
from lib.modules.API import users
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.CLI.firewall import AccessRuleCli
from lib.modules.API.users import UsersettingApi


suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_DMZ/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_DMZ/testplan/ula.json'
CONF_PATH = suite_path + 'definition/config'
HTTPS_SERVER_PATH = CONF_PATH + '/httpserver'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
configPath = os.environ["PYTHON_SONICOS_HOME"] + '/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/'
G_PASSWORD_NEW = Params.G_NEW_PASSWORD
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
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
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            f'\n PC3_ETH0_IP: {PC3_ETH0_IP}'
            f'\n PC3_ETH1_IP: {PC3_ETH1_IP}'
            f'\n PC4_ETH0_IP: {PC4_ETH0_IP}'
            f'\n PC4_ETH1_IP: {PC4_ETH1_IP}'
            f'\n PC5_ETH0_IP: {PC5_ETH0_IP}'
            f'\n PC5_ETH1_IP: {PC5_ETH1_IP}'
            f'\n FW_DNS1_IP: {Params.G_DNS1}'
            f'\n FW_DNS2_IP: {Params.G_DNS2}')
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)
PC5_login = Host(PC5_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    X2_IP = '12.12.2.168'
    X2_GW = '12.12.2.1'
    X2_SUBNET = '12.12.2.0'
    VALID_DNS = PC4_ETH1_IP
    FAKE_DNS1 = '2.2.2.2'
    FAKE_DNS2 = '3.3.3.3'
    X3_IP = '192.168.3.168'

    prebuild = Params.prebuild
    testbuild = Params.build

    R_X0_IP = '172.16.1.101'
    R_X1_IP = '12.12.1.201'
    R_X2_IP = '12.12.2.201'
    R_X0_NET = '172.16.1.0'
    R_X3_IP = '12.12.3.201'
    VPN_IF_IP_LOCAL = '1.1.1.2'
    VPN_IF_IP_REMOTE = '1.1.1.1'


class CaseParams:
   
    ula_user_name = 'auto_ula_test'


fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password=G_PASSWORD_NEW,
    supported_config_mode='api')
r_fw = Firewall(
    Parameter.R_X3_IP,
    user='admin',
    password=G_PASSWORD_NEW,
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password=G_PASSWORD_NEW,
    supported_config_mode='cli-ssh')

interfaceapi = network.InterfaceIPv4Api(fw)
licensecli = LicenseCli(fw_cli)
r_interfaceapi = network.InterfaceIPv4Api(r_fw)
r_accessruleapi = firewall.AccessRuleApi(r_fw)
fwupgradeapi = system.SettingApi(fw)
statusapi = system.StatusApi(fw)
userLocalapi = users.UserLocalApi(fw)
usersettingapi = users.UsersettingApi(fw)
userstatusapi = users.UserStatusApi(fw)
restartapi = system.RestartApi(fw)
access_rules = AccessRuleIPv4Api(fw)
accessrulecli = AccessRuleCli(fw_cli)
user_status = users.UserStatusApi(fw)
user_setting = UsersettingApi(fw)

x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
x2_wan_dict = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X2_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
x3_dmz_dict = {
    'if': 'X3',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
}

default_acl_dict = {
    # "uuid": '',
    "name": "Default Access Rule",
    "enable": True,
    "from": "LAN",
    "to": "WAN",
    "action": "allow",
    "source": {
        "address": {
            "any": True
        },
        "port": {
            "any": True
        }
    },
    "service": {
        "any": True
    },
    "destination": {
        "address": {
            "any": True
        }
    },
    "schedule": {
        "always_on": True
    },
    "users": {
        "included": {
            'all': True
        },
        "excluded": {
            "none": True
        }
    },
    "comment": "",
    "fragments": True,
    "logging": True,
    "sip": False,
    "h323": False,
    "flow_reporting": False,
    "botnet_filter": False,
    "geo_ip_filter": {
        "enable": False,
        "global": True
    },
    "block": {
        "countries": {
            "unknown": False
        }
    },
    "packet_monitoring": False,
    "management": False,
    "max_connections": 100,
    "priority": {
        "manual": {
            "value": 13
        }
    },
    "tcp": {
        "timeout": 15,
        "urgent": False
    },
    "udp": {
        "timeout": 30
    },
    "connection_limit": {
        "source": {},
        "destination": {}
    },
    "dpi": True,
    "dpi_ssl": {
        "client": True,
        "server": True
    },
    "redirect_unauthenticated_users_to_log_in": True,
    "quality_of_service": {
        "class_of_service": {},
        "dscp": {
            "preserve": True
        }
    }
}

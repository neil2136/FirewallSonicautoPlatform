import os
import sys
import re
import time
import copy
import requests
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
from lib.modules.API.users import UsersettingApi
from lib.modules.API.system import DiagnosticApi, RestartApi, SettingApi, SNMPApi
from modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = (
    os.environ["PYTHON_SONICOS_HOME"] + "/Network/PPPoE_Unnumbered_Interface_Part2/"
)
sys.path.append(suite_path)
sys.path.append(suite_path + "testcases")
TESTPLAN = suite_path + "testplan/PPPoE_Unnumbered_Interface.json"
CONF_PATH = suite_path + "definition/config"
HTTPS_SERVER_PATH = CONF_PATH + "/httpserver"
certPath = os.environ["PYTHON_COMMON_HOME"] + "/util/dpissl/cert"
configPath = (
    os.environ["PYTHON_SONICOS_HOME"] + "/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/"
)

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip("PC1", "eth0")
PC1_ETH1_IP = os_obj.get_node_interface_ip("PC1", "eth1")
PC2_ETH0_IP = os_obj.get_node_interface_ip("PC2", "eth0")
PC2_ETH1_IP = os_obj.get_node_interface_ip("PC2", "eth1")
PC3_ETH0_IP = os_obj.get_node_interface_ip("PC3", "eth0")
PC3_ETH1_IP = os_obj.get_node_interface_ip("PC3", "eth1")
PC4_ETH0_IP = os_obj.get_node_interface_ip("PC4", "eth0")
PC4_ETH1_IP = os_obj.get_node_interface_ip("PC4", "eth1")
logger.info(
    f"\n PC1_ETH0_IP: {PC1_ETH0_IP}"
    f"\n PC1_ETH1_IP: {PC1_ETH1_IP}"
    f"\n PC2_ETH0_IP: {PC2_ETH0_IP}"
    f"\n PC2_ETH1_IP: {PC2_ETH1_IP}"
    f"\n PC3_ETH0_IP: {PC3_ETH0_IP}"
    f"\n PC3_ETH1_IP: {PC3_ETH1_IP}"
    f"\n PC4_ETH0_IP: {PC4_ETH0_IP}"
    f"\n PC4_ETH1_IP: {PC4_ETH1_IP}"
    f"\n FW_DNS1_IP: {Params.G_DNS1}"
    f"\n FW_DNS2_IP: {Params.G_DNS2}"
)
PC1_login = Host(PC1_ETH0_IP)
PC2_login = Host(PC2_ETH0_IP)
PC3_login = Host(PC3_ETH0_IP)
PC4_login = Host(PC4_ETH0_IP)


# parameters on the fw
class Parameter:
    FIREWALL = "192.168.168.168"
    X1_IP = "12.12.1.168"
    X1_SUBNET = "12.12.1.0"
    X1_GW = "12.12.1.1"
    X1_NAT = "12.12.1.0"
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = "255.255.255.0"
    X2_IP = "192.168.2.168"
    X2_SUBNET = "192.168.2.0"
    X3_IP = "192.168.3.168"
    X3_GW = "192.168.3.1"
    X3_SUBNET = "192.168.3.0"
    # Change X2 IP
    X2_IP_NEW_1 = "192.168.2.200"
    # Change X2 Subnet
    X2_IP_NEW_2 = "192.168.222.250"
    X2_NETMASK_NEW = "255.255.255.240"


# Instantiate objects including API,CLI import
fw = Firewall(
    Parameter.FIREWALL, user="admin", password="sonicauto", supported_config_mode="api"
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user="admin",
    password="sonicauto",
    supported_config_mode="cli-ssh",
)
interfaceapi = network.InterfaceIPv4Api(fw)
zonesapi = network.ZoneObjectsApi(fw)
accessruleapi = AccessRuleIPv4Api(fw)
dhcpserverapi = network.DHCPServerApi(fw)
diagapi = DiagnosticApi(fw)
natapi = network.NatpolicyApi(fw)
restartapi = RestartApi(fw)
settingapi = SettingApi(fw)
snmpapi = SNMPApi(fw)
licensecli = LicenseCli(fw_cli)


class PPPoeParams:
    PPPOE_IF = "eth1"
    LOCAL_IP = PC4_ETH1_IP
    PPPOE_ASSIGN = Parameter.X2_IP
    PPP_SECRETS = f'{os.environ["PYTHON_SONICOS_HOME"]}/Network/PPPoE_Unnumbered_Interface_Part2/definition/config/pppoe/pap-secrets'
    PPPOE_OPTIONS = f'{os.environ["PYTHON_SONICOS_HOME"]}/Network/PPPoE_Unnumbered_Interface_Part2/definition/config/pppoe/pppoe-server-options'
    PPPOE_DOWN_IP = "0.0.0.0"


class CaseParams:
    wan_host_ip = PC4_ETH1_IP
    out_wan_host_ip = "22.22.22.22"
    include_x1_ip_range = "12.12.1.40-170"
    include_x1_gw_range = "12.12.1.1-20"
    in_wan_range1 = "12.12.1.10-100"
    in_wan_range2 = "12.12.1.90-120"
    in_wan_range3 = "12.12.1.171-200"
    out_wan_range = "22.22.22.171-200"
    custom_zone = "auto_test1"
    x3_network_range = "192.168.3.10-200"
    ao_group_name = "auto_include_host_range"
    exp_file_path = f"/tmp/pppoe_unnumbered_{Params.product}.exp"

    # PPPoE Unnumbered Common Settings
    x1_pppoe_unnum_dict = {
        "if": "x1",
        "zone": "WAN",
        "mode": "pppoe",
        "pppoe_unnumbered": "X2",
        "pppoe_user": "root",
        "pppoe_servicename": "def",
        "pppoe_passwd": "password",
        "mgmt_https": True,
        "mgmt_ssh": True,
        "mgmt_ping": True,
        "user_https": True,
        "mgmt_snmp": True,
    }

    x2_lan_unnum_dict = {
        "if": "x2",
        "zone": "LAN",
        "mode": "unnumbered",
        "ip": Parameter.X2_IP,
        "netmask": "255.255.255.0",
        "mgmt_https": True,
        "mgmt_ssh": True,
        "mgmt_ping": True,
        "user_https": True,
        "mgmt_snmp": True,
    }


# Init Settings
x1_wan_dict = {
    "if": "X1",
    "zone": "WAN",
    "mode": "static",
    "ip": Parameter.X1_IP,
    "netmask": Parameter.MASK,
    "gateway": Parameter.X1_GW,
    "dns1": Parameter.X1_DNS1,
    "dns2": Parameter.X1_DNS2,
    "mgmt_https": True,
    "mgmt_ssh": False,
    "mgmt_ping": True,
    "user_https": False,
    "mgmt_snmp": False,
}

x2_lan_dict = {
    "if": "X2",
    "zone": "LAN",
    "mode": "static",
    "ip": Parameter.X2_IP,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_ping": True,
    "user_https": False,
    "mgmt_snmp": False,
}

x3_lan_dict = {
    "if": "X3",
    "zone": "LAN",
    "mode": "static",
    "ip": Parameter.X3_IP,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_ping": True,
    "user_https": False,
    "mgmt_snmp": False,
}

snmp_user_group = "snmpgGroup"

snmp_user_dict = {
    "user_name": "snmpUser",
    "user_security": "",
    "user_group": snmp_user_group,
}

snmp_acc_dict = {
    "access_name": "snmpAcc",
    "access_security": "",
    "access_view": "root",
    "access_group": snmp_user_group,
}

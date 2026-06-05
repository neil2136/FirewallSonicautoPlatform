import asyncio
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
from lib.modules.API import users
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.system import (
    DiagnosticApi,
    RestartApi,
    SettingApi,
    SNMPApi,
    PacketmonitorApi,
)

# from modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.CLI.system import LicenseCli

# import form test suite root path like definition
suite_path = (
    os.environ["PYTHON_SONICOS_HOME"] + "/Network/PPPoE_Unnumbered_Interface_Part3/"
)
sys.path.append(suite_path)
sys.path.append(suite_path + "testcases")
TESTPLAN = suite_path + "testplan/PPPoE_Unnumbered_Interface.json"
CONF_PATH = suite_path + "definition/config"
SCRIPTS_PATH = suite_path + "definition/scripts"
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
PC2_ETH1_IP = "192.168.2.192"
PC3_ETH0_IP = os_obj.get_node_interface_ip("PC3", "eth0")
PC3_ETH1_IP = os_obj.get_node_interface_ip("PC3", "eth1")
PC4_ETH0_IP = os_obj.get_node_interface_ip("PC4", "eth0")
PC4_ETH1_IP = os_obj.get_node_interface_ip("PC4", "eth1")
PC5_ETH0_IP = os_obj.get_node_interface_ip("PC5", "eth0")
PC5_ETH1_IP = os_obj.get_node_interface_ip("PC5", "eth1")
X4_VLAN_ID = os_obj.get_node_interface_vlan_id("UTM", "X4:1")
logger.info(
    f"\n PC1_ETH0_IP: {PC1_ETH0_IP}"
    f"\n PC1_ETH1_IP: {PC1_ETH1_IP}"
    f"\n PC2_ETH0_IP: {PC2_ETH0_IP}"
    f"\n PC2_ETH1_IP: {PC2_ETH1_IP}"
    f"\n PC3_ETH0_IP: {PC3_ETH0_IP}"
    f"\n PC3_ETH1_IP: {PC3_ETH1_IP}"
    f"\n PC4_ETH0_IP: {PC4_ETH0_IP}"
    f"\n PC4_ETH1_IP: {PC4_ETH1_IP}"
    f"\n PC5_ETH0_IP: {PC5_ETH0_IP}"
    f"\n PC5_ETH1_IP: {PC5_ETH1_IP}"
    f"\n X4_VLAN_ID: {X4_VLAN_ID}"
    f"\n FW_DNS1_IP: {Params.G_DNS1}"
    f"\n FW_DNS2_IP: {Params.G_DNS2}"
)
PC1_login = Host(PC1_ETH0_IP)  # MGMT
PC2_login = Host(PC2_ETH0_IP)  # LAN
PC3_login = Host(PC3_ETH0_IP)  # LAN
PC4_login = Host(PC4_ETH0_IP)  # LAN
PC5_login = Host(PC5_ETH0_IP)  # WAN


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
    X4_VLAN_IP = "192.168.4.168"
    X4_VLAN_GW = "192.168.4.1"
    X4_VLAN_SUBNET = "192.168.4.0"


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
userstatusapi = users.UserStatusApi(fw)
usersettingapi = users.UsersettingApi(fw)
userLocalapi = users.UserLocalApi(fw)
aoapi = network.AddressobjectsApi(fw)
interfaceapi = network.InterfaceIPv4Api(fw)
zonesapi = network.ZoneObjectsApi(fw)
# accessruleapi = AccessRuleIPv4Api(fw)
accessruleapi = AccessRuleApi(fw)
dhcpserverapi = network.DHCPServerApi(fw)
natapi = network.NatpolicyApi(fw)
diagapi = DiagnosticApi(fw)
packetmonitorapi = PacketmonitorApi(fw)
restartapi = RestartApi(fw)
settingapi = SettingApi(fw)
snmpapi = SNMPApi(fw)
serviceobjectapi = network.ServiceObjectApi(fw)
licensecli = LicenseCli(fw_cli)


class PPPoeParams:
    PPPOE_IF = "eth1"
    LOCAL_IP = PC5_ETH1_IP
    PPPOE_ASSIGN = Parameter.X2_IP
    PPP_SECRETS = f'{os.environ["PYTHON_SONICOS_HOME"]}/Network/PPPoE_Unnumbered_Interface_Part3/definition/config/pppoe/pap-secrets'
    PPPOE_OPTIONS = f'{os.environ["PYTHON_SONICOS_HOME"]}/Network/PPPoE_Unnumbered_Interface_Part3/definition/config/pppoe/pppoe-server-options'
    PPPOE_DOWN_IP = "0.0.0.0"


class CaseParams:
    wan_host_ip = PC5_ETH1_IP

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

    x1_pppoe_unnum_vlan_dict = {
        "if": "x1",
        "zone": "WAN",
        "mode": "pppoe",
        "pppoe_unnumbered": f"X4:V{X4_VLAN_ID}",
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

    x4_vlan_unnum_dict = {
        "name": "X4",
        "vlan": X4_VLAN_ID,
        "ip_assignment": {
            "mode": {
                "unnumbered": {"ip": Parameter.X4_VLAN_IP, "netmask": "255.255.255.0"}
            },
            "zone": "LAN",
        },
        "management": {
            "https": True,
            "ping": True,
            "ssh": True,
            "snmp": True,
        },
        "user_login": {
            "http": False,
            "https": True,
        },
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

x4_vlan_dict = {
    "if": "x4",
    "type": "vlan",
    "vlan_tag": X4_VLAN_ID,
    "zone": "LAN",
    "mode": "static",
    "ip": Parameter.X4_VLAN_IP,
    "mgmt_https": True,
    "mgmt_ssh": True,
    "mgmt_ping": True,
    "user_https": False,
    "mgmt_snmp": False,
}

pc3_ao_dict = {
    "object_type": "host",
    "name": "lan_pc3",
    "zone": "LAN",
    "value": PC3_ETH1_IP,
}


pc3_ssh_serv_obj_dict = {
    "object_type": "tcp",
    "name": "ssh_20022",
    "tcp": {"begin": 20022, "end": 20022},
}

# ACL template
default_acl_dict = {
    "action": "allow",
    "botnet_filter": False,
    "comment": "",
    "connection_limit": {"destination": {}, "source": {}},
    "destination": {"address": {"any": True}},
    "dpi": True,
    "dpi_ssl": {"client": True, "server": True},
    "enable": True,
    "flow_reporting": False,
    "fragments": True,
    "from": "WAN",
    "geo_ip_filter": {"enable": False, "global": True},
    "h323": False,
    "logging": True,
    "management": False,
    "max_connections": 100,
    "name": "Default Access Rule",
    "packet_monitoring": False,
    "priority": {"manual": {"value": 17}},
    "quality_of_service": {"class_of_service": {}, "dscp": {"preserve": True}},
    "redirect_unauthenticated_users_to_log_in": True,
    "schedule": {"always_on": True},
    "service": {"any": True},
    "sip": False,
    "source": {"address": {"any": True}, "port": {"any": True}},
    "tcp": {"timeout": 15, "urgent": False},
    "to": "LAN",
    "udp": {"timeout": 30},
    "users": {"excluded": {"none": True}, "included": {"all": True}},
}

# NAT template
nat_base_dict = {
    "name": "",
    "enable": True,
    "comment": "test for add a nat policy",
    "inbound": "any",
    "outbound": "any",
    "source": {"any": True},
    "translated_source": {"original": True},
    "destination": {"any": True},
    "translated_destination": {"original": True},
    "service": {"any": True},
    "translated_service": {"original": True},
    "ticket": {"tag1": "", "tag2": "", "tag3": ""},
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

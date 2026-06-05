import os
import sys
import re
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])

# from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi
from lib.modules.API.wireguard import WireguardPeerBaseSettingAPI, WireguardTunnelInterfaceAPI, \
    WireguardGeneralSettingAPI
from lib.modules.API.system import CertificateApi, RestartApi
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host

import unittest
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                '/Network/WireGuard_VPN/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/WireGuard_VPN')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
           '/Network/WireGuard_VPN/testplan/wireguard_vpn.json'

g_wgexport = False
g_wgaccess = False

FIREWALL = '192.168.168.168'
X1_IP = '172.16.1.168'
MASK = '255.255.255.0'
X1_GW = '172.16.1.1'
X1_DNS1 = Params.G_DNS1
X1_DNS2 = Params.G_DNS2

PC1_ETH0_IP = '192.168.168.169'
PC2_wg0_IP = '192.168.2.10'
PC2_ETH0_IP = '172.16.1.200'
PC2_ETH1_IP = '10.0.1.200'

WG0_Tunnel_IP = '192.168.2.1'
wg0_Network = '192.168.2.0/24'
wg_tunnel_edit_dict = {
    "comment": "Default WireGuard",
    "ip": "192.168.2.5",
    "netmask": "255.255.255.0",
    "listen_port": 51820,
    "public_key": "",
    "private_key": "",
    "mtu": 1420
}
wg_base_setting_dict = {
    "enable": True,
    "allowedipsany": True
}
wg_valid_name_list = ['SHabc_01', 'SHabc=02', 'SHabc.03', 'SHabc-04']
wg_invalid_name_list = ["CON", "PRN", "AUX", "NUL",
                        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
                        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9", 'test 01']
address_object1 = {
    "object_type": "host",
    "name": PC1_ETH0_IP,
    "zone": "LAN",
    "value": PC1_ETH0_IP
}
address_object2 = {
    "object_type": "host",
    "name": '192.168.168.170',
    "zone": "LAN",
    "value": '192.168.168.170'
}
wg_peer_dict = {
    "name": "autotest10",
    "ip": PC2_wg0_IP,
    "public_key": "",
    "preshared_key": "",
    "private_key": ""
}

fw = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
# lc = LicenseCli(fw_cli)
interfaceipv4 = InterfaceIPv4Api(fw)
ao = AddressobjectsApi(fw)
pc2login = Host(PC2_ETH1_IP)
restartfw =RestartApi(fw)

wgpeerbasesetting = WireguardPeerBaseSettingAPI(fw)
wgtunnelinterface = WireguardTunnelInterfaceAPI(fw)
wgbasesetting = WireguardGeneralSettingAPI(fw)

import os
import sys
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.CLI.network import AddressObjectCli, InterfaceCli
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.API.vpn import VpnbasesettingApi, VpnAdvancedsettingApi
from lib.modules.API.system import PacketmonitorApi
# from trafficGen import ScapyPacketSend
import re
from runner.unittest.suite import UnittestSuite
import unittest

from utm import Firewall
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi
from lib.modules.API.network import ArpApi
from lib.modules.API.network import ZoneObjectsApi
from runner.settings import logger
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from runner.settings import logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/MTU_Settings')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/MTU_Settings/definition')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
testplan = os.environ["PYTHON_SONICOS_HOME"] + '/Network/'


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_IP = '192.168.168.168'
    X0_Net = '192.168.168.0 255.255.255.0'
    TESTPLAN = testplan + 'MTU_Settings/testplan/MTU_Settings.json'

    X1_IP = '12.12.1.168'
    X1_Getway = '12.12.1.1'
    Src_IP = '192.168.168.3'
    Dst_IP = '12.12.1.201'
    VPN2_IP = '12.12.1.201'
    VPN2_Host = '172.16.1.3'
    VPN2_X0_IP = '172.16.1.101'
    VPN2_X0_Net = '172.16.1.0,255.255.255.0'
    x1_Config = {
        'if': 'x1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': X1_IP,
        'netmask': '255.255.255.0',
        'gateway': X1_Getway,
        'mgmt_https': True,
        'mgmt_ping': True,
        'mtu': 1000,
        'ignore_df_bit': False
    }


packer_monitor_config = {
    'bytes_to_capture': 1520,
    'monitor_filter': {
        'destination_ips': Parameter.Dst_IP,
        'destination_ports': '6666',
        'ether_types': '!0x69,!0x806,!0x6a',
    }
}
vpn_packer_monitor_config = {
    'bytes_to_capture': 1520,
    'monitor_filter': {
        'destination_ips': Parameter.VPN2_Host + ',' + Parameter.VPN2_IP,
        'destination_ports': '6666',
        'ether_types': '!0x69,!0x806,!0x6a',
    }
}
send_udp_conf = {
    'iface': 'eth0',
    'dst': Parameter.Dst_IP,
    'lenth': 1458,
    'flags': 2}

local_ao_dict = {
    "object_type": "network",
    "name": "remote_vpn_net",
    "zone": "LAN",
    "value": Parameter.VPN2_X0_Net
}
local_s2svpn_dict = {
    'type': 'site_to_site',  # site_to_site, tunnel_interface
    'name': 'localvpn',
    'pri_gate': Parameter.VPN2_IP,
    'edit_auth': False,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    'secret': '123456',  # add local cert
    # arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'local_ike_type': 'ipv4',
    # arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'peer_ike_type': 'ipv4',
    'local_ike_id': '4.4.4.4',
    'peer_ike_id': '4.4.4.4',

    'edit_network': False,
    'local_net_type': 'name',  # name, group, host, network, range, any,chcp
    'local_net_name': 'X0 Subnet',
    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'remote_vpn_net',
    'keep_alive': True,
}
vpn_advanced_setting_dict = {
    'enable': True,
    'frag_packets': True,
    'ignore_df_bit': True
}
remote_x0_config = {
        'if': 'x0',
        'zone': 'LAN',
        'mode': 'static',
        'ip': Parameter.VPN2_X0_IP,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ping': True,
        'mgmt-ssh': True
    }
remote_ao_dict = {
    'name': 'remote_vpn_net',
            'version': 'ipv4',
            'type': 'network',
            'zone': 'WAN',
            'network': Parameter.X0_Net
}
remote_s2svpn_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
            'name': 'remotevpn',
            'mode': 'shared-secret',  # certificate or shared-secret or manual-key
            'pri_gate': Parameter.X1_IP,
            'secret': '123456',
            'local_ike_id': 'ipv4 4.4.4.4',
            'peer_ike_id': 'ipv4 4.4.4.4',
            'local_net_type': 'name',
            'remote_net_type': 'name',
            'local_network': "'X0 Subnet'",
            'remote_network': 'remote_vpn_net',  # add obj
}

fw = Firewall(Parameter.FIREWALL, user='admin', password='password')
R_fw = Firewall(
    Parameter.VPN2_IP,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

packetmonitor = PacketmonitorApi(fw)
# packetsend = ScapyPacketSend(iface='eth0', count=1)
interface = InterfaceIPv4Api(fw)

localao = AddressobjectsApi(fw)
localvpn = VpnbasesettingApi(fw)
localvpnadvanced = VpnAdvancedsettingApi(fw)

remoteinterface = InterfaceCli(R_fw)
remoteao = AddressObjectCli(R_fw)
remotevpn = VpnBaseSettingsCli(R_fw)

import os
import sys
import re
import copy
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API import firewall
from lib.modules.API import system

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/IPv6_DHCP_Client_2474/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/IPv6_DHCP_Client_2474')

os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
pc1_defaultgw = os_obj.get_pc_default_gw_ip('PC1')
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')

console_info = os_obj.get_console_info(dut= 'DHCPv6_Server')
if console_info:
    consvr = console_info[0]
    conport = console_info[1]

PC1_vlan_eth2 = os_obj.get_node_interface_vlan_id('UTM','X2')

tc_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Client_2474/testcases'
lib_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Client_2474/lib'


ip = '192.168.168.168'
dhcpv6_server = '11.11.11.101'
dhcpv6_server_v6 = "3000::11"
X1_Prefix = "3000::"
X2_Prefix = "2012::"

class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '11.11.11.100'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Client_2474/testplan/IPv6_DHCP_Client_2474.json'
    DIBBLER_SERVER_CONF = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_2474/confs/server.conf'
    DIBBLER_CLIENT_CONF = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_2474/confs/client.conf'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_dhcpv6 = Firewall(dhcpv6_server, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
fw_dhcpv6_server = Firewall(ip, console_ip=consvr, console_port=conport,user='admin', password='password', new_password='password',supported_config_mode='cli-console')

interface_ipv4 = network.InterfaceIPv4Api(fw)
interface_ipv6 = network.InterfaceIPv6Api(fw)
ao_obj = network.AddressobjectsApi(fw)
access_rules_obj = firewall.AccessRuleApi(fw)
service_obj = network.ServiceObjectApi(fw)
natpolicy_obj = network.NatpolicyApi(fw)
packet_obj = system.PacketmonitorApi(fw)

interface_v6_server = network.InterfaceIPv6Api(fw_dhcpv6)
dhcp_v6_server = network.DHCPServerApi(fw_dhcpv6)

localhost = Host('localhost')
httpserver = Host(httpserver_pc)




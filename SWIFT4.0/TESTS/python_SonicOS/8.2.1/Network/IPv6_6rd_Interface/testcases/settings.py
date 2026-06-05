import sys
import re
import os
import time
import copy
import json
import ipaddress
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_6rd_Interface')
from runner.unittest.setup import Test, repeat_method
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.network import DhcpServerCli
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import vpn
from utm import Firewall
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from tools import trafficGen
from lib.modules.CLI.system import LicenseCli


class Parameter():
    DUT_X0_IP = "192.168.168.168" 
    DUT_X0_IPV6 = "2010:0:a8::168"   
    DUT_X1_IP = "12.12.1.168"  
    DUT_X1_GW = "12.12.1.1"  
    DUT_X2_IP = "12.12.2.168"    
    DUT_X2_GW = "12.12.2.1"    
    DUT_X2_IP_NEW = "12.12.2.100"
    DUT_X3_IP = "12.12.3.168"   
    DUT_X3_GW = "12.12.3.1"   
    DUT_X3_NETWORK = "12.12.3.0"
    TUNNEL_IP = '100::100'
    IP_6RD = '2022::100'
    REMOTE_X1 = '12.12.1.201' 
    REMOTE_X2 = '12.12.2.169' 
    REMOTE_X1_GW = '12.12.1.1'
    NETMASK = '255.255.255.0'
    PC1_ETH0 = '192.168.168.100'
    PC1_ETH0_V6 = '2012::100'
    PC2_ETH1 = '12.12.2.100'
    PC3_ETH1 = '12.12.3.100'
    BORDER_RELAY = '4.4.4.4'
    PPPOE_SERVER = PC3_ETH1
    PPPOE_ETH = 'eth1'
    PPPOE_ASSIGH = "12.12.3.168"   
    PPPOE_USER = 'root'
    PPPOE_PASSWD = 'password'
    PPPOE_SERVICE = 'def'
    PPP_FILE    = os.environ['PYTHON_SONICOS_HOME'] + "/Network/IPv6_6rd_Interface/confs/pap-secrets"
    PPPOE_OPTION= os.environ['PYTHON_SONICOS_HOME'] + "/Network/IPv6_6rd_Interface/confs/pppoe-server-options"
    PKG_DIR = '/logs/6rd.png'
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/IPv6_6rd_Interface/testplan/ipv6_6rd_interface.json"

###### new config json by yxu######
Lx1 = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        # 'ip': Parameter.DUT_X1_IP,
        'ip': '12.12.4.20',
        'netmask': '255.255.255.0',
        # 'gateway': Parameter.DUT_X1_GW,
        'gateway': '12.12.4.1',
        'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        }
x0_6rd = {
            'name': 'X0',
            'mode': 'static',
            'type': '6rd',
            'preferred_ip': '::168',
            'prefix_length': 64,
            'subnet_prefix_adv':True,
            # '':
        }
Lx0_ipv6 = {
            'name': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            "ip": "2010:0:a8::33",
            'router_adv':True,
            "managed": True,
            "other_config": True  ,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,  
}
DHCP_6rd = {
            'name': '6rd',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X2'},
            'dynamic': True,
        }
Manual_6rd = {
            'name': '6rd',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X1'},
            'dynamic': False,
            '6rd_prefix': '3::',
            '6rd_prefix_length': 64,
            'border_relay_ipv4_address': '1.2.3.4',
            'mask_length':24
        }
manual_tc44 = {
            'name': 'tc44',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 56,
            'bound_to': {'interface': 'X2'},
            'dynamic': False,
            '6rd_prefix': '2010::',
            '6rd_prefix_length': 40,
            'border_relay_ipv4_address': Parameter.BORDER_RELAY,
            'mask_length':24,
            "default_route":True
        }
tc29_6rd = {
            'name': 'tc29',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 56,
            'bound_to': {'interface': 'X2'},
            'dynamic': False,
            '6rd_prefix': '6868::',
            '6rd_prefix_length': 64,
            'border_relay_ipv4_address': '1.2.3.4',
            'mask_length':24
        }
dhcp_6rd = {
            'name': 'tc16',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X2'},
            'dynamic': True,
        }
x2_dhcp_dict = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'dhcp',
        }
x2_static = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
            'gateway': Parameter.DUT_X2_GW,
        }

pkt_setting= {   
            'display_filter': {
                'bidirectional': True,
                'destination_ips': '',
                'destination_ports': '',
                'ip_types': '6OVER4',
            }
        }

pc2 = Host(Params.testbed + '-PC2')
pc3 = Host(Params.testbed + '-PC3')
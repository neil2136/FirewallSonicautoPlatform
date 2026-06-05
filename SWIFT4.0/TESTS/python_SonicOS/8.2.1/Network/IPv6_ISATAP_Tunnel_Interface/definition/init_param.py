import os
import re
import sys
from time import sleep

import unittest
import paramunittest
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
import threading


sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_ISATAP_Tunnel_Interface')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_ISATAP_Tunnel_Interface/testcases')

from lib.modules.API import network
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '172.16.1.168'
    X1_GW = '172.16.1.1'
    X1_IPv6 = '2004:c03:1a8::202'
    X2_IP = '2.2.2.6'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X0_V100_IP = '4.4.4.5'
    MASK = '255.255.0.0'
   
    PC1_ETH0 = '192.168.168.201'
    PC1_ETH1 = '2.2.2.7'
    PC1_ETH2 = '192.168.2.2'
    PC1_ETH3 = '192.168.3.2'

    PC2_ETH0 = '192.168.4.3'
    PC2_ETH1 = '2.2.2.8'
    PC2_ETH2 = '192.168.2.3'

    PC3_ETH0 = '192.168.5.3'
    PC3_ETH1 = '172.16.1.102'
    PC3_ETH2 = '192.168.3.3'

    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_ISATAP_Tunnel_Interface/testplan/IPv6_ISATAP_Tunnel_Interface.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')

PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')

PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3','eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3','eth2')

logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC1_ETH3_IP :' + PC1_ETH3_IP + '\n' \

    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
    + 'PC2_ETH2_IP :' + PC2_ETH2_IP + '\n' \

    + 'PC3_ETH0_IP :' + PC3_ETH0_IP + '\n' \
    + 'PC3_ETH1_IP :' + PC3_ETH1_IP + '\n' \
    + 'PC3_ETH2_IP :' + PC3_ETH2_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/IPv6_ISATAP_Tunnel_Interface'

remote_url = 'ipv6.sjtu.edu.cn'
pc3_ipv6_ip = '2004:c03:1a8::201'
x2_ip_15 = '2.2.2.9'
ip = Parameter.FIREWALL
tunnel_ipv6 = '2002::200:5efe:202:206'
tunnel_ipv6_2 = '2002::200:5efe:202:209'
tunnel_ipv6_3 = '3003::200:5efe:202:207'

fw = Firewall(
    Parameter.FIREWALL, 
    user='admin', 
    password='password', 
    supported_config_mode='api')

fwcli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh'


interface_obj = network.InterfaceIPv4Api(fw)
interface_ipv6_obj = network.InterfaceIPv6Api(fw)
settingObj = system.SettingApi(fw)
systemObj = system.DiagnosticApi(fw)
addrObj = network.AddressobjectsApi(fw)
natObj = network.NatpolicyApi(fw)
packetObj = system.PacketmonitorApi(fw)
licensecli = LicenseCli(fwcli)

local_host = Host('localhost')
pc2_ssh = Host(PC2_ETH2_IP, user='root', password='password')
pc3_ssh = Host(PC3_ETH2_IP, user='root', password='password')





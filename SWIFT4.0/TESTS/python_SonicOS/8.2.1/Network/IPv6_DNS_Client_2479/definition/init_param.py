import os
import re
import sys


import unittest
import paramunittest
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from time import sleep

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DNS_Client_2479')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DNS_Client_2479/testcases')

from lib.modules.API import network
from lib.modules.API import system

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '172.17.1.168'
    X2_IP = '172.18.1.168'
    X1_IPv6 = '2001::12'
    X2_IPv6 = '2002::12'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
   
    PC1_ETH0 = '192.168.2.3'
    PC1_ETH1 = '192.168.168.65'
    PC1_ETH2 = '172.17.1.169'
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DNS_Client_2479/testplan/IPv6_DNS_Client_2479.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')

logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/IPv6_DNS_Client_2479'
conf_path = os.environ['PYTHON_SONICOS_HOME']  + '/Network/IPv6_DNS_Client_2479/confs'

dnsmasq_conf = '/etc/dnsmasq.conf'
dibbler_conf = '/etc/dibbler/server.conf'

WAN_host = '2001::11'
WAN_host_if = 'eth2'
bogus_dns1 = '1::10'
bogus_dns2 = '1::11'
bogus_dns3 = '1::12'
invalid_dns6 = 'ff02::1'
domain_url = "www.test6.com"
resolveIP = "2001:0:0:0:0:0:0:10"
jira_dns6 = 'fd56:3812:9157:7f22::10'

ip = Parameter.FIREWALL

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

interface_obj = network.InterfaceIPv4Api(fw)
interface_ipv6_obj = network.InterfaceIPv6Api(fw)
systemObj = system.DiagnosticApi(fw)
failoverlbObj = network.FailoverLbApi(fw)
dnsObj = network.DnsSettingsApi(fw)

local_host = Host('localhost')





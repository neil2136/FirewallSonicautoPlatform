import os
import re
import sys
import copy

import unittest
import paramunittest
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from nose_parameterized import parameterized
from time import sleep


sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_Port_Scanning_TP766')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_Port_Scanning_TP766/testcases')

from lib.modules.API import network, firewallsettings, log
from lib.modules.CLI.system import LicenseCli

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '13.0.0.13'
    X1_GW = '13.0.0.1'
    X0_IPv6 = '1001:1::168'
    X1_IPv6 = '2001:1::168'
    X1_IPv6_GW = '2001:1::1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'

    PC1_ETH0 = '192.168.168.169'
    PC1_ETH1 = '13.0.0.12'
    PC1_ETH2 = '192.168.2.3'
    PC1_ETH3 = '172.16.16.100'
    PC1_ETH0_IPv6 = '1001:1::169'
    PC1_ETH1_IPv6 = '2001:1::12'

    PC2_ETH0 = '13.0.0.15'
    PC2_ETH1 = '192.168.4.2'
    PC2_ETH2 = '172.16.16.200'
    PC2_ETH0_IPv6 = '2001:1::15'

    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_Port_Scanning_TP766/testplan/IPv6_Port_Scanning_TP766.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')

PC1_ETH0_IPv6 = os_obj.get_node_interface_ipv6('PC1','eth0')
PC1_ETH1_IPv6 = os_obj.get_node_interface_ipv6('PC1','eth1')


PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')

PC2_ETH0_IPv6 = os_obj.get_node_interface_ipv6('PC2','eth0')

WAN_IPV6 = Parameter.X1_IPv6

logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC1_ETH3_IP :' + PC1_ETH3_IP + '\n' \
    
    + 'PC1_ETH0_IPv6 :' + PC1_ETH0_IPv6 + '\n' \
    + 'PC1_ETH1_IPv6 :' + PC1_ETH1_IPv6 + '\n' \


    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
    + 'PC2_ETH2_IP :' + PC2_ETH2_IP + '\n' \
    
    + 'PC2_ETH0_IPv6 :' + PC2_ETH0_IPv6 + '\n' \

    + '-' * 30
)

TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/IPv6_Port_Scanning_TP766'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

interface_obj = network.InterfaceIPv4Api(fw)
interface_ipv6_Obj = network.InterfaceIPv6Api(fw)
systemlogObj = log.LogMonitorApi(fw)
logCategoryObj = log.LogCategoryApi(fw)
advanceObj = firewallsettings.AdvanceApi(fw)
logSettingObj = log.LogSettingsApi(fw)

#pc
local_host = Host('localhost')
pc2_ssh = Host(PC2_ETH2_IP, user='root', password='password')




import os
import re
import sys
import copy
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




sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/DHCP_Multi_Scope_2372')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/DHCP_Multi_Scope_2372/testcases')

from lib.modules.API import network, system
from lib.modules.CLI.network import DhcpServerCli


class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X2_IP = '2.2.2.1'
    MASK = '255.255.255.0'   

    PC1_ETH0 = '192.168.168.65'
    PC1_ETH1 = '192.168.2.2'
 
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/DHCP_Multi_Scope_2372/testplan/DHCP_Multi_Scope_2372.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')

logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/DHCP_Multi_Scope_2372'


ip = Parameter.FIREWALL

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interfaceObj = network.InterfaceIPv4Api(fw)
dhcpObj = network.DHCPServerApi(fw)
dhcpCli = DhcpServerCli(fw_cli)
diagObj = system.DiagnosticApi(fw)

local_host = Host('localhost')





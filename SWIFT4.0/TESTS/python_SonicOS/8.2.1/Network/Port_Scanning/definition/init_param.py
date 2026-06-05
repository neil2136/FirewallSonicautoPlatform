import os
import re
import sys
import copy
import time

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
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Port_Scanning')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Port_Scanning/testcases')

from lib.modules.API import network
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import firewallsettings
from lib.modules.API import log
class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '13.0.0.13'
    X1_GW = '13.0.0.1'
    X2_IP = '172.16.0.11'
    X2_GW = '172.16.0.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'

    PC1_ETH0 = '192.168.168.169'
    PC1_ETH1 = '13.0.0.12'
    PC1_ETH2 = '192.168.2.3'
    PC1_ETH3 = '192.168.3.3'
    PC1_ETH4 = '172.16.0.12'


    PC3_ETH0 = '13.0.0.15'
    PC3_ETH1 = '192.168.4.2'
    PC3_ETH2 = '192.168.5.2'
    PC3_ETH3 = '172.16.0.15'
    
 
    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/Port_Scanning/testplan/Port_Scanning.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')
PC1_ETH4_IP = os_obj.get_node_interface_ip('PC1','eth4')

PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3','eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3','eth2')
PC3_ETH3_IP = os_obj.get_node_interface_ip('PC3','eth3')
PC3_DMZ_IP = Parameter.PC3_ETH3
PC3_WAN_IP = Parameter.PC3_ETH0
WAN_IP = Parameter.X1_IP
PC1_LAN_IP = PC1_ETH0_IP

logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC1_ETH3_IP :' + PC1_ETH3_IP + '\n' \
    + 'PC1_ETH4_IP :' + PC1_ETH4_IP + '\n' \

    + 'PC3_ETH0_IP :' + PC3_ETH0_IP + '\n' \
    + 'PC3_ETH1_IP :' + PC3_ETH1_IP + '\n' \
    + 'PC3_ETH2_IP :' + PC3_ETH2_IP + '\n' \
    + 'PC3_ETH3_IP :' + PC3_ETH3_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/Port_Scanning'


binPath = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Port_Scanning/bin'
toolPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissh/tools'



ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')


interface_obj = network.InterfaceIPv4Api(fw)
licenseObj = LicenseCli(fw_cli)
addrObj = network.AddressobjectsApi(fw)
systemlogObj = log.LogMonitorApi(fw)
natObj = network.NatpolicyApi(fw)
logCategoryObj = log.LogCategoryApi(fw)
advanceObj = firewallsettings.AdvanceApi(fw)
logSettingObj = log.LogSettingsApi(fw)

#pc
local_host = Host('localhost')
pc3_ssh = Host(PC3_DMZ_IP, user='root', password='password')




import os
import sys
import re
import time

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.CLI.system import LicenseCli
#from lib.modules.API import system
#from lib.modules.API import securityservices
#from lib.modules.CLI.system import LicenseCli
#from lib.modules.API import firewall
#from lib.modules.API import dpissl 

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/MAC-IP_Anti_Spoof_2429/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/MAC-IP_Anti_Spoof_2429')

os_obj = Openstack(Params.testbed)
ROUTER_MGMT_IP = os_obj.get_node_interface_ip('ROUTER_PC','eth3')
PC2_MGMT_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC3_MGMT_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC4_MGMT_IP = os_obj.get_node_interface_ip('PC4','eth0')

logger.info("\n" + "-" * 30 + "\n" \
    + "ROUTER_MGMT_IP :" + ROUTER_MGMT_IP + "\n" \
    + "PC2_MGMT_IP :" + PC2_MGMT_IP + "\n" \
    + "PC3_MGMT_IP :" + PC3_MGMT_IP + "\n" \
    + "PC4_MGMT_IP :" + PC4_MGMT_IP + "\n" \
    + "-" * 30
)

PC2_login = Host(PC2_MGMT_IP, user='root', password='password')
PC3_login = Host(PC3_MGMT_IP, user='root', password='password')
PC4_login = Host(PC4_MGMT_IP, user='root', password='password')

FIREWALL = '192.168.168.168'
X1_IP    = '111.111.111.168'
X2_IP    = '12.12.2.168'
X3_IP    = '12.12.3.168'
MASK     = '255.255.255.0'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/MAC-IP_Anti_Spoof_2429/testplan/MAC-IP_Anti_Spoof_2429.json'

ip = FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
#lc = LicenseCli(fw_cli)
interface_obj = network.InterfaceIPv4Api(fw_api)
mac_obj = network.MacIPAntiSpoofApi(fw_api)
arp_obj = network.ArpApi(fw_api)
dhcp_obj = network.DHCPServerApi(fw_api)
zone_obj = network.ZoneObjectsApi(fw_api)
lc_obj = LicenseCli(fw_cli)

class Parameter():
    PC2_ETH0_MAC = ''
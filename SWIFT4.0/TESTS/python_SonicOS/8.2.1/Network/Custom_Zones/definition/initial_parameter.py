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

from runner.unittest.setup import Test, skip_if_dts
from runner.utils.assertion import Assertion
    
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import policy
from lib.modules.API import network
from lib.modules.ui.fw_page import FWPage

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Custom_Zones/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Custom_Zones')

os_obj = Openstack(Params.testbed)
PC2_ETH0_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth2')
PC2_ETH3_IP = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth3')
PC2_GW      = os_obj.get_node_interface_ip('DUT-X1-GW-PC','eth2')
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')
 
logger.info("\n" + "-" * 30 + "\n" \
    + "PC2_ETH0_IP :" + PC2_ETH0_IP + "\n" \
    + "PC2_ETH1_IP :" + PC2_ETH1_IP + "\n" \
    + "PC2_ETH2_IP :" + PC2_ETH2_IP + "\n" \
    + "PC2_ETH3_IP :" + PC2_ETH3_IP + "\n" \
    + "PC2_GW :" + PC2_GW + "\n" \
    + "PC1_ETH0_IP :" + PC1_ETH0_IP + "\n" \
    + "PC1_ETH1_IP :" + PC1_ETH1_IP + "\n" \
    + "-" * 30
)

PC2_login = Host(PC2_ETH3_IP, user='root', password='password')


class Parameter():
    FIREWALL = '192.168.168.168'
    X1_IP = '172.17.1.168'
    X1_GW = '172.17.1.1'
    X1_DNS = Params.G_DNS1
    X2_IP = '14.1.1.168'
    MASK = '255.255.255.0'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Custom_Zones/testplan/Custom_Zones.json'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
fw_cgi = Firewall(ip, user='admin', password='password', supported_config_mode='cgi')
security_policy_obj = policy.SecurityPolicyApi(fw)
interface_obj = network.InterfaceIPv4Api(fw)
zone_obj = network.ZoneObjectsApi(fw)
ui_obj = FWPage()

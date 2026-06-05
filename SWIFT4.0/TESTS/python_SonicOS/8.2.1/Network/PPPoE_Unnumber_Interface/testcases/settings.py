import sys
import re
import os
import time
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/PPPoE_Unnumber_Interface')
from runner.unittest.setup import Test, repeat_method
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import vpn
from lib.modules.CLI.system import LicenseCli
from utm import Firewall
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from tools import trafficGen


class Parameter():
    DUT_X0_IP = "192.168.168.168"    
    DUT_X2_IP = "2.2.2.168"    
    DUT_X2_IP_NEW = "2.2.2.170"    
    DUT_X3_IP = "3.3.3.168"    
    PPPOE_ETH = "eth1"    
    PPPOE_ASSIGH = "2.2.2.168"    
    PPPOE_ASSIGH_NEW = "22.22.22.168"    
    PPPOE_ASSIGH_NEW_NETWORK = "22.22.22."    
    PC2_SERVER = Params.testbed + "-PC2"    
    PC2_ETH1 = "13.0.12.169"    
    PC1_ETH1 = "2.2.2.169"    
    PC1_ETH2 = "3.3.3.169"    
    X3_DHCP_START = "3.3.3.100"    
    X3_DHCP_END  = "3.3.3.120"    
    MASK = "255.255.255.0"    
    X3_IF = "eth2" 
    PPP_FILE    = os.environ['PYTHON_SONICOS_HOME'] + "/Network/PPPoE_Unnumber_Interface/confs/pppoe/pap-secrets"
    PPPOE_OPTION= os.environ['PYTHON_SONICOS_HOME'] + "/Network/PPPoE_Unnumber_Interface/confs/pppoe/pppoe-server-options"
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/PPPoE_Unnumber_Interface/testplan/PPPoE_unnumbered_interface.json"



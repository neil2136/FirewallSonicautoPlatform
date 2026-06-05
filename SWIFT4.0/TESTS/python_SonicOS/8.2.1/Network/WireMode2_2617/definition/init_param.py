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
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/WireMode2_2617')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/WireMode2_2617/testcases')

from lib.modules.API import policy
from lib.modules.API import network
from lib.modules.API import dpissl
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.API import log
from lib.modules.API import securityservices
class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '172.16.1.168'
    X1_GW = '172.16.1.1'
    X2_IP = '172.16.3.203'
    X2_GW = '172.16.3.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'

    PC1_ETH0 = '192.168.168.169'
    PC1_ETH1 = '172.16.2.110'
    PC1_ETH2 = '172.16.5.101'

    PC2_ETH0 = '172.16.1.102'
    PC2_ETH1 = '172.16.2.120'
    PC2_ETH2 = '172.16.6.102'

    PC3_ETH0 = '172.16.3.103'
    PC3_ETH1 = '172.16.2.130'
    PC3_ETH2 = '172.16.7.103'
    
    PC4_ETH0 = '172.16.4.104'
    PC4_ETH1 = '172.16.2.140'
    PC4_ETH2 = '172.168.8.104'
 
    WEB_SERVER = '10.6.0.69'
    TMP_PATH = '/tmp/viruses'
    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/WireMode2_2617/testplan/WireMode2_2617.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3','eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3','eth2')
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4','eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4','eth1')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4','eth2')
logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
    + 'PC2_ETH2_IP :' + PC2_ETH2_IP + '\n' \
    + 'PC3_ETH0_IP :' + PC3_ETH0_IP + '\n' \
    + 'PC3_ETH1_IP :' + PC3_ETH1_IP + '\n' \
    + 'PC3_ETH2_IP :' + PC3_ETH2_IP + '\n' \
    + 'PC4_ETH0_IP :' + PC4_ETH0_IP + '\n' \
    + 'PC4_ETH1_IP :' + PC4_ETH1_IP + '\n' \
    + 'PC4_ETH2_IP :' + PC4_ETH2_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/WireMode2_2617'

configPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/config'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
toolPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/tools'
libPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/lib'
binPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/bin'
resPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissh/res'

TMP_PATH = '/tmp/viruses'
WWW_PATH = TMP_PATH

virus = '/tmp/viruses/packed_upx.exe'
ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interface_obj = network.InterfaceIPv4Api(fw)
zoneObj = network.ZoneObjectsApi(fw)
licenseObj = LicenseCli(fw_cli)
matchObj = firewall.MatchobjectApi(fw)
appObj = policy.AppRulesApi(fw)
settingObj = system.SettingApi(fw)
gavObj = securityservices.GAV(fw)
systemlogObj = log.LogMonitorApi(fw)
accessRulesObj = firewall.AccessRuleApi(fw)
addrObj = network.AddressobjectsApi(fw)


local_host = Host('localhost')
pc2_ssh = Host(PC2_ETH1_IP, user='root', password='password')
pc3_ssh = Host(PC3_ETH1_IP, user='root', password='password')
pc4_ssh = Host(PC4_ETH1_IP, user='root', password='password')



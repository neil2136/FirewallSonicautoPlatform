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




sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Interface_ARS')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Interface_ARS/testcases')

from lib.modules.API import policy
from lib.modules.API import network
from lib.modules.API import dpissl
from lib.modules.ui.fw_page import FWPage
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.API import log
from lib.modules.API import securityservices
from lib.modules.API import vpn

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '1.1.0.254'
    X1_GW = '1.1.0.1'
    X2_IP = '13.1.0.254'
    X2_GW = '13.1.0.1'
    X3_IP = '13.2.0.254'
    X3_GW = '13.2.0.1'
    X4_IP = '13.3.0.254'
    X4_GW = '13.3.0.1'
    X5_IP = '13.4.0.254'

    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
   

    PC1_ETH0 = '192.168.168.200'
    PC1_ETH1 = '192.168.3.254'
    PC1_ETH2 = '192.168.2.40'
    PC1_ETH3 = '192.168.4.2'
    PC1_ETH4 = '192.168.100.10'
    
    PC2_ETH0 = '192.168.2.50'
    PC2_ETH1 = '172.16.1.100'
    PC2_ETH2 = '192.168.5.2'
    PC2_ETH3 = '192.168.100.20'

    PC3_ETH0 = '172.16.1.5'
    PC3_ETH1 = '13.3.0.5'
    PC3_ETH2 = '13.4.0.5'
    PC3_ETH3 = '192.168.6.2'
    PC3_ETH4 = '192.168.100.30'

    PC4_ETH0 = '192.168.3.4'
    PC4_ETH1 = '13.1.0.4'
    PC4_ETH2 = '13.2.0.4'
    PC4_ETH3 = '192.168.7.2'
    PC4_ETH4 = '192.168.100.40'
   
 
    WEB_SERVER = '10.6.0.69'
    TMP_PATH = '/tmp/viruses'
    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/Interface_ARS/testplan/Interface_ARS.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')
PC1_ETH4_IP = os_obj.get_node_interface_ip('PC1','eth4')

PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')
PC2_ETH3_IP = os_obj.get_node_interface_ip('PC2','eth3')

PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3','eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3','eth2')
PC3_ETH3_IP = os_obj.get_node_interface_ip('PC3','eth3')
PC3_ETH4_IP = os_obj.get_node_interface_ip('PC3','eth4')

PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4','eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4','eth1')
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4','eth2')
PC4_ETH3_IP = os_obj.get_node_interface_ip('PC4','eth3')
PC4_ETH4_IP = os_obj.get_node_interface_ip('PC4','eth4')

logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC1_ETH3_IP :' + PC1_ETH3_IP + '\n' \
    + 'PC1_ETH4_IP :' + PC1_ETH4_IP + '\n' \
   
    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
    + 'PC2_ETH2_IP :' + PC2_ETH2_IP + '\n' \
    + 'PC2_ETH3_IP :' + PC2_ETH3_IP + '\n' \

    + 'PC3_ETH0_IP :' + PC3_ETH0_IP + '\n' \
    + 'PC3_ETH1_IP :' + PC3_ETH1_IP + '\n' \
    + 'PC3_ETH2_IP :' + PC3_ETH2_IP + '\n' \
    + 'PC3_ETH3_IP :' + PC3_ETH3_IP + '\n' \
    + 'PC3_ETH4_IP :' + PC3_ETH4_IP + '\n' \

    + 'PC4_ETH0_IP :' + PC4_ETH0_IP + '\n' \
    + 'PC4_ETH1_IP :' + PC4_ETH1_IP + '\n' \
    + 'PC4_ETH2_IP :' + PC4_ETH2_IP + '\n' \
    + 'PC4_ETH3_IP :' + PC4_ETH3_IP + '\n' \
    + 'PC4_ETH4_IP :' + PC4_ETH4_IP + '\n' \
  
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/Interface_ARS'

configPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/config'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
toolPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/tools'
libPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/lib'
binPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/bin'

Server_PC_IP = PC2_ETH1_IP
Client_PC_IP = PC1_ETH1_IP

TMP_PATH = '/tmp/viruses'
WWW_PATH = TMP_PATH

ip = Parameter.FIREWALL

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')


security_policy_obj = policy.SecurityPolicyApi(fw)
interface_obj = network.InterfaceIPv4Api(fw)

zone_obj = network.ZoneObjectsApi(fw)
ui_obj = FWPage()
client_ssl = dpissl.ClientSslApi(fw)
licenseObj = LicenseCli(fw_cli)
access_rules_obj = firewall.AccessRuleApi(fw)
addrObj = network.AddressobjectsApi(fw)
certObj = system.CertificateApi(fw)
syslogObj = log.SyslogSettingsApi(fw)
spyObj = securityservices.AntiSpywareApi(fw)
gavObj = securityservices.GAV(fw)
systemlogObj = log.LogMonitorApi(fw)
matchObj = firewall.MatchobjectApi(fw)
appObj = policy.AppRulesApi(fw)
ipsObj = securityservices.IPSApi(fw)
natObj = network.NatpolicyApi(fw)
settingObj = system.SettingApi(fw)
captureObj = system.PacketmonitorApi(fw)
systemObj = system.DiagnosticApi(fw)
routeObj = network.RoutePolicyApi(fw)
vpnObj = vpn.VpnbasesettingApi(fw)


local_host = Host('localhost')
pc2_ssh = Host(PC2_ETH0_IP, user='root', password='password')
pc3_ssh = Host(PC3_ETH4_IP, user='root', password='password')
pc4_ssh = Host(PC4_ETH0_IP, user='root', password='password')




import os
import re
import sys
import copy
from time import sleep
import requests


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
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Log/Logging_IPv6_TP2480')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Log/Logging_IPv6_TP2480/testcases')

from lib.modules.API import policy
from lib.modules.API import network
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.API import log
from lib.modules.API import vpn

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '11.11.1.168'
    X1_GW = '11.11.1.1'
    X2_IP = '12.12.1.168'
    X2_GW = '12.12.1.101'

    X0_IPv6 = '2000::168'
    X1_IPv6 = '2001::168'
    X2_IPv6 = '2002::168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'

    REMOTE_X0 = '172.16.1.201'
    REMOTE_X1 = '12.12.1.201'

    REMOTE_X1_v6 = '2002::201'
    PC1_ETH0 = '192.168.2.3'
    PC1_ETH1 = '192.168.168.100'
    PC1_ETH2 = '172.16.16.100'
    PC1_ETH3 = '172.17.17.100'
    PC1_ETH1_v6 = '2000::4'

    PC2_ETH0 = '172.16.16.102'
    PC2_ETH1 = '11.11.1.102'
    PC2_ETH1_v6 = '2001::4'
    
    PC3_ETH0 = '172.16.1.103'
    PC3_ETH1 = '172.17.17.103'
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Log/Logging_IPv6_TP2480/testplan/Logging_IPv6_TP2480.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')

PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')

PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3','eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3','eth1')
logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC1_ETH3_IP :' + PC1_ETH3_IP + '\n' \

    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
    
    + 'PC3_ETH0_IP :' + PC3_ETH0_IP + '\n' \
    + 'PC3_ETH1_IP :' + PC3_ETH1_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Log/Logging_IPv6_TP2480'

configPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/config'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
toolPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/tools'
libPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/lib'
binPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/bin'

IPv6_test = '2001::22'
VALID_NTP_SERVER="s2m.time.edu.cn"
INVALID_NTP_SERVER="192.168.168.168"
IP_6to4 = '2003::168'

ip = Parameter.FIREWALL
ipv6 = Parameter.X0_IPv6
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

fw_ipv6 = Firewall('['+ipv6+']', user='admin', password='password', supported_config_mode='api')

rt = Firewall(Parameter.REMOTE_X1, user='admin', password='password', supported_config_mode='api')

interfaceObj = network.InterfaceIPv4Api(fw)
interface_ipv6_obj = network.InterfaceIPv6Api(fw)
remote_interface_ipv6_obj = network.InterfaceIPv6Api(rt)

licenseObj = LicenseCli(fw_cli)
accessRulesIpv6Obj = firewall.AccessRuleIPv6Api(fw)
systemlogObj = log.LogMonitorApi(fw)
logSettingObj = log.LogSettingsApi(fw)
addressObj = network.AddressobjectsApi(fw)
natObj = policy.NatPolicyApi(fw)
networkMonitorObj = network.NetworkMonitorApi(fw)
timeObj = system.TimeApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
LAdv_obj = vpn.VpnAdvancedsettingApi(fw)
RAdv_obj = vpn.VpnAdvancedsettingApi(rt)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)


local_host = Host('localhost')
pc2_ssh = Host(PC2_ETH0_IP, user='root', password='password')
pc3_ssh = Host(PC3_ETH1_IP, user='root', password='password')





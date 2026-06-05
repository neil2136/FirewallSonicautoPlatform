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
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Interface_ARS_1')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Interface_ARS_1/testcases')

from lib.modules.API import network
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import log
from lib.modules.CLI.system import AdminCli
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.CLI.vpn import VpnBaseSettingsCli
class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '12.12.1.100'
    X1_GW = "12.12.1.201",
    X1_GW1 = '12.12.1.1'
    X2_IP = '12.12.2.100'
    X2_GW = '12.12.2.100'
    X3_IP = '30.3.3.4'
    X3_GW = '30.3.3.1'
    X4_IP = '40.4.4.4'
    X4_GW = '40.4.4.1'

    X0_IP_REMOTE = '172.16.1.101'
    X0_GW_REMOTE = '172.16.1.1'
    X1_IP_REMOTE = '12.12.1.201'
    X1_GW_REMOTE = '12.12.1.1'
    X2_IP_REMOTE = '12.12.2.201'
    X2_GW_REMOTE = '12.12.2.1'
    X3_IP_REMOTE = '30.3.3.5'
    X3_GW_REMOTE = '30.3.3.1'
    X4_IP_REMOTE = '40.4.4.5'
    X4_GW_REMOTE = '40.4.4.1'
   

    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
   

    PC1_ETH0 = '192.168.168.169'
    PC1_ETH1 = '192.168.2.3'
  
    
    PC2_ETH0 = '172.16.1.10'
    PC2_ETH1 = '192.168.2.4'


    WEB_SERVER = '10.6.0.69'
    TMP_PATH = '/tmp/viruses'
    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/Interface_ARS_1/testplan/Interface_ARS_1.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')


PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')


logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
   
    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
  
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/Interface_ARS_1'

configPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/config'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
toolPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/tools'
libPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/lib'
binPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/bin'

Server_PC_IP = PC2_ETH0_IP
Client_PC_IP = PC1_ETH0_IP
Server_sub = '172.16.1.0'
Client_sub = '192.168.168.0'

TMP_PATH = '/tmp/viruses'
WWW_PATH = TMP_PATH

ip = Parameter.FIREWALL
RM_X1_IP = Parameter.X1_IP_REMOTE
RM_X2_IP = Parameter.X2_IP_REMOTE

if Params.openstack :
        os_stack = Openstack(Params.testbed)
        os_host = os_stack.get_oshost()
        MY_SPEC_FILE = 'http://' + os_host + '/topology_details/' + Params.testbed + '.xml'
        vlan_id_X3 = os_stack.get_node_interface_vlan_id('UTM','X3:1')
        vlan_id_X4 = os_stack.get_node_interface_vlan_id('UTM','X4:1')
       
      



fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

rm_api = Firewall(RM_X1_IP, user='admin', password='password', supported_config_mode='api')
rm_cli = Firewall(RM_X1_IP, user='admin', password='password', supported_config_mode='cli-ssh')

interface_obj = network.InterfaceIPv4Api(fw)
interface_obj_remote = network.InterfaceIPv4Api(rm_api)

licenseObj = LicenseCli(fw_cli)
addrObj = network.AddressobjectsApi(fw)
addrObj_remote = network.AddressobjectsApi(rm_api)

logObj = log.LogCategoryApi(fw)

systemlogObj = log.LogMonitorApi(fw)
routeObj = network.RoutePolicyApi(fw)
routeObj_remote = network.RoutePolicyApi(rm_api)

Lvpn_obj = VpnbasesettingApi(fw)
Rvpn_obj = VpnBaseSettingsCli(rm_cli)
Radmin_obj = AdminCli(rm_cli)

local_host = Host('localhost')
pc2_ssh = Host(PC2_ETH1_IP, user='root', password='password')





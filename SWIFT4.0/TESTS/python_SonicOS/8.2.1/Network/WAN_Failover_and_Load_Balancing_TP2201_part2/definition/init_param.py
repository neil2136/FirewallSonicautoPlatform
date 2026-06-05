import os
import re
import sys
import subprocess


import unittest
import paramunittest
import datetime
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
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/WAN_Failover_and_Load_Balancing_TP2201_part2')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/WAN_Failover_and_Load_Balancing_TP2201_part2/testcases')

from lib.modules.API import policy
from lib.modules.API import network
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import system
from lib.modules.API import log
from lib.modules.API import object
from lib.modules.API import vpn


class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '11.11.11.168'
    X1_GW = '11.11.11.110'
    X1_GW_2 = '11.11.11.1'
    X2_IP = '12.12.2.168'
    X2_GW = '12.12.2.120'
    X3_IP = '13.13.0.110'
    X3_GW = '13.13.0.120'
    X4_IP = '13.14.0.110'
    X4_GW = '13.14.0.120'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    MASK = '255.255.255.0'

    REMOTE_X0 = '172.16.1.101'
    REMOTE_X1 = '12.12.1.201'

    PC1_ETH0 = '192.168.168.169'
    PC1_ETH1 = '192.168.11.100'
    PC1_ETH2 = '192.168.12.100'
    PC1_ETH3 = '192.168.13.100'
    PC1_ETH3 = '192.168.14.100'

    PC2_ETH0 = '172.16.1.200'
    PC2_ETH1 = '192.168.14.200'

    PC_GW1_ETH0 = '172.168.0.110'
    PC_GW1_ETH1 = '192.168.11.110'
    PC_GW1_ETH2 = '13.13.1.110'

    PC_GW2_ETH0 = '172.168.0.120'
    PC_GW2_ETH1 = '192.168.12.120'
    PC_GW2_ETH2 = '13.13.2.120'

    GW_X0 = '11.11.11.101'
    GW_X1 = '12.12.1.101'
    GW_X2 = '12.12.2.101'
    
    PC_Server_ETH0 = '172.168.0.200'
    PC_Server_ETH1 = '192.168.13.200'
    
 
    WEB_SERVER = '10.6.0.69'
    TMP_PATH = '/tmp/viruses'
    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/WAN_Failover_and_Load_Balancing_TP2201_part2/testplan/WAN_Failover_and_Load_Balancing_TP2201.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')
PC1_ETH4_IP = os_obj.get_node_interface_ip('PC1','eth4')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC_GW1_ETH0_IP = os_obj.get_node_interface_ip('PC_GW1','eth0')
PC_GW1_ETH1_IP = os_obj.get_node_interface_ip('PC_GW1','eth1')
PC_GW1_ETH2_IP = os_obj.get_node_interface_ip('PC_GW1','eth2')
PC_GW2_ETH0_IP = os_obj.get_node_interface_ip('PC_GW2','eth0')
PC_GW2_ETH1_IP = os_obj.get_node_interface_ip('PC_GW2','eth1')
PC_GW2_ETH2_IP = os_obj.get_node_interface_ip('PC_GW2','eth2')
PC_Server_ETH0_IP = os_obj.get_node_interface_ip('PC_Server','eth0')
PC_Server_ETH1_IP = os_obj.get_node_interface_ip('PC_Server','eth1')
logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC1_ETH3_IP :' + PC1_ETH3_IP + '\n' \
    + 'PC1_ETH4_IP :' + PC1_ETH4_IP + '\n' \
    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
    + 'PC_GW1_ETH0_IP :' +PC_GW1_ETH0_IP + '\n' \
    + 'PC_GW1_ETH1_IP :' +PC_GW1_ETH1_IP + '\n' \
    + 'PC_GW1_ETH2_IP :' +PC_GW1_ETH2_IP + '\n' \
    + 'PC_GW2_ETH0_IP :' + PC_GW2_ETH0_IP + '\n' \
    + 'PC_GW2_ETH1_IP :' + PC_GW2_ETH1_IP + '\n' \
    + 'PC_GW2_ETH2_IP :' + PC_GW2_ETH2_IP + '\n' \
    + 'PC_Server_ETH0_IP :' + PC_Server_ETH0_IP + '\n' \
    + 'PC_Server_ETH1_IP :' + PC_Server_ETH1_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/WAN_Failover_and_Load_Balancing_TP2201_part2'



configPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/config'
toolPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/tools'


dns1 = Parameter.X1_DNS1 
dns2 = Parameter.X1_DNS2
dns3 = Parameter.X1_DNS3

default_target_ip = '204.212.170.23'
http_server = Parameter.PC_Server_ETH0

rm_x0 = '172.16.1.101'
rm_x0_net = '172.16.1.0'
rm_x1_net = '12.12.1.0'
rm_x2_net = '12.12.2.0'
dut_x0_net = '192.168.168.0'
vpngw_x0_net = '11.11.11.0'
vpngw_x1_net = '12.12.1.0'
vpngw_x2_net = '12.12.2.0'

dut_x1_default = '11.11.11.200'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
rt = Firewall(Parameter.REMOTE_X1, user='admin', password='password', supported_config_mode='api')

interfaceObj = network.InterfaceIPv4Api(fw)
licenseObj = LicenseCli(fw_cli)
settingObj = system.SettingApi(fw)
systemlogObj = log.LogMonitorApi(fw)
dnsObj = network.DnsSettingsApi(fw)
failoverlbObj = network.FailoverLbApi(fw)
systemlogObj = log.LogMonitorApi(fw)
diagObj = system.DiagnosticApi(fw)
packetObj = system.PacketmonitorApi(fw)
routeObj = policy.RoutePolicyApi(fw)
LAddrObj = network.AddressobjectsApi(fw)
RAddrObj = network.AddressobjectsApi(rt)
LvpnObj = vpn.VpnbasesettingApi(fw)
RvpnObj = vpn.VpnbasesettingApi(rt)

local_host = Host('localhost')
pc_gw1_ssh = Host(PC_GW1_ETH1_IP, user='root', password='password')
pc_gw2_ssh = Host(PC_GW2_ETH1_IP, user='root', password='password')
pc_server_ssh = Host(PC_Server_ETH1_IP, user='root', password='password')
pc2_ssh = Host(PC2_ETH1_IP, user='root', password='password')

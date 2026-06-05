import os
import re
import sys
import copy


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
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IP_Helper_V3_TP2169')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IP_Helper_V3_TP2169/testcases')

from lib.modules.API import network,system,log,object
from lib.modules.CLI.system import LicenseCli


class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X1_IP = '13.0.0.168'
    X1_GW = '13.0.0.1'
    X2_IP = '2.2.2.168'
    X2_GW = '2.2.2.1'
    X3_IP = '3.3.3.168'
    X3_GW = '3.3.3.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'

#For debugging
    PC1_ETH0 = '192.168.168.169'
    PC1_ETH1 = '13.0.0.3'
    PC1_ETH2 = '2.2.2.2'
    PC1_ETH3 = '3.3.3.3'
    PC1_ETH4 = '192.0.1.11'
    PC1_ETH5 = '192.168.2.3'

    PC2_ETH0 = '13.0.0.5'
    PC2_ETH1 = '2.2.2.22'
    PC2_ETH2 = '3.3.3.22'
    PC2_ETH3 = '192.168.3.3'
    PC2_ETH4 = '192.0.1.22'

    WEB_SERVER = '10.6.0.69'
    TMP_PATH = '/tmp/viruses'
    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IP_Helper_V3_TP2169/testplan/IP_Helper_V3_TP2169.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')
PC1_ETH4_IP = os_obj.get_node_interface_ip('PC1','eth4')
PC1_ETH5_IP = os_obj.get_node_interface_ip('PC1','eth5')

PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2','eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')
PC2_ETH3_IP = os_obj.get_node_interface_ip('PC2','eth3')
PC2_ETH4_IP = os_obj.get_node_interface_ip('PC2','eth4')


logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC1_ETH3_IP :' + PC1_ETH3_IP + '\n' \
    + 'PC1_ETH4_IP :' + PC1_ETH4_IP + '\n' \
    + 'PC1_ETH5_IP :' + PC1_ETH5_IP + '\n' \
    + 'PC2_ETH0_IP :' + PC2_ETH0_IP + '\n' \
    + 'PC2_ETH1_IP :' + PC2_ETH1_IP + '\n' \
    + 'PC2_ETH2_IP :' + PC2_ETH2_IP + '\n' \
    + 'PC2_ETH3_IP :' + PC2_ETH3_IP + '\n' \
    + 'PC2_ETH4_IP :' + PC2_ETH4_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/IP_Helper_V3_TP2169'

confPath = TESTPATH + '/confs'
definitionPath = TESTPATH + '/confs'

TMP_PATH = '/tmp/viruses'
WWW_PATH = TMP_PATH
PC2_WAN_IP = Parameter.PC2_ETH0
PC1_LAN_IP = Parameter.PC1_ETH0
# remote_server_ip = PC2_ETH4_IP
remote_server_ip = PC2_ETH4_IP

DstPort1 = 53
INTERFACE_LAN = 'eth0'

virus = '/tmp/viruses/packed_upx.exe'
ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')


licenseObj = LicenseCli(fw_cli)
interfaceObj = network.InterfaceIPv4Api(fw)
addressObj = network.AddressobjectsApi(fw)
dhcpObj = network.DHCPServerApi(fw)
iphelper = network.IpHelperApi(fw)
settingObj = system.SettingApi(fw)
diagObj = system.DiagnosticApi(fw)
packetObj = system.PacketmonitorApi(fw)
syslogObj = log.SyslogSettingsApi(fw)
address_groupObj = object.AddressObjectGroupApi(fw)


local_host = Host('localhost')
pc2_ssh = Host(PC2_ETH4_IP, user='root', password='password')




dhcpdcfg = '''
ddns-update-style interim;
ignore client-updates;
subnet 2.2.2.0 netmask 255.255.255.0 {
''' + \
f'''
option routers {Parameter.FIREWALL};
'''+ \
'''
option subnet-mask 255.255.255.0;
option time-offset -18000;
range dynamic-bootp 2.2.2.150 2.2.2.200;
default-lease-time 21600;
max-lease-time 43200;
}
'''
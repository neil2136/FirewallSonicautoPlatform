import os
import sys

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])

from lib.modules.CLI import network
from lib.modules.API.network import InterfaceIPv4Api

from util.enhancedinfo import show_testcase_info
from utm import Firewall
from util.openstack import Openstack

import unittest
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'CLI/CLI3_Nework2/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'CLI/CLI3_Network2')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
    '/CLI/CLI3_Network2/testplan/testplan.json'
  
           
# configure fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.168'
    MASK = '255.255.255.0'
    X1_GW = '172.16.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


# case 1 parameter



# case 12 parameter
vlan_interface_dict = {
    'if': 'x3',
    'type': 'vlan',
    'vlan-tag': 200,
    'zone': 'wan',
    'mode': 'static',
    'ip': '200.1.1.1'
}
edit_vlan_interface_dict = {
    'if': 'x3',
    'type': 'vlan',
    'vlan-tag': 201,
    'zone': 'wan',
    'mode': 'static',
    'ip': '200.1.1.1'
}
arp_entry_dict ={
    'ip': "192.168.168.100",
    'mac' : '00:0C:F1:56:98:AD',
    'interface' : 'x0'
}
edit_arp_entry_dict ={
    'ip': "192.168.168.101",
    'mac' : '00:0C:F1:56:98:AC',
    'interface' : 'x0'
}
# Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
fwcli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')

interfaceapi = InterfaceIPv4Api(fw)
interfacecli = network.InterfaceCli(fwcli)
arpcli= network.ARPCli(fwcli)
zonecli = network.ZonesCli(fwcli)
failoverlbcli = network.FailoverLBCli(fwcli)
dhcpservercli = network.DhcpServerCli(fwcli)
aocli = network.AddressObjectCli(fwcli)
ddnscli = network.DDNSCli(fwcli)
routecli = network.RouteCli(fwcli)
iphelpercli = network.IpHelperCli(fwcli)
networkmonitorcli = network.NetworkMonitorCli(fwcli)
natcli = network.NatpolicyCli(fwcli)

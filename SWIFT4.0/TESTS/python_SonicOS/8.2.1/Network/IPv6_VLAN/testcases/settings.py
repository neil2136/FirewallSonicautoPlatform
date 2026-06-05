import os
import sys
import re
import time
import paramunittest
from util.openstack import Openstack
from runner.settings import Params
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_VLAN')
from runner.unittest.setup import Test, repeat_method
from lib.modules.API import network
from lib.modules.API import policy
# from lib.modules.API import switching
from lib.modules.API import system
from utm import Firewall
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from tools.trafficGen import ping6
from lib.modules.CLI import system
from lib.modules.API import vpn


class Parameter():
    DNS1 = Params.G_DNS1
    LAN_INTERFACE='eth0'
    WAN_INTERFACE='eth1'
    DMZ_INTERFACE='eth2'
    MY_LAN_PC_IP='192.168.168.169'
    MY_DMZ_PC_IP='2.2.2.169'
    MY_WAN_PC_IP='11.11.11.169'
    X0_IP='192.168.168.168'
    X1_IP='11.11.11.168'
    X1_IPv6 = '2001::168'
    MY_WAN_PC_IPv6='2001::169'
    X1_GW='11.11.11.1'
    X2_IP='2.2.2.168'
    PREFIX = '64'
    ZONES=['Public','Trusted']
    DESTINATION = '10.9.1.40'
    DNS_SERVER = MY_WAN_PC_IP
    VPN_DEF = os.environ['SONICOS_HOME'] + '/VPN/definition/OS_VPN_REMOTE.exp.exp'
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_VLAN/testplan/ipv6_vlan.json'
    DUT_IP= {
        'ipv4': {
            'X0': '192.168.168.168',
            'X1': '12.12.1.168',
            'X2': '12.12.2.168',
        },
        'ipv6': {
            'X0': '2010::168',
            'X1': '2022::168',
            'X2': '2012::168',
        },
        'prefix': {
            'X0': '2010::',
            'X1': '2022::',
            'X2': '2012::',
        },
    }
    REMOTE_IP= {
        'ipv4': {
            'X0': '176.16.1.201',
            'X1': '12.12.1.201',
            'X2': '12.12.2.201',
        },
        'ipv6': {
            'X0': '2010::201',
            'X1': '2022::201',
            'X2': '2012::201',
        },
        'prefix': {
            'X0': '2010::',
            'X1': '2022::',
            'X2': '2012::',
        },
    }
    PC1 = {
        'interface': {
            'dut-x0': 'eth0',
            'dut-x2': 'eth1',
        },
        'ipv4': {
            'eth0': '192.168.168.101',
            'eth1': '12.12.1.101',
        },
        'ipv6': {
            'eth0': '2010::100',
            'eth1': '2012::100',
        },
        'vlan': {

        },        
    }
    PC2 = {
        'interface': {
            'fw-x2': 'eth1',
            'dut-x2': 'eth2',
        },
        'ipv4': {
            'eth1': '173.16.1.101',
        },
        'ipv6': {
            'eth1': '2023::100',
            'eth2': '2012::101',
        },
        'vlan': {

        },        
    }
    PC3 = {
        'interface': {
            'fw-x1': 'eth1',
            'dut-x1': 'eth1',
        },
        'ipv6': {
            'eth1': '2022::100',
        },
        'vlan': {

        },        
    }
    DUT_X0_INTER = PC1['interface']['dut-x0']
    DUT_X1_INTER = PC3['interface']['dut-x1']
    DUT_X2_INTER = PC1['interface']['dut-x2']
    DUT_X2_INTER_PC2 = PC2['interface']['dut-x2']
    FW_X2_INTER = PC2['interface']['fw-x2']
    FW_X1_INTER = PC3['interface']['fw-x1']
    DUT_X2_IPv6_Network = '2012::'
    REMOTE_X2_IPv6_Network = '2023::'
    G_REMOTE = '3600'
    PC2_INTERFACE = 'eth1'
    PC3_INTERFACE = 'eth1'
    PC4_INTERFACE = 'eth1'
    USER = 'automation'
    PASSWD = 'automation'
    DIBBLER_SERVER_CONF = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_VLAN/confs/server.conf'
    DIBBLER_CLIENT_CONF = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_VLAN/confs/client.conf'

    if Params.openstack :
        os_stack = Openstack(Params.testbed)
        os_host = os_stack.get_oshost()
        MY_SPEC_FILE = 'http://' + os_host + '/topology_details/' + Params.testbed + '.xml'
        PC1['vlan']['eth0'] = os_stack.get_node_interface_vlan_id('UTM','X0')
        PC1['vlan']['eth1'] = os_stack.get_node_interface_vlan_id('UTM','X2')
        PC2['vlan']['eth1'] = os_stack.get_node_interface_vlan_id('RemoteGEN6','X2')
        PC2['vlan']['eth2'] = os_stack.get_node_interface_vlan_id('UTM','X2')
        PC3['vlan']['eth1'] = os_stack.get_node_interface_vlan_id('UTM','X1')

ip = Parameter.X0_IP
rem_ip = Parameter.X1_IP
fw = Firewall(ip, user='admin', password='password')
rem_fw = Firewall(rem_ip, user='admin', password='password')
interface = network.InterfaceIPv4Api(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
ao = network.AddressobjectsApi(fw)
rem_interface = network.InterfaceIPv4Api(rem_fw)
rem_interface_v6 = network.InterfaceIPv6Api(rem_fw)
rem_ao = network.AddressobjectsApi(rem_fw)
rem_setting_cli = system.SettingCli(rem_fw)
rem_vpn = vpn.VpnbasesettingApi(rem_fw)
zones= ['LAN', 'DMZ', 'WLAN', 'WAN']
route_obj = policy.RoutePolicyApi(fw)

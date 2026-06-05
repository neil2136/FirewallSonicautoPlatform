from inspect import Parameter
import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/Port_Redundancy_TP2542')

import paramunittest
from nose_parameterized import parameterized
from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall,FirewallAPI
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from modules.API import network,firewall
from tools.trafficGen import  MyFtp

OpenS = Openstack(Params.testbed)
fw = Firewall('192.168.168.168', user='admin', password='sonicauto', supported_config_mode='api')
Linterface = network.InterfaceIPv4Api(fw)
Laccess_rule_obj = firewall.AccessRuleApi(fw)
# define path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Network/Port_Redundancy_TP2542/testplan/Port_Redundancy_TP2542.json'
local_file ='/tmp/ftpDataFile1.txt'
rmt_file = 'ttt.py'
# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC3 = Host(Params.testbed + '-PC3')
pc1_ip = '192.168.168.201'
pc3_ip = '172.17.2.100'
PC1_Network_2= '192.168.2.0'
PC3_Network = '172.17.2.0'
DUT_X0 = '192.168.168.168'
DUT_X1 = '12.12.1.201'
DUT_X2 = '192.168.2.168'
DUT_X3 = '172.17.2.168'
PC1_IF_1 = 'eth1'
PC1_IF_2 = 'eth2'
PC3_IF = 'eth1'
LOCALSUBNET = "X0 Subnet"
REMOTESUBNET = "X0 Subnet"
my_ftp = MyFtp(host=pc3_ip,user='anonymous', password='password')
pc1_route_cmds = [f'ip r a {PC3_Network}/24 via {DUT_X2} dev {PC1_IF_2}',
                  "ip route"]
pc3_route_cmds = [f'ip r a {PC1_Network_2}/24 via {DUT_X3} dev {PC3_IF}',
                  "ip route"]
redundant_port = {
    'redundancy_aggregation_port':'redundancy',
    'redundancy_port':'X4'
}
remove_redundancy = {
    'redundancy_aggregation_port':False
}
link_speed1 = {"link_speed":"1000_full"}
link_speed2 = {"link_speed": {
                    "full": 1000
                }}
Lx0 = {
        'if': 'X0',
        'zone': 'LAN',
        'mode': 'static',
        'ip': DUT_X0,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
}
Lx1 = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X1,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
    }
Lx2 = {
        'if': 'X2',
        'zone': 'LAN',
        'mode': 'static',
        'ip': DUT_X2,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
    }
Lx3 = {
        'if': 'X3',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X3,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
    }
Lx4 = {
        'if': 'X4',
        'zone': 'WAN',
        'mode': 'static',
        'ip': '1.1.1.1',
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
    }
rule_opt = {
            "name": "wan2lan",
            "comment": "",
            "action": "allow",
            "priority": {"auto": True},
            "enable": True,
            "from": "WAN",
            "source": {
                "address": {"any": True},
                "port": {"any": True}},
            "to": "LAN",
            "destination": {
                "address": {"any": True}},
            "service": {"any": True},
            "users": {
                "included": {"all": True},
                "excluded": {"none": True}},
            "tcp": {"timeout": 15,"urgent": True},
            "udp": {"timeout": 30},
            "dpi": True,
            "dpi_ssl": {"client": True,"server": True},
            "quality_of_service": {
                "class_of_service": {},
                "dscp": {"preserve": True}},
            "botnet_filter": False,
            "geo_ip_filter": {"enable": False},
            "logging": True,
            "flow_reporting": False,
            "connection_limit": {"source": {},"destination": {}},
            "sip": False,
            "h323": False,
            "fragments": True,
            "management": False,
            "max_connections": 100,
            "packet_monitoring": False,
            "reflexive": False
}
import sys
import os
import copy
import time
import re

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params,logger
from runner.utils.assertion import Assertion
from lib.modules.API import log
from lib.modules.API import system
from lib.modules.API import firewall
from lib.modules.API import network
from lib.modules.CLI.system import SettingCli
from lib.modules.CLI.system import AdminCli
from utm import Firewall
from utm import FirewallCGI
from networkdevice import Host
from util.openstack import Openstack
from lib.modules.ui.fw_page import FWPage
from lib.modules.CLI.system import LicenseCli

OpenS = Openstack(Params.testbed)

# get all PC nodes and check GW exists or not from openstack
node_list = OpenS.get_nodes_as_dictionary().keys()
if ('VPNGW' in node_list):
    GW = 1
    logger.info('gw exits, need to config it' )
else:
    GW = 0

rm_device = 'RemoteGEN7' if ('RemoteGEN7' in node_list) else "RemoteGEN5"
logger.info(rm_device)

# preference file path
RM_PREF = "/SWIFT4.0/COMMON/data/prefs/OS_REMOTE.exp"
GW_PREF = "/SWIFT4.0/COMMON/data/prefs/OS_GW.exp"
VPN_bin = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/bin'
cfg_path = os.environ["PYTHON_COMMON_HOME"] + '/config/'

# get PC nodes IP
if 'PC2' in node_list:
    PC2_login = Host(Params.testbed + '-PC2')

if 'PC3' in node_list:
    PC3_IP = OpenS.get_node_interface_ip('PC3', 'eth1')
    PC3_login = Host(Params.testbed + '-PC3')
    DNS_Server = OpenS.get_node_interface_ip('PC3', 'eth0')
    DNS_Server_login = Host(Params.testbed + '-PC3')
    
if 'PC4' in node_list:
    PC4_IP = OpenS.get_node_interface_ip('PC4', 'eth1')
    PC4_login = Host(Params.testbed + '-PC4')

if 'PC5' in node_list:
    PC5_IP = OpenS.get_node_interface_ip('PC5', 'eth1')
    PC5_login = Host(Params.testbed + '-PC5')


class Parameter():
    FIREWALL        = '192.168.168.168'
    # Local DUT
    DUT             = "192.168.168.168"
    WANIP           = "11.11.11.200"
    DUTX2           = "12.12.2.200"
    DUTX3           = "192.168.170.168"
    DUTX3NET        = "192.168.170.0"
    LOCALNET        = "192.168.168.0"
    LOCALLANIP      = "X0 IP"
    LOCALSUBNET     = "X0 Subnet"
    DNSSERVER       = DNS_Server if ('PC3' in node_list) else "11.11.11.100"
    DNSREGISTER     = "10.217.131.101"
    DNSPUBLIC       = "10.9.1.40"
    LOCALHOST       = OpenS.get_node_interface_ip('PC1', 'eth0')
    # Remote DUT
    REMOTEX0        = "172.16.1.101"
    REMOTEX1        = "12.12.1.201"
    REMOTEX2        = "12.12.2.201"
    REMOTEX3        = "172.16.3.101"
    REMOTENET       = "172.16.1.0"
    REMOTEX3NET       = "172.16.3.0"
    REMOTESUBNET    = "X0 Subnet"
    REMOTEHOST      = OpenS.get_node_interface_ip('PC2', 'eth0')
    #GW
    WANGW           = "11.11.11.101"
    PRIGWWAN       = "12.12.1.101"
    SECGWWAN       = "12.12.2.101"
    #NAT
    LOCTRANSNET  = "9.9.9.0"
    REMTRANSNET  = "8.8.8.0"
    LOCTRANSHOST = "9.9.9.2"
    REMTRANSHOST = "8.8.8.101"
    LOCATRANSDUT = "9.9.9.168"
    DMZSUBNET    = "6.6.6.0"
    NETMASK      = "255.255.255.0"

if (GW == 0):
    Parameter.WANIP      ="12.12.1.200"
    Parameter.DUTX2      ="12.12.2.200"
    Parameter.WANGW      ="12.12.1.1"
    Parameter.DNSSERVER  ="0.0.0.0"
    Parameter.SECGWWAN   ="12.12.2.1"
    Parameter.REMOTEX1   ="12.12.1.201"
    Parameter.REMOTEX2   ="12.12.2.201"




fw = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='api')
gw = Firewall(Parameter.WANGW, user='admin', password='password', supported_config_mode='cgi')
rt = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='api')
rmt = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')

rule_opt = {
            "name": "any_to_any",
            "comment": "",
            "action": "allow",
            "priority": {"auto": True},
            "enable": True,
            "from": "Any",
            "source": {
                "address": {"any": True},
                "port": {"any": True}},
            "to": "Any",
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

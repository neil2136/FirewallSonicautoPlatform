from inspect import Parameter
import sys
import os
import re
import time
import copy
import socket

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DNS_Loopback_340')

from collections import OrderedDict
import re
import paramunittest
from nose_parameterized import parameterized

from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall,FirewallAPI
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network
from lib.modules.API import firewall

OpenS = Openstack(Params.testbed)
fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
Linterface = network.InterfaceIPv4Api(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
Lzone_obj = network.ZoneObjectsApi(fw)
Laccess_rule_obj = firewall.AccessRuleApi(fw)
natPolicyObj = network.NatpolicyApi(fw)
dnsObj = network.DnsSettingsApi(fw)
# define path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Loopback_340/testplan/DNS_Loopback_340.json'
suite_path = os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Loopback_340'
conf_path = os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Loopback_340/conf'
# PC SSH
PC1 = Host(Params.testbed + '-PC1')
http_server = Host(Params.testbed + '-PC-HTTP')
dns_server = Host(Params.testbed + '-PC-DNS')
# define IP
DUT_X0 = '192.168.168.168'
DUT_X1 = '10.2.1.70'
DUT_GW = '10.1.1.1'
DUT_X2 = '192.100.100.20'
DUT_X3 = '192.200.200.20'
PC1_LAN = '10.1.1.10'
PC1_eth1 = '192.168.168.200'
C2_WAN = '10.1.1.20'
PC2_WAN2 = '10.2.1.20'
PC3_DMZ  = '10.1.1.30'
PC3_eth1 = '192.100.100.100'
PC4_CST = '10.1.1.40'
PC4_eth1 = '192.200.200.200'
PC_DNS  = '10.1.1.50'
PC_DNS2 = '10.2.1.50'
PC_HTTP = '10.1.1.60'
http_domain = 'http://www.http.test.com'
#cmds
install_bind9_cmds = [f"cp {conf_path}/bind-9.10.2.tar.gz ./",
                      "tar -xvzf bind-9.10.2.tar.gz",
                      "cd bind-9.10.2",
                      "./configure sysconfdir=/etc",
                      "make",
                      "make install"]
config_bind9_cmds = ["rndc-confgen > /etc/rndc.conf",
                     "mkdir -p /var/named",
                     f"cp {conf_path}/named.conf /etc/",
                     f"cp {conf_path}/*.zone /var/named/",
                     f"cp {conf_path}/named.* /var/named/",
                     "tail /etc/rndc.conf|sed '/^# End/ d'|sed 's/^#//g'>>/etc/named.conf",
                     "ls  /var/named/"]
start_bind9_cmds = ['named -c /etc/named.conf &',
                    'service dnsmasq restart']
config_http_cmds = ["echo 'HELLO' > /tmp/index.html",
                    f"iptables -I INPUT -j REJECT -d {PC_HTTP} -p tcp --dport 80",
                    "service httpd start",
                    "service httpd status"]

# DUT local Address object and group


http_public_ao = {
    'name': 'HTTP_Public',
    'zone': 'WAN',
    'object_type': 'host',
    'value': '10.1.1.60',
}
http_private1_ao = {
    'name': 'HTTP_Private_LAN',
    'zone': 'LAN',
    'object_type': 'host',
    'value': '192.168.168.250',
}
http_private2_ao = {
    'name': 'HTTP_Private_DMZ',
    'zone': 'DMZ',
    'object_type': 'host',
    'value': '192.100.100.250',
}

http_private3_ao = {
    'name': 'HTTP_Private_CST',
    'zone': 'CST',
    'object_type': 'host',
    'value': '192.200.200.250',
}

#Nat opts
nat_opts = {
            "nat_policies":[
                {
                    "ipv4":{
                        "name": "tc_nat_rule",
                        "enable": True,
                        "dns_doctoring":False,
                        "reflexive":False,
                        "comment": "test",
                        "priority":{"auto":True},
                        "inbound": "X1",
                        "outbound": 'any',
                        "source": {"name":''},
                        "translated_source":  {'name': 'X1 IP'},
                       'destination': {"name":"HTTP_Public"},
                        'translated_destination':{'name': ''},
                        'service': {"name":"HTTP"},
                        'translated_service': {'original': True}, 
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": "",
                        }
                        #"source_port_remap": True  ###this option can be enabled only when "translated source" is not Original
                    }
                }
            ]
        }

#zone set 
zone_ref = {"zones":
[{
    "name":"CST",
    "security_type":"public",
}]}

Lx1 = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X1,
        'netmask': '255.255.255.0',
        'gateway': DUT_GW,
        'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
Lx2 = {
        'if': 'X2',
        'zone': 'DMZ',
        'mode': 'static',
        'ip': DUT_X2,
        'netmask': '255.255.255.0',
        # 'gateway': Parameter.WANGW,
        # 'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
Lx3 = {
        'if': 'X3',
        'zone': 'CST',
        'mode': 'static',
        'ip': DUT_X3,
        'netmask': '255.255.255.0',
        # 'gateway': Parameter.WANGW,
        # 'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
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






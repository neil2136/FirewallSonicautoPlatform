from inspect import Parameter
import sys
import os
import re
import time
import copy
import socket

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/FQDN_based_NAT')

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
from lib.modules.API import object
from lib.modules.API import log
from lib.modules.API import vpn
from lib.modules.API import system
from lib.modules.API.system import SettingApi,RestartApi
from lib.modules.API import firewall
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from tools.trafficGen import  MyFtp
from lib.modules.CLI.system import LicenseCli

OpenS = Openstack(Params.testbed)
fw_cli = Firewall('192.168.168.168', user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='cli-ssh')
# rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
# fw_api = FirewallAPI(Parameter.DUT)
fw = Firewall('192.168.168.168', user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='api')
Linterface = network.InterfaceIPv4Api(fw)
LCACertObj = system.CertificateApi(fw)
LTimeObj = system.TimeApi(fw)
LRestartObj = system.RestartApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Lzone_obj = network.ZoneObjectsApi(fw)
Laccess_rule_obj = firewall.AccessRuleApi(fw)
natPolicyObj = network.NatpolicyApi(fw)
dnsObj = network.DnsSettingsApi(fw)
setting_obj = SettingApi(fw)
restart_obj = RestartApi(fw)
LPackageMonitObj = system.PacketmonitorApi(fw)
license_obj = LicenseCli(fw_cli)
# define path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Network/FQDN_based_NAT/testplan/FQDN_based_NAT.json'
suite_path = os.environ["PYTHON_SONICOS_HOME"]+'/Network/FQDN_based_NAT'
dhcp_file = os.environ["PYTHON_SONICOS_HOME"]+'/Network/FQDN_based_NAT/definition/dhcpd_fqdn.conf'
dhcp_db = os.environ["PYTHON_SONICOS_HOME"]+'/Network/FQDN_based_NAT/definition/fqdn.com.db'
dhcp_name = os.environ["PYTHON_SONICOS_HOME"]+'/Network/FQDN_based_NAT/definition/named.conf'
dns_file = os.environ["PYTHON_SONICOS_HOME"]+'/Network/FQDN_based_NAT/definition/dns.txt'
# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
PC3 = Host(Params.testbed + '-PC3')
PC4 = Host(Params.testbed + '-PC4')
PC5 = Host(Params.testbed + '-PC5')
PC1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
dns_server = OpenS.get_node_interface_ip('PC3', 'eth1')
PC3_Eth2 = OpenS.get_node_interface_ip('PC3', 'eth2')
# res =  Linterface.get_interface_address(name='X1')
# X1_ip = res['ip_address'] #192.200.200.150
X1_ip = '192.200.200.150'
# define IP
PC1_IP_edit = '192.168.168.200'
X1_IP_N = "192.200.200.205"
wanpc_fqdn = 'wanpc.fqdn.com'
wanpc_fqdn_edit = 'wanpcedit.fqdn.com'
x1ao_fqdn = 'x1ao.fqdn.com'

#cmds
cmd_route = 'ip r a 192.200.200.0/24 via 192.168.168.168 dev eth1'
cmd1 = f"\nnameserver {PC3_Eth2}\n"
cmd2 = f"\nnameserver {dns_server}\n"
# DUT local Address object and group
opt1 = {
    'name': 'lanpc',
    'zone': 'LAN',
    'object_type': 'host',
    'value': PC1_IP,
}
opt2 = {
    'name': 'wanpc_fqdn',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': wanpc_fqdn,
    'dns_ttl':0
}
edit_opt2 = {"address_objects":
            [
                {
                "fqdn":{
                    "name":"wanpc_fqdn",
                    "zone":"WAN",
                    "domain":wanpc_fqdn_edit,
                    "dns_ttl":0
                    }
                }
            ]
            }

opt3 = {
    'name': 'x1_addr',
    'zone': 'WAN',
    'object_type': 'host',
    'value': X1_IP_N,
}
opt4 = {
    'name': 'lanpc1',
    'zone': 'LAN',
    'object_type': 'host',
    'value': PC1_IP_edit,
}
opt5 = {
    'name': 'x1_fqdn',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': x1ao_fqdn,
    'dns_ttl':0
}

opt6 = {
    'name': 'member1',
    'zone': 'WAN',
    'object_type': 'host',
    'value': '192.200.200.105',
}
opt7 = {
    'name': 'member2',
    'zone': 'WAN',
    'object_type': 'host',
    'value': '192.200.200.106',
}
opt8={
    "address_groups":[{
        "ipv4":{
            "address_object":{
                "ipv4":[{"name":"member2"}],
                "fqdn":[{"name":"wanpc_fqdn"}]
                },
            "name":"nat_group"
            }
        }]
    }
opt9 = {
    'name': 'fqdntest',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': 'fqdntest.fqdn.com',
    'dns_ttl':0
}
opt10={
    "address_groups":[{
        "ipv4":{
            "address_object":{
                "ipv4":[{"name":"lanpc"},{"name":"lanpc1"}],
                },
            "name":"lanpc_group"
            }
        }]
    }

##Nat opts
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
                        "source": {"name":opt2['name']},
                        "translated_source":  {'original': True},
                       'destination': {"name":"X1 IP"},
                        'translated_destination':{'name': opt1['name']},
                        'service': {"any": True},
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

dns_dict = {
    "dns": {
        "server": {
            "inherit": False,
            "static": {
                "primary": dns_server,
                "secondary": '',
                "tertiary": '',
            }
        }
    }
}


Lx1 = {
        'if' : 'X1',
        'zone': 'WAN' ,
        'mode': 'dhcp',
        'dhcp_hostname' : 'test',
        'dhcp_renew_on_startup':False,
        'dhcp_initiate_renewals_with_discover':False,
        'dhcp_force_discover_interval':0,
        'type':'',
        'comment':'',
        'flow_reporting':True,
        'multicast':False,
        'cos_8021p':False,
        'exclude_route':False,
        'asymmetric_route':False,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
        'user_http':False
}
Lx1_r = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_ip,
            'netmask': '255.255.255.0',
            'gateway': '192.200.200.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
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






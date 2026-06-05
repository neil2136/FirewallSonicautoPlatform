import os
import sys
import re
import time
import copy

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test,repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from networkdevice import Host
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network,vpn,firewall,system,log,sdwan
from lib.modules.CLI.system import LicenseCli
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_GUI_Network_Part1')

OpenS = Openstack(Params.testbed)
MASK = '255.255.255.0'
DUT_X0 = '192.168.168.168'
DUT_X1 = '13.0.0.10'
DUT_X1_GW = '13.0.0.1'
DUT_X0_ipv6 = '2003::1'
DUT_X2 = '23.0.0.10'
DUT_X2_ipv6 = '2004::1'
DUT_X3 = '12.12.1.200'
Remote_X0 = '172.16.1.101'
Remote_X1 = '12.12.1.201'
# pc1_ip = "192.168.168.200"
pc1_ip = OpenS.get_node_interface_ip('PC1','eth0')
logger.info(f'------pc1 ip---------{pc1_ip}')
pc2_ip = "13.0.0.5"
pc3_ip = "172.16.1.168"
PC2_Network = '13.0.0.0'
PC1_Network = '192.168.168.0'
PC3_Network = '172.16.1.0'
DUT_Network = '12.12.1.0'
PC1_IF = 'eth0'
PC2_IF = 'eth1'
LOCALSUBNET = "X0 Subnet"
REMOTESUBNET = "X0 Subnet"
PC2 = Host(Params.testbed + '-PC2')
PC1 = Host(Params.testbed + '-PC1')
PC3 = Host(Params.testbed + '-PC3')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_GUI_Network_Part1/testplan/Config_Auditing_GUI_Network_Part1.json'
CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_GUI_Network_Part1/confs/'
cfg_path = os.environ["PYTHON_COMMON_HOME"] + '/config/'
OpenS = Openstack(Params.testbed)
node_list = OpenS.get_nodes_as_dictionary().keys()
logger.info(node_list)
fw_api = Firewall(DUT_X0, user='admin', password='sonicauto', supported_config_mode='api')
rt_api = Firewall(Remote_X1, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
vlan = OpenS.get_node_interface_vlan_id('UTM','X2')
Linterface = network.InterfaceIPv4Api(fw_api)
Rinterface = network.InterfaceIPv4Api(rt_api)
LAddrOBJ = network.AddressobjectsApi(fw_api)
RAddrOBJ = network.AddressobjectsApi(rt_api)
Lvpn_obj = vpn.VpnbasesettingApi(fw_api)
Rvpn_obj = vpn.VpnbasesettingApi(rt_api)
Laccess_rule_obj = firewall.AccessRuleApi(fw_api)
snmp_obj = system.SNMPApi(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
license_obj = LicenseCli(fw_cli)
log_obj = log.LogMonitorApi(fw_api)
audit_logobj = log.AuditlogMonitorApi(fw_api)
Linterface_ipv6= network.InterfaceIPv6Api(fw_api)
failover_obj = network.FailoverLbApi(fw_api)
zones_obj = network.ZoneObjectsApi(fw_api)
vlan_translation = network.VLANTranslationApi(fw_api)
dns_setting = network.DnsSettingsApi(fw_api)
dns_proxy = network.DnsProxyApi(fw_api)
dns_security = network.DNSSecurityApi(fw_api)
dns_filter = network.DnsFilteringApi(fw_api)
logsetting_obj = log.LogSettingsApi(fw_api)
route_obj = network.RoutePolicyApi(fw_api)
sdwan_group = sdwan.SDWANGroupAPI(fw_api)
sdwan_probe = sdwan.SDWANProbesAPI(fw_api)
sdwan_obj = sdwan.SDWANPerfClassAPI(fw_api)
sdwan_path = sdwan.SDWANPathSelectionAPI(fw_api)
sdwan_rt_obj = sdwan.SdwanRouteApi(fw_api)
dynamic_route =network.DynamicRoutingApi(fw_api)
nat_policy = network.NatpolicyApi(fw_api)
arp_obj = network.ArpApi(fw_api)
ndp_obj = network.NeighborDiscoveryApi(fw_api)
mac_spoof = network.MacIPAntiSpoofApi(fw_api)
dhcp_obj = network.DHCPServerApi(fw_api)

rm_device = 'RemoteGEN7'

pc1_route_cmds = [f'ip r a {PC2_Network}/24 via {DUT_X0} dev {PC1_IF}',
                  f'route add -net {PC3_Network}/24 gw {DUT_X0}',
                  f'route add -net 12.12.1.0/24 gw {DUT_X0}',
                  "ip route"]
pc2_route_cmds = [f'ip r a {PC1_Network}/24 via {DUT_X1} dev {PC2_IF}',
                  "ip route"]
pc3_route_cmds = [f'route add -net {PC1_Network}/24 gw {Remote_X0}',
                  f'route add -net {DUT_Network}/24 gw {Remote_X0}',
                  "ip route"]

dhcp_server_settings_v6 = {"dhcp_server":{
    "ipv6":{
        "enable":False
        }
    }
}
dhcp_scope_static_v6 = {
    "dhcp_server":{
        "ipv6":{
            "scope":{
                "static":[
                    {
                        "name":"static_ipv6",
                        "enable":True,
                        "prefix":"2003::",
                        "ip":"2003::5",
                        "iaid":5,
                        "duid":"16",
                        "lifetime":{"valid":2160,"preferred":1440},
                        "comment":"",
                        "always_send_option":False,
                        "domain_name":"",
                        "dns":{
                            "server":{"inherit":True}
                            },
                        "generic_option":{}
                    }
                ]
            }
        }
    }
}
dhcp_scope_dynamic_v6 = {
            "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "scope_ipv6",
                                "enable": True,
                                "prefix": "2003::",
                                "range": {
                                    "from": "2003::6",
                                    "to": "2003::9"
                                }
                            }
                        ]
                    }
                }
            }
        }
dhcp_scope_dynamic_x0 = {
    "dhcp_server":{
        "ipv4":{
            "scope":{
                "dynamic":[
                    {"from":"192.168.168.200",
                     "to":"192.168.168.200",
                     "enable":True,
                     "lease_time":1440,
                     "default_gateway":"192.168.168.168",
                     "netmask":"255.255.255.0",
                     "comment":"",
                     "allow_bootp":False,
                     "domain_name":"",
                     "dns":{
                         "server":{"inherit":True}
                         },
                    "wins":{"primary":"0.0.0.0","secondary":"0.0.0.0"},
                    "call_manager":{"primary":"","secondary":"","tertiary":""},
                    "network_boot":{"next_server":"0.0.0.0","boot_file":"","server_name":""},
                    "generic_option":{},
                    "always_send_option":False
                        }
                    ]
                }
            }
        }
    }
dhcp_scope_dynamic = {
    "dhcp_server":{
        "ipv4":{
            "scope":{
                "dynamic": [
                    {"from":'23.0.0.1',
                    "to":'23.0.0.9',
                    "enable": True,
                    "lease_time": 1440,
                    "default_gateway": "23.0.0.10",
                    "netmask": "255.255.255.0",
                    "comment": "",
                    "allow_bootp": False,
                    "domain_name": "",
                    "dns": {
                        'server':{
                            "static": {"primary":"10.50.129.148","secondary":"10.50.129.149","tertiary":"0.0.0.0"}}
                            },
                    "wins": {"primary": "0.0.0.0"},
                    }]
                }}}}
dhcp_scope_static = {
    "dhcp_server":{
        "ipv4":{
            "scope":{
                "static":[{
                    "ip":"23.0.0.11",
                    "mac":"000102030471",
                    "enable":True,
                    "name":"TEST",
                    "lease_time":1440,
                    "default_gateway":"23.0.0.10",
                    "netmask":"255.255.255.0",
                    "comment":"",
                    "domain_name":"",
                    "dns":{
                        "server":{
                            "static":{"primary":"10.50.129.148","secondary":"10.50.129.149","tertiary":"0.0.0.0"}}
                            },
                    "wins":{"primary":"0.0.0.0","secondary":""},
                    }]
                    }
                }
            }
        }
dhcp_server_settings = {
            "dhcp_server": {
                "ipv4": {
                    "enable":True,
                    "persistence":True,
                    "conflict_detection":True,
                    "persistence_monitoring_interval":5,
                }
            }
        }
mac_set_ipv4 = {
            'mac_ip_anti_spoof': {
                'interface': [
                    {
                        'name': 'X2',
                        'enable': True,
                        'static_arp': False, 
                        'dhcp_server': False,
                        'dhcp_relay': False,
                        'arp_lock': False,
                        'arp_watch': False,
                        'enforce_ingress': False,
                        'spoof_detection': False,
                        'allow_management': True
                    }
                ]
            }
        }
mac_set_ipv6 = {
    "mac_ip_anti_spoof":{
        "ipv6":{
            "interface":[
                {
                    "allow_management":True,
                    "ndp_lock":False,
                    "static_ndp":False,
                    "enable":True,
                    "enforce_ingress":False,
                    "name":"X2",
                    "spoof_detection":False
                }
            ]
        }
    }
}
mac_cache_ipv4 = {
    "mac_ip_anti_spoof":{
        "cache":{
            "entry":[
                {
                    "ip":DUT_X2,
                    "mac":"2CB8ED6D7FF6",
                    "interface":"X2",
                    "router":False,
                    "blacklisted":False
                }
            ]
        }
    }
}
mac_cache_ipv6 = {
    "mac_ip_anti_spoof":{
        "ipv6":{
            "cache":{
                "entry":[
                    {
                        "ip":"28::28",
                        "mac":"2CB8ED6D7FF6",
                        "interface":"X2",
                        "router":False,
                        "blacklisted":False
                        }
                    ]
                }
            }
        }
    }

ndp_dict = {'ip': '48::48',
                'mac': '2CB8ED6D7FF6',
                'interface': 'X2'
                }
static_arp_dict = {
    'ip': pc2_ip,
    'mac': '2cb8ed6d7ff7',
    'interface': 'X2',
    'publish': False,
    'bind_mac': False,
}
nat_dict =  {
    "nat_policies":[
        {
            "ipv4":{
                "name":"test_nat",
                "dns_doctoring":False,
                "reflexive":False,
                "inbound":"any",
                "outbound":"X2",
                "comment":"",
                "enable":True,
                "translated_destination":{"original":True},
                "translated_source":{"original":True},
                "translated_service":{"original":True},
                "source":{"any":True},
                "destination":{"any":True},
                "service":{"any":True},
                "priority":{"auto":True},
                "ticket":{"tag1":"","tag2":"","tag3":""}
        }}]}
nat_ipv6_dict = {
    "nat_policies":[
        {
            "ipv6":{
                "name":"test_nat_ipv6",
                "reflexive":False,
                "inbound":"any",
                "outbound":"X2",
                "comment":"",
                "enable":True,
                "translated_destination":{"original":True},
                "translated_source":{"original":True},
                "translated_service":{"original":True},
                "source":{"any":True},
                "destination":{"any":True},
                "service":{"any":True},
                "priority":{"auto":True},
                "ticket":{"tag1":"","tag2":"","tag3":""}
        }}]}

ospfv2_dict = {
            'interface': 'X2',
            'mode': 'enable',
        }
rip_dict ={
            'interface': 'X2',
            'mode': 'send_and_receive',
}
ospfv3_dict = {
            'interface': 'X2',
            'mode': 'enable',
        }
ripng_dict= {
            'mode': 'enable',
            'interface': 'X2',
        }
sdwan_group_json = {
            'name': 'test',
            'interface_name': ['X3'],
            'priority': 1
        }
sdwan_probe_json = {
            'name': 'test',
            'sdwan_group': 'test',
            'probe_target': 'Default Gateway',
            'probe_type': 'tcp',
            'port': 8080,
            'interval': 8,
            'reply_timeout': 6,
            'missed': 6,
            'successful': 2,
            'rst_as_miss': True
        }
sdwan_object_json = {
            'name': 'test',
            'latency': 12,
            'jitter': 2,
            'packet_loss': 10,
        }
sdwan_psp = {
            'name': 'test',
            'sdwan_group': 'test',
            'sla_probe': 'test',
            'sla_class': 'test',
            'backup_interface': "",
            'reset_connections': False,
        }
sdwan_route = {
            'name': 'test3_route',
            'path_selection_profile': 'test',
            'interface': 'test',
            'metric': 2
}
route_ipv6 = {"route_policies":[{
    "ipv6":{
        "name":"test_ipv6",
        "comment":"",
        "interface":"X1",
        "metric":1,
        "service":{"any":True},
        "gateway":{"default":True},
        "source":{"any":True},
        "destination":{"any":True},
        "disable_on_interface_down":True,
        "vpn_precedence":False,
        "probe":"",
        "ticket":{"tag1":""},
        "distance":{"auto":True},
        "tos":"0x00",
        "mask":"0x00",
        "type":"standard"}}]}
route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X1",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "any": True },
                        "service": { "any": True },
                        "gateway": { "default":True },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": 'test1_route',
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }
dns_security_enable = {
    'action':'dropping_with_logs'
}
dns_proxy_json = {
            'enforce_all_dns_requests': True,
            "dns_cache": False,
        }
dns_proxy_entry = {
            'domain': 'www.baidu.com',
            'ipv4_primary':'58.58.58.58',
            'ipv6_primary': '58::58',
        }
dns_dict_ipv4 = {
            'domain': 'test',
            'ipv4': {
                'primary': Params.G_DNS1,
            },
            'local_interface': 'X1',
        }
dns_dict_ipv6 = {
            'domain': 'mail.126.com',
            'ipv6': {
                'primary': '33::33',
            },
            'local_interface': 'X1',
        }
#dns setting
dns_set = {
    "dns":{
        "server":
                {
                    "inherit":True,
                    "static":
                        {
                            "primary":"0.0.0.0",
                            "secondary":"0.0.0.0",
                            "tertiary":"0.0.0.0"
                        },
                    "ipv6":
                        {
                            "inherit":True,
                            "static":
                                {
                                    "primary":"::",
                                    "secondary":"::",
                                    "tertiary":"::"
                                },
                            "preferred":False
                        }
                },
            "rebinding":
                {
                    "enable":True,
                    "action":"drop-dns-reply",
                    "allowed_domains":{}
                },
        "fqdn_binding":False,
        "split_servers":True,
        "fqdn_over_tcp_dns":False
        }
    }
vlan_trans_json = {
    'ingress_interface':'X2',
    'ingress_vlan':1,
    'egress_interface':'X4',
    'egress_vlan':3,
    'reverse':False
}
customer_zone = {
            "zones": [
                {
                    "name": "test",
                    "security_type": "public",
                    "interface_trust": True,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "gateway_anti_virus": True,
                    "intrusion_prevention": False
                }
            ]
        }
syslog_param = {
            "name":pc1_ip,
        }
lb = {
            'enable': True
        }
lb_group = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical"
                            },
                            {
                                "name": "X3",
                                "rank": 2,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {}
                        ]
                    }
                ]
            }
        }
local_obj = {
            "object_type": "host",
            "name": pc1_ip,
            "zone": "LAN",
            "value": pc1_ip,
        }
syslog_obj = {
            "object_type": "host",
            "name": 'test_syslog',
            "zone": "LAN",
            "value": '192.168.168.100',
        }
snmp_json = {"snmp":
                         {
                             "enable": True,
                             "system_name": "sonicwall",
                             "get_community_name": "public",
                             "trap_community_name": "public",
                             "host_1": pc2_ip,
                             "host_2": "",
                             "host_3": "",
                             "host_4": ""
                         }
        }
redundant_port = {
    'redundancy_aggregation_port':'redundancy',
    'redundancy_port':'X4'
}
remove_redundancy = {
    'redundancy_aggregation_port':False
}
Lx0_ipv6 = {
        'name': 'X0',
            'mode': 'static',
            'zone':'LAN',
            "ip": DUT_X0_ipv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'router_adv': True,
            'ra_max': 300,
            'managed': True,
            'other_config': True,
}
Lx1 = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': DUT_X1,
    'netmask': MASK,
    'gateway': DUT_X1_GW,
    'dns1': Params.G_DNS1,
    'dns2': Params.G_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_https': True,
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
Lx2_wiremode = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X4',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
Lx2_ipv6 =  {
            'name': 'X2',
            'mode': 'static',
            'zone':'LAN',
            "ip": DUT_X2_ipv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'router_adv': True,
            'ra_max': 300,
            'managed': True,
            'other_config': True,
        }
Lx2_ti = {
            'name':'x2_ti',
            "zone": "LAN",
            "type": "manual",
            'ip':'2005::1',
            'bound_to': {"any":True},
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_snmp': True, 
            'prefix_length':64,
            'ipv4_address':{"name":"test_syslog"},
            'ipv6_network':{"name":"X0 IPv6 Link-Local Address"}
        }
Lx2_vlan = {
                'if': 'x2',
                'type': 'vlan',
                'vlan_tag': vlan,
                'zone': 'LAN',
                'mode': 'static',
                'ip': '1.1.1.1',
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
Lx5 = {
            'if': 'X5',
            'zone': 'LAN',
            'mode': 'portshield',
            'portshield_to': 'X2',
            'link_speed':'auto'
}
Rx1 = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': Remote_X1,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
    }
local_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(PC3_Network),
}
#RemoteDUT local and remote object
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(PC1_Network),
}
Lvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Remote_X1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : DUT_X0,
    'peer_ike_id'       : Remote_X0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : LOCALSUBNET,
    'remote_net_name'   : local_r['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
}

Rvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : DUT_X3,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Remote_X0,
    'peer_ike_id'       : DUT_X0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],

}
log_level_settings = {
            "log": {
                "event": [{
                    "id": 1382,
                    "name": "",
                    "category": "Log",
                    "group": "",
                    "priority_level": "alert",
                    "log_monitor": {
                        "redundancy_interval": 0
                    },
                    "email_alert": {
                        "redundancy_interval": 600
                    },
                    "syslog": {
                        "redundancy_interval": 0
                    },
                    "event_profile": {
                        "syslog_server_profile": 0
                    },
                    "trap":{
                        "redundancy_interval":0
                    },
                    "ipfix": {
                        "redundancy_interval": 60
                    },
                    "log_digest": True ,
                    "color": {
                        "hex": "0x00FF0000"
                    },
                    "alert_email": {}
                }]
            }
}
rule_opt = {
            "name": "any2any",
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

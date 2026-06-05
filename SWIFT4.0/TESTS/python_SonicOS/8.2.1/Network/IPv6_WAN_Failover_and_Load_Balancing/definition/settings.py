import os
import sys
import copy
import re
import time
import base64
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_WAN_Failover_and_Load_Balancing')
from runner.unittest.setup import Test, repeat_method,repeat_class
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from lib.modules.API import network,system,log
from lib.modules.CLI.network import FailoverLBCli
from utm import Firewall
from lib.modules.CLI.system import LicenseCli,DiagnosticsCli

OpenS = Openstack(Params.testbed)
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
PC3 = Host(Params.testbed + '-PC3')
PC_Server = Host(Params.testbed + '-PC-Server')
TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_WAN_Failover_and_Load_Balancing/testplan/IPv6_WAN_Failover_and_Load_Balancing.json'
vlan_tag = OpenS.get_node_interface_vlan_id('UTM','X3:1')

DUT_X0_IPV4 = '192.168.168.168'
DUT_X0_IPV6 = '2001:db0::193'
DUT_X0_NET_IPV6 = '2001:db0::/64'
DUT_X1_IPV4 = '13.0.0.10'
# DUT_X1_NET
DUT_X2_IPV4 = '23.0.0.10'
DUT_X3_IPV4 = '33.0.0.10'
DUT_X1_IPV6 = '2001:db1::193'
DUT_X1_GW= '2001:db1::1'
DUT_X1_NET_IPV6 = '2001:db1::/64'
DUT_X2_IPV6 = '2001:db2::193'
DUT_X2_GW= '2001:db2::1'
DUT_X2_NET_IPV6 = '2001:db2::/64'
DUT_X3_IPV6 = '2001:db3::193'
PC2_ETH0_IPV6 = '2001:db1::1093'
PC3_ETH0_IPV6 = '2001:db2::1093'
PC2_ETH2_IPV6 = '2001:db4::183'
PC3_ETH2_IPV6 = '2001:db4::193'
PC_Server_ETH0_IPV6 = '2001:db4::1093'
PC_Server_NET_IPV6 = '2001:db4::/64'

result = {}

fw_api = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto',ssh_version=2, supported_config_mode='cli-ssh')

interfacev4api = network.InterfaceIPv4Api(fw_api)
interfacev6api = network.InterfaceIPv6Api(fw_api)
failover_obj = network.FailoverLbApi(fw_api)
packetObj = system.PacketmonitorApi(fw_api)
setting_obj = system.SettingApi(fw_api) 
nat_obj = network.NatpolicyApi(fw_api)
failover_cli = FailoverLBCli(fw_cli)
license_obj = LicenseCli(fw_cli)
diag_api = system.DiagnosticApi(fw_api)
log_api = log.LogMonitorApi(fw_api)

pc1_route_cmds = [
    f"ip -6 route add {DUT_X1_NET_IPV6} via {DUT_X0_IPV6}",
    f"ip -6 route add {DUT_X2_NET_IPV6} via {DUT_X0_IPV6}",
    f"ip -6 route add {PC_Server_NET_IPV6} via {DUT_X0_IPV6}",
    "ip -6 route"
]
pc2_route_cmds = [
    f"ip -6 route add {DUT_X0_NET_IPV6} via {DUT_X1_IPV6}",
    "ip -6 route"
]
pc3_route_cmds = [
    f"ip -6 route add {DUT_X0_NET_IPV6} via {DUT_X2_IPV6}",
    "ip -6 route"
]
pc_server_route_cmds = [
    f"ip -6 route add {DUT_X1_NET_IPV6} via {PC2_ETH2_IPV6}",
    f"ip -6 route add {DUT_X2_NET_IPV6} via {PC3_ETH2_IPV6}",
    "ip -6 route"
]
forward_cmds = ['echo "net.ipv6.conf.all.forwarding = 1" >> /etc/sysctl.conf',
                "sysctl -p /etc/sysctl.conf"]
traffic_cmd = [f'ping6 -c 2 {PC_Server_ETH0_IPV6}']
x0_ipv6 = {'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': DUT_X0_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'ra_max': 30
        }
x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUT_X1_IPV4,
            'netmask': '255.255.255.0',
            'gateway': '13.0.0.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }
x1_ipv6 = {'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': DUT_X1_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'gateway':PC2_ETH0_IPV6,
            'ra_max': 30
            }
x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUT_X2_IPV4,
            'netmask': '255.255.255.0',
            'gateway': '23.0.0.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }
x2_ipv6 = {'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': DUT_X2_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'gateway':PC3_ETH0_IPV6,
            'ra_max': 30
            }
x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': vlan_tag,
            'zone': 'WAN',
            'mode': 'static',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'ip': DUT_X3_IPV4,
            'asymmetric_route': True,
        }
x3_ipv6 = {'name': 'X3',
            'mode': 'static',
            'zone': 'WAN',
            'vlan': vlan_tag,
            'ip': DUT_X3_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'ra_max': 30
        }
lb_ipv6 = {
            "failover_lb": {
                "group": [
                    {
                        "name":" Default LB Group IPv6",
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
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X2",
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
x1_both = {
    "name":"X1",
    "rank":1,
    "probe_type":"logical",
    "probe_condition":"both",
    "main_target":{
        "protocol":{"ping":True},
        "host":PC_Server_ETH0_IPV6
        },
    "alternate_target":{
        "protocol":{"ping":True},
        "host":PC2_ETH0_IPV6
        },
    "default_target":{"value":PC_Server_ETH0_IPV6}
}
x2_both = {
    "name":"X2",
    "rank":2,
    "probe_type":"logical",
    "probe_condition":"both",
    "main_target":{
        "protocol":{"tcp":{"value":50000}},
        "host":"responder.global.sonicwall.com"
        },
    "alternate_target":{
        "protocol":{"tcp":{"value":50000}},
        "host":"responder.global.sonicwall.com"
        },
    "default_target":{"value":PC_Server_ETH0_IPV6}
    }
x1_main = {
    "name":"X1",
    "rank":1,
    "probe_type":"logical",
    "probe_condition":"main",
    "main_target":{
        "protocol":{"ping":True},
        "host":PC_Server_ETH0_IPV6
        },
    "default_target":{"value":PC_Server_ETH0_IPV6}
    }
x2_main = {
    "name":"X2",
    "rank":2,
    "probe_type":"logical",
    "probe_condition":"main",
    "main_target":{
        "protocol":{"tcp":{"value":50000}},
        "host":"responder.global.sonicwall.com"
        },
    "default_target":{"value":PC_Server_ETH0_IPV6}
    }
x1_either={
    "name":"X1",
    "rank":1,
    "probe_type":"logical",
    "probe_condition":"either",
    "main_target":{
        "protocol":{"ping":True},
        "host":PC_Server_ETH0_IPV6
        },
    "alternate_target":{
        "protocol":{"ping":True},
        "host":PC2_ETH0_IPV6
        },
    "default_target":{"value":PC_Server_ETH0_IPV6}
    }
x2_either={
    "name":"X2",
    "rank":2,
    "probe_type":"logical",
    "probe_condition":"either",
    "main_target":{
        "protocol":{"tcp":{"value":50000}},
        "host":"responder.global.sonicwall.com"
        },
    "alternate_target":{
        "protocol":{"tcp":{"value":50000}},
        "host":"responder.global.sonicwall.com"
        },
    "default_target":{"value":PC_Server_ETH0_IPV6}
    }
lb_ipv6_round_robin = {
    "failover_lb":{
        "group":[
            {
                "name":" Default LB Group IPv6",
                "type":"round-robin",
                "final_backup":"",
                "address_binding":True,
                "probing":{
                    "health_check":5,
                    "missed_intervals":3,
                    "successful_intervals":3,
                    "global_responder":False
                    },
                "interface":[
                    {
                        "name":"X1",
                        "probe_type":"physical",
                        "probe_condition":"always",
                        "rank":1
                    },
                    {
                        "name":"X2",
                        "probe_type":"physical",
                        "probe_condition":"always",
                        "rank":2
                    },
                    {}
                ]
            }
        ]
    }
}
lb_ipv6_spill = {
    "failover_lb":{
        "group":[
            {
                "name":" Default LB Group IPv6",
                "type":"spillover",
                "final_backup":"",
                "address_binding":True,
                "spillover_bandwidth":{"value":1},
                "probing":{
                    "health_check":5,
                    "missed_intervals":3,
                    "successful_intervals":3,
                    "global_responder":False
                    },
                "interface":[
                    {
                        "name":"X1",
                        "rank":1,
                        "probe_type":"physical",
                        "probe_condition":"always"
                    },
                    {
                        "name":"X2",
                        "rank":2,
                        "probe_type":"physical",
                        "probe_condition":"always"
                    },
                    {}
                ]
            }
        ]
    }
}
lb_ipv6_radio = {
    "failover_lb":{
        "group":[
            {
                "name":" Default LB Group IPv6",
                "type":"ratio","final_backup":"",
                "address_binding":True,
                "probing":{
                    "health_check":5,
                    "missed_intervals":3,
                    "successful_intervals":3,
                    "global_responder":False
                    },
                "interface":[
                    {"name":"X1"},
                    {"name":"X2"},
                    {}
                ],
                "percent":[
                    {
                        "interface":"X1",
                        "percent":50
                    },
                    {
                        "interface":"X2",
                        "percent":50
                    }
                ]
            }
        ]
    }
}

lb_ipv4 = {
            "failover_lb": {
                "group": [
                    {
                        "name":" Default LB Group",
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
                            },
                            # {"name": "X2",
                            # "rank": 2
                            # }
                        ]
                    }
                ]
            }
        }
failover_json = {
        'enable'    : False,
        'probes'    : False,
        'syn'       : False,
        'port'      : 1,
    }
failover_port = {
        'enable'    : True,
        'probes'    : True,
        'syn'       : True,
        'port'      : 1,
    }
lb_cli = {
    'enable': True,
}
basic_cli = {
    'type': 'basic',
    'preempt': True,   
    'version': '6', 
    'global-responder': True,
    'final-backup':f'X3:V{vlan_tag}',
    'health-check': '5',
    'missed-intervals': '6',
    'successful-intervals': '7',
}
ratio_cli = {
    'type': 'ratio',
    'address-binding': True,    
    'add-interfaces': ['X1', 'x2'],
    'percentages': ['60', '40'],
    'version': '6', 
    # 'auto-adjust-ratio': True,
    'global-responder': True,
    'health-check': '5',
    'missed-intervals': '6',
    'successful-intervals': '7',
}
round_robin_cli = {
    'type': 'round-robin',
    'version': '6', 
    'address-binding': True,    
    'global-responder': True,
    'health-check': '5',
    'missed-intervals': '6',
    'successful-intervals': '7',
    }
spill_cli = {
    'type': 'spillover',
    'version': '6', 
    'spillover-bandwidth': '1000',
    'address-binding': True,    
    'global-responder': False,
    'health-check': '5',
    'missed-intervals': '6',
    'successful-intervals': '7',
    }
nat_policy1 = {
    "nat_policies":[
        {
            "ipv6":{
                "name":"test1",
                "reflexive":False,
                "source_port_remap":True,
                "inbound":"any",
                "outbound":"X1",
                "comment":"",
                "enable":True,
                "translated_destination":{"original":True},
                "translated_source":{"name":"X1 IPv6 Primary Static Address"},
                "translated_service":{"original":True},
                "source":{"any":True},
                "destination":{"any":True},
                "service":{"any":True},
                "priority":{"auto":True},
                "ticket":{"tag1":"","tag2":"","tag3":""}
            }
        }
    ]
}
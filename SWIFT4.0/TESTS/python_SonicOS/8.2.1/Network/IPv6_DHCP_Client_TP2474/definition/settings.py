import sys
import os
import time
import copy
import paramunittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Client_TP2474')
from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network,system
from lib.modules.CLI.system import LicenseCli

OpenS = Openstack(Params.testbed)
fw_cli = Firewall('192.168.168.168', user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw = Firewall('192.168.168.168', user='admin', password='sonicauto', supported_config_mode='api')
dhcpv6_server = Firewall('12.12.2.201', user='admin', password='sonicauto', supported_config_mode='api')
Linterface = network.InterfaceIPv4Api(fw)
Rinterface = network.InterfaceIPv4Api(dhcpv6_server)
Linterface_ipv6 = network.InterfaceIPv6Api(fw)
Rinterface_ipv6 = network.InterfaceIPv6Api(dhcpv6_server)
failover_obj = network.FailoverLbApi(fw)
license_obj = LicenseCli(fw_cli)
Rdhcp_obj = network.DHCPServerApi(dhcpv6_server)
LPackageMonitObj = system.PacketmonitorApi(fw)
Lzone_obj = network.ZoneObjectsApi(fw)
Lrestart = system.RestartApi(fw)

# define path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_DHCP_Client_TP2474/testplan/IPv6_DHCP_Client_TP2474.json'
cfg_path = os.environ["PYTHON_COMMON_HOME"] + '/config/'
DUT_X1 = '12.12.1.200'
DUT_GW = '12.12.1.1'
DUT_X2 = '12.12.2.200'
DUT_X2_VLAN = '12.12.3.200'
X2_VLAN_GW = '12.12.3.1'
DHCPV6_X1 ='12.12.1.201' 
DHCPV6_X2 ='12.12.2.201' 
DHCPV6_X3 ='12.12.3.201' 
DHCPV6_X3_GW ='12.12.3.1' 
# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
rm_device = 'RemoteGEN7'
vlan_tag = OpenS.get_node_interface_vlan_id('UTM','X2:1')
#cmd
show_ips = [f'show interface ipv6 X2 vlan {vlan_tag} ips']


Lx1_ipv4 = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X1,
        'netmask': '255.255.255.0',
        'gateway': DUT_GW,
        'dns1': Params.G_DNS1,
        'dns2':Params.G_DNS2,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
Lx2_ipv4 = {
        'if': 'X2',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X2,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
Lx2_vlan = {
        'if': 'x2',
        'type': 'vlan',
        'vlan_tag': vlan_tag,
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X2_VLAN,
        'gateway': X2_VLAN_GW,
}
Lx2_vlan_ipv6 = {
            'name': 'X2',
            'vlan': vlan_tag,
            'mode': 'dhcpv6',
            'zone': 'WAN',
            "dhcpv6": {"rapid_commit": True},
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
            "listen_router_advertisement":True,
            'stateless_address_autoconfig':False,
}
Lx1_ipv6 = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'zone': 'WAN',
            "dhcpv6": {"rapid_commit": True},
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
            "listen_router_advertisement":True,
            'stateless_address_autoconfig':False
        }
Rx3_ipv4 = {
        'if': 'X3',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DHCPV6_X3,
        'netmask': '255.255.255.0',
        'gateway': DHCPV6_X3_GW,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
}
Rx1_ipv6 = {
            'name': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            "ip": "2023::3",
            'router_adv':True,
            "managed": True,
            "other_config": True    
}
Rx3_ipv6 = {
            'name': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            "ip": "2024::3",
            'router_adv':True,
            "managed": True,
            "other_config": True    
}
zone_dict = {
    "zones":[
        {
            'name': 'test',
            'security_type': 'public'
        }
    ]
}
lb = {
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
                                "name": "X2",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X1",
                                "rank": 2
                            },
                            {}
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
                                "name": "X2",
                                "rank": 1,
                            },
                            {}
                        ]
                    }
                ]
            }
        }
dhcp_scope_dyn_v6 = {
     "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "scope_ipv6",
                                "enable": True,
                                "prefix": "2023::",
                                "range": {
                                    "from": "2023::5",
                                    "to": "2023::9"
                                }
                            }
                        ]
                    }
                }
            }
        }
dhcp_scope_dyn_v6_x3 = {
     "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "dyn_ipv6",
                                "enable": True,
                                "prefix": "2024::",
                                "range": {
                                    "from": "2024::5",
                                    "to": "2024::9"
                                }
                            }
                        ]
                    }
                }
            }
        }
dhcp_scope_dyn_v6_x3_modify = {
     "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "dyn_ipv6",
                                "enable": True,
                                "prefix": "2024::",
                                "range": {
                                    "from": "2024::5",
                                    "to": "2024::11"
                                }
                            }
                        ]
                    }
                }
            }
        }
import os
import sys
import copy
import re
import time
import base64
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IPv6_VPN_TP2334')
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from lib.modules.API import network,system,log,vpn,firewall,object
from lib.modules.CLI.network import FailoverLBCli
from utm import Firewall
from lib.modules.CLI.system import LicenseCli,DiagnosticsCli

OpenS = Openstack(Params.testbed)
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
PC3 = Host(Params.testbed + '-PC3')
TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/VPN/IPv6_VPN_TP2334/testplan/IPv6_VPN_TP2334.json'
vlan_tag = OpenS.get_node_interface_vlan_id('UTM','X3:1')
rvlan_tag = OpenS.get_node_interface_vlan_id('RemoteGEN7','X3:1')

DUT_X0_IPV4 = '192.168.168.168'
DUT_X0_IPV6 = '2001:db0::193'
DUT_X0_NET_IPV4 = '192.168.168.0/24'
DUT_X0_NET_IPV6 = '2001:db0::/64'
DUT_X1_IPV4 = '12.12.1.200'
DUT_X2_IPV4 = '12.12.2.200'
DUT_X3_IPV4 = '12.12.13.200'
DUT_X1_NET_IPV4 = '12.12.1.0/24'
DUT_X2_NET_IPV4 = '12.12.2.0/24'
DUT_X1_IPV6 = '2001:db1::183'
DUT_X1_GW= '2001:db1::1'
DUT_X1_NET_IPV6 = '2001:db1::/64'
DUT_X2_IPV6 = '2001:df1::183'
DUT_X2_NET_IPV6 = '2001:df1::/64'
DUT_X3_IPV6 = '2001:de1::183'
DUT_X3_NET_IPV6 = '2001:de1::/64'
Remote_X0_IPV4 = '172.16.1.101'
Remote_X0_NET_IPV4 = '172.16.1.0/24'
Remote_X1_IPV4 = '12.12.1.201'
Remote_X2_IPV4 = '12.12.2.201'
Remote_X3_IPV4 = '12.12.13.201'
Remote_X4_IPV4 = '12.12.4.201'
Remote_X0_IPV6 = '2001:db2::193'
Remote_X0_NET_IPV6 = '2001:db2::/64'
Remote_X4_NET_IPV6 = '2001:db4::/64'
Remote_X1_IPV6 = '2001:db1::193'
Remote_X2_IPV6 = '2001:df1::193'
Remote_X3_IPV6 = '2001:de1::193'
Remote_X4_IPV6 = '2001:db4::193'
PC1_ETH1_IPV6 = '2001:db0::1093'
PC2_ETH1_IPV6 = '2001:db2::1093'
PC2_ETH1_IPV4 = '172.16.1.3'
PC3_ETH1_IPV6 = '2001:db4::1093'

LOCALSUBNET = "X0 Subnet"
REMOTESUBNET = "X0 Subnet"


rt_api = Firewall(Remote_X1_IPV4, user='admin', password='sonicauto', supported_config_mode='api')
fw_api = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto',ssh_version=2, supported_config_mode='cli-ssh')

license_obj = LicenseCli(fw_cli)
interfacev4api = network.InterfaceIPv4Api(fw_api)
interfacev6api = network.InterfaceIPv6Api(fw_api)
Rinterfacev4api = network.InterfaceIPv4Api(rt_api)
Rinterfacev6api = network.InterfaceIPv6Api(rt_api)
nat_obj = network.NatpolicyApi(fw_api)
Rnat_obj = network.NatpolicyApi(rt_api)
LAddrOBJ = network.AddressobjectsApi(fw_api)
Lsetting_obj = system.SettingApi(fw_api)
RAddrOBJ = network.AddressobjectsApi(rt_api)
Lvpn_obj = vpn.VpnbasesettingApi(fw_api)
Rvpn_obj = vpn.VpnbasesettingApi(rt_api)
Laccess_rule_obj = firewall.AccessRuleApi(fw_api)
Raccess_rule_obj = firewall.AccessRuleApi(rt_api)
LRestartObj = system.RestartApi(fw_api)
Log_obj = log.LogMonitorApi(fw_api)
Rlog_obj = log.LogMonitorApi(rt_api)
Laddrgroup = object.AddressObjectGroupApi(fw_api)
Raddrgroup = object.AddressObjectGroupApi(rt_api)
LpacketObj = system.PacketmonitorApi(fw_api)

pc1_route_cmds = [
    f"ip -6 route add {DUT_X1_NET_IPV6} via {DUT_X0_IPV6}",
    f"ip -6 route add {DUT_X2_NET_IPV6} via {DUT_X0_IPV6}",
    f"ip -6 route add {DUT_X3_NET_IPV6} via {DUT_X0_IPV6}",
    f"ip -6 route add {Remote_X0_NET_IPV6} via {DUT_X0_IPV6}",
    f"ip -6 route add {Remote_X4_NET_IPV6} via {DUT_X0_IPV6}",
    f'route add -net {DUT_X1_NET_IPV4} gw {DUT_X0_IPV4}',
    f'route add -net {DUT_X2_NET_IPV4} gw {DUT_X0_IPV4}',
    f'route add -net {Remote_X0_NET_IPV4} gw {DUT_X0_IPV4}',
    "ip -6 route",'ip route'
]
pc2_route_cmds = [
    f"ip -6 route add {DUT_X0_NET_IPV6} via {Remote_X0_IPV6}",
    f"ip -6 route add {DUT_X1_NET_IPV6} via {Remote_X0_IPV6}",
    f"ip -6 route add {DUT_X2_NET_IPV6} via {Remote_X0_IPV6}",
    f"ip -6 route add {DUT_X3_NET_IPV6} via {Remote_X0_IPV6}",
     f'route add -net {DUT_X1_NET_IPV4} gw {Remote_X0_IPV4}',
    f'route add -net {DUT_X2_NET_IPV4} gw {Remote_X0_IPV4}',
    f'route add -net {DUT_X0_NET_IPV4} gw {Remote_X0_IPV4}',
    "ip -6 route",'ip route'
]
pc3_route_cmds = [
    f"ip -6 route add {DUT_X0_NET_IPV6} via {Remote_X4_IPV6}",
    f"ip -6 route add {DUT_X1_NET_IPV6} via {Remote_X4_IPV6}",
    f"ip -6 route add {DUT_X2_NET_IPV6} via {Remote_X4_IPV6}",
    "ip -6 route",
]
x0_ipv6 = {'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': DUT_X0_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30
        }
x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUT_X1_IPV4,
            'netmask': '255.255.255.0',
            'gateway': '12.12.1.1',
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
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            # 'gateway':PC2_ETH0_IPV6,
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
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            # 'gateway':PC3_ETH0_IPV6,
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
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30
        }
r_x0_static = {
            'if': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Remote_X0_IPV4,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30

}
r_x4_static = {
            'if': 'X4',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Remote_X4_IPV4,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30

}
r_x0_ipv6 = {'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Remote_X0_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30
        }
# r_x1_static = {
#             'if': 'X1',
#             'zone': 'WAN',
#             'mode': 'static',
#             'ip': DUT_X1_IPV4,
#             'netmask': '255.255.255.0',
#             'gateway': '12.12.1.1',
#             'dns1': Params.G_DNS1,
#             'dns2': Params.G_DNS2,
#             'mgmt_https': True,
#             'mgmt_ssh': True,
#             'mgmt_snmp': True,
#             'mgmt_ping': True,
#             'user_https':True,
#         }
r_x1_ipv6 = {'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Remote_X1_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30
            }
r_x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Remote_X2_IPV4,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }
r_x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': rvlan_tag,
            'zone': 'WAN',
            'mode': 'static',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'ip': Remote_X3_IPV4,
            'asymmetric_route': True,
        }
r_x3_ipv6 = {'name': 'X3',
            'mode': 'static',
            'zone': 'WAN',
            'vlan': rvlan_tag,
            'ip': Remote_X3_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30
        }
r_x2_ipv6 = {'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Remote_X2_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30
            }
r_x4_ipv6 = {'name': 'X4',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Remote_X4_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30
            }

local_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    # 'value': '{},255.255.255.0'.format(Remote_X0_NET_IPV4),
    'value': '172.16.1.0,255.255.255.0',
}
#RemoteDUT local and remote object
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '192.168.168.0,255.255.255.0',
}
local_l_x0 = {
    'name': 'local_net_x0',
    'zone': 'VPN',
    'object_type': 'network',
    'subnet': "2001:db0::",
    'mask':"64",
}
local_r_ipv6 = {
    'name': 'remote_net_ipv6',
    'zone': 'VPN',
    'object_type': 'network',
    'subnet': "2001:db2::",
    'mask':"64",
}
local_r_x4 = {
    'name': 'remote_net_x4',
    'zone': 'VPN',
    'object_type': 'network',
    'subnet': "2001:db4::",
    'mask':"64",
}
local_l_host={
    'name': 'local_host',
    'zone': 'LAN',
    'object_type': 'host',
    'ip':PC1_ETH1_IPV6
}
local_r_host={
    'name': 'remote_host',
    'zone': 'VPN',
    'object_type': 'host',
    'ip':PC2_ETH1_IPV6
}
local_r_group={
    "address_groups":[
        {"ipv6":{
            "address_object":
            {"ipv6":[
                {"name":local_r_ipv6['name']},
                {"name":local_r_x4['name']}
                ]
            },
        "name":"remote_group"
        }
    }
]}
local_test_ipv6 = {
    'name': 'remote_test_ipv6',
    'zone': 'VPN',
    'object_type': 'network',
    'subnet': "2001:db2::",
    'mask':"32",
}
local_r_net = {
    'name': 'remote_net_all',
    'zone': 'VPN',
    'object_type': 'network',
    'subnet': "0::0",
    'mask':"0",
}
#RemoteDUT local and remote object
remote_r_ipv6 = {
    'name': 'remote_net_ipv6',
    'zone': 'VPN',
    'object_type': 'network',
    'subnet': "2001:db0::",
    'mask':"64",
}
remote_l_x0 = {
    'name': 'local_net_X0',
    'zone': 'LAN',
    'object_type': 'network',
    'subnet': "2001:db2::",
    'mask':"64",
}
remote_l_x4 = {
    'name': 'local_net_X4',
    'zone': 'LAN',
    'object_type': 'network',
    'subnet': "2001:db4::",
    'mask':"64",
}
remote_l_host={
    'name': 'local_host',
    'zone': 'LAN',
    'object_type': 'host',
    'ip':PC2_ETH1_IPV6
}
remote_r_host={
    'name': 'remote_host',
    'zone': 'VPN',
    'object_type': 'host',
    'ip':PC1_ETH1_IPV6
}
remote_l_net= {
    'name': 'local_net_all',
    'zone': 'LAN',
    'object_type': 'network',
    'subnet': "0::0",
    'mask':"0",
}
remote_l_group={
    "address_groups":[
        {"ipv6":{
            "address_object":
            {"ipv6":[
                {"name":remote_l_x0['name']},
                {"name":remote_l_x4['name']}
                ]
            },
        "name":"local_group"
        }
    }
]}

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
Lvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1_ipv4',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Remote_X1_IPV4,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    # 'local_ike_id'      : DUT_X0,
    # 'peer_ike_id'       : Remote_X0,
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
    'name'              : 'vpn2_ipv4',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : DUT_X1_IPV4,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    # 'local_ike_id'      : Remote_X0,
    # 'peer_ike_id'       : DUT_X0,
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
Lvpn_ipv6 = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Remote_X1_IPV6,
    'sec_gate'          : '2001:db1::',
    'local_ike_type'    : 'ipv6',
    'peer_ike_type'     : 'ipv6',
    # 'local_ike_id'      : DUT_X0,
    # 'peer_ike_id'       : Remote_X0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : "X0 IPv6 Primary Static Address Subnet",
    'remote_net_name'   : local_r_ipv6['name'],
    'ike_exchange'      : 'ikev2',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
}

Rvpn_ipv6 = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : DUT_X1_IPV6,
    'sec_gate'          : '2001:db1::',
    'local_ike_type'    : 'ipv6',
    'peer_ike_type'     : 'ipv6',
    # 'local_ike_id'      : Remote_X0,
    # 'peer_ike_id'       : DUT_X0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : "X0 IPv6 Primary Static Address Subnet",
    'remote_net_name'   : remote_r_ipv6['name'],
    'ike_exchange'      : 'ikev2',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],

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
import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from modules.API.network import WebproxyApi
from modules.API.network import InterfaceIPv6Api
from modules.API.network import ZoneObjectsApi
from modules.API.network import DHCPServerApi
from modules.API.network import NatpolicyApi
from modules.API.network import DnsProxyApi
from modules.API.network import DnsSettingsApi
from modules.API.network import NeighborDiscoveryApi
from modules.API.network import DDNSApi
from modules.API.network import DNSSecurityApi

ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
'''
webproxy = WebproxyApi(fw)
webproxy_dict = {
    'server':'1.1.1.1',
    'port':'3128',
    'bypass_upon_failure': True,
    'forward_public_requests':True,
}
rc = webproxy.config_webproxy(**webproxy_dict)
if rc:
    print('Config webproxy success')
else:
    print('Config weproxy fail')

webproxy_dict_fail = {
    'server':'1.1.1.1',
    'port':'_1',
    'bypass_upon_failure':True,
    'forward_public_requests':True,
}
rc = webproxy.config_webproxy(**webproxy_dict_fail, msg=True)
if rc[0]:
    print('Config webproxy success')
else:
    print('Config webproxy fail, fail code:')
    print(rc[1]['status']['info'][0]['message'])

# rc = webproxy.edit_bypass_upon_failure(True)
# rc = webproxy.edit_bypass_upon_failure(False)
# rc = webproxy.edit_forward_public_requests(True)
# rc = webproxy.edit_forward_public_requests(False)
rc = webproxy.add_user_proxy_server('1.1.1.1','2.2.2.2')
rc = webproxy.del_user_proxy_server('1.1.1.1','2.2.2.2')
output = webproxy.show_webproxy()
'''

from modules.API.network import InterfaceIPv4Api
interface = InterfaceIPv4Api(fw)
'''
x2_static_opt = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': '2.34.5.6',
    'netmask': '255.255.255.0',
    'gateway': '2.34.5.1',
    'mgmt_http': False,
    # 'mac_ovesrride': '345678901222'
}
x2_dhcp_opt = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'dhcp',
}
# rc = x2.config_interface(**x2_static_opt)
# rc = x2.config_interface(**x2_dhcp_opt)
x2_pppoe_opt_dynamic = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': '',
    'pppoe_passwd': '',
    'pppoe_service': '',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': True,
    'pppoe_inactivity': 0,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,    
}
x2_pppoe_opt_unnumber = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': '',
    'pppoe_passwd': '',
    'pppoe_service': '',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': False,
    'pppoe_unnumbered': 'X4',
    'pppoe_inactivity': 0,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,    
}
x2_pppoe_opt_ip = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': '',
    'pppoe_passwd': '',
    'pppoe_service': '',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': False,
    'pppoe_ip': '1.2.3.4',
    'pppoe_inactivity': 0,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,    
}

# rc = x2.config_interface(**x2_pppoe_opt_dynamic)
# rc = x2.config_interface(**x2_pppoe_opt_unnumber)
# rc = x2.config_interface(**x2_pppoe_opt_ip)

x2_pptp_opt_static = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pptp',
    'pptp_user': 'pptp_test',
    'pptp_passwd': 'password',
    'pptp_server': '10.10.10.10',
    'pptp_schedule': 'always_on',
    'pptp_dynamic': False,
    'pptp_ip': '1.2.3.4',
    'pptp_netmask': '255.255.255.0',
    'pptp_gateway': '1.2.3.40',
    'pptp_inactivity': 0,
}
x2_pptp_opt_dyn = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pptp',
    'pptp_user': 'pptp_test',
    'pptp_passwd': 'password',
    'pptp_server': '10.10.10.10',
    'pptp_schedule': 'always_on',
    'pptp_dynamic': True,
    'pptp_inactivity': 0,
}
# rc = x2.config_interface(**x2_pptp_opt_static)
# rc = x2.config_interface(**x2_pptp_opt_dyn)

x2_l2bridge = {
    'if': 'x2',
    'zone': 'DMZ',
    'mode': 'l2bridge',
    'bridge_to': 'x4',
    'vlan_filtering_mode': 'allow',
    'filtered_vlan' : '6 7',
}
# rc = x2.config_interface(**x2_l2bridge)

x2_lan_static = {
    'if': 'x2',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': '11.11.11.11',
    'netmask': '255.255.255.0',
    'gateway' : '11.11.11.12',
}
#rc = x2.config_interface(**x2_lan_static)
x2_lan_unnumber = {
    'if': 'x2',
    'zone': 'DMZ',
    'mode': 'unnumbered',
    'ip': '11.11.11.11',
    'netmask': '255.255.255.0',
    'gateway' : '11.11.11.12',
}
rc = x2.config_interface(**x2_lan_unnumber)
rc = x2.unassign_interface(**x2_lan_unnumber)



'''
x7_static_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'static',
    'ip': '66.7.8.9',
    'netmask': '255.255.255.0',
    'gateway': '66.7.8.99',
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    'user_https': True,
    'dns1': '1.1.1.1',
    'dns2': '2.2.2.2',
    'dns3': '3.3.3.3',
    'link_speed':'1000_full',#100_full,100_half,10_full,10_half,auto
    'port': 'aggregation',#None, aggregation, redundancy
    'port_aggregation': 'X10',
    }
x7_dhcp_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'dhcp',
    'force_discover_interval': False,# or False
    'initiate_renewals_with_discover': True,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    }

x7_pppoe_dynamic_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_ip': 'dynamic',
    'pppoe_user': 'abc',
    'pppoe_servicename': 'def',
    'pppoe_passwd': 'password',
    'pppoe_lcp_echo_packets': True,
    'pppoe_inactivity': 10, #or False
    'pppoe_reconnect' : 5, # or False
   'pppoe_schedule': 'always_on', 
#    'pppoe_schedule': 'name "Work Hours"',
    # 'pppoe_schedule': 'M_T_W_TH_F 08:00 to 17:00',
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': False,
    }   
x7_pppoe_static_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_ip': '7.7.7.7',
    'pppoe_user': 'abc',
    'pppoe_servicename': 'def',
    'pppoe_passwd': 'password',
    'pppoe_lcp_echo_packets': True,
    'pppoe_inactivity': 10,
    'pppoe_reconnect' : 0,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    }
x7_pppoe_unnumbered_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_unnumbered': 'X3',
    'pppoe_user': 'abc',
    'pppoe_servicename': 'def',
    'pppoe_passwd': 'password',
    }           
x7_pptp_static_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pptp',
    'pptp_ip': '60.7.8.9',
    'pptp_gateway': '60.7.8.1',
    'pptp_server': '9.9.9.9',
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_snmp': False,
    }
x7_pptp_dynamic_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pptp',
    'pptp_ip': 'dynamic',
    'mgmt_https': True,
    'mgmt_ssh': False,
    }
x7_l2tp_static_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'l2tp',
    'l2tp_server': '1.1.1.1',
    'l2tp_ip': '60.7.8.9',
    'l2tp_gateway': '60.7.8.1',
    'mgmt_https': False,
    'mgmt_snmp': True,
    }
x7_l2tp_dynmic_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'l2tp',
    'l2tp_server': '1.1.1.1',
    'l2tp_ip': 'dynamic',
    'mgmt_https': False,
    'mgmt_snmp': True,
    }
x7_wiremode = {
    'if': 'X7',
    'zone': 'WAN',
    'mode': 'wire_mode',
    'type': 'bypass', #bypass, inspect, secure
    'paired_interface': 'X10',
    'paired_interface_zone': 'WAN',
    'linkstate_propagation': True,
}
x7_tapmode = {
    'if': 'X7',
    'zone': 'WAN',
    'mode': 'tap_mode',
}

x8_static = {
    'if': 'X8',
    'zone': 'LAN', # LAN, DMZ, custom zone name
    'mode': 'static',
    'ip': '8.8.8.8',
    'gateway': '8.8.8.1',
    'routed_mode': 'any',#False,any,interface X1....
}
x3_dict = {
    'if': 'X3',
    'comment': 'transmodetest',
    'zone': 'LAN',
    'mode': 'transparent',
    'transparent_range': {'name': 'tc1aohost'},
    'gratuitous_arp_wan_forwarding': False,
    'gratuitous_arp_wan_generation': False,
    'mgmt_https': True,
    'mgmt_ping': True,
}
x8_l2bridge = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'l2bridge',
    'bridge_to': 'X2',
    'block_non_ip': False,
    'only_sniff': True,
    'route_on_bridge_pair': True,
    'stateful_inspection': True,
    'vlan_filtering_mode': 'allow',  #allow, block
    'no_filter_vlans': [1, 2, 4],
    'filter_vlans': [3, 5],
}
x8_wiremode = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'wire-mode',
    'type': 'inspect', #bypass, inspect, secure
    'wire_paired_interface': 'X9',
    'wire_paired_zone': 'WAN',
    'wire_link_propagation': True,
    'stateful_inspection': True,
    'restrict_analysis': True,
}
x8_tapmode = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'tap-mode',
}
x8_unnumbered = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'unnumbered',
    'ip': '8.8.8.8',
    'gateway': '8.8.8.1',
}
x8_portshield = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'portshield',
    'portshield_to': 'X3',
}
x8_native = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'nativebridge',
    'bridge_to': 'X1',
    'firewalling': True,
}
x9_wlan_static = {
    'if': 'X9',
    'zone': 'WLAN',
    'mode': 'static',
    'ip': '91.91.91.91',
    'netmask': '255.255.252.0',
    'gateway': '91.91.91.91',
    'sp_limit': 24,
    # 'sp_reserve_address': 'dynamic',
    'sp_reserve_address': '91.91.91.4',
}
x9_wlan_l2bridge = {
    'if': 'X9',
    'zone': 'WLAN',
    'mode': 'l2bridge',
    'bridge_to': 'X0',
    'block_non_ip': False,
    'only_sniff': True,
}
x2_wlan_portshield = {
    'if': 'X2',
    'zone': 'WLAN',# LAN, DMZ, custom zone name
    'mode': 'portshield',
    'portsheild_to': 'X9',
}
x9_wlan_native = {
    'if': 'X9',
    'zone': 'WLAN',# LAN, DMZ, custom zone name
    'mode': 'nativebridge',
    'bridge_to': 'X1',
    'firewalling': True,
}
# interface.config_interface(**x7_pppoe_static_dict)
# interface.config_interface(**x7_pppoe_dynamic_dict)
# interface.config_interface(**x7_pppoe_unnumbered_dict)
# interface.config_interface(**x7_static_dict)
# interface.config_interface(**x7_dhcp_dict)
# interface.config_interface(**x7_pptp_static_dict)
# interface.config_interface(**x7_pptp_dynamic_dict)
# interface.config_interface(**x7_l2tp_static_dict)
# interface.config_interface(**x7_l2tp_dynmic_dict)

###lan zone 
# interface.config_interface(**x8_static)
# interface.config_interface(**x8_l2bridge)
# interface.config_interface(**x8_unnumbered)
## interface.config_interface(**x8_portshield)
## interface.config_interface(**x8_native)
# interface.config_interface(**x8_tapmode)
# interface.config_interface(**x8_wiremode)
# interface.config_interface(**x9_wlan_static)
# interface.unassign_interface(interface='X8')


# interface.get_interface_status('X8')
###mgmt zone
mgmt_static = {
    'if': 'MGMT',
    'zone': 'MGMT',
    'ip': '8.8.8.8',
    'gateway': '8.8.8.1',
    ###optional
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_snmp': True,
    'user_https': True,
    'https_redirect':True,
    'bandwidth_management': True,
    'ibwm': True,
    'ibwm_amount':'380',
    'ebwm':False,
    'flow_reporting':True,
    'mtu':1480,
}

#interface.config_interface(**mgmt_static)

x9_vlan = {
    'if': 'x9',
    'type': 'vlan',
    'vlan_tag': 100,
    'zone': 'wan',
    'mode': 'static',
    'ip': '11.2.3.4',
    'gateway': '11.1.1.1',
}
x9_wlan_tunnel_static = {
    'type': 'wlan-tunnel',
    'tunnel-id': '0',
    'tunnel-if': 'x1',
    'mode': 'static',
    'zone': 'wlan', 
    'ip': '92.92.92.92',
    'netmask': '255.255.252.0',
    'gateway': '92.92.92.1',
    'sp-limit': 24,
    # 'sp-reserve-address': 'dynamic',
    'sp-reserve-address': 'manual',
    'sp-reserve-ip': '92.92.92.4',  
}
x9_wlan_tunnel_l2b = {
    'type': 'wlan-tunnel',
    'tunnel-id': '0',
    'tunnel-if': 'x9',
    'mode': 'l2bridge', 
    'zone': 'wlan', 
    'bridge-to': 'X0',
    'block-non-ip': False,
    'only-sniff': True, 
}
wlan_tunnel_del = {
    'type': 'wlan-tunnel',
    'tunnel-name': 'WT0',
}
vpn_tunnel = {
    'type': 'vpn_tunnel',
    'tunnel_name': 'test-vpn',
    'vpn_policy': '1.1.1.1',
    'ip': '3.4.5.4',
    'netmask': '255.255.255.0',
    'multicast': True,
    'flow_reporting': True,
    'asymmetric_route': True,
    'fragment_packets': True,
    'ignore_df_bit': True,
    'mgmt_ping': True,
    'user_https': True,
}
tunnel_4to6_dslite = {
    'type': '4to6',
    'zone': 'WAN',
    'tunnel_name': 'test-4to6',
    'tunnel_type': 'dslite', #dslite, gre4to6
    'bound_to': "X1", # or any
    'local_ipv6': '2000::1', # or dynamic
    'aftr_addr': 'www.aaa.com',
    # 'aftr-addr': 'ipv6 "2001::1"'
    # 'aftr-addr': 'dynamic',
    'local_ipv4': '192.0.0.2',
}
tunnel_4to6_gre4to6 = {
    'type': '4to6',
    'zone': 'WAN',
    'tunnel_name': 'test-4to6',
    'tunnel_type': 'gre4to6', #dslite, gre4to6
    'bound_to': "X1", # or any
    'local_ipv6': 'dynamic', # or ipv6 **::**
    'remote': '1::1',
    'ip_ipv4': '192.0.0.2',
    'netmask': '255.255.255.0'
}

# interface.add_interface(**x9_vlan)
# interface.add_interface(**vpn_tunnel)
# interface.del_interface(**vpn_tunnel)
# interface.add_interface(**tunnel_4to6_dslite)
# interface.add_interface(**tunnel_4to6_gre4to6)
# interface.del_interface(**tunnel_4to6_dslite)
# interface.del_interface(**tunnel_4to6_gre4to6)
# interface.get_vlan_interface_status(name='X9', vlan_id=100)
# interface.get_tunnel_interface_status(name='test-4to6', type='4to6')
# interface.get_tunnel_interface_status(name='test-vpn', type='vpn')


x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': '2001:111::10',
            'prefix_length': 64
        }
interface.config_interface_ipv6(**x1_opt)


interface_ipv6_auto = {
            'name': 'X1',
            'mode': 'auto',
        }
interface.config_interface_ipv6(**x1_opt)


# interface_ipv6_dhcpv6 = {
#      'name': 'x1',
#      'mode': 'dhcpv6',
#      #'comment': '',
#      'dhcpv6': {
#          'prefix_delegation': {}, # disable prefix_delegation
#          'rapid_commit': False,
#          'send_hints': False,
#          'mode': 'auto',  # manual
#          'aftr_name_option': False
#     }
#     }

# interface_ipv6_dhcpv6 = {
#      'name': 'x1',
#      'mode': 'dhcpv6',
#      #'comment': '',
#      'dhcpv6': {
#          'prefix_delegation': True,  # enable prefix_delegation
#          "preferred_delegated_prefix" :True,  # enable preferred_delegated_prefix only when prefix_delegation is enabled
#          'rapid_commit': False,
#          'send_hints': False,
#          'mode': 'auto',  # manual
#          'aftr_name_option': False
#     }
#     }

interface_ipv6_dhcpv6 = {
     'name': 'x1',
     'mode': 'dhcpv6',
     #'comment': '',
     'dhcpv6': {
         'prefix_delegation': True,  # enable prefix_delegation
         "preferred_delegated_prefix":True,  # enable preferred_delegated_prefix only when prefix_delegation is enabled
         'preferred_delegated_prefix_addr': '11::11', # enable preferred_delegated_prefix_addr only when preferred_delegated_prefix is enabled
         'preferred_delegated_prefix_prefix': '64', # enable preferred_delegated_prefix_prefix only when preferred_delegated_prefix is enabled
         'rapid_commit': False,
         'send_hints': False,
         'mode': 'manual',  # auto or manual
         'info_only': True,  # only can be set when mode is manual
         'aftr_name_option': False
    }
    }

interface_ipv6_dmz = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '3.3.3.3',
            'mask': '255.255.255.0',
        }
interface_v4.config_interface(**interface_ipv6_dmz)

interface_ipv6_x0 = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': '2000:2222::1',
            'prefix_length': 80,
        }
interface.config_interface_ipv6(**x0_opt)


unassignX1_ipv6(self):
#         out = interface.unassign_ipv6_interface(interface='X1')
#         Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")

interface_ipv6_pppoe6_auto={
    'name': 'x1',
    'mode': 'pppoe6',
    'pppoe6': {
        'mode_assign':'auto',
        'inactivity': 5,
        'lcp_echo_packets': False,
        'ncp_neg_retrans': 5,
        'reconnect': 5,
    }
}
interface_ipv6_pppoe6_dhcp={
    'name': 'x1',
    'mode': 'pppoe6',
    'pppoe6': {
        'mode_assign':'dhcpv6',
        'prefix_delegation': True,
        'rapid_commit': False,
        'inactivity': 5,
        'lcp_echo_packets': False,
        'ncp_neg_retrans': 5,
        'reconnect': 5,
    }
}
interface_ipv6_pppoe6_static={
    'name': 'x1',
    'mode': 'pppoe6',
    'pppoe6': {
        'mode_assign':'static',
        'ip':'100::100',
        'gateway':'100::1',
        'dns1':'1::1',
        'dns2':'2::1',
        'dns3':'3::1',
        'inactivity': 5,
        'lcp_echo_packets': False,
        'ncp_neg_retrans': 5,
        'reconnect': 5,
        'prefix_length':64,
        'router_advertisement': {
            "enable": False,
            "interval_min": 200,
            "interval_max": 600,
            "link_mtu": 10,
            "reachable_time": 20,
            "retransmit_timer": 30,
            "current_hop_limit": 64,
            "router_lifetime": 1800,
            "router_preference": "medium",
            "managed": False,
            "other_config": False
        }
    }
}            
InterfaceIPv6 = InterfaceIPv6Api(fw)

#rc = InterfaceIPv6.config_interface_ipv6(**interface_ipv6_pppoe6_auto)
#rc = InterfaceIPv6.config_interface_ipv6(**interface_ipv6_pppoe6_dhcp)
#rc = InterfaceIPv6.config_interface_ipv6(**interface_ipv6_pppoe6_static)

zone_obj = ZoneObjectsApi(fw)
zonejson = {
    "zones": [
        {
            "name": "custom_zone",
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

zonejson_1 = {
    "zones": [
        {
            "name": "custom_zone",
            "security_type": "trusted",
            "interface_trust": True,
            "auto_generate_access_rules": {
                "allow_from_to_equal": True,
                "allow_from_higher": True,
                "allow_to_lower": True,
                "deny_from_lower": True
            },
            "gateway_anti_virus": True,
            "intrusion_prevention": True,
            "anti_spyware": True,
            "app_control": True,
            "dpi_ssl_client": True,
            "dpi_ssl_server": False,
            "create_group_vpn": False,
            "ssl_control": False,
            "sslvpn_access": False,
            "guest_services": {
                "enable": False,
                "inter_guest": False,
                "external_auth": {
                    "enable": False,
                    "client_redirect": "https",
                    "web_server_1": {},
                    "web_server_2": {},
                    "web_server": {
                        "timeout": 15
                    },
                    "message_auth": {
                        "method": "md5",
                        "shared_secret": "6,4b37f142e03bc979948b1d9886650d198c78d10b2ea51cbb7ceeee86666994b82504ac707d14597b0701620fd5fd72bcfdf9a201f3aac9b86d2aafceaee9c3a964bff11dff72f6c4633612e696cf4bd50db34058bb53029d76addfe49a32e084a528ab7e482b00470f826e9430d8a1e2989491ffb6c3b7acb21dbddd473afe0face7ed7a08a1a6f53e4a90880f17138379f8dda0f621c07ac9601c3cb4b89751",
                        "confirm_secret": "6,4b37f142e03bc979948b1d9886650d198c78d10b2ea51cbb7ceeee86666994b82504ac707d14597b0701620fd5fd72bcfdf9a201f3aac9b86d2aafceaee9c3a964bff11dff72f6c4633612e696cf4bd50db34058bb53029d76addfe49a32e084a528ab7e482b00470f826e9430d8a1e2989491ffb6c3b7acb21dbddd473afe0face7ed7a08a1a6f53e4a90880f17138379f8dda0f621c07ac9601c3cb4b89751"
                    },
                    "social_network": {
                        "enable": False,
                        "facebook": False,
                        "google": False,
                        "twitter": False
                    },
                    "auth_pages": {
                        "web_server_1": {
                            "login": "",
                            "expiration": "",
                            "timeout": "",
                            "max_sessions": "",
                            "traffic_exceeded": ""
                        },
                        "web_server_2": {
                            "login": "",
                            "expiration": "",
                            "timeout": "",
                            "max_sessions": "",
                            "traffic_exceeded": ""
                        }
                    },
                    "web_content": {
                        "redirect": {
                            "use_default": True
                        },
                        "server_down": {
                            "use_default": True
                        }
                    },
                    "logout_expired": {
                        "every": 1,
                        "cgi": {
                            "web_server_1": "",
                            "web_server_2": ""
                        },
                        "enable": False
                    },
                    "status_check": {
                        "every": 5,
                        "cgi": {
                            "web_server_1": "",
                            "web_server_2": ""
                        },
                        "enable": False
                    },
                    "session_sync": {
                        "every": 10,
                        "cgi": {
                            "web_server_1": "",
                            "web_server_2": ""
                        },
                        "enable": False
                    }
                },
                "policy_page_non_authentication": {
                    "enable": False,
                    "guest_usage_policy": "",
                    "idle_timeout": {},
                    "auto_accept": False
                },
                "captive_portal_authentication": {
                    "enable": False,
                    "internal_url": "",
                    "external_url": "",
                    "welcome_url_source": "from-radius",
                    "welcome_url": "",
                    "session_timeout_source": "from-radius",
                    "session_timeout": {},
                    "idle_timeout_source": "from-radius",
                    "idle_timeout": {},
                    "method": "chap"
                },
                "custom_auth_page": {
                    "enable": False,
                    "footer": {},
                    "header": {}
                },
                "post_auth": "",
                "bypass_guest_auth": {},
                "smtp_redirect": {},
                "deny_networks": {},
                "pass_networks": {},
                "max_guests": 10
            }
        }
    ]
}



zonejson_edit = {
    "zones": [
        {
            "name": "custom_zone",
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
# zoneobj.add_zone_object(**zonejson)
# zoneobj.show_zone_object()
# zoneobj.show_zone_object(name = 'custom_zone')
# zoneobj.edit_zone_object(name = 'custom_zone',**zonejson_edit)
zoneobj.delete_zone_object(name = 'custom_zone')

dhcp_server = DHCPServerApi(fw)
dhcp_server_setting_v4 = {
    "dhcp_server":{
        "ipv4":{
            "enable": True,
        }
    }
}
dhcp_server.config_dhcp_server_settings(**dhcp_server_setting_v4)

nat_policy = NatpolicyApi(fw)
#output = nat_policy.get_nat_policy()

natpolicy_dict = {
    "nat_policies":[
        {
            "ipv4":{
                "name": "test",
                "enable": True,
                "comment": "test",
                "inbound": "X2",
                "outbound": "X1",
                "source": {
                    "any": True
                },
                "translated_source": {
                    "name": "X2 IP"
                },
                "destination": {
                    "any": True
                },
                "translated_destination": {
                    "original": True
                },
                "service": {
                    "group": "Ping"
                },
                "translated_service": {
                    "original": True
                },
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
                #"source_port_remap": True  ###this option can be enabled only when "translated source" is not Original
            }
        }
    ]
}
#output = nat_policy.add_nat_policy(**natpolicy_dict)
output = nat_policy.del_nat_policy("test")
print("*******************")
print(output)
print("*******************")


# from lib.modules.API.network import ServiceGroupApi
# ip = '192.168.168.168'
# fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
# service_group_obj = ServiceGroupApi(fw)
# service_group = {
#     "name": "http_https3",
#     "service_object": [
#         {
#             "name": "HTTPS"
#         },
#         {
#             "name": "HTTP"
#         }
#     ]
# }
# (rc,uuid) = service_group_obj.config_service_group(**service_group)
# # print("sophie service group uuid" + uuid)
# print(rc)

# from lib.modules.API.network import ServiceObjectApi
# ip = '192.168.168.168'
# fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
# serviceobject = ServiceObjectApi(fw)
# service_object_tcp = {"object_type": "tcp",
#                       "name": "http_test",
#                       "tcp": {
#                           "begin": 8000,
#                           "end": 8000
#                       }
#                       }
# name, rc = serviceobject.config_service_object(**service_object_tcp)

'''
dnsproxy_api=DnsProxyApi(fw)
dns_setting = {
    'enable': True,# True or False
    'mode': 'ipv4-to-ipv4', # ipv4-to-ipv4,ipv4-to-ipv6
    "dns_cache": False,
    'protocol': 'udp-only',
    'enforce_all_dns_requests': False,
    }
rc = dnsproxy_api.config_dnsproxy(**dns_setting)
entry = {
    'domain': 'www.baidu.com',
    'ipv4_primary': '1.1.1.1',
    'ipv4_secondary': '1.1.1.2',
    'ipv6_primary': '1::1',
    'ipv6_secondary': '1::2',
}
rc = dnsproxy_api.add_dns_proxy_entry(**entry)
rc =dnsproxy_api.show_dns_proxy_entry(domain='www.baidu.com')
rc = dnsproxy_apidelete_dns_proxy_entry(domain='www.baidu.com')
rc =dnsproxy_api.show_dns_proxy_caches()
rc =dnsproxy_api.flush_caches('ipv4') 
rc =dnsproxy_api.flush_caches('ipv6') 
'''

'''
split_dns_api = DnsSettingsApi(fw)
split_dns_dict = {
    'domain': '*.baidu.com',
    'ipv4': {
        'primary': '8.8.8.8',
    },
    'ipv6': {
        'primary': '1::1',
    },
    'local_interface': 'X1',
}
rc = split_dns_api.add_split_dns(**split_dns_dict)
rc = split_dns_api.ecit_split_dns(**split_dns_dict)
rc = split_dns_api.delete_split_dns(domain='*.baidu.com')
rc =  split_dns_api.show_dns_proxy_entry(domain='*.baidu.com')
'''
from modules.API.network import ArPApi

arpApi = ArPApi(fw)
output = arpApi.show_arp_caches()
static_arp = {
    'ip': '1.1.1.1',
    'mac': '22:22:33:44:55:66',
    'interface': 'X2',
    'publish': False,
    'bind_mac': False,
}
'''
output = arpApi.add_static_arp(**static_arp)
output = arpApi.show_static_arp_entries()
edit_arp = {
    'raw_ip': Parameter.DMZ_HOST,
    'raw_mac': '222233445566',
    'raw_interface': 'X2',
    'raw_publish': False,
    'raw_bind_mac': False,
    'ip': Parameter.DMZ_HOST,
    'mac': Parameter.DMZ_HOST_MAC,
    'interface': 'X2',
    'publish': False,
    'bind_mac': False,
}
output = arpApi.edit_static_arp(**edit_arp)
del_static = {
    'ip': Parameter.DMZ_HOST,
    'mac': Parameter.DMZ_HOST_MAC,
    'interface': 'X2',
    'publish': False,
    'bind_mac': False,
}
output = arpApi.del_static_arp(**del_static)
'''

'''
ndpApi = NeighborDiscoveryApi(fw)
entry={
    'ip': '1::1',
    'mac':'11:22:33:44:55:66',
    'interface':'X0',
}
entry_edit={
    'ip_old': '1::1',
    'mac_old':'11:22:33:44:55:66',
    'interface_old':'X0',
    'ip': '1::2',
    'mac':'11:22:33:44:55:67',
    'interface':'X1',
}
ndpApi.add_static_entry(**entry)
ndpApi.edit_static_entry(**entry_edit)
ndpApi.delete_static_entry(**entry)
ndpApi.show_static_entry()
ndpApi.show_NDP_cache()

'''
'''
ddnsApi = DDNSApi(fw)
profile_v4 = {
        'version':'ipv4', # ipv4,ipv6
        'profile_name': 'test',
        'enable': True,
        'use_online': True,
        'provider': 'dyn',#dyn,changeip,noip
        'user_name':'aaa',
        'password':'bbb',
        'domain':'ccc',
        'service_type':'dynamic',
        'bound_to': {'interface':'X1'},#
        'online_settings':{'detect':True},#detect:true,set_to_wan:true,manual:1.1.1.1
        'offline_settings':{'do_nothing': True}#do_nothing:true,use_previous:true,make_host_unknown:true,manual:1.1.1.1
    }
ddnsApi.add_ddns_profile(**profile_v4)
profile_v4_edit = {
        'version':'ipv4', # ipv4,ipv6
        'profile_name': 'test',
        'enable': True,
        'use_online': True,
        'provider': 'dyn',#dyn,changeip,noip
        'user_name':'aaa',
        'password':'bbb',
        'domain':'ccc',
        'service_type':'dynamic',
        'bound_to': {'interface':'X2'},#
        'online_settings':{'set_to_wan':True},#detect:true,set_to_wan:true,manual:1.1.1.1
        'offline_settings':{'do_nothing': True}#do_nothing:true,use_previous:true,make_host_unknown:true,manual:1.1.1.1
    }
ddnsApi.edit_ddns_profile(**profile_v4_edit)
ddnsApi.show_ddns_profile(version='ipv4', name='test')
ddnsApi.delete_ddns_profile(version='ipv4', name='test')
'''
'''
dns_securityApi= DNSSecurityApi(fw)
dns_securityApi.disable_dns_sinkhole()
dns_s1={
    'action':'dropping_with_dns_reply_of_forged_ip',#dropping_with_logs,dropping_with_negative_dns_reply_to_source or dropping_with_dns_reply_of_forged_ip
    'ipv4':'1.1.1.1',
    'ipv6':'1::1'
}
dns_securityApi.enable_dns_sinkhole(**dns_s1)
dns_securityApi.show_dns_sinkhole()
dns_securityApi.add_dns_custom_list(domain='www.aaa.com')
dns_securityApi.add_dns_custom_list(domain='www.bbb.com')
dns_securityApi.show_dns_custom_list()
dns_securityApi.delete_dns_custom_list(domains=['www.aaa.com','www.bbb.com'])
dns_securityApi.add_dns_white_list(domain='www.aaa.com')
dns_securityApi.add_dns_white_list(domain='www.bbb.com')
dns_securityApi.show_dns_white_list()
dns_securityApi.delete_dns_white_list(domains=['www.aaa.com','www.bbb.com'])
dns_securityApi.set_dns_tunnel(enable=True, block=True)
dns_securityApi.show_detected_client()
dns_securityApi.add_dns_tunnel_white_list(ip='1.1.1.1')
dns_securityApi.add_dns_tunnel_white_list(domain='2.2.2.2')
dns_securityApi.show_dns_tunnel_white_list()
dns_securityApi.delete_tunnel_dns_white_list(ips=['1.1.1.1','2.2.2.2'])
'''


wlb_conf_dict = {
    "failover_lb": {
        "group": [
            {
                "final_backup": "",
                "interface": [
                    {
                        "name": "X1",
                        "probe_condition": "always",
                        "probe_type": "physical",
                        "rank": 1
                    },
                    {
                        "default_target": {
                            "value": "204.212.170.23"
                        },
                        "main_target": {
                            "host": "responder.global.sonicwall.com",
                            "protocol": {
                                "tcp": {
                                    "value": 50000
                                }
                            }
                        },
                        "name": "X2",
                        "probe_condition": "main",
                        "probe_type": "logical",
                        "rank": 2
                    },
                    {}
                ],
                "name": " Default LB Group",
                "preempt": True,
                "probing": {
                    "global_responder": False,
                    "health_check": 5,
                    "missed_intervals": 3,
                    "successful_intervals": 3
                },
                "type": "basic"
            }
        ]
    }
}

failoverapi = FailoverLbApi(fw)
failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)



vlan_trans_json = {
    'ingress_interface':'X2',
    'ingress_vlan':1,
    'egress_interface':'X4',
    'egress_vlan':3,
    'reverse':False
}
vlan_trans_edit_json={
    'ingress_interface':'X5',
    'ingress_vlan':3,
    'old_ingress_interface':'X2',
    'old_ingress_vlan':1,
    'old_egress_interface':'X4',
    'old_egress_vlan':3,
}
vlan_trans_del_json = {"vlan_translations":[
    {
        "ingress":{
            "interface":"X2",
            "vlan":2
            },
        "egress":{
            "interface":"X4",
            "vlan":4
            },
        "reverse":True
    },
    {
        "ingress":{
            "interface":"X4",
            "vlan":4
            },
        "egress":{
            "interface":"X2",
            "vlan":2
            },
        "reverse":True
    }]}
vlan_translation_api = VLANTranslationApi(fw)
vlan_translation_api.add_vlan_translation(**vlan_trans_json)
vlan_translation_api.del_vlan_translation(**vlan_trans_json)
vlan_translation_api.edit_vlan_translation(**vlan_trans_edit_json)
vlan_translation_api.del_multiple_vlan_translation(**vlan_trans_del_json)


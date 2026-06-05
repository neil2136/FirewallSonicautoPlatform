import sys
import os
#sys.path.append(os.environ["SONICOS_HOME"]+'/6.5.4/python_lib')
sys.path.append('/home/python_lib')

import modules.CLI.network
from utm import Firewall

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
# ip = '192.168.168.168'
# port = '2033'
# fw = FirewallCLI(ip, user='admin', password='password', supported_config_mode='cli-ssh')
# ip = '10.6.0.43'
# fw = Firewall(ip, user='admin', password='password', port=port, supported_config_mode='cli-console')
'''
webproxy_dict = { 
    'server':'1.1.1.1',
    'port':'3128',
    'bypass-upon-failure': True,
    'forward-public-requests': True
    }
webproxy = modules.CLI.network.WebproxyCli(fw)
output1 = webproxy.show_webproxy()
output2 = webproxy.add_user_proxy_server('1.1.1.2', '1.1.1.3')
output3 = webproxy.config_webproxy(**webproxy_dict)
'''

from modules.CLI.network import InterfaceCli
ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
interface = InterfaceCli(fw)
x7_static_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'static',
    'ip': '66.7.8.9',
    'netmask': '255.255.255.0',
    'gateway': '66.7.8.99',
    'mgmt-https': True,
    'mgmt-ssh': True,
    'mgmt-snmp': True,
    'user_https': True,
    'dns1': '1.1.1.1',
    'dns2': '2.2.2.2',
    'dns3': '3.3.3.3',
    'link-speed':'1000-full',#100-full,100-half,10-full,10-half,auto
    'port': 'aggregation',#None, aggregation, redundancy
    'port-aggregation': 'X10',
    }
x7_dhcp_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'dhcp',
    'force-discover-interval': '9',# or False
    'initiate-renewals-with-discover': True,
    'mgmt-https': True,
    'mgmt-ssh': True,
    'mgmt-snmp': True,
    }

x7_pppoe_dynamic_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe-ip': 'dynamic',
    'pppoe-user': 'abc',
    'pppoe-servicename': 'def',
    'pppoe-passwd': 'password',
    'pppoe-lcp-echo-packets': True,
    'pppoe-inactivity': 10, #or False
    'pppoe-reconnect' : 5, # or False
#    'pppoe-schedule': 'always-on', 
#    'pppoe-schedule': 'name "Work Hours"',
    'pppoe-schedule': 'M-T-W-TH-F 08:00 to 17:00',
    'mgmt-https': True,
    'mgmt-ssh': True,
    'mgmt-snmp': False,
    }   
x7_pppoe_static_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe-ip': '7.7.7.7',
    'pppoe-user': 'abc',
    'pppoe-servicename': 'def',
    'pppoe-passwd': 'password',
    'pppoe-lcp-echo-packets': True,
    'pppoe-inactivity': 10,
    'pppoe-reconnect' : False,
    'mgmt-https': True,
    'mgmt-ssh': True,
    'mgmt-snmp': True,
    }
x7_pppoe_unnumbered_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pppoe',
    'unnumbered': 'X3',
    'pppoe-user': 'abc',
    'pppoe-servicename': 'def',
    'pppoe-passwd': 'password',
    }           
x7_pptp_static_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pptp',
    'pptp-ip': '60.7.8.9',
    'pptp-gateway': '60.7.8.1',
    'pptp-server': '9.9.9.9',
    'mgmt-https': True,
    'mgmt-ssh': False,
    'mgmt-snmp': False,
    }
x7_pptp_dynamic_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'pptp',
    'pptp-ip': 'dynamic',
    'pptp-server': '9.9.9.9',
    'mgmt-https': True,
    'mgmt-ssh': False,
    }
x7_l2tp_static_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'l2tp',
    'l2tp-server': '1.1.1.1',
    'l2tp-ip': '60.7.8.9',
    'l2tp-gateway': '60.7.8.1',
    'mgmt-https': False,
    'mgmt-snmp': True,
    }
x7_l2tp_dynmic_dict = {
    'if': 'x7',
    'zone': 'WAN',
    'mode': 'l2tp',
    'l2tp-server': '1.1.1.1',
    'l2tp-ip': 'dynamic',
    'mgmt-https': False,
    'mgmt-snmp': True,
    }
x7_wiremode = {
    'if': 'X7',
    'zone': 'WAN',
    'mode': 'wire-mode',
    'type': 'bypass', #bypass, inspect, secure
    'paired-interface': 'X10',
    'paired-interface-zone': 'WAN',
    'linkstate-propagation': True,
}
x7_tapmode = {
    'if': 'X7',
    'zone': 'WAN',
    'mode': 'tap-mode',
}

x8_static = {
    'if': 'X8',
    'zone': 'LAN', # LAN, DMZ, custom zone name
    'mode': 'static',
    'ip': '8.8.8.8',
    'gateway': '8.8.8.1',
    'routed-mode': 'any',#False,any,interface X1....
}
x8_transparent = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'transparent',
    'gratuitous-arp-wan-forwarding': True,
    'gratuitous-arp-wan-generation': False, 
    'transparent-range': 'group "WAN Subnets"',   
}
x8_l2bridge = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'l2bridge',
    'bridge-to': 'X2',
    'block-non-ip': False,
    'only-sniff': True,
    'route-on-bridge-pair': True,
    'stateful-inspection': True,
    'vlan-filtering-mode': 'allow',  #allow, block
    'no-filter-vlans': [1, 2, 4],
    'filter-vlans': [3, 5],
}
x8_wiremode = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'wire-mode',
    'type': 'inspect', #bypass, inspect, secure
    'paired-interface': 'X9',
    'paired-interface-zone': 'WAN',
    'linkstate-propagation': True,
    'stateful-inspection': True,
    'restrict-analysis': True,
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
    'portsheild-to': 'X3',
}
x8_native = {
    'if': 'X8',
    'zone': 'LAN',# LAN, DMZ, custom zone name
    'mode': 'nativebridge',
    'bridge-to': 'X1',
    'firewalling': True,
}
x9_wlan_static = {
    'if': 'X9',
    'zone': 'WLAN',
    'mode': 'static',
    'ip': '91.91.91.91',
    'netmask': '255.255.252.0',
    'gateway': '91.91.91.91',
    'sp-limit': 24,
    # 'sp-reserve-address': 'dynamic',
    'sp-reserve-address': 'manual',
    'sp-reserve-ip': '91.91.91.4',    
}
x9_wlan_l2bridge = {
    'if': 'X9',
    'zone': 'WLAN',
    'mode': 'l2bridge',
    'bridge-to': 'X0',
    'block-non-ip': False,
    'only-sniff': True,
}
x2_wlan_portshield = {
    'if': 'X2',
    'zone': 'WLAN',# LAN, DMZ, custom zone name
    'mode': 'portshield',
    'portsheild-to': 'X9',
}
x9_wlan_native = {
    'if': 'X9',
    'zone': 'WLAN',# LAN, DMZ, custom zone name
    'mode': 'nativebridge',
    'bridge-to': 'X1',
    'firewalling': True,
}
# interface.config_interface(**x7_pppoe_static_dict)
# interface.config_interface(**x7_static_dict)
# interface.config_interface(**x7_dhcp_dict)
# interface.config_interface(**x7_pppoe_dynamic_dict)
# interface.config_interface(**x7_pppoe_unnumbered_dict)
# interface.config_interface(**x7_pptp_static_dict)
# interface.config_interface(**x7_pptp_dynamic_dict)
# interface.config_interface(**x7_l2tp_static_dict)
# interface.config_interface(**x7_l2tp_dynmic_dict)
# interface.config_interface(**x7_wiremode)
# interface.config_interface(**x7_tapmode)
# interface.config_interface(**x8_static)
# interface.config_interface(**x8_transparent)
# interface.config_interface(**x8_l2bridge)
# interface.config_interface(**x8_wiremode)
# interface.config_interface(**x8_unnumbered)
# interface.config_interface(**x8_portshield)
# interface.config_interface(**x87_tapmode)
# interface.show_interface_status('X7')
# interface.config_interface(**x8_native)
# interface.config_interface(**x9_wlan_static)
# interface.config_interface(**x9_wlan_l2bridge)
# interface.config_interface(**x2_wlan_portshield)
# interface.config_interface(**x9_wlan_native)
# interface.unassign_interface('X8')
# interface.show_interface_status(interface='X0', version='ipv4')
# interface.show_interface_status(interface='X0', version='ipv6')

x9_vlan = {
    'if': 'x9',
    'type': 'vlan',
    'vlan-tag': 100,
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
    'type': 'vpn-tunnel',
    'tunnel-name': 'test-vpn',
    'vpn-policy': '1.1.1.1',
    'ip': '3.4.5.4',
    'netmask': '255.255.255.0',
    'multicast': True,
    'flow-reporting': True,
    'asymmetric-route': True,
    'fragment-packets': True,
    'ignore-df-bit': True,
    'mgmt-ping': True,
    'user-https': True,
}
tunnel_4to6_dslite = {
    'type': '4to6',
    'zone': 'WAN',
    'tunnel-name': 'test-4to6',
    'tunnel-type': 'dslite', #dslite, gre4to6
    'bound-to': 'interface "X1"', # or any
    'local-ipv6': 'ipv6 "2000::1"', # or dynamic
    'aftr-addr': 'fqdn "www.aaa.com"',
    # 'aftr-addr': 'ipv6 "2001::1"'
    # 'aftr-addr': 'dynamic',
    'local-ipv4': '192.0.0.2',
}
tunnel_4to6_gre4to6 = {
    'type': '4to6',
    'zone': 'WAN',
    'tunnel-name': 'test-4to6',
    'tunnel-type': 'gre4to6', #dslite, gre4to6
    'bound-to': 'interface "X1"', # or any
    'local-ipv6': 'dynamic', # or ipv6 **::**
    'remote': '1::1',
    'ip-ipv4': '192.0.0.2',
}
# interface.add_interface(**x9_vlan)
# interface.add_interface(**x9_wlan_tunnel_static)
# interface.add_interface(**x9_wlan_tunnel_l2b)
# interface.del_interface(**wlan_tunnel_del)
# interface.del_interface(**x9_vlan)
# interface.add_interface(**vpn_tunnel)
# interface.del_interface(**vpn_tunnel)
# interface.add_interface(**tunnel_4to6_dslite)
# interface.del_interface(**tunnel_4to6_dslite)
# interface.add_interface(**tunnel_4to6_gre4to6)
# interface.del_interface(**tunnel_4to6_gre4to6)
# interface.show_interface_status(interface='WT0')
# interface.show_tunnel_status(type='vpn', name='test-vpn')
# interface.show_tunnel_status(type='vpn')
# interface.show_tunnel_status(type='4to6', name='test-4to6')
# interface.show_tunnel_status(type='4to6')
#####ipv6 part#####
x1_ipv6_static = {
    'if': 'X1',
    'mode': 'static',
    'zone': 'WAN',
    'ip': '1::1',
    'gateway': '1::2',
    'dns1': '2::2',
    'prefix-length': 64,
    'subnet-prefix': True,
    'mgmt-ping': True,
    'user-https': True,
    ####router advertisement tab####
    'router-advertisement': True,
    'interval-min': 100,
    'interval-max': 200,
    'link-mtu': '1300',
    'reachable-time': '100',
    'retransmit-timer': '0',
    'current-hop-limit': 64,
    'router-lifetime': 2000,
    'router-preference': 'Medium', #High, Low, Medium
    'managed': True,
    'other-config': True,
    # 'add_prefix': ['2001::', '2003::'],
    # '2001::': {
    #     'autonomous': True,
    #     'on-link': True,
    #     'valid-lifetime': 40000,
    #     'preferred': 20000,
    # },
    # '2003::': {},
    # 'del_prefix': ['2001::', '2004::'],
    ########advance tab#####
    'ipv6-traffic': True,
    'listen-router-advertisement': True,
    'stateless-address-autoconfig': True,
    'duplicate-address-detection-transmits': 1,
    'ndp-reachable-time': 50,
    'ndp-size': 100, #or False
    # 'add_address': ['7::8', '9::10', 'A::B'],
    # '7::8': {
    #     'type': 'static',
    #     'ip': '7::8',
    #     'prefix-length': '64',
    # },
    # '9::10': {
    #     'type': 'prefix-delegation',
    #     'delegated-prefix': 'X2 Delegated Prefix',
    #     'ip': '7::8',
    #     'prefix-length': '64',        
    # },
    # 'A::B': {
    #     'type': '6rd',
    #     'ip': 'A::B',
    #     'prefix-length': '64',         
    # },
    # 'del_address': ['C::D'],
    'advertise': True,
}
x1_ipv6_auto = {
    'if': 'X1',
    'mode': 'auto',
    'zone': 'WAN',
    'ipv6-traffic': True,
    'duplicate-address-detection-transmits': 1,
    'ndp-reachable-time': 50,
    'ndp-size': 100, #or False
}  
x1_dhcpv6 = {
    'if': 'X1',
    'mode': 'dhcpv6',
    'zone': 'WAN', 
    'prefix-delegation': True,
    'preferred-delegation-prefix': '2000:: 64',
    'preferred-send-hints': True,
    'rapid-commit': True,
    'send-hints': True,
    'dhcpv6-mode': 'manual', #auto, manual
    'info-only': True, 
    'ipv6-traffic': True,
    'duplicate-address-detection-transmits': 1,
    'ndp-reachable-time': 50,
    'aftr-name-option': True,
    'ndp-size': 100, #or False
} 
x3_pppoev6_static = {
    'if': 'X3',
    'mode': 'pppoe6',
    'zone': 'WAN',
#    'pppoe-schedule': 'always-on', 
#    'pppoe-schedule': 'name "Work Hours"',
    'pppoe-schedule': 'M-T-W-TH-F 08:00 to 17:00',
    'mode-assignment': 'static', 
    'ip': '1::1',
    'gateway': '1::2',
    'prefix-length': 64,
    'subnet-prefix': True,
    'mgmt-ping': True,
    'user-https': True,
    ####router advertisement tab####
    'router-advertisement': True,
    'interval-min': 100,
    'interval-max': 200,
    'link-mtu': '1300',
    'reachable-time': '100',
    'retransmit-timer': '0',
    'current-hop-limit': 64,
    'router-lifetime': 2000,
    'router-preference': 'Medium', #High, Low, Medium
    'managed': True,
    'other-config': True,        
}
x3_pppoev6_auto = {
    'if': 'X3',
    'mode': 'pppoe6',
    'zone': 'WAN',
    'pppoe-schedule': 'always-on', 
#    'pppoe-schedule': 'name "Work Hours"',
    'mode-assignment': 'auto',
}
x3_pppoev6_dhcpv6 = {
    'if': 'X3',
    'mode': 'pppoe6',
    'zone': 'WAN',
    'pppoe-schedule': 'always-on',
    'mode-assignment': 'dhcpv6',
    'prefix-delegation': True,
    'preferred-delegation-prefix': '2000:: 64',
    'preferred-send-hints': True,
    'rapid-commit': True,
    'send-hints': True,
    'dhcpv6-mode': 'manual', #auto, manual
    'info-only': True, 
    'ipv6-traffic': True,
    'duplicate-address-detection-transmits': 1,
    'ndp-reachable-time': 50,
    'ndp-size': 100, #or False
}
x0_ipv6_static = {
    'if': 'X0',
    'mode': 'static',
    'zone': 'LAN',
    'ip': '11::1',
    'prefix-length': 64,
    'subnet-prefix': True,
    'mgmt-ping': True,
    'user-https': True,
    ####router advertisement tab####
    'router-advertisement': True,
    'interval-min': 100,
    'interval-max': 200,
    'link-mtu': '1300',
    'reachable-time': '100',
    'retransmit-timer': '0',
    'current-hop-limit': 64,
    'router-lifetime': 2000,
    'router-preference': 'Medium', #High, Low, Medium
    'managed': True,
    'other-config': True,
    'add_prefix': ['2001::', '2003::'],
    '2001::': {
        'autonomous': True,
        'on-link': True,
        'valid-lifetime': 40000,
        'preferred': 20000,
    },
    '2003::': {},
    'del_prefix': ['2001::', '2004::'],
    ########advance tab#####
    'ipv6-traffic': True,
    'listen-router-advertisement': True,
    'stateless-address-autoconfig': True,
    'duplicate-address-detection-transmits': 1,
    'ndp-reachable-time': 50,
    'ndp-size': 100, #or False
    'add_address': ['7::8', '9::10', 'A::B'],
    '7::8': {
        'type': 'static',
        'ip': '7::8',
        'prefix-length': '64',
    },
    '9::10': {
        'type': 'prefix-delegation',
        'delegated-prefix': 'X2 Delegated Prefix',
        'ip': '7::8',
        'prefix-length': '64',        
    },
    'A::B': {
        'type': '6rd',
        'ip': 'A::B',
        'prefix-length': '64',         
    },
    'del_address': ['C::D'],
    'advertise': True,
}
x0_dhcpv6 = {
    'if': 'X0',
    'mode': 'dhcpv6',
    'zone': 'LAN', 
    'prefix-delegation': True,
    'preferred-delegation-prefix': '2000:: 64',
    'preferred-send-hints': True,
    'rapid-commit': True,
    'send-hints': True,
    'dhcpv6-mode': 'manual', #auto, manual
    'info-only': True, 
    'ipv6-traffic': True,
    'duplicate-address-detection-transmits': 1,
    'ndp-reachable-time': 50,
    'aftr-name-option': True,
    'ndp-size': 100, #or False
} 
# interface.config_interface_ipv6(**x1_ipv6_static)
# interface.config_interface_ipv6(**x1_ipv6_auto)
# interface.config_interface_ipv6(**x1_dhcpv6)
# interface.config_interface_ipv6(**x3_pppoev6_static)
# interface.config_interface_ipv6(**x3_pppoev6_auto)
# interface.config_interface_ipv6(**x3_pppoev6_dhcpv6)
# interface.config_interface_ipv6(**x0_ipv6_static)
# interface.config_interface_ipv6(**x0_dhcpv6)
tunnel_manual = {
    'type': 'manual',
    'zone': 'WAN',
    'name': 'test-manual',
    'bound-to': 'interface "X1"',# or any
    'ip': '88::88',
    'prefix-length': '64',
    'remote-ipv4': '10.10.10.10',
    'remote-ipv6': 'group "DMZ IPv6 Subnets"',
    'mgmt-ping': True,
    'user-https': True,
}
tunnel_6rd = {
    'type': '6rd',
    'zone': 'WAN',
    'name': 'test-6rd',
    'bound-to': 'interface "X1"',# or any
    'ip': '88::88',
    'prefix-length': '64',
    'mode': 'manual', # dynamic, manual
    '6rd-prefix': '888::',
    '6rd-prefix-length': 64,
    'border-relay-ipv4-address': '1.2.3.4',
    'mask-length': 24,
    'default_route': True,
    'link-mtu': 1280,
}
tunnel_6rd_edit = {
    'name': 'test-6rd',
    'name-new': 'test-6rd-edit',
    'type': '6rd',
    'ip': '88::89',
}
tunnel_gre = {
    'type': 'gre',
    'zone': 'WAN',
    'name': 'test-gre',
    'bound-to': 'interface "X1"',# or any
    'ip': '88::88',
    'prefix-length': '64',
    'remote-ipv4': '10.10.10.10',
    'remote-ipv6': 'group "DMZ IPv6 Subnets"',
    'mgmt-ping': True,
    'user-https': True,
}
tunnel_gre_edit = {
    'type': 'gre',
    'zone': 'WAN',
    'name': 'test-gre',
    'name-new': 'test-6rd-edit',
    'bound-to': 'interface "X2"',# or any
}
tunnel_6to4 = {
    'type': '6to4',
    'zone': 'WAN',
    'name': 'test-6to4',
    'bound-to': 'interface "X1"',# or any
    'ip': '88::88',
    'prefix-length': '64',
    'enable': True,
    'link-mtu': 1280,
    'mgmt-ping': True,
    'user-https': True,
}
tunnel_6to4_edit = {
    'type': '6to4',
    'zone': 'WAN',
    'name': 'test-6to4',
    'name-new': 'test-6to4-edit',
    'bound-to': 'interface "X2"',# or any
}
tunnel_isatap = {
    'type': 'isatap',
    'zone': 'WAN',
    'name': 'test-isatap',
    'bound-to': 'interface "X1"',# or any
    'prefix': 'name "2000::"',
    'link-mtu': 1280,
    'mgmt-ping': True,
    'user-https': True,
}
tunnel_isatap_edit = {
    'type': 'isatap',
    'zone': 'WAN',
    'name': 'test-isatap',
    'name-new': 'test-isatap-edit',
    'bound-to': 'interface "X2"',# or any
}
# interface.add_tunnel_interface_ipv6(**tunnel_manual)
# interface.del_tunnel_interface_ipv6(name=tunnel_manual['name'])
# interface.add_tunnel_interface_ipv6(**tunnel_6rd)
# interface.edit_tunnel_interface_ipv6(**tunnel_6rd_edit)
# interface.del_tunnel_interface_ipv6(name='test-6rd-edit')
# interface.add_tunnel_interface_ipv6(**tunnel_gre)
# interface.edit_tunnel_interface_ipv6(**tunnel_gre_edit)
# interface.del_tunnel_interface_ipv6(name='test-gre-edit')
# interface.add_tunnel_interface_ipv6(**tunnel_6to4)
# interface.edit_tunnel_interface_ipv6(**tunnel_6to4_edit)
# interface.del_tunnel_interface_ipv6(name='test-6to4-edit')
# interface.add_tunnel_interface_ipv6(**tunnel_isatap)
# interface.edit_tunnel_interface_ipv6(**tunnel_isatap_edit)
# interface.del_tunnel_interface_ipv6(name='test-isatap-edit')
# interface.show_tunnel_status(type='manual', name='test-manual')
# interface.show_tunnel_status(type='6to4', name='test-6to4')
# interface.show_tunnel_status(type='gre', name='test-gre')
# interface.show_tunnel_status(type='6rd', name='test-6rd')
# interface.show_tunnel_status(type='isatap', name='isatap')
'''

wlb = modules.CLI.network.FailoverLBCli(fw)
lb = {
    'enable': True,
    'tcp_sync_port': '800',
    'tcp_sync': True,
}
# wlb.enable_Load_Balancing(**lb)

default_basic = {
    'type': 'basic',
    'preempt': True,    
    'add_interfaces': ['x3','x4'],
    'global-responder': True,
    'health-check': '5',
    'missed-intervals': '6',
    'successful-intervals': '7',
}
default_ratio = {
    'type': 'ratio',
    'address-binding': True,    
    'add_interfaces': ['X1', 'x3', 'x4'],
    'percentages': ['40', '30', '30'],
    'auto-adjust-ratio': True,
    'global-responder': True,
    'health-check': '5',
    'missed-intervals': '6',
    'successful-intervals': '7',
}
default_roundrobin = {
    'type': 'round-robin',
    'address-binding': True,    
    'add-interfaces': ['x3','x4'],
    'add-interfaces': ['x5'],
    'global-responder': True,
    'health-check': '5',
    'missed-intervals': '6',
    'successful-intervals': '7',
    }
default_spillover = {
    'type': 'spillover',
    'address-binding': True,    
    'spillover-bandwidth': '1000',
    'add-interfaces': ['x3','x4'],
    'global-responder': True,
    'health-check': '5',
    'missed-intervals': '6',
    'successful-intervals': '7',
    }
# wlb.edit_default_LB(**default_basic)
# wlb.edit_default_LB(**default_ratio)
# wlb.edit_default_LB(**default_spillover)
# wlb.edit_default_LB(**default_roundrobin)

group_member_physical = {
    'interface': 'X1', 
    'probe-type': 'physical', # 'logical','physical'
    'rank': '2',
    }

group_member_logical = {
    'interface': 'X4', 
    'probe-type': 'logical', # 'logical','physical'
    'rank': '2',
    'probe-condition': 'either',    #always,both,either,main
    'main_target_method': 'tcp',     # 'tcp'
    'main_target_host': '1.1.1.1',
    'main_target_port': '1000',
    'alter_target_method':'ping',
    'alter_target_host': '2.2.2.2',
    'alter_target_port': '2000',
    'default_target_ip': '3.3.3.3',    
    }
# wlb.edit_groupmember(**group_member_logical)

group_member_logical_v6 = {
    'version': '6',
    'interface': 'X4', 
    'probe-type': 'logical', # 'logical','physical'
    'rank': '2',
    'probe-condition': 'either',    #always,both,either,main
    'main_target_method': 'tcp',     # 'tcp'
    'main_target_host': '1::1',
    'main_target_port': '1000',
    'alter_target_method':'ping',
    'alter_target_host': '2::2',
    'alter_target_port': '2000',
    'default_target_ip': '3::3',    
    }
# wlb.edit_groupmember(**group_member_logical_v6)

dns = modules.CLI.network.DNSCli(fw)
dns_inhrit_v6 = {
    'type': 'inherit',
    'version': '6',
    }
# dns.dns_setting(**dns_inhrit_v6)
dns_inhrit_v4 = {
    'type': 'inherit',
    }
# dns.dns_setting(**dns_inhrit_v4)
dns_static_v6={
    'type': 'static',
    'version': '6',
    'primary': '1::1',
    }
# dns.dns_setting(**dns_static_v6)
dns_static_v4 = {
    'type': 'static',
    'version': '4',
    'primary': '1.1.1.1',
    'secondary': '2.2.2.2',
    'dns fqdn-over-tcp-dns': True,
    'dns rebinding': True,
    'dns rebinding action': 'drop-dns-reply',   # drop-dns-reply,log-attack-only,return-query-refused
    'dns rebinding allowed-domains': 'name fordns',# name,fqdn,group
    }
# dns.dns_setting(**dns_static_v4)

dns_sinkhole_service = {
    'enable': True,
    'action-type': '3',
    'forged_ipv4': '2.2.2.2',
    'forged_ipv6': '2::2',
    }
# dns.dns_sinkhole_service(**dns_sinkhole_service)

dns_tunnel_detection = {
    'enable': True,
    'block-all': True,
    }
# dns.dns_sinkhole_service(**dns_sinkhole_service)

custom_entries = ['aaa.com', 'bbb.com', 'ccc.com']
# dns.add_custom_malicious_entry(*custom_entries)
# dns.del_custom_malicious_entry('all')

white_list = ['ddd.com', 'ccc.com', 'eee.com']
# dns.add_white_list_entry(*white_list)
# dns.del_white_list_entry('all')

tunnel_white_list = ['1.1.1.1', '2.2.2.2', '3.3.3.3']
# dns.add_tunnel_white_list_entry(*tunnel_white_list)
# dns.del_tunnel_white_list_entry('all')
'''
########nat policy###########
'''
nat = modules.CLI.network.NatpolicyCli(fw)

add_nat = {
    'version': 'ipv4', # ipv4, ipv6, nat64 or not defined
#    'name': 'add_nat', #can define or not
    'comment':'add_nat', #can define or not
    'orig_source_type': 'name', # any，fqdn，group，host， name， network，range or not defined
    'orig_source': 'X0 Subnet', #define if orig_source_type is one of fqdn，group，host， name， network，range
    'trans_source_type': 'name', # original, name， network，range or not defined
    'trans_source': 'X2 IP', #define if trans_source_type is one of fqdn，group，host， name， network，range
    'orig_dest_type': 'any', # any，fqdn，group，host， name， network，range or not defined
    'trans_dest_type': '', # original, name， network，range or not defined
    'orig_service_type': 'protocol', #any, group, name, protocol
    'orig_service': 'TCP 20 20', #any, group, name, protocol
    'trans_service_type': 'name', #any, group, name, protocol   
    'trans_service': 'BGP', #define if trans_service_type is one of group, name, protocol 
}
nat.add_natpolicy(**add_nat)
show_ipv4_all = {
    'version': 'ipv4',
    'entries': 'all',
    'type': 'custom', #custom, default
}
# ipv4_all = nat.show_natpolicy(**show_ipv4_all)
# print(ipv4_all)

show_ipv4_name = {
    'version': 'ipv4',
    'name': 'add_nat',
}
# ipv4_name = nat.show_natpolicy(**show_ipv4_name)
# print(ipv4_name)
# ipv4_nat = nat.show_natpolicy(**add_nat)
# print(ipv4_nat)

add_nat_v6 = {
    'version': 'ipv6', # ipv4, ipv6, nat64 or not defined
    'name': 'add_nat_v6', #can define or not
    'comment':'add_nat_v6', #can define or not
    'orig_source_type': 'group', # any，fqdn，group，host， name， network，range or not defined
    'orig_source': 'Firewalled IPv6 Subnets', #define if orig_source_type is one of fqdn，group，host， name， network，range
    'trans_source_type': 'name', # original, name， network，range or not defined
    'trans_source': 'X1 IPv6 Primary Dynamic Address', #define if trans_source_type is one of fqdn，group，host， name， network，range
    'orig_dest_type': 'any', # any，fqdn，group，host， name， network，range or not defined
    'trans_dest_type': '', # original, name， network，range or not defined
    'orig_service_type': 'group', #any, group, name, protocol
    'orig_service': 'ICMPv6', #any, group, name, protocol
}

add_nat_nat64 = {
    'version': 'nat64', # ipv4, ipv6, nat64 or not defined
    'name': 'add_nat64', #can define or not
    'comment':'add_na64', #can define or not
    'trans_source_type': 'name', # original, name， network，range or not defined
    'trans_source': 'X1 IP', #define if trans_source_type is one of fqdn，group，host， name， network，range
    'pref64_type': 'name',
    'pref64': 'Well-Known Pref64',
}

nat.add_natpolicy(**add_nat_v6)
show_ipv6_all = {
    'version': 'ipv6',
    'entries': 'all',
    'type': 'custom', #custom, default
}
ipv6_all = nat.show_natpolicy(**show_ipv6_all)
print(ipv6_all)

show_ipv6_name = {
    'version': 'ipv6',
    'name': 'add_nat_v6',
}
ipv6_name = nat.show_natpolicy(**show_ipv6_name)
print(ipv6_name)
ipv6_nat = nat.show_natpolicy(**add_nat_v6)
print(ipv6_nat)
ipv6_edit = {
    'orig_service_type_new': 'name', #any, group, name, protocol
    'orig_service_new': '6over4', #any, group, name, protocol
}
nat.edit_natpolicy(add_nat_v6, ipv6_edit)
# nat.del_natpolicy('all')
# nat.del_natpolicy('ipv6:name:add_nat_v6')
# nat.del_natpolicy(add_nat_v6, add_nat)

nat.add_natpolicy(**add_nat_nat64)
'''


'''dhcpserver part'''
'''
dhcpserver = modules.CLI.network.DhcpServerCli(fw)

dynamic_scope = {
    'enable': True,
    'type': 'dynamic',
    'start': '192.168.168.221',
    'end': '192.168.168.230',
    'netmask': '255.255.255.0',
    'gateway': '192.168.168.168',
    'lease-time': '100',
    'dns1': '1.1.1.1',
    'dns2': '2.2.2.2',
    'wins1':'1.1.1.1',
    'voip1':'1.1.1.1',
}
dynamic_scope_v6 = {
    'version': 'ipv6',
    'type': 'dynamic',
    'enable': True,
    'start': '200::2',
    'end': '200:10',
    'netmask': '200::1',
    'gateway': '192.168.168.168',
    'lease-time': '100',
    'dns1': '1.1.1.1',
    'dns2': '2.2.2.2',
    'wins1':'1.1.1.1',
    'voip1':'1.1.1.1',
}
# dhcpserver.add_dhcpserver_scope_v4 (**dynamic_scope)
static_scope = {
    'name': 'test1',
    'type': 'static',
    'ip': '192.168.168.173',
    'mac': '11:22:33:44:55:66',
    'gateway': '192.168.168.168',
    'netmask': '255.255.255.0',
    'lease-time': '100',
    'dns1': '1.1.1.1',
    'dns2': '2.2.2.2',
    'wins1':'1.1.1.1',
    'voip1':'1.1.1.1',
}
# dhcpserver.add_dhcpserver_scope_v4 (**static_scope)
enable={
    'monitoring-interval': '6',
    'persistence': True,
}
# dhcpserver.enable_dhcpserver(**enable)
# dhcpserver.enable_dhcpserver(version='ipv6')
# dhcpserver.disable_dhcpserver()
# dhcpserver.disable_dhcpserver(version='ipv6')
# dhcpserver.delete_all_scopes(type='')#means both dynamic and static
# dhcpserver.delete_all_scopes(type='dynamic')
# dhcpserver.delete_all_scopes(type='static')

dynamic_edit_v4 = {
    'lease-time-new': '200',
    'dns1-new': '5.6.7.8',
    'start-new': '192.168.168.222',
}

static_edit_v4 = {
    'lease-time-new': '200',
    'dns1-new': '5.6.7.8',
    'ip': '192.168.168.253',
}
# dhcpserver.edit_dhcpserver_scope_v4(dynamic_scope, dynamic_edit_v4)
# dhcpserver.edit_dhcpserver_scope_v4(static_scope, static_edit_v4)
# dhcpserver.show_dhcpserver_v4()
# dhcpserver.show_dhcpserver_v6()

object_option_v4 = {
    'name': 'test2',
    'number': '254',
    'type': 'ip',# ip, domain-name, boolean, one-type, two-type, four-type,string, hex-string
    'value': '1.1.1.1',
    'array': True,
}
# dhcpserver.add_option_object_v4(**object_option_v4)

object_option_v6 = {
    'name': 'test-ipv6',
    'number': '12',
    'value': '1::1',
    # 'array': True,
}
# dhcpserver.add_dhcpserver_scope_v6(**object_option_v6)

group_option_v4_1 = {
    'name': 'group-test',
    'objects': ['test1', 'test2'],
}
group_option_v4_2 = {
    'name': 'group-test2',
    'objects': ['test1', 'test2'],
    'groups': ['group-test']
}
# dhcpserver.add_option_group_v4(**group_option_v4_1)
# dhcpserver.add_option_group_v4(**group_option_v4_2)
# dhcpserver.del_option(groups=['group-test2', 'group-test'], version='ipv4')
# dhcpserver.del_option(objects=['test1', 'test2'], version='ipv4')
dhcpserver.del_option(groups='all', version='ipv4')
dhcpserver.del_option(objects='all', version='ipv4')
dhcpserver.del_option(groups='all', version='ipv6')
dhcpserver.del_option(objects='all', version='ipv6')
'''

'''
arp = modules.CLI.network.ARPCli(fw)
entry = {
    'ip': '192.168.168.101',
    'mac': '12:23:34:45:56:67',
    'interface': 'X0',
    # 'publish': True,
    'bind-mac': True,
    'dynamic': True,
}
entry_new = {
    'ip-new': '192.168.168.200',
}
arp.add_arp_entry(**entry)
arp.show_arp_entry()
arp.edit_arp_entry(entry, entry_new)
arp.del_arp_entry(**entry)
arp.del_all_arp_entries()
'''

###################iphelper part###################
'''
iphelper = modules.CLI.network.IpHelper(fw)
# iphelper.enable_IPhelper()
# iphelper.disable_IPhelper()
protocol_v4 = {
    'name': 'iph-v4',
    'port1': '30',
    'port2': '40',
}
# iphelper.add_relay_protocol(**protocol_v4)
protocol_v4_edit = {
    'port1-new': '31',
}
# iphelper.edit_ralay_protocol(protocol_v4, protocol_v4_edit)
# iphelper.del_relay_protocol(name='iph-v4')
# iphelper.del_relay_protocol()
policy_v4 = {
    'name': 'iph-v4',
    'protocol': 'DHCP',
    'from': 'X1',
    'to': 'name "X1 IP"',
}
# iphelper.add_policy(**policy_v4)
policy_v4_edit = {
    'to-new': 'group "Firewalled Subnets"'
}
# iphelper.edit_policy(policy_v4, policy_v4_edit)
# iphelper.del_policy(**policy_v4)

policy_v6 = {
    'version': 'ipv6',
    'name': 'iph-v6',
    'protocol': 'DHCPv6',
    'from': 'X1',
    'to': '1::1',
    'egressif': 'X2',
}
iphelper.add_policy(**policy_v6)
policy_v6_edit ={
    'to-new': '2::2',
}
iphelper.edit_policy(policy_v6, policy_v6_edit)
policy_v6['to'] = policy_v6_edit['to-new']
iphelper.del_policy(**policy_v6)
iphelper.show_dhcp_relay_lease()
iphelper.show_dhcpv6_relay_lease()
'''


#################ddns part##################
'''
ddns = modules.CLI.network.DDNSCli(fw)
profile = {
    'name': 'test', #must specify
    'domain': 'aaa.com',#must specify
    'password': 'test', #must specify
    'user-name': 'automation', #must specify
    'offline-settings': 'use-previous', #do-nothing, use-previous
    'online-settings': '10.10.10.10', #detect, the ip of manual, set-to-wan
    'bound-to': 'any', # any, X**
    'service-type': 'dynamic', #custom, dynamic, static
    'provider': 'dyn',
}
ddns_edit = {
    'name': 'test',
    'name-new': 'test-edit',
    'domain-new': 'bbb.com',
}
ddns.add_ddns_profile(**profile)
ddns.edit_ddns_profile(**ddns_edit)
ddns.del_ddns_profile(name='test-edit')
ddns.del_ddns_profiles()

profile_v6 = {
    'version': 'ipv6',
    'name': 'testv6', #must specify
    'domain': 'aaa.com',#must specify
    'password': 'test', #must specify
    'user-name': 'automation', #must specify
    'offline-settings': 'use-previous', #do-nothing, use-previous
    'online-settings': 'detect', #detect, the ip of manual, set-to-wan
    'bound-to': 'X1', # any, X**
    'service-type': 'dynamic', #custom, dynamic, static
    'provider': 'dyn',
}
ddns_edit_v6 = {
    'version': 'ipv6',
    'name': 'testv6',
    'name-new': 'testv6-edit',
    'domain-new': 'bbb.com',
}
ddns.add_ddns_profile(**profile_v6)
ddns.edit_ddns_profile(**ddns_edit_v6)
ddns.del_ddns_profile(name='testv6-edit', version='ipv6')
ddns.del_ddns_profiles(version='ipv6')
ddns.show_ddns()
'''


'''
################neighbor discovery#############
ndp = modules.CLI.network.NeighborDiscoveryCli(fw)
ndp_opt = {
    'ip' : '2::2',
    'mac': '00:11:22:33:44:55',
    'interface': 'X1',
}
ndp_opt_edit = {
    'ip-new': '3::3',
}
ndp.add_ndp_entry(**ndp_opt)
ndp.del_ndp_entry(**ndp_opt)
# ndp.edit_ndp_entry(ndp_opt, ndp_opt_edit)
ndp.show_ndp_entries()
ndp.show_ndp_caches()
ndp.set_reachable_time(50)
ndp.del_ndp_entries()
'''


'''
##########zone part#########
zone = modules.CLI.network.ZonesCli(fw)
zone_opt = {
    'name': 'test1',
    'security-type': 'trusted',
    'interface-trust': True,
    'guest-services': True,
    'external-auth': {
        'general': {
            'client-redirect': 'https',
            'web-server1': {
                'protocol': 'http',
                'host': 'ipv6 host "X1 IPv6 Primary Static Address"',
                'port': '80',
            },
            'web-server2': {
                'protocol': 'https',
                'host': 'name "X1 IP"',
                'port': '443',
            },
            'timeout': 3, 
            'message-auth': {
                'method': 'md5',
                'secret': 'password',
                'confirm-secret': 'password',
            },    
            'social-network': ['google', 'twitter'],
            'wechat': {
                'enable': True,
                'only-qr-auth': True,
                'qr-auth-page': 'login.html',
            },
        },
        'auth-pages': {
            'web-server1': {
                'login': 'login1.html',
                'expiration': 'exp1.html',
                'timeout': 'idle1.html',
                'max-sessions': 'max1.html',
                'traffic-exceeded': 'trafficExceeded1.html',
            },
            'web-server2': {
                'login': 'login2.html',
                'expiration': 'exp2.html',
                'timeout': 'idle2.html',
                'max-sessions': 'max2.html',
                'traffic-exceeded': 'trafficExceeded2.html',
             },
        },
        'web-content': {
            # 'redirect': 'default',
            'redirect': 'custom "My custom redirect message"',
            'server-down': 'use-default',
        },
        'advanced': {
            'logout': {
                'expire': 5,
                'cgi1': 'logout.cgi',
                'cgi2': 'logout.cgi', 
            },
            'status-check': {
                'expire': 5,
                'cgi1': 'status.cgi',
                'cgi2': 'status.cgi', 
            },
            'session-sync': {
                'expire': 5,
                'cgi1': 'session.cgi',
                'cgi2': 'session.cgi', 
            },
        },
    },
    'custom-auth-page':{
        'header': {
            'type': 'url',
            'contenet': 'header.html',
        },
        'footer': {
            'type': 'url',
            'contenet': 'footer.html',
        },        
    },
    'policy-page-non-authentication':{
        'guest-usage-policy': 'welcome to sonicwall',
        'idle-timeout': '1 minutes', #  minutes, seconds, days, hours
    },
}

zone_simple = {
    'name': 'test2',
    'security-type': 'trusted',#trusted, public, wireless, sslvpn
    'interface-trust': True,
    'allow-from-higher': True,
    'guest-services': True,    
}
zone_wireless = {
    'name': 'test-wireless',
    'security-type': 'wireless',#trusted, public, wireless, sslvpn
    'local-radius': {
        'interface-server-numbers': 2,
        'port': 100,
        'client-password': 'password',
        'tls-cache': True,
        'tls-lifetime': 10,
        'database': {
            'server': '1.1.1.1',
            'base-dn': 11,
            'identity-dn': 11,
            'identity-dn-password': 'password',
            'tls': True,
            'cache': True,
            'cache-lifetime': 100,
            },
        # 'active-directory':{
        #     'admin-name': 'admin',
        #     'admin-password': 'password',
        #     'domain': 'aaa.com',
        #     'full-name': 'www.aaa.com',
        # },
    }, 
    'wireless': {
        'sslvpn-enforcement': True,
        'sslvpn-server': 'name "X2 IP"',
        'sslvpn-service': 'name "MMS TCP"',
        'auto-channel-limitation': True,
        'only-sonicpoint-traffic': True,
        'sonicpoint-management': True,
        'sonicwave-online-registeration': True,
        'sonicpoit-ac': {
            'auto-provisioning': True,
            'profile': 'SonicPointACe/ACi/N2',
        },
        'sonicpoit-n': {
            'auto-provisioning': True,
            'profile': 'SonicPointN',
        },
        'sonicpoit-ndr': {
            'auto-provisioning': True,
            'profile': 'SonicPointNDR',
        },
        'sonicpoit-wave2': {
            'auto-provisioning': True,
            'profile': 'SonicWave',
        },
    },
}
zone_edit = {
    'name': 'test-wireless',
    'security-type': 'wireless',#trusted, public, wireless, sslvpn
    'name-new': 'test-wireless-edit',
    'local-radius': {
        'active-directory':{
            'admin-name': 'admin',
            'admin-password': 'password',
            'domain': 'aaa.com',
            'full-name': 'www.aaa.com',
        },
    },     
}
# zone.add_zone(**zone_opt)
# zone.add_zone(**zone_simple)
# zone.add_zone(**zone_wireless)
zone.show_zones('test-wireless')
zone.show_zones()
zone.edit_zone(**zone_edit)
zone.del_zone('test-wireless-edit')
zone.del_zone()
'''


###########routing#############
routing = modules.CLI.network.RouteCli(fw)
policy = {
    'if': 'X1',
    'metric': 8,
    'source': 'group "Firewalled Subnets"', #any,group,host,name,network,range
    'destination': 'name "X2 Subnet"',
    'name': 'route_v4',
    'wxa-group': 'Group one',
    'probe': 'ddd',
    'vpn-precedence': True,
}
policy_v6 = {
    'version': 'ipv6',
    'if': 'X1',
    'metric': 8,
    'source': 'host "::"', #any,group,host,name,network,range
    'name': 'route_v6',
    'vpn-precedence': True,    
}
'''
routing.add_route_policy(**policy)
routing.add_route_policy(**policy_v6)
routing.show_route_policies()
routing.show_route_policies(version='ipv4', type='custom')
routing.show_route_policies(version='ipv6')
routing.show_route_policy(**policy)
routing.show_route_policy(**policy_v6)
routing.del_route_policy(**policy)
routing.del_route_policy(**policy_v6)
routing.del_route_policies('ipv4')
routing.del_route_policies('ipv6')
routing.del_route_policies()
'''
# routing.set_route('advanced') #simple, advanced
ripng_opt = {
    'if': 'X0',
    'enable': True,
    'split': True,
    'poison': True,
}

rip_opt = {
    'if': 'X0',
    'network': '192.168.168.0/24', #the network map to the corresponding interface
    'type': 'send-receive',#disable,send-receive,send,receive,passive
    'receive-version': '2',
    'send-version': '2',#1,2,1-compatible
    'split': True,
    'poison': True,   
    'password': 'password', 
}

ospf_opt = {
    'if': 'X0',
    'type': 'enable', # enable, disable, passive
    'network': '192.168.168.0/24', #the network map to the corresponding interface
    'dead-interval': 100,
    'hello-interval': 200,
    'auth': 'message-digest',#null, simple, message-digest
    'password':'password',
    'area': '10',
    'area-type': 'stub', #stub, totally-stub, nssa, totally-nssa
    'cost': '',
    'priority': 2,
    'mtu-ignore': True,
}
ospf_disable = {
    'if': 'X0',
    'type': 'disable', # enable, disable, passive
    'network': '192.168.168.0/24', #the network map to the corresponding interface
    'area': '10',
}
ospf_passive = {
    'if': 'X0',
    'type': 'passive', # enable, disable, passive
}
ospfv3_opt = {
    'if': 'X0',
    'type': 'enable', # enable, disable, passive
    'dead-interval': 100,
    'hello-interval': 200,
    'area': '21',
    'area-type': 'stub', #stub, totally-stub
    'cost': '',
    'priority': 2,
}
ospfv3_passive = {
    'if': 'X0',
    'type': 'passive', # enable, disable, passive
     'area': '21',
}
ospfv3_disable = {
    'if': 'X0',
    'type': 'disable', # enable, disable, passive 
    'area': '21',
}
# routing.config_ospf(**ospf_opt)
# routing.config_ospf(**ospf_disable)
# routing.config_ospf(**ospf_passive)
# routing.config_ospf3(**ospfv3_opt)
# routing.config_ospf3(**ospfv3_passive)
# routing.config_ospf3(**ospfv3_disable)
# routing.config_rip(**rip_opt)
# routing.config_ripng(**ripng_opt)


######mac ip anti sproof
macip = modules.CLI.network.MacIPAntiSproofCli(fw)

x1_macip = {
    'interface': 'X1',
    'version': 'ipv4',
    'enable': True,
    'allow-management': True,
    'enfore-ingress': True,
    'spoof-detection': True,
    'static-arp': True,
    'dhcp-relay': True,
    'dhcp-server': True,
    'arp-lock': True,
    'arp-watch': True,
}

x1_macip_v6 = {
    'interface': 'X1',
    'version': 'ipv6',
    'enable': True,
    'allow-management': True,
    'enfore-ingress': True,
    'spoof-detection': True,
    'ndp-lock': True,
    'static-ndp': True,
}
x1_cache_entry= {
    'interface': 'X1',
    'ip': '1.1.1.1',
    'mac': '00:11:22:33:44:55',
    'router': True,
    'blacklisted': True,
}
x1_cache_entry_v6= {
    'interface': 'X1',
    'version': 'ipv6',
    'ip': '1::1',
    'mac': '00:11:22:33:44:55',
    'router': True,
    'blacklisted': True,
}
x1_cache_entry_edit = {
    'router-new': False,
}
# macip.set_interface(**x1_macip)
# macip.set_interface(**x1_macip_v6)
# macip.add_cache_entry(**x1_cache_entry)
# macip.add_cache_entry(**x1_cache_entry_v6)
# macip.edit_cache_entry(x1_cache_entry, x1_cache_entry_edit)
# macip.resolve_detected_list()
# macip.resolve_detected_list(ver='ipv6')
# macip.clear_macip_detected_list()
# macip.clear_macip_detected_list(ver='ipv6')
# macip.clear_macip_staticstics()
# macip.clear_macip_staticstics(ver='ipv6')
# macip.show_macip_detected_list()
# macip.show_macip_detected_list(ver='ipv6')
# macip.show_macip_entries()
# macip.show_macip_entries(ver='ipv6')
# macip.show_macip_interaface()
# macip.show_macip_interaface(interface='X1')
# macip.show_macip_interaface(ver='ipv6')
# macip.show_macip_interaface(ver='ipv6', interface='X1')
# macip.del_cache_entry(**x1_cache_entry)
# macip.del_cache_entry(**x1_cache_entry_v6)
# macip.del_cache_entries(ver='ipv4')
# macip.del_cache_entries(ver='ipv6')
# macip.del_cache_entries()


######vlan Translation#####
'''
vt = modules.CLI.network.VlanTranslationCli(fw)
vt_opt = {
    'ingress-if': 'x4',
    'ingress-vlan': 100,
    'egress-if': 'X6',
    'egress-vlan': 200,
    'reverse': True,
}
vt_opt_edit = {
    'ingress-vlan-new': 300,
}
vt.add_vlan_translation(**vt_opt)
vt.edit_vlan_translation(vt_opt, vt_opt_edit)
vt.show_vlan_translation()
vt_opt['ingress-vlan'] = 300
vt.del_vlan_translation(**vt_opt)
'''

'''
###############Network Monitor############
nm = modules.CLI.network.NetworkMonitorCli(fw)
nm_tcp_opt = {
    'name': 'nm_ipv4',
    'probe-target': 'name "X1 IP"',
    'outbound-interface': 'X1',
    'next-hop': 'name "X0 IP"',
    'probe-type': 'tcp explicit',#tcp,tcp explicit,ping,ping explicit
    'port': '100',
    'intervel': 5,
    'reply-timeout': 2,
    'down-after': 6,
    'up-after': 7,
    'must-respond': True,
    'rst-as-miss': True,
}
nm_icmp_opt = {
    'name': 'nm_ipv4',
    'probe-target': 'name "X1 IP"',
    'outbound-interface': 'X1',
    'next-hop': 'name "X0 IP"',
    'probe-type': 'ping explicit',
}
nm_tcp_v6 = {
    'name': 'nm_ipv6',
    'version': 'ipv6',
    'probe-target': 'group "X3 IPv6 Addresses"',
    'probe-type': 'tcp',#tcp,tcp explicit,ping,ping explicit
    'port': '100',    
}
nm.add_nm_policy(**nm_tcp_opt)
nm.add_nm_policy(**nm_icmp_opt)
nm.add_nm_policy(**nm_tcp_v6)
nm.show_nm_policies('ipv6')
nm.show_nm_policies('ipv4')
nm.show_nm_policies()
nm.show_nm_policy(name='nm_ipv6', version='ipv6')
nm.show_nm_policy(name='nm_ipv4', version='ipv4')
nm.show_nm_policies_status(version='ipv4')
nm.show_nm_policies_status(version='ipv6')
nm.show_nm_policy_status(name='nm_ipv6', version='ipv6')
nm.show_nm_policy_status(name='nm_ipv4', version='ipv4')
nm.del_nm_policy(name='nm_ipv6', version='ipv6')
nm.del_nm_policies('ipv4')
nm.del_nm_policies('ipv6')
'''

###########portshieldGroup###########
'''
pg = modules.CLI.network.PortShieldGroupCli(fw)

port_opt = {
    'interface': 'X5',
    'port-enable': True, # or False
    'portshield-to': 'X0',
    'link-speed':'1000-full',#100-full,100-half,10-full,10-half,auto
}
pg.config_port(**port_opt)
'''


###############service##################
'''
service = modules.CLI.network.ServiceCli(fw)
service_icmp = {
    'name': 'icmp-service',
    'protocol': 'icmp',
    'sub-type': 'echo-request',
}
service_igmp = {
    'name': 'igmp-service',
    'protocol': 'igmp',
    'sub-type': 'v1-member-report',
}
service_tcp = {
    'name': 'tcp-service',
    'protocol': 'tcp',
    'port': '100 120',
}
service_udp = {
    'name': 'udp-service',
    'protocol': 'udp',
    'port': '100 120',
}
service_6over4 = {
    'name': '6over4-service',
    'protocol': '6over4',
}
service_gre = {
    'name': 'gre-service',
    'protocal': 'gre',
}
service_esp = {
    'name': 'esp-service',
    'protocol': 'esp',
}
service_ah = {
    'name': 'ah-service',
    'protocol': 'ah',
}
service_icmpv6 = {
    'name': 'icmpv6-service',
    'protocol': 'icmpv6',
    'sub-type': 'echo-request',
}
service_eigrp = {
    'name': 'eigrp-service',
    'protocol': 'eigrp',
}
service_ospf = {
    'name': 'ospf-service',
    'protocol': 'ospf',
    'sub-type': 'hello',
}
service_pim = {
    'name': 'pim-service',
    'protocol': 'pim',
    'sub-type': 'assert',
}
service_l2tp = {
    'name': 'l2tp-service',
    'protocol': 'l2tp',
}
service_pim_edit = {
    'name': 'pim-service',
    'protocol': 'pim',
    'sub-type': 'graft',    
}
# service.add_service_object(**service_6over4)
# service.add_service_object(**service_icmp)
# service.add_service_object(**service_udp)
# service.add_service_object(**service_ah)
# service.add_service_object(**service_eigrp)
# service.add_service_object(**service_icmpv6)
# service.add_service_object(**service_pim)
# service.edit_service_object(**service_pim_edit)
# service.del_service_object(name='pim-service')
# service.del_service_object()
group = {
    'name': 'test-group',
    'add-group': ['"Host Name Server"'],
    'del-group': ['MMS', 'MSN'],
    'add-object': ['"Citrix UDP"'],
    'del-object': ['"FTP Data"', 'FTP'],
}
group_edit = {
    'name': 'test-group',
    'name-new': 'test-group1',
    'add-group': ['"Host Name Server"'],
}
# service.add_service_group(**group)
# service.edit_service_group(**group_edit)
# service.show_service_group()
# service.show_service_object()
# service.del_service_group(name='test-group1')
# service.del_service_group()
'''

#####adress object#############
ao = modules.CLI.network.AddressObjectCli(fw)
host_ao = {
    'name': '1.1.1.1',
    'version': 'ipv4',
    'type': 'host',
    'zone': 'WAN',
    'host': '1.1.1.1',
}
range_ao = {
    'name': '2.2.2.1-2.2.2.10',
    'version': 'ipv4',
    'type': 'range',
    'zone': 'WAN',
    'range': '2.2.2.1 2.2.2.10',
}
network_ao = {
    'name': '3.3.3.0',
    'version': 'ipv4',
    'type': 'network',
    'zone': 'WAN',
    'network': '3.3.3.0 255.255.255.0',
}
mac_ao = {
    'name': '11:22:33:44:55:66',
    'type': 'mac',
    'zone': 'WAN',
    'address': '11:22:33:44:55:66',
    'multi-homed': True, #or False
}
mac_ao_edit = {
    'name': '11:22:33:44:55:66',
    'type': 'mac',
    'zone': 'WAN',
    'address-new': '11:22:33:44:55:77',
    'multi-homed-new': False,   
}
fqdn_ao = {
    'name': 'www.aaa.com',
    'type': 'fqdn',
    'zone': 'WAN',
    'domain': 'www.aaa.com',
    'dns-ttl': '150', #or False
}
fqdn_ao_edit = {
    'name': 'www.aaa.com',
    'type': 'fqdn',
    'name-new': 'www.bbb.com',
    'domain-new': 'www.bbb.com',
    'dns-ttl-new': False,
}
host_ao_edit = {
    'name': '1.1.1.1',
    'version': 'ipv4',
    'name-new': '5.5.5.0',
    'type-new': 'network',
    'network-new': '"5.5.5.0" "255.255.255.0"',
}
# ao.add_address_object(**host_ao)
# ao.add_address_object(**network_ao)
# ao.add_address_object(**range_ao)
# ao.add_address_object(**mac_ao)
# ao.add_address_object(**fqdn_ao)
# ao.show_address_object()
# ao.show_address_object(version='ipv4', type='custom')
# ao.show_address_object(version='ipv4', name='1.1.1.1')
# ao.show_address_object(name='fqdn www.aaa.com')
# ao.show_address_object(name='mac 11:22:33:44:55:66')
# ao.del_address_object(**host_ao)
# ao.del_address_object(**range_ao)
# ao.del_address_object(**network_ao)
# ao.del_address_object(**fqdn_ao)
# ao.del_address_object(**mac_ao)
# ao.del_address_objects('host') # host, fqdn, mac, network, range
# ao.edit_address_object(**fqdn_ao_edit)
# ao.edit_address_object(**mac_ao_edit)
# ao.edit_address_object(**host_ao_edit)
host_ipv6 = {
    'name': '1::1',
    'version': 'ipv6',
    'type': 'host',
    'zone': 'LAN',
    'host': '1::1',
}
range_ipv6 = {
    'name': '2::2-2::10',
    'version': 'ipv6',
    'type': 'range',
    'zone': 'LAN',
    'range': '2::2 2::10',
}
network_ipv6 = {
    'name': '3::',
    'version': 'ipv6',
    'type': 'network',
    'zone': 'WAN',
    'network': '3:: 64',
}
# ao.add_address_object(**host_ipv6)
# ao.add_address_object(**range_ipv6)
# ao.add_address_object(**network_ipv6)
# ao.show_address_object(version='ipv6', type='custom')
# ao.show_address_object(version='ipv6', name='1::1')
# ao.del_address_object(**host_ipv6)
# ao.del_address_object(**range_ipv6)
# ao.del_address_object(**network_ipv6)
group = {
    'name': 'test-group',
    'version': 'ipv4',
    'objects': ['ipv4 2.2.2.1-2.2.2.10', 'ipv4 3.3.3.0', 'ipv4 1.1.1.1', 'fqdn www.bbb.com', 'mac 11:22:33:44:55:66'],
    'groups': ['ipv4 "All Interface IP"'],
}
group_ipv6 = {
    'name': 'test-group-v6',
    'version': 'ipv6',
    'objects': ['ipv6 1::1', 'ipv6 2::2-2::10', 'ipv6 ::', 'fqdn www.bbb.com', 'mac 11:22:33:44:55:66'],
    'groups': ['ipv6 "Firewalled IPv6 Subnets"', 'ipv6 "LAN Interface IPv6 Addresses"'],    
}
###any group include fqdn and mac , the version defined to ipv6
group_edit_v6 = {
    'name': 'test-group',
    'version': 'ipv6',
    'del_objects': ['ipv4 2.2.2.1-2.2.2.10', 'ipv4 3.3.3.0', 'ipv4 1.1.1.1', 'fqdn www.bbb.com', 'mac 11:22:33:44:55:66'],
    'del_groups': ['ipv4 "All Interface IP"'],
    'add_objects':['ipv6 "Well-Known Pref64"'],
    'add_groups': ['ipv6 "DMZ IPv6 Subnets"'],
}
# ao.add_address_group(**group)
# ao.add_address_group(**group_ipv6)
# ao.edit_address_group(**group_edit_v6)
ao.show_address_group()
ao.show_address_group(version='ipv4', type='custom') #type is custom or defalut
ao.show_address_group(name='test-group', version='ipv4')
ao.show_address_group(name='test-group-v6', version='ipv6')
ao.del_address_group(**group)
ao.del_address_group(**group_ipv6)
ao.del_address_groups(version='ipv4')
ao.del_address_groups(version='ipv6')
ao.del_address_groups() # delete both ipv4 and ipv6

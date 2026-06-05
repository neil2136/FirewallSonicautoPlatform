import sys
import os
sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
from utm import Firewall
from modules.API.firewallsettings import AdvanceApi
from modules.API.firewallsettings import BwmApi
from modules.API.firewallsettings import FloodprotectionApi
from modules.API.firewallsettings import MulticastApi
from modules.API.firewallsettings import SslcontrolApi
from modules.API.firewallsettings import QosmappingApi
ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fwsettings_adv = AdvanceApi(fw)
fwsettings_bwm = BwmApi(fw)
fwsettings_flood_protection = FloodprotectionApi(fw)
fwsettings_multicast = MulticastApi(fw)
fwsettings_ssl_control = SslcontrolApi(fw)
fwsettings_qos = QosmappingApi(fw)

############################################################################
# Advance page #
############################################################################
adv_dict0 = {
    'stealth_mode': True,
    'randomize_id': True,
    'decrement ttl': True,
#    'icmp time_exceeded_packets': False,#move to func config_advance_access_rule
    'ftp_transforms_in_service_object': {'name': 'NTP'},
    'sqlnet': True,
    'rtsp_transformations': True,
    'drop source_routed': False,
    'connections': 'highest',#value can be highest, optimized, recommended
    'ip checksum_enforcement': True,
    'udp checksum_enforcement': True,
    'control_plane_flood_protection': {'threshold': 76},
    'jumbo_frame': True,
}

adv_dict1 = {
    'force_ftp_data': True,
    'apply_rules_for_intra_lan': True,
    'issue_rst_for_outgoing_discards': True,
    'icmp redirect_on_lan': True,
    'icmp time_exceeded_packets': False,
}

adv_dict2 = {
    'ipv6 drop all_traffic': True,
    'ipv6 drop routing_header_0': True,
    'ipv6 decrement hop_limit': True,
    'ipv6 drop reserved_address_packets': True,
    'ipv6 icmp time_exceeded': False,
    'ipv6 icmp destination_unreachable': False,
    'ipv6 icmp redirect': False,
    'ipv6 icmp parameter_problem': False,
    'ipv6 site-local_unicast': True,
    'ipv6 extension_header_check': True,
    'ipv6 extension_header_order_check': True,# need firewall restart for changes to take effect.
    'ipv6 netbios_for_isatap': True,# need firewall restart for changes to take effect.
}
#output0_0 = fwsettings_adv.show_adv_setttings()
#output0_1 = fwsettings_adv.config_advance(**adv_dict0)
#output0_2 = fwsettings_adv.config_advance_access_rule(**adv_dict1)
#output0_3 = fwsettings_adv.config_advance_ipv6(**adv_dict2)
#print('-------------------output:start-------------------')
#print(output0_0)
#print(output0_1)
#print(output0_2)
#print(output0_3)
#print('--------------------output:end--------------------')

############################################################################
# BWM page #
############################################################################
bwm_dict = {
    'type': 'global',# type can be advanced, global, none
    'guaranteed': {
        'realtime': 10,
        'highest': 10,
        'high': 20,
        'medium_high': 10,
        'medium': 10,
        'medium_low': 10,
        'low': 10,
        'lowest': 10,
    },
    'maximum': {
        'realtime': 10,
        'highest': 20,
        'high': 30,
        'medium_high': 10,
        'medium': 10,
        'medium_low': 10,
        'low': 10,
        'lowest': 20,
    },
}

#output1_0 = fwsettings_bwm.show_bwm()
#output1_1 = fwsettings_bwm.config_bwm(**bwm_dict)
#print('-------------------output:start-------------------')
#print(output1_0)
#print(output1_1)
#print('--------------------output:end--------------------')

############################################################################
# Flood_Protection page #
############################################################################
fp_dict0 = {
    'type': 'tcp', # type can be tcp, udp, icmp
}

fp_dict1 = {
    'enforce_strict_compliance': True,
    'handshake_enforcement': True,
    'checksum_enforcement': True,
    'drop syn_with_data': True,
    'handshake_timeout': 40,
    'default_connection_timeout': 20,
    'maximum_segment_lifetime': 10,
    'syn_flood_protection_mode': 'proxy-suspect-attack',#mode type: watch-and-report, proxy-suspect-attack, always-proxy
    'syn_attack_threshold': 500,
    'support_tcp_sack': True,
    'limit_mss': {'max': 1400},
    'always_log_syn_packets': True,
    'syn_flood_blacklisting': True,
    'blacklist_threshold': 1100,
    'never_blacklist_wan': True,
    'always_allow_management': True,
    'ddos_on_wan_interfaces': True,
    'ddos_threshold': 1001,
    'ddos_fliter_bypass_rate': 1,
    'ddos_allow_list_timeout': 2,
    'ddos_always_allow_management': True,
    'ddos_always_allow_negotiation': True,
}

fp_dict2 = {
    'type': 'icmp', # type can be udp or icmp
    'default-connection-timeout': 50,
    'flood protection': True,
    'flood attack-threshold': 1001,
    'flood block-timeout': 3,
    'flood protected-dest-list': {'host': '192.168.168.168'} #value can be any,group,host,name,network,range
}

fp_dict3 = {
    'flood protection': True,
    'flood attack-threshold': 300,
    'flood block-timeout': 5,
    'flood protected-dest-list': {'name': "X0 Subnet"},
}

#output2_0 = fwsettings_flood_protection.show_flood_protection(**fp_dict0)
#output2_1 = fwsettings_flood_protection.config_tcp(**fp_dict1)
#output2_2 = fwsettings_flood_protection.config_udp_icmp(**fp_dict2)
#print('-------------------output:start-------------------')
#print(output2_0)
#print(output2_1)
#print(output2_2)
#print(output2_3)
#print('--------------------output:end--------------------')

############################################################################
# multicast page #
############################################################################
multicast_dict = {
    'multicast': True, # set value to False can disable multicast
    'require_igmp_membership': True,
    'timeout': 21,
    'reception_name': 'test1', # without this option, reception set to all multicast address
}

multicast_dict1 = {
    'delete_way': 'all', # or can be all
    'address': '224.10.10.10',
    'interface': 'X0',
}

#output3_0 = fwsettings_multicast.show_multicast()
#output3_1 = fwsettings_multicast.config_multicast(**multicast_dict)
#output3_2 = fwsettings_multicast.delete_state_entry(**multicast_dict1)
#print('-------------------output:start-------------------')
#print(output3_0)
#print(output3_1)
#print(output3_2)
#print('--------------------output:end--------------------')

############################################################################
# ssl_control page #
############################################################################
customlists_dict = {
    'action': 'add', # action option can be add or delete
    'black_name': ['black1.local1','black2.local2','black3.local3'],
    'white_name': ['white1.local1','white2.local1','white3.local1'],
}

ssl_control_dict = {
    'enable': True,
    'action': 'log',
    'blacklist': True,
    'whitelist': True,
    'detect_ssl_v2': True,
    'detect_ssl_v3': True,
    'detect_weak_ciphers': True,
    'detect_self_signed': True,
    'detect_weak_digest_cert': True,
    'detect_expired': True,
    'detect_untrusted_ca': True,
    'detect_tls_v1': True,
}

#output4_0 = fwsettings_ssl_control.show_ssl_control()
#output4_1 = fwsettings_ssl_control.config_customlists(**customlists_dict)
#output4_2 = fwsettings_ssl_control.config_ssl_control(**ssl_control_dict)
#print('-------------------output:start-------------------')
#print(output4_0)
#print(output4_1)
#print(output4_2)
#print('--------------------output:end--------------------')

############################################################################
# QoS Mapping page #
############################################################################
qos_dict = {
    '0': {'from_dscp': {'begin': 2, 'end': 5}, 'to_dscp': 0},
    '1': {'from_dscp': {'begin': 8, 'end': 15},'to_dscp': 8},
    '2': {'from_dscp': {'begin': 16, 'end': 23},'to_dscp': 16},
    '3': {'from_dscp': {'begin': 24, 'end': 31},'to_dscp': 24},
    '4': {'from_dscp': {'begin': 36, 'end': 37},'to_dscp': 36},
    '5': {'from_dscp': {'begin': 40, 'end': 47},'to_dscp': 40},
    '6': {'from_dscp': {'begin': 48, 'end': 55},'to_dscp': 48},
    '7': {'from_dscp': {'begin': 56, 'end': 63},'to_dscp': 56},
}

#output5_0 = fwsettings_qos.show_qosmapping()
#output5_1 = fwsettings_qos.config_qosmapping(**qos_dict)
#output5_2 = fwsettings_qos.reset_qosmapping()
#print('-------------------output:start-------------------')
#print(output5_0)
#print(output5_1)
#print(output5_2)
#print('--------------------output:end--------------------')



import modules.CLI.firewallsettings
from utm import Firewall
ip = '192.168.168.168'
fw = Firewall(
    ip,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

fwsettingsadv = modules.CLI.firewallsettings.AdvancedCli(fw)
fwsettingsbwm = modules.CLI.firewallsettings.BwmCli(fw)
fwsettingsfp = modules.CLI.firewallsettings.FloodprotectionCli(fw)
fwsettingsmulticast = modules.CLI.firewallsettings.MulticastCli(fw)
fwsettingsqosmapping = modules.CLI.firewallsettings.QosmappingCli(fw)
fwsettingssslcontrol = modules.CLI.firewallsettings.SslcontrolCli(fw)

############################################################################
# Advanced page #
############################################################################
adv_dict0 = {
    'stealth-mode': True,
    'randomize-id': True,
    'decrement ttl': True,
    'ftp-transforms-in-service-object': 'name NTP',
    'icmp time-exceeded-packets': False,#decrement ttl must be set to true prehand
    'sqlnet': False,
    'rtsp-transformations': True,
    'drop source-routed': True,
    'ip checksum-enforcement': True,
    'udp checksum-enforcement': True,
    'control-plane-flood-protection': True,
    'control-plane-flood-protection threshold': '80',#control-plane-flood-protection must be set to true prehand
    'starting-vlan': '10',
    'jumbo-frame': True,
}

adv_dict1 = {
    'force-ftp-data': True,
    'apply-rules-for-intra-lan': True,
    'issue-rst-for-outgoing-discards': True,
    'icmp redirect-on-lan': True,
    'drop source-subnet-broadcast': True,
}

adv_dict2 = {
    'ipv6 drop all-traffic': True,
    'ipv6 drop routing-header-0': True,
    'ipv6 decrement hop-limit': True,
    'ipv6 drop reserved-address-packets': True,
    'ipv6 icmp time-exceeded': False,
    'ipv6 icmp destination-unreachable': False,
    'ipv6 icmp redirect': False,
    'ipv6 icmp parameter-problem': False,
    'ipv6 site-local-unicast': True,
    'ipv6 extension-header-check': True,
    'ipv6 extension-header-order-check': True,# need firewall restart for changes to take effect.
    'ipv6 netbios-for-isatap': True,# need firewall restart for changes to take effect.
}

#output1_0 = fwsettingsadv.show_firewall()
#output1_1 = fwsettingsadv.config_advanced(**adv_dict0)
#output1_2 = fwsettingsadv.config_advanced_access_rule(**adv_dict1)
#output1_3 = fwsettingsadv.config_advanced_ipv6(**adv_dict2)
#print('-------------------output:start-------------------')
#print(output1_0)
#print(output1_1)
#print(output1_2)
#print(output1_3)
#print('--------------------output:end--------------------')

############################################################################
# BWM page #
############################################################################
bwm_dict0 = {
    'type': 'global',# type can be advanced, global, none
}

bwm_dict1 = {
    'guaranteed':{'realtime': '10',
                'highest': '10',
                'high': '10',
                'medium-high': '10',
                'medium': '10',
                'medium-low': '10',
                'low': '10',
                'lowest': '10',
                },
    'maximum':{'realtime': '10',
                'highest': '10',
                'high': '10',
                'medium-high': '10',
                'medium': '10',
                'medium-low': '10',
                'low': '10',
                'lowest': '20',
              },
}

#output2_0 = fwsettingsbwm.show_bandwidth_management()
#output2_1 = fwsettingsbwm.config_bwm_type(**bwm_dict0)
#output2_2 = fwsettingsbwm.config_bwm_priority(**bwm_dict1)
#print('-------------------output:start-------------------')
#print(output2_0)
#print(output2_1)
#print(output2_2)
#print('--------------------output:end--------------------')

############################################################################
# Flood Protection page #
############################################################################
fp_dict0 = {
    'show': 'tcp', # show type can be: tcp, icmp.etc
}

fp_dict1 = {
    'enforce-strict-compliance': True,
    'handshake-enforcement': True,
    'checksum-enforcement': True,
    'drop syn-with-data': True,
    'handshake-time': '60',
    'default-connection-timeout': '30',
    'maximum-segment-lifetime': '10',
    'syn-flood-protection-mode': 'always-proxy', #mode: always-proxy, proxy-suspect-attack, watch-and-report
    'syn-attack-threshold': '500',
    'support-tcp-sack': True,
    'limit-mss': True,
    'always-log-syn-packets': True,
    'syn-flood-blacklisting': True,
    'blacklist-threshold': '1300',
    'never-blacklist-wan': True,
    'always-allow-management': True,
}

fp_dict2 = {
    'ddos on-wan-interfaces': True,
    'ddos threshold': '1200',
    'ddos fliter-bypass-rate': '3',
    'ddos allow-list-timeout': '5',
    'ddos always-allow-management': True,
    'ddos always-allow-negotiation': True,
}

fp_dict3 = {
    'default-connection-timeout': '60',
    'flood protection': True,
    'flood attack-threshold': '211',
    'flood block-timeout': '6',
    'flood protected-dest-list': 'host 192.168.168.168',#value can be any,group,host,name,network,range
}

fp_dict4 = {
    'flood protection': True,
    'flood attack-threshold': '290',
    'flood block-timeout': '6',
    'flood protected-dest-list': 'name "X0 Subnet"',
}

#output3_0 = fwsettingsfp.show_floodprotection(**fp_dict0)
#output3_1 = fwsettingsfp.config_tcp(**fp_dict1)
#output3_2 = fwsettingsfp.config_tcp_ddos(**fp_dict2)
#output3_3 = fwsettingsfp.config_udp(**fp_dict3)
#output3_4 = fwsettingsfp.config_icmp(**fp_dict4)
#print('-------------------output:start-------------------')
#print(output3_0)
#print(output3_1)
#print(output3_2)
#print(output3_3)
#print(output3_4)
#print('--------------------output:end--------------------')

############################################################################
# Multicast page #
############################################################################
mc_dict0 = {
    'multicast': True,
}

mc_dict1 = {
    'require-igmp-membership': True,
    'require-igmp-membership timeout': '15',
}

mc_dict2 = {
#    'reception': 'range 192.168.168.10 192.168.168.20',
    'reception': 'all',
}
#example: 'reception all'
#         'reception name Multicast Address'
#         'reception group Multicast Group'
#         'reception host 224.0.0.12'
#         'reception range 192.168.168.10 192.168.168.20'
#         'reception network 192.168.168.0 255.255.255.0'

mc_dict3 = {
    'address': '224.10.10.10',
    'interface': 'X0',
}

#output4_0 = fwsettingsmulticast.show_multicast()
#output4_1 = fwsettingsmulticast.enable_multicast(**mc_dict0)
#output4_2 = fwsettingsmulticast.config_multicast_snooping(**mc_dict1)
#output4_3 = fwsettingsmulticast.config_multicast_policies(**mc_dict2)
#output4_4 = fwsettingsmulticast.clear_state_entry(**mc_dict3)
#print('-------------------output:start-------------------')
#print(output4_0)
#print(output4_1)
#print(output4_2)
#print(output4_3)
#print(output4_4)
#print('--------------------output:end--------------------')

############################################################################
# Qos Mapping page #
############################################################################
qos_dict0 = {
    'qos-index': '0',
    'to-dscp-value': '0',
    'from-dscp-value': '0 5',
}

#output5_0 = fwsettingsqosmapping.show_qos_mapping()
#output5_1 = fwsettingsqosmapping.config_qos_setting(**qos_dict0)
#output5_2 = fwsettingsqosmapping.reset_qos_setting()
#print('-------------------output:start-------------------')
#print(output5_0)
#print(output5_1)
#print(output5_2)
#print('--------------------output:end--------------------')

############################################################################
# SSL Control page #
############################################################################
sslc_dict0 = {
    'enable': True,
}

sslc_dict1 = {
    'action-type': 'block',#action type can be log and block
}

sslc_dict2 = {
    'blacklist': True,
    'whitelist': True,
    'detect weak-ciphers': True,
    'detect expired': True,
    'detect weak-digest-cert': True,
    'detect self-signed': True,
    'detect untrusted-ca': True,
    'detect ssl-v2': True,
    'detect ssl-v3': True,
    'detect tls-v1': True,
}

sslc_dict3 = {
    'action': 'delete',  # action option can be add or delete
    'black_name': ['black1.local1', 'black2.local2', 'black3.local3'],
    'white_name': ['white1.local1', 'white2.local1', 'white3.local1'],
}
#output6_0 = fwsettingssslcontrol.show_ssl_control()
#output6_1 = fwsettingssslcontrol.set_ssl_control(**sslc_dict0)
#output6_2 = fwsettingssslcontrol.set_ssl_control_action(**sslc_dict1)
#output6_3 = fwsettingssslcontrol.config_ssl_control(**sslc_dict2)
#output6_4 = fwsettingssslcontrol.config_ssl_customlists(**sslc_dict3)
#print('-------------------output:start-------------------')
#print(output6_0)
#print(output6_1)
#print(output6_2)
#print(output6_3)
#print(output6_4)
#print('--------------------output:end--------------------')
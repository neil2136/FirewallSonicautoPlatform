import sys
import os
sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
from utm import Firewall
from modules.API.vpn import VpnbasesettingApi
from modules.API.vpn import VpnAdvancedsettingApi
from modules.API.vpn import DhcpOverVpnApi
from modules.API.vpn import L2tpServerApi

# L_ip = '192.168.168.168'
L_ip = '10.6.0.164'

R_ip = '12.12.1.201'
L_fw = Firewall(L_ip, user='admin', password='password', supported_config_mode='api')
R_fw = Firewall(R_ip, user='admin', password='password', supported_config_mode='api')



############################################################################
#######################  1. example of vpnbasesetting#######################
############################################################################


'''
##  get certinfo
cert_file = '/tmp/logs/01.pem'
command = "openssl x509 -in /tmp/logs/01.pem -noout -subject >  info"
os.system(command)
with open(r'info', 'r') as f:
    certinfo = f.read()
'''

Cert_name='my_cert'
Cert_ID='/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO'
Cert_ID='ou=gmail.com'
# Cert_ID='abc'


Local_ike_id='ipv4 12.12.1.200'  #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
local_net='local_net'
Local_group='local_group'
Local_range='192.168.168.2 192.168.168.200'   ###'local_range'
Local_host='1.1.1.1'
Local_network='192.168.168.0 255.255.255.0'     ###'local_range'

Remote_X1='12.12.1.201'
Remote_X2='12.12.2.201'

Remote_ike_id='ipv4 12.12.1.201'  #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX

Remote_net='remote_net'
Remote_group='remote_group'
Remote_range='172.16.1.1 172.16.1.123'        ###'remote_range'
Remote_host='2.2.2.2'
Remote_network='172.16.1.0 255.255.255.0'      ###'remote_range'

default_lan_gw='12.12.1.201'
hash_url='http://www.baidu.com'

s2svpn_certauth_ikev2_dict = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn1',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'default-id',   ### arg can be:default-id; distinguished_name; domain_name; email_id; ip
    'peer_ike_type': 'ip',  ### arg can be:distinguished_name; domain_name; email_id; ip
    'peer_ike_id': '1.1.1.1',
    'pri_gate': Remote_X1,
    'sec_gate': Remote_X2,
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'X0 Subnet',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,

    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'remote_net',
    # 'remote_net_group': Remote_group,
    # 'remote_net_host': Remote_host,
    # 'remote_net_network': Remote_network,
    # 'remote_net_range': Remote_range,

    ### proposal setting ######
    'ike_exchange': 'ikev2',
    'ike_dh_group': '2',
    'ike_encryption': 'aes-128',
    'ike_auth': 'sha-1',
    'ike_lifetime': '28800',
    'ipsec_protocol': 'esp',         ### esp, ah
    'ipsec_encryption': 'aes_128',   ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
                                     ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    'ipsec_lifetime': '28800',
    'ipsec_pfs': ['dh_group', '19'],


    ## advanced setting #####
    # 'netbios': False,
    'anti_replay': True,
    'wxa_group': 'Group One',
    'multicast': True,
    'ocsp_checking': True,
    'ocsp_resp_url': 'http://www.sonicwall.com/ocsp',
    'management_https': True,
    'management_ssh': True,
    'management_snmp': True,
    'keep_alive': True,
    'allow_sonicpointn_layer3': True,
    'user_login_http': True,
    'user_login_https': True,
    'default_lan_gateway': default_lan_gw,        #arg=gw or none
    'bound_to': ['interface', 'X1'],     ##['zone', 'WAN']
    'suppress_auto_add_rule': True,
    'apply_nat': True,
    'nat_local_type': 'name',  # name, group, host, network, range, original
    'nat_local_name': 'X0 Subnet',
    # 'nat_local_group': Local_group,
    # 'nat_local_host': Local_host,
    # 'nat_local_network': Local_network,
    # 'nat_local_range': Local_range,
    
    'nat_remote_type': 'name',  # name, group, host, network, range, original
    'nat_remote_name': 'remote_net',
    # 'nat_remote_group': Remote_group,
    # 'nat_remote_host': Remote_host,
    # 'nat_remote_network': Remote_network,
    # 'nat_remote_range': Remote_range,
    
    'suppress_trigger_packet': True,    ### for site-to-site ikev2
    'accept_hash': True,                ### for site-to-site ikev2
    'send_hash': 'http://www.example.com/products/',   ### for site-to-site ikev2
}



s2svpn_certauth_main_aggressive_dict = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 's2svpn2',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'default-id',   ### arg can be:default-id; distinguished_name; domain_name; email_id; ip
    'peer_ike_type': 'ip',  ### arg can be:distinguished_name; domain_name; email_id; ip
    'peer_ike_id': '1.1.1.1',
    'pri_gate': Remote_X1,
    'sec_gate': Remote_X2,
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'X0 Subnet',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,

    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'IP Sec',
    # 'remote_net_group': Remote_group,
    # 'remote_net_host': Remote_host,
    # 'remote_net_network': Remote_network,
    # 'remote_net_range': Remote_range,

    # ### proposal setting ######
    # 'ike_exchange': 'aggressive',  ### main, aggressive
    # 'ike_dh_group': '2',
    # 'ike_encryption': 'aes-128',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': '28800',
    # 'ipsec_protocol': 'esp',         ###esp, ah
    # 'ipsec_encryption': 'aes_128',   ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    #                                  ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': '28800',
    # 'ipsec_pfs': False,
    # 'ipsec_pfs_dhgroup': 2,
    #
    #
    # ## advanced setting #####
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'multicast': True,
    # 'ocsp_checking': True,
    # 'ocsp_resp_url': 'http://www.sonicwall.com/ocsp',
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'keep_alive': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'default_lan_gateway': default_lan_gw,        #arg=gw or none
    # 'bound_to': ['interface', 'X0'],     ##['zone', 'WAN']
    # 'suppress_auto_add_rule': True,
    # 'apply_nat': True,
    # 'nat_local_type': 'name',  # name, group, host, network, range, original
    # 'nat_local_name': 'X0 Subnet',
    # # 'nat_local_group': Local_group,
    # # 'nat_local_host': Local_host,
    # # 'nat_local_network': Local_network,
    # # 'nat_local_range': Local_range,
    #
    # 'nat_remote_type': 'name',  # name, group, host, network, range, original
    # 'nat_remote_name': 'remote_net',
    # # 'nat_remote_group': Remote_group,
    # # 'nat_remote_host': Remote_host,
    # # 'nat_remote_network': Remote_network,
    # # 'nat_remote_range': Remote_range,
    # 'require_xauth':'Everyone',   ##for site-to-site main/aggressive
}

s2svpn_secretauth_ikev2_dict = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 's2svpn3',
    'enable': True,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    'secret': '123456',  # add local cert
    'local_ike_type': 'ipv4',   ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'local_ike_id': '1.1.1.1',
    'peer_ike_id': '2.2.2.2',    
    'pri_gate': Remote_X1,
    'sec_gate': Remote_X2,
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'X0 Subnet',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,

    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'test12345',
    # 'remote_net_group': Remote_group,
    # 'remote_net_host': Remote_host,
    # 'remote_net_network': Remote_network,
    # 'remote_net_range': Remote_range,

    # ### proposal setting ######
    # 'ike_exchange': 'ikev2',
    # 'ike_dh_group': '2',
    # 'ike_encryption': 'aes-128',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': '28800',
    # 'ipsec_protocol': 'esp',         ### esp, ah
    # 'ipsec_encryption': 'aes_128',   ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    #                                  ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': '28800',
    # 'ipsec_pfs': False,
    # 'ipsec_pfs_dhgroup': 2,    
    #
    # ## advanced setting #####
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'multicast': True,
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'keep_alive': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'default_lan_gateway': default_lan_gw,        #arg=gw or none
    # 'bound_to': ['interface', 'X0'],     ##['zone', 'WAN']
    # 'suppress_auto_add_rule': True,
    # 'apply_nat': True,
    # 'nat_local_type': 'name',  # name, group, host, network, range, original
    # 'nat_local_name': 'X0 Subnet',
    # # 'nat_local_group': Local_group,
    # # 'nat_local_host': Local_host,
    # # 'nat_local_network': Local_network,
    # # 'nat_local_range': Local_range,
    #
    # 'nat_remote_type': 'name',  # name, group, host, network, range, original
    # 'nat_remote_name': 'remote_net',
    # # 'nat_remote_group': Remote_group,
    # # 'nat_remote_host': Remote_host,
    # # 'nat_remote_network': Remote_network,
    # # 'nat_remote_range': Remote_range,
    #
    # 'suppress_trigger_packet': True,    ### for site-to-site ikev2
    # 'accept_hash': True,                ### for site-to-site ikev2
    # 'send_hash': 'http://www.example.com/products/',   ### for site-to-site ikev2
}

s2svpn_secretauth_main_aggressive_dict = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn1',
    'enable': True,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    'secret': '123456',  # add local cert
    'local_ike_type': 'ipv4',   ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'local_ike_id': '1.1.1.1',
    'peer_ike_id': '2.2.2.2',   
    'pri_gate': Remote_X1,
    'sec_gate': Remote_X2,
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'X0 Subnet',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,

    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'remote_net',
    'remote_net_group': Remote_group,
    'remote_net_host': Remote_host,
    'remote_net_network': Remote_network,
    'remote_net_range': Remote_range,

    # ### proposal setting ######
    # 'ike_exchange': 'aggressive',  ### main, aggressive
    # 'ike_dh_group': '2',
    # 'ike_encryption': 'aes-128',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': 28800,
    # 'ipsec_protocol': 'esp',         ###esp, ah
    # 'ipsec_encryption': 'aes_128',   ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    #                                  ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': 28800,
    # 'ipsec_pfs': True,
    # 'ipsec_pfs_dhgroup': '19',
    #
    #
    # ## advanced setting #####
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'multicast': True,
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'keep_alive': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'default_lan_gateway': default_lan_gw,        #arg=gw or none
    # 'bound_to': ['interface', 'X0'],     ##['zone', 'WAN']
    # 'suppress_auto_add_rule': True,
    # 'apply_nat': True,
    # 'nat_local_type': 'name',  # name, group, host, network, range, original
    # 'nat_local_name': 'X0 Subnet',
    # # 'nat_local_group': Local_group,
    # # 'nat_local_host': Local_host,
    # # 'nat_local_network': Local_network,
    # # 'nat_local_range': Local_range,
    #
    # 'nat_remote_type': 'name',  # name, group, host, network, range, original
    # 'nat_remote_name': 'remote_net',
    # # 'nat_remote_group': Remote_group,
    # # 'nat_remote_host': Remote_host,
    # # 'nat_remote_network': Remote_network,
    # # 'nat_remote_range': Remote_range,
    # 'require_xauth': 'Everyone',   ##for site-to-site main/aggressive
}


s2svpn_manualkeyauth_dict = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn1',
    'enable': True,
    'auth_mode': 'manual',  # certificate or shared-secret   
    'pri_gate': Remote_X1,
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'X0 Subnet',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,

    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'remote_net',
    # 'remote_net_group': Remote_group,
    # 'remote_net_host': Remote_host,
    # 'remote_net_network': Remote_network,
    # 'remote_net_range': Remote_range,

    # # ### proposal setting ######
    # 'ipsec_protocol': 'esp',         ###esp, ah
    # 'ipsec_encryption': 'aes_128',   ###
    # 'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'in_spi': '0xaa1254cd',       ###  3-8 bit Hexa characters
    # 'out_spi': '0xacd12345',      ###  3-8 bit Hexa characters
    # 'encryption_key': '12345652212545221234565221254522',   ###  16 bit Hexa characters
    # 'authentication_key': 'aa1254cdaa1254cdaa1254cdaa1254cdaa1254cd',    ### 40 bit Hexa characters
    #
    # ## advanced setting #####
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'default_lan_gateway': default_lan_gw,        #arg=gw or none
    # 'bound_to': ['interface', 'X0'],     ##['zone', 'WAN']
    # 'suppress_auto_add_rule': True,
    # 'apply_nat': True,
    # 'nat_local_type': 'name',  # name, group, host, network, range, original
    # 'nat_local_name': 'X0 Subnet',
    # # 'nat_local_group': Local_group,
    # # 'nat_local_host': Local_host,
    # # 'nat_local_network': Local_network,
    # # 'nat_local_range': Local_range,
    #
    # 'nat_remote_type': 'name',  # name, group, host, network, range, original
    # 'nat_remote_name': 'remote_net',
    # # 'nat_remote_group': Remote_group,
    # # 'nat_remote_host': Remote_host,
    # # 'nat_remote_network': Remote_network,
    # # 'nat_remote_range': Remote_range,
}

################################################################
############## tunnel vpn examples #############################
################################################################

tunnelvpn_certauth_ikev2_dict = {
    'type': 'tunnel_interface',  # site-to-site, tunnel_interface
    'name': 'tunnelvpn1',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'default-id',  ### arg can be:default-id; distinguished_name; domain_name; email_id; ip
    'peer_ike_type': 'ip',  ### arg can be:distinguished_name; domain_name; email_id; ip
    'peer_ike_id': '1.1.1.1',
    'pri_gate': Remote_X1,

    ### proposal setting ######
    'ike_exchange': 'ikev2',
    'ike_dh_group': '2',
    'ike_encryption': 'aes-128',
    'ike_auth': 'sha-1',
    'ike_lifetime': '28800',
    'ipsec_protocol': 'esp',  ### esp, ah
    'ipsec_encryption': 'aes_128',  ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    'ipsec_auth': 'sha_1',  ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    'ipsec_lifetime': '28800',
    'ipsec_pfs': False,
    'ipsec_pfs_dhgroup': 2,

    # advanced setting #####
    'netbios': False,
    'anti_replay': False,
    'wxa_group': 'Group One',
    'multicast': False,
    'ocsp_checking': False,
    'ocsp_resp_url': 'http://www.sonicwall.com/ocsp',
    'management_https': False,
    'management_ssh': False,
    'management_snmp': False,
    'keep_alive': False,
    'allow_sonicpointn_layer3': False,
    'user_login_http': False,
    'user_login_https': False,
    'bound_to': ['interface', 'X1'],  ##['zone', 'WAN']
    'suppress_trigger_packet': False,                    ### for tunnel  ikev2
    'accept_hash': False,                                ### for tunnel  ikev2
    # 'send_hash': 'http://www.example.com/products/',    ### for tunnel  ikev2
    'advanced_routing': False,
}

tunnelvpn_certauth_main_aggressive_dict = {
    'type': 'tunnel_interface',  # site-to-site, tunnel_interface
    'name': 'tunnelvpn2',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'default-id',  ### arg can be:default-id; distinguished_name; domain_name; email_id; ip
    'peer_ike_type': 'ip',  ### arg can be:distinguished_name; domain_name; email_id; ip
    'peer_ike_id': '1.1.1.1',
    'pri_gate': Remote_X1,

    # ### proposal setting ######
    # 'ike_exchange': 'main',
    # 'ike_dh_group': '2',
    # 'ike_encryption': 'aes-128',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': '28800',
    # 'ipsec_protocol': 'esp',  ### esp, ah
    # 'ipsec_encryption': 'aes_128',  ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    # ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',  ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': '28800',
    # 'ipsec_pfs': False,
    # 'ipsec_pfs_dhgroup': 2,
    #
    # ## advanced setting #####
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'multicast': True,
    # 'ocsp_checking': True,
    # 'ocsp_resp_url': 'http://www.sonicwall.com/ocsp',
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'keep_alive': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'bound_to': ['interface', 'X0'],  ##['zone', 'WAN']
    # 'advanced_routing': True,
    # 'transport_mode': True                 ### for tunnel  main/aggressive
}


tunnelvpn_secretauth_ikev2_dict = {
    'type': 'tunnel_interface',  # site-to-site, tunnel_interface
    'name': 'tunnelvpn3',
    'enable': True,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    'secret': '123456',  # add local cert
    'local_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'local_ike_id': '1.1.1.1',
    'peer_ike_id': '2.2.2.2',
    'pri_gate': Remote_X1,

    # ### proposal setting ######
    # 'ike_exchange': 'ikev2',
    # 'ike_dh_group': '2',
    # 'ike_encryption': 'aes-128',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': '28800',
    # 'ipsec_protocol': 'esp',  ### esp, ah
    # 'ipsec_encryption': 'aes_128',  ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    # ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',  ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': '28800',
    # 'ipsec_pfs': False,
    # 'ipsec_pfs_dhgroup': 2,
    #
    # ## advanced setting #####
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'multicast': True,
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'keep_alive': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'bound_to': ['interface', 'X0'],  ##['zone', 'WAN']
    # 'suppress_trigger_packet': True,                    ### for tunnel  ikev2
    # 'accept_hash': True,                                ### for tunnel  ikev2
    # 'send_hash': 'http://www.example.com/products/',    ### for tunnel  ikev2
    # 'advanced_routing': True,
}

tunnelvpn_secretauth_main_aggressive_dict = {
    'type': 'tunnel_interface',  # site-to-site, tunnel_interface
    'name': 'tunnelvpn4',
    'enable': True,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    'secret': '123456',  # add local cert
    'local_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'local_ike_id': '1.1.1.1',
    'peer_ike_id': '2.2.2.2',
    'pri_gate': Remote_X1,

    # ### proposal setting ######
    # 'ike_exchange': 'main',
    # 'ike_dh_group': '2',
    # 'ike_encryption': 'aes-128',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': '28800',
    # 'ipsec_protocol': 'esp',  ### esp, ah
    # 'ipsec_encryption': 'aes_128',  ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    # ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',  ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': '28800',
    # 'ipsec_pfs': False,
    # 'ipsec_pfs_dhgroup': 2,
    #
    # ## advanced setting #####
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'multicast': True,
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'keep_alive': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'bound_to': ['interface', 'X0'],  ##['zone', 'WAN']
    # 'advanced_routing': True,
    # 'transport_mode': True                 ### for tunnel  main/aggressive
}

tunnelvpn_manualkeyauth_dict = {
    'type': 'tunnel_interface', 
    'name': 'tunnelvpn5',
    'enable': True,
    'auth_mode': 'manual',  # certificate or shared-secret   
    'pri_gate': '100.100.100.10',

    # # ### proposal setting ######
    # 'ipsec_protocol': 'esp',         ###esp, ah
    # 'ipsec_encryption': 'aes_128',   ###
    # 'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'in_spi': '0xaa1254cd',       ###  3-8 bit Hexa characters
    # 'out_spi': '0xacd12345',      ###  3-8 bit Hexa characters
    # 'encryption_key': '12345652212545221234565221254522',   ###  16 bit Hexa characters
    # 'authentication_key': 'aa1254cdaa1254cdaa1254cdaa1254cdaa1254cd',    ### 40 bit Hexa characters
    #
    # ## advanced setting #####
    # # 'netbios': False,
    # # 'wxa_group': 'Group One',
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'bound_to': ['interface', 'X0'],     ##['zone', 'WAN']
}


Vpnbasesetting = VpnbasesettingApi(L_fw)


####################   s2s vpn      #############################
#################################################################
# rc = Vpnbasesetting.del_s2svpn_policy(**s2svpn_certauth_ikev2_dict)

# rc = Vpnbasesetting.edit_vpn_policy(**s2svpn_certauth_ikev2_dict)


### s2s vpn policy
# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_certauth_ikev2_dict)
# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_certauth_main_aggressive_dict)
# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_secretauth_ikev2_dict)

# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_secretauth_main_aggressive_dict)
# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_manualkeyauth_dict)

#############  show && delete  #############
# rc = Vpnbasesetting.show_s2svpnpolicy()
# rc = Vpnbasesetting.del_tunnelvpn_policy(**tunnelvpn_certauth_ikev2_dict)



############################  tunnel vpn ##########################
# #################################################################
# ### tunnel vpn policy

# rc = Vpnbasesetting.add_vpn_policy(**tunnelvpn_certauth_ikev2_dict)
# rc = Vpnbasesetting.add_vpn_policy(**tunnelvpn_certauth_main_aggressive_dict)
# rc = Vpnbasesetting.add_vpn_policy(**tunnelvpn_secretauth_ikev2_dict)
# rc = Vpnbasesetting.add_vpn_policy(**tunnelvpn_secretauth_main_aggressive_dict)
# rc = Vpnbasesetting.add_vpn_policy(**tunnelvpn_manualkeyauth_dict)

#############  show && delete  #############
# rc = Vpnbasesetting.del_tunnelvpn_policy(**tunnelvpn_manualkeyauth_dict)
# rc = Vpnbasesetting.show_tunnelvpnpolicy()
#
#
# if rc:
#     print('Config s2svpn success')
# else:
#     print('Config s2svpn fail')


########################################################################
########################################################################
##################### examples of edit s2s vpn policy ##################

edit_s2svpn_dict = {
    'type': 'site_to_site',  # site_to_site, tunnel_interface
    'name': 'vpn1',
    # 'new_name': 's2svpn1_new',
    # 'pri_gate': Remote_X1,
    # 'sec_gate': Remote_X2,

    'edit_auth': False,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    # 'secret': '123456',  # add local cert
    # 'local_ike_type': 'ipv4',   ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    # 'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    # 'local_ike_id': '1.1.1.1',
    # 'peer_ike_id': '2.2.2.2',

    'edit_network': False,
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'X0 Subnet',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,
    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'remote_net',
    # 'remote_net_group': Remote_group,
    # 'remote_net_host': Remote_host,
    # 'remote_net_network': Remote_network,
    # 'remote_net_range': Remote_range,

    # 'edit_proposal': True,
    'ike_exchange': 'main',  ### main, aggressive
    # 'ike_dh_group': '19',
    # 'ike_encryption': 'aes-256',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': 28800,
    # 'ipsec_protocol': 'ah',         ###esp, ah
    # 'ipsec_encryption': 'aes_128',   ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    #                                  ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': 28800,
    # 'ipsec_pfs': True,
    # 'ipsec_pfs_dhgroup': '2',
    #
    #
    # 'edit_advanced': True,
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'multicast': True,
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'keep_alive': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'default_lan_gateway': default_lan_gw,        #arg=gw or none
    # 'bound_to': ['zone', 'WAN'],     ##['interface', 'X0'] ['zone', 'WAN']
    # 'suppress_auto_add_rule': True,

    # 'edit_applynat': True,
    # 'apply_nat': True,
    # 'nat_local_type': 'name',  # name, group, host, network, range, original
    # 'nat_local_name': 'X0 Subnet',
    # # 'nat_local_group': Local_group,
    # # 'nat_local_host': Local_host,
    # # 'nat_local_network': Local_network,
    # # 'nat_local_range': Local_range,
    #
    # 'nat_remote_type': 'name',  # name, group, host, network, range, original
    # 'nat_remote_name': 'remote_net',
    # # 'nat_remote_group': Remote_group,
    # # 'nat_remote_host': Remote_host,
    # # 'nat_remote_network': Remote_network,
    # # 'nat_remote_range': Remote_range,
    # 'require_xauth': 'Everyone',   ##for site-to-site main/aggressive
}

edit_tunnelvpn_dict = {
    'type': 'tunnel_interface',  # site-to-site, tunnel_interface
    'name': 'tunnelvpn1',
    # 'pri_gate': Remote_X1,

    # 'edit_auth': True,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    # 'secret': '123456',  # add local cert
    # 'local_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    # 'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    # 'local_ike_id': '1.1.1.1',
    # 'peer_ike_id': '2.2.2.2',

    # 'edit_proposal': True,
    'ike_exchange': 'main',
    # 'ike_dh_group': '19',
    # 'ike_encryption': 'aes-256',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': '28800',
    # 'ipsec_protocol': 'ah',     ### esp, ah
    # 'ipsec_encryption': 'aes_128',  ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
    #                                 ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',      ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': '28800',
    # 'ipsec_pfs': False,
    # 'ipsec_pfs_dhgroup': 19,

    # 'edit_advanced': True,
    # # 'netbios': False,
    # 'anti_replay': True,
    # 'wxa_group': 'Group One',
    # 'multicast': True,
    # 'management_https': True,
    # 'management_ssh': True,
    # 'management_snmp': True,
    # 'keep_alive': True,
    # 'allow_sonicpointn_layer3': True,
    # 'user_login_http': True,
    # 'user_login_https': True,
    # 'bound_to': ['interface', 'X1'],  ##['zone', 'WAN']
    # 'advanced_routing': True,
    # 'transport_mode': True                 ### for tunnel  main/aggressive
}


edit_ipv6_dict = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'ipv6vpn1',
    'pri_gate': '11::11',
    'sec_gate': '12::11',

    # 'edit_auth': True,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    # 'secret': '123456',  # add local cert
    # 'local_ike_type': 'ipv4',   ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    # 'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    # 'local_ike_id': '1.1.1.1',
    # 'peer_ike_id': '2.2.2.2',
    # 'pri_gate': '100::10:11',
    # 'sec_gate': '100::20:11',

    # 'edit_network': True,
    # 'local_net_type': 'name',  ### name, group, host, network, range
    # 'local_net_name': 'test123456',
    # # 'local_net_group': Local_group,
    # # 'local_net_host': Local_host,
    # # 'local_net_network': Local_network,
    # # 'local_net_range': Local_range,
    # 'remote_net_type': 'name',  # name, group, host, network, range
    # 'remote_net_name': 'test123456',
    # # 'remote_net_group': Remote_group,
    # # 'remote_net_host': Remote_host,
    # # 'remote_net_network': Remote_network,
    # # 'remote_net_range': Remote_range,

    # 'edit_proposal': True,
    # 'ike_exchange': 'ikev2',
    # 'ike_dh_group': '19',
    # 'ike_encryption': 'aes-256',
    # 'ike_auth': 'sha-1',
    # 'ike_lifetime': '28800',
    # 'ipsec_protocol': 'esp',         ### esp, ah
    # 'ipsec_encryption': 'aes_128',   ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
                                     ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    # 'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    # 'ipsec_lifetime': '28800',
    # 'ipsec_pfs': True,
    # 'ipsec_pfs_dhgroup': 19,


    # 'edit_advanced': True,
    # 'anti_replay': False,
    # 'management_https': False,
    # 'management_ssh': False,
    # 'management_snmp': True,
    # 'keep_alive': False,
    # 'allow_sonicpointn_layer3': False,
    # 'bound_to': ['interface', 'X1'],     ##['zone', 'WAN']
    # 'local_ip': ['primary', 'true'],       ##['primary', 'true']  or ['custom', '100.100.100.10']
    # 'suppress_trigger_packet': False,    ### for site-to-site ikev2
    # 'accept_hash': False,                ### for site-to-site ikev2
    # 'send_hash': 'http://www.example.com/products/',   ### for site-to-site ikev2
}


####################  edit existed vpn      #############################
#################################################################
### s2s vpn policy
# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_certauth_ikev2_dict)
# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_certauth_main_aggressive_dict)
# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_secretauth_ikev2_dict)

# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_secretauth_main_aggressive_dict)
# rc = Vpnbasesetting.add_vpn_policy(**s2svpn_manualkeyauth_dict)

#############  show && delete  #############
# rc = Vpnbasesetting.show_s2svpnpolicy()
# rc = Vpnbasesetting.del_s2svpn_policy(**s2svpn_secretauth_ikev2_dict)

###########  edit vpn policy ############
# rc = Vpnbasesetting.edit_vpn_policy(**edit_s2svpn_dict)
# rc = Vpnbasesetting.edit_vpn_policy(**edit_tunnelvpn_dict)



# rc = Vpnbasesetting.edit_ipv6_vpn_policy(**edit_ipv6_dict)



###########################################################################
############################# example of ipv6 s2s vpn######################
ipv6_s2svpn_certauth_ikev2_dict = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'ipv6vpn1',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'default-id',   ### arg can be:default-id; distinguished_name; domain_name; email_id; ip
    'peer_ike_type': 'ip',  ### arg can be:distinguished_name; domain_name; email_id; ip
    'peer_ike_id': '1.1.1.1',
    'pri_gate': '11::11',
    'sec_gate': '12::11',
    'local_net_type': 'name',  ### name, group, host, network, range
    'local_net_name': 'test123456',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,

    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'test123456',
    # 'remote_net_group': Remote_group,
    # 'remote_net_host': Remote_host,
    # 'remote_net_network': Remote_network,
    # 'remote_net_range': Remote_range,

    ### proposal setting ######
    'ike_exchange': 'ikev2',
    'ike_dh_group': '2',
    'ike_encryption': 'aes-128',
    'ike_auth': 'sha-1',
    'ike_lifetime': '28800',
    'ipsec_protocol': 'ah',         ### esp, ah
    'ipsec_encryption': 'aes_128',   ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
                                     ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    'ipsec_lifetime': '28800',
    'ipsec_pfs': True,
    'ipsec_pfs_dhgroup': 19,


    ## advanced setting #####
    'anti_replay': True,
    'management_https': True,
    'management_ssh': True,
    'management_snmp': True,
    'keep_alive': True,
    'allow_sonicpointn_layer3': True,
    'bound_to': ['interface', 'X0'],     ##['zone', 'WAN']
    'local_ip': ['primary', 'true'],       ##['primary', 'true']  or ['custom', '100.100.100.10']  
    'suppress_trigger_packet': True,    ### for site-to-site ikev2
    'accept_hash': True,                ### for site-to-site ikev2
    'send_hash': 'http://www.example.com/products/',   ### for site-to-site ikev2
}

ipv6_s2svpn_secretauth_ikev2_dict = {
    'type': 'site_to_site',  # only site-to-site type
    'name': 'ipv6vpn1',
    'enable': True,
    'auth_mode': 'shared_secret',  # certificate or shared-secret
    'secret': '123456',  # add local cert
    'local_ike_type': 'ipv4',   ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
    'local_ike_id': '1.1.1.1',
    'peer_ike_id': '2.2.2.2',    
    'pri_gate': '100::10:11',
    'sec_gate': '100::20:11',
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'test123456',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,

    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'test123456',
    # 'remote_net_group': Remote_group,
    # 'remote_net_host': Remote_host,
    # 'remote_net_network': Remote_network,
    # 'remote_net_range': Remote_range,

    ### proposal setting ######
    'ike_exchange': 'ikev2',
    'ike_dh_group': '2',
    'ike_encryption': 'aes-128',
    'ike_auth': 'sha-1',
    'ike_lifetime': '28800',
    'ipsec_protocol': 'esp',         ### esp, ah
    'ipsec_encryption': 'aes_128',   ###  des, triple_des,  aes_128, aes_192, aes_256, aes_gcm16_128, aes_gcm16_192
                                     ### aes_gcm16_256, aes_gmac_128, aes_gmac_192, aes_gmac_256
    'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    'ipsec_lifetime': '28800',
    'ipsec_pfs': True,
    'ipsec_pfs_dhgroup': 19,


    ## advanced setting #####
    'anti_replay': True,
    'management_https': True,
    'management_ssh': True,
    'management_snmp': True,
    'keep_alive': True,
    'allow_sonicpointn_layer3': True,
    'bound_to': ['interface', 'X0'],     ##['zone', 'WAN']
    'local_ip': ['custom', '100::100:10'],       ##['primary', 'true']  or ['custom', '100::100:10']
    'suppress_trigger_packet': True,    ### for site-to-site ikev2
    'accept_hash': True,                ### for site-to-site ikev2
    'send_hash': 'http://www.example.com/products/',   ### for site-to-site ikev2
}


ipv6_s2svpn_manualkeyauth_dict = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'ipv6vpn1',
    'enable': True,
    'auth_mode': 'manual',  # certificate or shared-secret   
    'pri_gate': Remote_X1,
    'local_net_type': 'name',  ### name, group, host, network, range, any,chcp
    'local_net_name': 'test123456',
    # 'local_net_group': Local_group,
    # 'local_net_host': Local_host,
    # 'local_net_network': Local_network,
    # 'local_net_range': Local_range,

    'remote_net_type': 'name',  # name, group, host, network, range
    'remote_net_name': 'test123456',
    # 'remote_net_group': Remote_group,
    # 'remote_net_host': Remote_host,
    # 'remote_net_network': Remote_network,
    # 'remote_net_range': Remote_range,

    # ### proposal setting ######
    'ipsec_protocol': 'esp',         ###esp, ah
    'ipsec_encryption': 'aes_128',   ###
    'ipsec_auth': 'sha_1',           ### md5, sha_1, sha_256, sha_384, sha_512, aes_xcbc
    'in_spi': '0xaa1254cd',       ###  3-8 bit Hexa characters
    'out_spi': '0xacd12345',      ###  3-8 bit Hexa characters
    'in_encryption_key': '12345652212545221234565221254522',   ###  16 bit Hexa characters
    'in_authentication_key': 'aa1254cdaa1254cdaa1254cdaa1254cdaa1254cd',    ### 40 bit Hexa characters
    'out_encryption_key': '12345652212545221234565221254522',   ###  16 bit Hexa characters
    'out_authentication_key': 'aa1254cdaa1254cdaa1254cdaa1254cdaa1254cd',    ### 40 bit Hexa characters

    ## advanced setting #####
    'management_https': True,
    'management_ssh': True,
    'management_snmp': True,
    'allow_sonicpointn_layer3': True,
    'bound_to': ['interface', 'X0'],     ##['zone', 'WAN']

}


# Vpnbasesetting = VpnbasesettingApi(L_fw)

### delete vpn
# rc = Vpnbasesetting.del_tunnelvpn_policy(**ipv6_s2svpn_certauth_ikev2_dict)
#
# if rc:
#     print('delete exited vpn success')
# else:
#     print('delete exited vpn fail')

#################################################################
### s2s vpn policy
# rc = Vpnbasesetting.add_ipv6_vpn_policy(**ipv6_s2svpn_certauth_ikev2_dict)
# rc = Vpnbasesetting.add_ipv6_vpn_policy(**ipv6_s2svpn_secretauth_ikev2_dict)
# rc = Vpnbasesetting.add_ipv6_vpn_policy(**ipv6_s2svpn_manualkeyauth_dict)

# if rc:
#     print('Config s2svpn success')
# else:
#     print('Config s2svpn fail')

##########################################################
############# example of add,edit.delet provision server vpn policy ######################
vpn_pro_server = {
    'type'              : 'provision_server',
    'name'              : 'vpn_server',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'ipversion'         : 'ipv4',
    'ap_client_id'      : 'vpn_server',
    'use_default_key'   : False,
    'secret'            :'12345',
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_name'   : Remote_net
}
vpn_pro_server_edit = {
    'type'              : 'provision_server',
    'name'              : 'vpn_server',
    'enable'            : True,
    'auth_mode'         : 'certificate',
    'ipversion'         : 'ipv4',
    'local_cert'        : 'my_cert',
    'distinguished_name'       : '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_name'   : Remote_net
}
# vpn_obj = VpnbasesettingApi(L_fw)
# ###add vpn provsion server policy
# rc = vpn_obj.add_vpn_policy(**vpn_pro_server)
# ###edit vpn provsion server policy
# rc = vpn_obj.edit_provision_vpn_policy(**vpn_pro_server_edit)
# #delete  vpn provsion server policy
# rc = vpn_obj.del_provision_server(**vpn_pro_server)


##########################################################
############# example of add,edit.delet provision client vpn policy ######################

vpn_pro_client = {
    'type'              : 'provision_client',
    'name'              : 'vpn_client',
    'enable'            : True,
    'pri_gate'          : Remote_X1,
    'user_name'         : 'user1',
    'user_password'     : '123456',
    'auth_mode'         : 'shared_secret',
    'ap_client_id'      : 'vpn_server',
    'use_default_key'   : False,
    'secret'            :'12345',
}
vpn_pro_client_edit = {
    'type'              : 'provision_client',
    'name'              : 'vpn_client',
    'enable'            : True,
    'pri_gate'          : Remote_X1,
    'user_name'         : 'user5',
    'user_password'     : '123456',
    'auth_mode'         : 'certificate',
    'local_cert'        : 'my_cert',
}

# vpn_obj = VpnbasesettingApi(L_fw)
# ###add vpn provsion client policy
# rc = vpn_obj.add_vpn_policy(**vpn_pro_client)
# ###edit vpn provsion client policy
# rc = vpn_obj.edit_provision_vpn_policy(**vpn_pro_client_edit)
# #delete vpn provsion client policy
# rc = vpn_obj.del_provision_client(**vpn_pro_client)


################################################################
################################################################
##############  VPN Advancedsetting example  ###################
vpn_advanced_setting_dict = {
    'enable': True,
    # 'firewall_identifier': 'C0EAE486F76C',
    # 'cleanup_tunnels': True,
    # 'preserve_ike_port': True,
    # 'traps_on_change': True,
    # 'nat_traversal': True,
    # 'ocsp_checking': True,
    # 'responder_url': 'http://www.sonicwall.com/ocsp',
    # 'frag_packets': True,
    # 'ignore_df_bit': True,
    # 'ike_dpd': True,
    # 'dpd_interval': '60',
    # 'dpd_trigger': '3',
    # 'idle_dpd': True,
    # 'idle_dpd_interval': '600',
    # 'dns_server': 'static',  ## inherit or static
    # 'dns_primary': '1.1.1.1',
    # 'dns_sencondary': '2.2.2.2',
    # 'dns_tertiary': '3.3.3.3',
    # 'win_primary': '10.10.10.10',
    # 'win_sencondary': '20.20.20.20',
    # 'send_cookie': True,
    # 'send_invalid_spi': True,
    # 'dh_group': '19',
    # 'encryption': 'aes-256',
    # 'authentication': 'sha-1',
    }


Vpnadvanced = VpnAdvancedsettingApi(L_fw)
#
# rc = Vpnadvanced.config_vpnadvanced(**vpn_advanced_setting_dict)
#
# if rc:
#     print('config vpn advanced setting success')
# else:
#     print('config vpn advanced setting fail')






###############################################################
###############################################################
############### example of dhcp over vpn ######################

centralgw_dict = {
    'internal_dhcp': False,
    'global_vpn': True,
    'remote': False,
    'relay_ip': '0.0.0.0',
    'send_requests': True,
    'dhcp_server_ip_list': ['2.2.2.2','10.1.1.10'],
    }

remotegw_dict = {
    'bound_to': 'X2',
    'accept_bridged_wlan_request': True,
    'relay_ip': '20.10.10.10',
    'management_ip': '200.100.100.10',
    'block_spoof': True,
    'temp_lease': True,
    'lease_time': '2',
    # 'static_device_ip_list': ['1.1.1.10','10.1.1.10'],
    # 'static_device_mac_list': ['a112412124da','acbda5115514'],
    # 'excluded_device_mac_list': ['b11231d521c5','ca123456d2f1'],
    }


DhcpOverVpn = DhcpOverVpnApi(L_fw)

# rc = DhcpOverVpn.config_dhcpvpn_centralgw(**centralgw_dict)
# rc = DhcpOverVpn.edit_dhcpvpn_centralgw(**centralgw_dict)
# rc = DhcpOverVpn.del_dhcpvpn_centralgw(**centralgw_dict)
#
#
# if rc:
#     print('config dhcpovervpn centralgw success')
# else:
#     print('config dhcpovervpn centralgw fail')


# rc = DhcpOverVpn.config_dhcpvpn_remotegw(**remotegw_dict)
# rc = DhcpOverVpn.edit_dhcpvpn_remotegw(**remotegw_dict)
# rc = DhcpOverVpn.del_dhcpvpn_remotegw(**remotegw_dict)

# rc = DhcpOverVpn.show_dhcpovervpn(**remotegw_dict)


# if rc:
#     print('config dhcpovervpn remotegw success')
# else:
#     print('config dhcpovervpn remotegw fail')




##########################################################
##########################################################
############# example of l2tpserver ######################

l2tpserver_dict = {
    'enable': False,
    'keep_alive': 60,
    # 'dns_primary': '10.10.10.10',
    # 'dns_secondary': '20.20.20.20',
    # 'wins_primary': '30.30.30.30',
    # 'wins_secondary': '40.40.40.40',
    'ip_pool': 'provided',   ### local or provided
    'ippool_begin': '100.10.10.10',
    'ippool_end': '100.10.10.100',
    # 'user_group': 'Everyone',
}

# L2tpServer = L2tpServerApi(L_fw)

# rc = L2tpServer.config_l2tpserver(**l2tpserver_dict)
# rc = L2tpServer.show_l2tpserver(**l2tpserver_dict)

# if rc:
#     print('config l2tpserver success')
# else:
#     print('config l2tpserver fail')
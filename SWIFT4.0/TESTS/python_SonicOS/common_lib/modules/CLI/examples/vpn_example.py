import sys
import os
import time

import modules.CLI.vpn
from utm import Firewall
L_ip = '192.168.168.168'
R_ip = '12.12.1.201'
L_fw = Firewall(L_ip, user='admin', password='password', supported_config_mode='cli-ssh')
R_fw = Firewall(R_ip, user='admin', password='password', supported_config_mode='cli-ssh')


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

Local_ike_id='ipv4 12.12.1.200'  #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
Local_addobj='local_net'
Local_group='local_group'
Local_range='192.168.168.100 192.168.168.200'   ###'local_range'
Local_host='192.168.168.201'
Local_network='192.168.168.0 255.255.255.0'     ###'local_range'

Remote_X1='12.12.1.201'
Remote_ike_id='ipv4 12.12.1.201'  #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
Remote_addobj='remote_net'
Remote_group='remote_group'
Remote_range='172.16.1.10 172.16.1.100'        ###'remote_range'
Remote_host='172.16.1.15'
Remote_network='172.16.1.0 255.255.255.0'      ###'remote_range'

default_lan_gw='12.12.1.201'
hash_url='http://www.baidu.com'


##### 1.1. example1 of certificate auth mode #################
localvpn_certauth_dict = {
    'type': 'site-to-site',   #site-to-site, tunnel-interface
    'name': 'vpn1',
    'mode': 'certificate',   #certificate or shared-secret
    'pri_gate': Remote_X1,
    # 'sec_gate': Remote_X2,
    'local_cert': Cert_name,         #add local cert
    'local_ike_type': 'distinguished-name', #arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type': 'distinguished-name',  #arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id': Cert_ID,
    'local_net_type': 'name',         #name, group, host, network, range, any
    'remote_net_type': 'name',        #name, group, host, network, range
    'local_network': "'X0 Subnet'",   #  X0subnet,     add_group, hostip, add_network, add_range, none
    'remote_network': Remote_addobj,  #add_remote_net, add_group, hostip, add_network, add_range
}


##### 1.2. example of shared-secret auth mode ######################+
localvpn_secretauth_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
    'name': 'vpn1',
    'mode': 'shared-secret',  # certificate or shared-secret or manual-key
    'pri_gate': Remote_X1,
    # 'sec_gate':Remote_X2,
    'secret': '123456',
    'local_ike_id': 'ipv4 12.12.1.200',   #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'peer_ike_id': 'ipv4 12.12.1.200',     #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_network': "'X0 Subnet'",
    'remote_network': Remote_addobj,  # add obj
}


##### 1.3. example of manual-key auth mode #################
localvpn_manualauth_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
    'name': 'vpn1',
    'mode': 'manual-key',  # certificate or shared-secret or manual-key
    'pri_gate': Remote_X1,
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_network': "'X0 Subnet'",
    'remote_network': Remote_addobj,  # add obj

    ####### maunal key proposal
    'proposal ipsec authentication': 'aes-xcbc',  #aes-xcbc,md5,sha-1,sha-256,sha-384,sha-512,none
    'proposal ipsec authentication-key': '0123456989abcdef0123456989abcdef',     #String of hexadecimal 32 digits
    'proposal ipsec encryption': 'des',          #aes,des,none
    'proposal ipsec encryption-key': '0123456989abcdef0123456989abcdef',     #String of hexadecimal 32 digits
    'proposal ipsec in-spi': '0xaa55aa55',   #Hexadecimal integer in the form: 0xHHHHHHHH
    'proposal ipsec out-spi': '0xaa55aa55',  #Hexadecimal integer in the form: 0xHHHHHHHH
    'proposal ipsec protocol': 'ah',         #ah, esp

    ### maunal key advanced
    'suppress-auto-add-rule': True,
    # 'netbios': True,
    # 'wxa-group': "'Group One'",
    'nat_local_type': 'original',  # name, group, host, network, range, original
    'nat_local_network': 'network',
    'nat_remote_type': 'network',  # name, group, host, network, range, original
    'nat_remote_network': Remote_network,
    'allow-sonicpointn-layer3': True,
    'management https': True,
    'management ssh': True,
    'management snmp': True,
    'user-login http': True,
    'user-login https': True,
    'default-lan-gateway': default_lan_gw,
    'bound-to': "interface 'X1'"
}

Lvpnpolicy = modules.CLI.vpn.VpnBaseSettingsCli(L_fw)
# ### delete all vpn policy
# output1 = Lvpnpolicy.delete_allvpnpolicy()
# ### add vpn policy
# output3 = Lvpnpolicy.add_vpnpolicy(**localvpn_manualauth_dict)



##### 1.4. example of proposal && advanced setting
localvpn_proposal_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
    'name': 'vpn1',
    'mode': 'shared-secret',  # certificate or shared-secret or manual-key
    'pri_gate': Remote_X1,
    # 'sec_gate':Remote_X2,
    'secret': '123456',
    'local_ike_id': 'ipv4 12.12.1.200',   #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'peer_ike_id': 'ipv4 12.12.1.200',     #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_network': "'X0 Subnet'",
    'remote_network': Remote_addobj,  # add obj

    ####### proposal setting ######
    'proposal ike exchange': 'aggressive',   #main, aggressive, ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,

    ###### advanced setting #####
    'keep-alive':True,
    'anti-replay': True,
    # 'netbios':True,
    'multicast': True,
    'wxa-group':"'Group One'",
    #'suiteB':'',
    'nat_local_type': 'original',  # name, group, host, network, range, original
    'nat_local_network': 'network',
    'nat_remote_type': 'network',  # name, group, host, network, range, original
    'nat_remote_network': Remote_network,
    'OCSP': True,
    'responder-url': 'http://www.sonicwall.com/ocsp',
    'allow-sonicpointn-layer3': True,
    'management https': True,
    'management ssh': True,
    'management snmp': True,
    'user-login http': True,
    'user-login https': True,
    'bound-to': "interface 'X1'",


    ####for main/aggressive site-to-site ###

    'suppress-auto-add-rule': True,
    'require-xauth':'Everyone',
    'default-lan-gateway':default_lan_gw,        #arg=gw or none
    #######################################
    #
    # ####for main/aggressive tunnel ######
    # 'advanced-routing': True,
    # 'transport-mode':True,
    # #####################################
    
    # ####for ikev2 site-to-site ##########
    # 'suppress-trigger-packet': True,
    # 'accept-hash': True,
    # 'send-hash':hash_url,
    # 'suppress-auto-add-rule': True,
    # 'default-lan-gateway':default_lan_gw,        #arg=gw or none
    # #####################################
    
    # ####for ikev2 tunnel ################
    # 'suppress-trigger-packet': True,
    # 'accept-hash': True,
    # 'send-hash':hash_url,
    # 'advanced-routing': True,
    # #####################################
}

Lvpnpolicy = modules.CLI.vpn.VpnBaseSettingsCli(L_fw)
# ### delete all vpn policy
# output1 = Lvpnpolicy.delete_allvpnpolicy()
# ### add vpn policy
# output3 = Lvpnpolicy.add_vpnpolicy(**localvpn_proposal_dict)


#######  1.5. example of network type

localvpn_net_dict = {
    'type':'site-to-site',   #site-to-site, tunnel-interface
    'name':'vpn1',
    'mode':'certificate',   #certificate or shared-secret
    'pri_gate':Remote_X1,
    # 'sec_gate':Remote_X2,
    'local_cert':Cert_name,         #add local cert
    'local_ike_type':'distinguished-name', #arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type':'distinguished-name',  #arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id':Cert_ID,
    'local_net_type':'name',         #name, group, host, network, range, any
    'remote_net_type':'name',        #name, group, host, network, range, any
    'local_network':"'X0 Subnet'",   #  X0subnet,     add_group, hostip, add_network, add_range, none
    'remote_network':Remote_addobj,  #add_remote_net, add_group, hostip, add_network, add_range
}

#
localvpn_net_dict = {
    'type':'site-to-site',   #site-to-site, tunnel-interface
    'name':'vpn1',
    'mode':'certificate',   #certificate or shared-secret
    'pri_gate':Remote_X1,
    # 'sec_gate':Remote_X2,
    'local_cert':Cert_name,         #add local cert
    'local_ike_type':'distinguished-name', #arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type':'distinguished-name',  #arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id':Cert_ID,
    'local_net_type':'name',         #name, group, host, network, range, any
    'remote_net_type':'name',        #name, group, host, network, range, any
    'local_network':"'X0 Subnet'",   #  X0subnet,     add_group, hostip, add_network, add_range, none
    'remote_network':Remote_addobj,  #add_remote_net, add_group, hostip, add_network, add_range
}


### network group
localvpn_group_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
    'name': 'vpn1',
    'mode': 'certificate',  # certificate or shared-secret
    'pri_gate': Remote_X1,
   #'sec_gate':Remote_X2,
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'distinguished-name',  # arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type': 'distinguished-name',  # arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id': Cert_ID,
    'local_net_type':'group',         #name, group, host, network, range, any
    'remote_net_type':'group',        #name, group, host, network, range
    'local_network':Local_group,   #  X0subnet,     add_group, hostip, add_network, add_range, none
    'remote_network':Remote_group,  #add_remote_net, add_group, hostip, add_network, add_range
}
### network host
localvpn_host_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
    'name': 'vpn1',
    'mode': 'certificate',  # certificate or shared-secret
    'pri_gate': Remote_X1,
   #'sec_gate':Remote_X2,
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'distinguished-name',  # arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type': 'distinguished-name',  # arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id': Cert_ID,
    'local_net_type':'host',         #name, group, host, network, range, any
    'remote_net_type':'host',        #name, group, host, network, range
    'local_network':Local_host,   #  X0subnet,     add_group, hostip, add_network, add_range, none
    'remote_network':Remote_host,  #add_remote_net, add_group, hostip, add_network, add_range
}
### network range
localvpn_range_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
    'name': 'vpn1',
    'mode': 'certificate',  # certificate or shared-secret
    'pri_gate': Remote_X1,
   #'sec_gate':Remote_X2,
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'distinguished-name',  # arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type': 'distinguished-name',  # arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id': Cert_ID,
    'local_net_type':'range',         #name, group, host, network, range, any
    'remote_net_type':'range',        #name, group, host, network, range
    'local_network':Local_range,      #  X0subnet,     add_group, hostip, add_network, add_range, none
    'remote_network':Remote_range,    #add_remote_net, add_group, hostip, add_network, add_range
}
# ### network network
localvpn_net_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
    'name': 'vpn1',
    'mode': 'certificate',  # certificate or shared-secret
    'pri_gate': Remote_X1,
   #'sec_gate':Remote_X2,
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'distinguished-name',  # arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type': 'distinguished-name',  # arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id': Cert_ID,
    'local_net_type':'network',             #name, group, host, network, range, any
    'remote_net_type':'network',        #name, group, host, network, range
    'local_network':Local_network,      #  X0subnet,     add_group, hostip, add_network, add_range, none
    'remote_network':Remote_network,    #add_remote_net, add_group, hostip, add_network, add_range
}



####### 1.6. example of function use

# Lvpnpolicy = modules.CLI.vpn.VpnBaseSettingsCli(L_fw)
# Rvpnpolicy = modules.CLI.vpn.VpnBaseSettingsCli(R_fw)
# ## delete all vpn policy
# output1 = Lvpnpolicy.delete_allvpnpolicy()
# output2 = Rvpnpolicy.delete_allvpnpolicy()
# ### add vpn policy
# output3 = Lvpnpolicy.add_vpnpolicy(**localvpn_dict)
# output4 = Rvpnpolicy.add_vpnpolicy(**remotevpn_dict)
# ## show allvpn policy
# output7 = Lvpnpolicy.show_allvpnpolicy()
# output8 = Rvpnpolicy.show_allvpnpolicy()
# ## show vpn policy
# output7 = Lvpnpolicy.show_vpnpolicy(**localvpn_dict)
# output8 = Rvpnpolicy.show_vpnpolicy(**remotevpn_dict)
# ## ping test
# time.sleep(5)
# os.system('ping 172.16.1.15 -c 10')
# ## delete vpn policy
# output5 = Lvpnpolicy.delete_vpnpolicy(**localvpn_dict)
# output6 = Rvpnpolicy.delete_vpnpolicy(**remotevpn_dict)




Lvpnpolicy = modules.CLI.vpn.VpnBaseSettingsCli(L_fw)
# ### delete all vpn policy
# output1 = Lvpnpolicy.delete_allvpnpolicy()
# ### add vpn policy
# output3 = Lvpnpolicy.add_vpnpolicy(**localvpn_net_dict)
# # output3 = Lvpnpolicy.enable_vpnpolicy(**localvpn_dict)

### enable global vpn
# output1 = Lvpnpolicy.enable_global_vpn()
### disable global vpn
# output1 = Lvpnpolicy.disable_global_vpn()

### enable vpn policy
# output1 = Lvpnpolicy.enable_vpnpolicy(**localvpn_dict)
### disable vpn policy
# output1 = Lvpnpolicy.disable_vpnpolicy(**localvpn_dict)




######################################################################
##################### add ipv6 vpn policy ############################

##### 1.7. example of ipv6 vpn setting shared-secret auth
ipv6_local_vpn_proposal_secretauth_dict = {
    'name': 'vpn11',
    'mode': 'shared-secret',  # certificate or shared-secret
    'pri_gate': '12:1::202',
    'sec_gate': '12:2::202',
    'secret': '123456',
    'local_ike_id': 'ipv4 12.12.1.200',   #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'peer_ike_id': 'ipv4 12.12.1.200',     #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'local_net_type': 'group',
    'remote_net_type': 'name',
    'local_network': "'X0 IPv6 Addresses'",
    'remote_network': 'ipv6_remote_net',  # add obj

    ####### ipv6 vpn proposal setting ######
    'proposal ike exchange': 'ikev2',   ### ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,  ###False or dh-group num.

    ###### ipv6 vpn advanced setting #####
    'keep-alive':True,
    'anti-replay':True,
    #'suiteB':'',
    'allow-sonicpointn-layer3': True,
    'management https': True,
    'management ssh': True,
    'management snmp': True,
    'bound-to': "interface 'X1'",
    'local-ip': 'primary',        ### primary or custom 'ipv6ip'
    'preempt-secondary-gateway': '28800',        ### False or seconds
    'suppress-trigger-packet': True,
    'suppress-trigger-packet': True,
    'accept-hash': True,
    'send-hash': hash_url
}

##### 1.8. example of ipv6 vpn setting certificate auth
ipv6_local_vpn_proposal_certificate_dict = {
    'name': 'vpn11',
    'mode': 'certificate',  # certificate or shared-secret
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'distinguished-name',  # arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type': 'distinguished-name',  # arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id': Cert_ID,
    'pri_gate': '12:1::202',
    'sec_gate':'12:2::202',
    'local_net_type': 'group',
    'remote_net_type': 'name',
    'local_network': "'X0 IPv6 Addresses'",
    'remote_network': 'ipv6_remote_net',  # add obj

    ####### ipv6 vpn proposal setting ######
    'proposal ike exchange': 'ikev2',   ### ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,  ###False or dh-group num.

    ###### ipv6 vpn advanced setting #####
    'keep-alive': True,
    'anti-replay': True,
    #'suiteB':'',
    'allow-sonicpointn-layer3': True,
    'management https': True,
    'management ssh': True,
    'management snmp': True,
    'bound-to': "interface 'X1'",
    'local-ip': "custom '14::13'",        ### primary or custom ipv6ip
    'preempt-secondary-gateway':'28800',        ### False or seconds
    'suppress-trigger-packet': True,
    'suppress-trigger-packet': True,
    'accept-hash': True,
    'send-hash': hash_url
}

##### 1.9. example of ipv6 vpn setting manual-key auth
ipv6_localvpn_manualauth_dict = {
    'name': 'vpn11',
    'mode': 'manual-key',  # certificate or shared-secret
    'pri_gate': '12:1::202',
    'sec_gate': '12:2::202',
    'local_net_type': 'group',
    'remote_net_type': 'name',
    'local_network': "'X0 IPv6 Addresses'",
    'remote_network': 'ipv6_remote_net',  # add obj

    ####### ipv6 vpn proposal setting ######
    'proposal ike exchange': 'ikev2',   ### ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,  ###False or dh-group num.

    ###### ipv6 vpn advanced setting #####
    'allow-sonicpointn-layer3': True,
    'management https': True,
    'management ssh': True,
    'management snmp': True,
    'bound-to': "interface 'X1'"
}

ipv6_edit_dict = {
    'name': 'vpn11',
    'new_name': 'vpn22222',
    'mode': 'shared-secret',  # certificate or shared-secret
    'pri_gate': '12:1::202',
    'sec_gate': '12:2::202',
    'secret': '123456',
    'local_ike_id': 'ipv4 12.12.1.200',   #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'peer_ike_id': 'ipv4 12.12.1.200',     #arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'local_net_type': 'group',
    'remote_net_type': 'name',
    'local_network': "'X0 IPv6 Addresses'",
    'remote_network': 'ipv6_remote_net',  # add obj

    ####### ipv6 vpn proposal setting ######
    'proposal ike exchange': 'ikev2',   ### ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,  ###False or dh-group num.

    ###### ipv6 vpn advanced setting #####
    'keep-alive': True,
    'anti-replay':True,
    #'suiteB':'',
    'allow-sonicpointn-layer3': True,
    'management https': True,
    'management ssh': True,
    'management snmp': True,
    'bound-to': "interface 'X1'",
    'local-ip': 'primary',        ### primary or custom 'ipv6ip'
    'preempt-secondary-gateway': '28800',        ### False or seconds
    'suppress-trigger-packet': True,
    'suppress-trigger-packet': True,
    'accept-hash': True,
    'send-hash': hash_url
}

###### config ipv6 vpn
Lvpnpolicy = modules.CLI.vpn.VpnBaseSettingsCli(L_fw)
output1 = Lvpnpolicy.delete_allvpnpolicy()

# output1 = Lvpnpolicy.add_ipv6_vpnpolicy(**ipv6_local_vpn_proposal_secretauth_dict)
# output1 = Lvpnpolicy.add_ipv6_vpnpolicy(**ipv6_local_vpn_proposal_certificate_dict)
# output1 = Lvpnpolicy.add_ipv6_vpnpolicy(**ipv6_localvpn_manualauth_dict)

output1 = Lvpnpolicy.add_ipv6_vpnpolicy(**ipv6_edit_dict)


########################################################
############# 1.10. example of edit vpn policy #########

edit_vpn_dict = {
    'type': 'site-to-site',  # site-to-site, tunnel-interface
    'name': 'vpn1',
    'new_name': 'vpn2',
    'pri_gate': Remote_X1,
    # 'sec_gate':Remote_X2,

    'edit_authmode': True,
    # 'mode': 'shared-secret',  # certificate or shared-secret or manual-key
    # 'secret': '123456',
    # 'local_ike_id': 'email-address mlai@sonicwall.com',  # arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    # 'peer_ike_id': 'email-address mlai@sonicwall.com',  # arg=domian-name XXX; email-address XXX; firewall-id XXX; ipv4 XXX; key-id XXX
    'mode': 'certificate',  # certificate or shared-secret
    'local_cert': Cert_name,  # add local cert
    'local_ike_type': 'distinguished-name',  # arg can be:default-id; distinguished-name; domain-name; email-id; ip
    'peer_ike_type': 'distinguished-name',  # arg can be:distinguished-name; domain-name; email-id; ip
    'peer_ike_id': Cert_ID,

    'edit_network': True,
    ###### local&remote network #####
    'local_net_type': 'host',
    'remote_net_type': 'host',
    'local_network': Local_host,
    'remote_network': Remote_host,  # add obj

    'edit_proposal': True,
    ####### proposal setting ######
    'proposal ike exchange': 'aggressive',  # main, aggressive, ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,


    'edit_advanced': True,
    ###### advanced setting #####
    'keep-alive': False,
    'netbios': False,
    'anti-replay': True,
    'multicast': False,
    'wxa-group': "'Group One'",
    # 'suiteB':'',
    'ocsp-checking': True,
    'responder-url': 'http://www.sonicwall.com/ocsp',
    'allow-sonicpointn-layer3': True,
    'management https': False,
    'management ssh': False,
    'management snmp': False,
    'user-login http': True,
    'user-login https': True,
    'bound-to': "interface 'X1'",
    'nat_local_type': 'original',  # name, group, host, network, range, original
    'nat_local_network': Local_network,
    'nat_remote_type': 'network',  # name, group, host, network, range, original
    'nat_remote_network': Remote_network,

    ####for main/aggressive site-to-site ###
    'suppress-auto-add-rule': True,
    'require-xauth': 'Everyone',
    'default-lan-gateway': default_lan_gw,  # arg=gw or none
    #######################################
    #
    # ####for main/aggressive tunnel ######
    # 'advanced-routing': True,
    # 'transport-mode':True,
    # #####################################

    # ####for ikev2 site-to-site ##########
    # 'suppress-trigger-packet': True,
    # 'accept-hash': True,
    # 'send-hash':hash_url,
    # 'suppress-auto-add-rule': True,
    # 'default-lan-gateway':default_lan_gw,        #arg=gw or none
    # #####################################

    # ####for ikev2 tunnel ################
    # 'suppress-trigger-packet': True,
    # 'accept-hash': True,
    # 'send-hash':hash_url,
    # 'advanced-routing': True,
    # #####################################
}

###### edit a vpn policy
Lvpnpolicy = modules.CLI.vpn.VpnBaseSettingsCli(L_fw)
# output1 = Lvpnpolicy.delete_allvpnpolicy()

# output1 = Lvpnpolicy.add_vpnpolicy(**localvpn_proposal_dict)

# output1 = Lvpnpolicy.edit_vpnpolicy(**edit_vpn_dict)


############################################################################
############################################################################
############################################################################
######################  2. VpnAdvancedSetting example ######################
############################################################################


####### 2.1. example of advanced setting
vpnadvanced_dict = {
    'ike-dpd': True,
    'interval': '120',  # <3..120>
    'trigger': '10',   # <3..10>
    'idle-dpd': True,
    'idle-dpd interval': '60',  #<60..3600>
    'frag-packets': True,
    'ignore-df-bit': True,
    'nat-traversal': True,
    'cleanup-tunnels': True,
    'ocsp-checking': True,
    'responder-url': 'http://www.sonicwall.com/ocsp',
    'traps-on-change': True,
    ### dns server
    'dns server': 'static',  #inherit or static
    'dns server primary': '10.10.10.10',
    'dns server secondary': '11.11.11.10',
    'dns server tertiary': '12.12.12.10',
    ### win server
    'win primary': '100.100.100.10',
    'win secondary': '200.200.200.10',
    ### ikev2 setting
    'ikev2': True,
    'send-cookie': True,
    'send-invalid-spi': True,
    'proposal dh-group': '1',
    'proposal encryption': 'aes-256',
    'proposal authentication': 'md5',
}


####### 2.2. example of function use 
# Vpnadvanced = modules.CLI.vpn.VpnAdvancedSettingsCli(L_fw)
# output_advandseting = Vpnadvanced.vpn_advanced_setting(**vpnadvanced_dict)



############################################################################
############################################################################
############################################################################
############################################################################
######################  3. DhcpOverVpnCli example ######################
############################################################################


####### 3.1. example of DhcpOverVpnCli setting
centralgw_dict = {
    'internal-dhcp': False,
    'global-vpn': False,
    'remote': False,
    'send-requests': False,
    'dhcp-server':'100.100.100.10',
    'relay-ip': '10.10.10.10',
}
remotegw_dict = {
    'bound-to': 'X0',
    'accept-bridged-wlan-request': True,
    'relay-ip': '10.10.10.10',
    'management-ip': '20.20.20.20',
    'block-spoof': True,
    'temp-lease': True,
    'lease-time': '30',   #<1..60> 
    'static-device': '192.168.168.170 01:02:03:04:05:06', # <IPV4_HOST> <MAC>
    'excluded-device': '00:0C:F1:56:98:AD',   # <EXCLUDE_DEVICE_MAC>
}


####### 3.2. example of function use 
# DhcpOverVpn = modules.CLI.vpn.DhcpOverVpnCli(L_fw)
# output_centralgw = DhcpOverVpn.central_gw_setting(**centralgw_dict)
# output_remotegw = DhcpOverVpn.remote_gw_setting(**remotegw_dict)

# output_remotegw = DhcpOverVpn.show_dhcp_over_vpn_leases()





############################################################################
############################################################################
############################################################################
############################################################################
######################  4. VpnL2TPServerCli example ######################
############################################################################


####### 4.1. example of l2tpserver setting
l2tpserer_dict = {
    'l2tp-server': True,
    'keep-alive': '100', # <1..999>
    'dns primary': '10.10.10.10',
    'dns secondary': '11.11.11.10',
    'wins primary': '100.100.100.10',
    'wins secondary': '200.200.200.10',
    'ip-pool': 'local 20.20.20.10 20.20.20.100',   #arg: provided or local 20.20.20.10 20.20.20.100
    'user-group': 'Everyone',
}




# ####### 4.2. example of function use 
# Vpnl2tpserver = modules.CLI.vpn.VpnL2TPServerCli(L_fw)
# output_advandseting = Vpnl2tpserver.vpn_l2tpserver_setting(**l2tpserer_dict)

# output_remotegw = Vpnl2tpserver.show_vpn_l2tp_server()

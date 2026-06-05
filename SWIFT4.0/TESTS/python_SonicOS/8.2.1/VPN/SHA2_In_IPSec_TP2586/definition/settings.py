import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/SHA2_In_IPSec_TP2586')

from bin.global_settings import *
from runner.settings import logger, Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network
# from lib.modules.API import object
from lib.modules.API import log
from lib.modules.API import vpn
from lib.modules.API import system


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
RTimeObj = system.TimeApi(rt)
LRestartObj = system.RestartApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LogObj = log.LogMonitorApi(fw)
Lsetting = system.SettingApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)

# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/SHA2_In_IPSec_TP2586/testplan/SHA2_In_IPSec_TP2586.json'
ca_cert = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/SHA2_In_IPSec_TP2586/cert/rootca.pem'
local_cert =os.environ["PYTHON_SONICOS_HOME"]+'/VPN/SHA2_In_IPSec_TP2586/cert/my_cert.pfx'
#show cert cmds
show_cmds = ['show certificates status imported']

# DUT object
remote_l = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
#RemoteDUT object
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
}

# VPN policy
#########################################
#                Notice!                #
#          Key:"_"      Value:"-"       #
#       site_to_site & site-to-site     #
#         triple_des & triple-des       #
#########################################
Lvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.DUT,
    'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-256',
    'ike_auth'          : 'sha-256',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_256',
    'ipsec_lifetime'    : '28800',
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
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.REMOTEX0,
    'peer_ike_id'       : Parameter.DUT,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-256',
    'ike_auth'          : 'sha-256',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_256',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],

}
Lvpn_cert = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : "certificate",
    'pri_gate'          : Parameter.REMOTEX1,
    'local_cert'        : 'my_cert',
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : "/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO",
    'local_net_type'    : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_type'   : 'name',
    'remote_net_name'   : 'remote_net',
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-256',
    'ike_auth'          : 'sha-256',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_256',
    'ipsec_lifetime'    : '28800',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],
}
Rvpn_cert = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : "certificate",
    'pri_gate'          : Parameter.WANIP,
    'local_cert'        : 'my_cert',
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : "/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO",
    'local_net_type'    : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_type'   : 'name',
    'remote_net_name'   : 'remote_net',
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-256',
    'ike_auth'          : 'sha-256',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_256',
    'ipsec_lifetime'    : '28800',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],
}
Lvpn_Manual = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'manual',
    'secret'            : '123456',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.DUT,
    'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'encryption_key'    :'4cd0294851dfd46e8efb271f1641f788',
    'authentication_key': '7023a13a19b79295daf059a2ca00f4db3b60114c7023a13a19b79295d059a2ca',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_256',
    'in_spi'            :'0xa5ce265b',
    'out_spi'           :'0xed2fed7a',
    'ike_exchange'      : 'main',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          :["interface", 'X1'],
}
Rvpn_Manual = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'manual',
    'secret'            : '123456',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.REMOTEX0,
    'peer_ike_id'       : Parameter.DUT,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'encryption_key'    :  '4cd0294851dfd46e8efb271f1641f788',
    'authentication_key':  '7023a13a19b79295daf059a2ca00f4db3b60114c7023a13a19b79295d059a2ca',
    'ipsec_encryption'  :  'aes_128',
    'ipsec_auth'        :  'sha_256',
    'in_spi'            :'0xed2fed7a',
    'out_spi'           :'0xa5ce265b',
    'ike_exchange'      : 'main',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ["interface", 'X1'],
}
Lvpn_TI = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.DUT,
    'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : "remote_net",
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_encryption'  : 'aes_128', 
    'ipversion'          : 'ipv4', 
    'ike_auth'          : 'sha-256', 
    'ike_dh_group'      : '2', 
    'ike_lifetime'      : '28800', 
    'ipsec_lifetime'    : '28800', 
    'ipsec_protocol'    : 'esp', 
    'ipsec_auth'        : 'sha_256', 
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}
Rvpn_TI = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.REMOTEX0,
    'peer_ike_id'       : Parameter.DUT,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : "remote_net",
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_encryption'  : 'aes_128',
    'ipversion'          : 'ipv4', 
    'ike_auth'          : 'sha-256', 
    'ike_dh_group'      : '2', 
    'ike_lifetime'      : '28800', 
    'ipsec_lifetime'    : '28800', 
    'ipsec_protocol'    : 'esp', 
    'ipsec_auth'        : 'sha_256', 
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}
Lvpn_TI_Manual = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'manual',
    'secret'            : '123456',
    'pri_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.DUT,
    'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'encryption_key'    :'4cd0294851dfd46e8efb271f1641f788',
    'authentication_key': '7023a13a19b79295daf059a2ca00f4db3b60114c7023a13a19b79295d059a2ca',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_256',
    'in_spi'            :'0xa5ce265b',
    'out_spi'           :'0xed2fed7a',
    'ike_exchange'      : 'main',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          :["interface", 'X1'],
}
Rvpn_TI_Manual = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'manual',
    'secret'            : '123456',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.REMOTEX0,
    'peer_ike_id'       : Parameter.DUT,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'encryption_key'    :  '4cd0294851dfd46e8efb271f1641f788',
    'authentication_key':  '7023a13a19b79295daf059a2ca00f4db3b60114c7023a13a19b79295d059a2ca',
    'ipsec_encryption'  :  'aes_128',
    'ipsec_auth'        :  'sha_256',
    'in_spi'            :'0xed2fed7a',
    'out_spi'           :'0xa5ce265b',
    'ike_exchange'      : 'main',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ["interface", 'X1'],
}
Lvpn_TI_cert = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn',
    'enable'            : True,
    'auth_mode'         : "certificate",
    'pri_gate'          : Parameter.REMOTEX1,
    'local_cert'        : 'my_cert',
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : "/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO",
    'local_net_type'    : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_type'   : 'name',
    'remote_net_name'   : 'remote_net',
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-256',
    'ike_auth'          : 'sha-256',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_256',
    'ipsec_lifetime'    : '28800',
    'keep_alive'        : True,
    'bound_to'          : ['interface', 'X1'],
}
Rvpn_TI_cert = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn',
    'enable'            : True,
    'auth_mode'         : "certificate",
    'pri_gate'          : Parameter.WANIP,
    'local_cert'        : 'my_cert',
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : "/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO",
    'local_net_type'    : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_type'   : 'name',
    'remote_net_name'   : 'remote_net',
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-256',
    'ike_auth'          : 'sha-256',
    'ike_lifetime'      : '28800',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_256',
    'ipsec_lifetime'    : '28800',
    'keep_alive'        : True,
    'bound_to'          : ['interface', 'X1'],
}
LVPN_edit={
    'name':'vpn1',
    'type':'site_to_site',
    'edit_proposal':True,
    'auth_mode':'shared_secret',
    'ipversion':'ipv4',
    'ipsec_auth':'aes_xcbc'

}
import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/VPN_NAT')
from bin.global_settings import *

from runner.settings import logger, Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network
from lib.modules.API import object
from lib.modules.API import log
from lib.modules.API import vpn
from lib.modules.CLI.vpn import VpnBaseSettingsCli

OpenS  = Openstack(Params.testbed)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
# Rvpn_obj = VpnBaseSettingsCli(rt)

# PC SSH
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_NAT/testplan/VPN_NAT.json'

# DUT object
remote_l = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
local_Tran_l = {
    'name': 'local_Tran',
    'zone': 'LAN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCTRANSNET),
}
remote_Tran_l = {
    'name': 'remote_Tran',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMTRANSNET),
}
new_zone_l = {
    'name': 'new_zone',
    'zone': 'DMZ',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.DMZSUBNET),
}
#RemoteDUT object
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
}
local_Tran_r = {
    'name': 'local_Tran',
    'zone': 'LAN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMTRANSNET),
}
remote_Tran_r = {
    'name': 'remote_Tran',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCTRANSNET),
}
new_zone_r = {
    'name': 'new_zone',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.DMZSUBNET),
}

# GROUP
LocGroup_l = {
    'address_groups': [{
        'ipv4':{
            'name': 'lan_and_dmz',  
            'address_object': {'ipv4': [
                {'name': 'X0 Subnet'}, 
                {'name': new_zone_l['name']}
            ]}
        }
    }]
}
LocTranGroup_l = {
    'address_groups': [{
        'ipv4':{
            'name': 'LocTranGroup',  
            'address_object': {'ipv4': [
                {'name': local_Tran_l['name']}, 
                {'name': new_zone_l['name']}
            ]}
        }
    }]
}
RemTranGroup_r = {
    'address_groups': [{
        'ipv4':{
            'name': 'RemTranGroup',  
            'address_object': {'ipv4': [
                {'name': remote_Tran_r['name']}, 
                {'name': new_zone_r['name']}
            ]}
        }
    }]
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
    'bound_to'          : ['zone', 'WAN'],
    'keep_alive'        : True,
    'apply_nat'         : True,
    'nat_local_type'    : 'name',
    'nat_local_name'    : local_Tran_l['name'],
    'nat_remote_type'   : 'original',
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
    'remote_net_name'   : remote_Tran_r['name'],
    'bound_to'          : ['zone', 'WAN'],
    'keep_alive'        : True,
}
Lvpn_04 = {
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
    'local_net_type'    : 'group',                  # group
    'remote_net_type'   : 'name',         
    'local_net_group'   : LocGroup_l['address_groups'][0]['ipv4']['name'],     # lan and dmz
    'remote_net_name'   : remote_l['name'],
    'bound_to'          :['zone', 'WAN'],
    'keep_alive'        : True,
    'apply_nat'         :True,
    'nat_local_type'    : 'group',
    'nat_local_name'    : LocTranGroup_l['address_groups'][0]['ipv4']['name'],         #  group
    'nat_remote_type'   : 'original',
}
Rvpn_04 = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.REMOTEX0,
    'peer_ike_id'       : Parameter.DUT,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'group',                        # group
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_group'  : RemTranGroup_r['address_groups'][0]['ipv4']['name'],      # group
    'bound_to'          :['zone', 'WAN'],
    'keep-alive'        : True,
}
vpn_raw = {
    "local_net"  : Parameter.LOCALNET,
    "local_mask" : "255.255.255.0",
    "remote_net" : Parameter.REMOTENET,
    "remote_mask": "255.255.255.0",
    "remote_gw"  : Parameter.REMOTEX1,
}

import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/VPN_bound_to_VLAN_interface_TP2464 ')

from bin.global_settings import *
from runner.settings import logger, Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network,firewall
from lib.modules.API import vpn
from lib.modules.API import system


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
interfacev4api = network.InterfaceIPv4Api(fw)
Rinterfacev4api = network.InterfaceIPv4Api(rt)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
Lvpn_adv =  vpn.VpnAdvancedsettingApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
LpacketObj = system.PacketmonitorApi(fw)
access_rule_obj = firewall.AccessRuleApi(fw)
# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
PC2_eth1 = OpenS.get_node_interface_ip('PC2', 'eth1')
DUT_X1_IPV4 = '11.11.11.200'
DUT_X1_GW = '11.11.11.1'
DUT_X2_IPV4 = '12.12.22.200'
DUT_X3_IPV4 = '12.12.33.200'
GW_X0 = '11.11.11.101'
Remote_X1_IPV4 = '12.12.1.201'
Remote_X2_IPV4 = '12.12.2.201'
Remote_X3_IPV4 = '12.12.3.201'
Remote_X4_IPV4 = '12.12.44.201'

lx3_tag = OpenS.get_node_interface_vlan_id('UTM','X3:1')
rx2_tag = OpenS.get_node_interface_vlan_id('RemoteGEN7','X2:1')
rx4_tag = OpenS.get_node_interface_vlan_id('RemoteGEN7','X4:1')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_bound_to_VLAN_interface_TP2464/testplan/VPN_bound_to_VLAN_interface_TP2464.json'

Lx1={
    'if'     : 'X1',
    'zone'   : 'WAN',
    'mode'   : 'static',
    'ip'     : DUT_X1_IPV4,
    'mask'   : '255.255.255.0',
    'gateway': DUT_X1_GW,
    'dns1'   : Params.G_DNS1,
    'mgmt_https': True,
    'mgmt_ssh'  : True,
    'mgmt_ping' : True,
    'fragment_packets': True,
}



Lx2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUT_X2_IPV4,
            'netmask': '255.255.255.0',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }
Rx1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Remote_X1_IPV4,
            'netmask': '255.255.255.0',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
}
Rx2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '11.11.2.200',
            'netmask': '255.255.255.0',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
}
Rv2 = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag': rx2_tag,
            'zone': 'WAN',
            'mode': 'static',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'ip': Remote_X2_IPV4,
            'asymmetric_route': True,
        }
Lv3 = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': lx3_tag,
            'zone': 'WAN',
            'mode': 'static',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'ip': DUT_X3_IPV4,
            'asymmetric_route': True,
        }
Rx3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Remote_X3_IPV4,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }
Rv4 = {
            'if': 'X4',
            'type': 'vlan',
            'vlan_tag': rx4_tag,
            'zone': 'WAN',
            'mode': 'static',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'ip': Remote_X4_IPV4,
            'asymmetric_route': True,
        }
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
    'ike_exchange'      : 'aggressive',
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
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],

}
dpd={
    "ike_dpd":True
}

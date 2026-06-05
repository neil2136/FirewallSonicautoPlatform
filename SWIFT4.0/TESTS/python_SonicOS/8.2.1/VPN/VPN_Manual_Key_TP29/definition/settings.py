import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/VPN_Manual_Key_TP29')

from bin.global_settings import *
from runner.settings import logger, Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import vpn,firewall,system,network


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
LTimeObj = system.TimeApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
LpacketObj = system.PacketmonitorApi(fw)
Raccess_rule_obj = firewall.AccessRuleApi(rt)
# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')
PC1_eth0 = OpenS.get_node_interface_ip('PC1', 'eth0')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_Manual_Key_TP29/testplan/VPN_Manual_Key_TP29.json'


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
    'authentication_key': '7023a13a19b79295daf059a2ca00f4db3b60114c',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_1',
    'in_spi'            :'0xa5ce265b',
    'out_spi'           :'0xed2fed7a',
    'ike_exchange'      : 'main',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          :["interface", 'X1'],
}

Rvpn = {
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
    'authentication_key':  '7023a13a19b79295daf059a2ca00f4db3b60114c',
    'ipsec_encryption'  :  'aes_128',
    'ipsec_auth'        :  'sha_1',
    'in_spi'            :'0xed2fed7a',
    'out_spi'           :'0xa5ce265b',
    'ike_exchange'      : 'main',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ["interface", 'X1'],

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
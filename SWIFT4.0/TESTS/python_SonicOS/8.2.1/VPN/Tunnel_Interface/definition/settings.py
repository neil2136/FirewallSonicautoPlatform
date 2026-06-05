import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/Tunnel_Interface')
from bin.global_settings import *

from runner.settings import logger, Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.network import RouteCli
from lib.modules.API import object
from lib.modules.API import log
from lib.modules.API import vpn
from lib.modules.API import system
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.API import policy
from modules.API.accessrule import AccessRuleIPv4Api


OpenS  = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')

LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
LRestartObj = system.RestartApi(fw)
LIntObj = InterfaceIPv4Api(fw)
LRouteObj = RouteCli(fw_cli)
RIntObj = InterfaceCli(rmt)
RRouteObj = RouteCli(rmt)
LRoutePolicyObj = policy.RoutePolicyApi(fw)
RRoutePolicyObj = policy.RoutePolicyApi(rt)
accessRuleApi = AccessRuleIPv4Api(fw)

LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
# Rvpn_obj = vpn.VpnbasesettingApi(rt)
Rvpn_obj = VpnBaseSettingsCli(rmt)

# PC SSH
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Tunnel_Interface/testplan/tunnel_interface.json'



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
    'type'              : 'tunnel_interface',
    'name'              : 'vpn_test',
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
    # 'bound_to'          :['zone', 'WAN'],
    'keep_alive'        : True,
}
Rvpn = {
    'type'              : 'tunnel-interface',
    'name'              : 'vpn_test',
    'enable'            : True,
    'mode'              : 'shared-secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.WANIP,
    'local_ike_id'      : 'ipv4 {}'.format(Parameter.REMOTEX0),
    'peer_ike_id'       : 'ipv4 {}'.format(Parameter.DUT),
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_network'     : "'{}'".format(Parameter.REMOTESUBNET),
    'remote_network'    : remote_r['name'],
    'keep-alive'        : True,
}

LInt_tunnel = {
    'type': 'vpn_tunnel',
    'tunnel_name': 'tunnel_test',
    'vpn_policy': Lvpn['name'],
    'ip': '1.1.1.2',
    'netmask': '255.255.255.0',
    'mgmt_https': True,
}

RInt_tunnel = {
    'type': 'vpn-tunnel',
    'tunnel-name': 'tunnel_test',
    'vpn-policy': Rvpn['name'],
    'ip': '1.1.1.1',
    'netmask': '255.255.255.0',
    'mgmt_https': True,
}

LRip_opt = {
    'if': LInt_tunnel['tunnel_name'],
    'network': '1.1.1.0/24', 
    'type': 'send-receive',
    'receive-version': '2',
    'send-version': '2',
    'split': True,
    'poison': True,   
    'redistribute': True, 
}

RRip_opt = {
    'if': RInt_tunnel['tunnel-name'],
    'network': '1.1.1.0/24', 
    'type': 'send-receive',
    'receive-version': '2',
    'send-version': '2',
    'split': True,
    'poison': True,   
    'redistribute': True, 
}

LOspf_opt = {
    'if': LInt_tunnel['tunnel_name'],
    'type': 'enable',
    'network': '1.1.1.0/24',
    'redistribute': True, 
    # 'auth': 'simple',
    'password':'password',
    'area': '10',
    # 'area-type': 'stub',
    # 'mtu-ignore': True,
}

ROspf_opt = {
    'if': RInt_tunnel['tunnel-name'],
    'type': 'enable',
    'network': '1.1.1.0/24',
    'redistribute': True, 
    # 'auth': 'simple',
    'password':'password',
    'area': '10',
    # 'area-type': 'stub',
    # 'mtu-ignore': True,
}

LRoute_policy = {
    "route_policies": [{
        "ipv4": {
            "interface": "tunnel_test",
            "metric": 1,
            "source": {'name': 'X0 Subnet'},
            "destination": {'name': 'remote_net'},
            "service": {'any': True},
            "gateway": {'default': True},
            "tos": "0x00",
            "mask": "0x00",
            "distance": {"auto": True},
            "name": "static_rm",
            # "type": "standard",
            # "priority": 1,
            # "comment": "",
            # "disable_on_interface_down": True,
            # "vpn_precedence": False,
            # "auto_add_access_rules": True,
            # "probe": "",
            # "ticket": {"tag1": "","tag2": "","tag3": ""}
        }
    }]
}

RRoute_policy = {
    "route_policies": [{
        "ipv4": {
            "interface": "tunnel_test",
            "metric": 1,
            "source": {'name': 'X0 Subnet'},
            "destination": {'name': 'local_net'},
            "service": {'any': True},
            "gateway": {'default': True},
            "name": "static_local",
            # "comment": "",
            # "disable_on_interface_down": True,
            # "vpn_precedence": False,
            # "wxa_group": "",
            # "auto_add_access_rules": True,
            # "probe": ""
        }
    }]
}

access_rule_option = {
    'name': 'test_lan_vpn',
    'from': 'LAN',
    'to': 'VPN',
    'source_addr': {'name': 'X0 Subnet'},
    'dst_addr': {'name': 'tunnel_test Subnet'},
    'service': {'any': True},
    'action': 'allow',
}

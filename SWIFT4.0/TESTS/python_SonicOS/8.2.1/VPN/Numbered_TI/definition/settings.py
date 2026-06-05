from inspect import Parameter
import sys
import os
import re
import time
import copy
import requests

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/Numbered_TI')

from collections import OrderedDict
import re
import paramunittest
from nose_parameterized import parameterized
from bin.global_settings import *

from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall,FirewallAPI
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network
from lib.modules.API import object
from lib.modules.API import log
from lib.modules.API import vpn
from lib.modules.API import system,appflow, firewallsettings,firewall,highavailability
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from tools import trafficGen
from modules.CLI.system import LicenseCli


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
fw_api = FirewallAPI(Parameter.DUT)
license_obj = LicenseCli(fw_cli)
Linterface = network.InterfaceIPv4Api(fw)
Rinterface = network.InterfaceIPv4Api(rt)
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
RTimeObj = system.TimeApi(rt)
LRestartObj = system.RestartApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LogObj = log.LogMonitorApi(fw)
AuditlogObj = log.AuditlogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
LDynRouteObj = network.DynamicRoutingApi(fw)
RDynRouteObj = network.DynamicRoutingApi(rt)
LRoutePolicyObj =network.RoutePolicyApi(fw)
RRoutePolicyObj =network.RoutePolicyApi(rt)
Laccess_rule_obj = firewall.AccessRuleApi(fw)
Raccess_rule_obj = firewall.AccessRuleApi(rt)
LSNMPObj = system.SNMPApi(fw)
RSNMPObj = system.SNMPApi(rt)
LAppflowObj = appflow.AppflowsettingsApi(fw)
LflowreportObj = appflow.GmsflowreportingApi(fw)
LPackageMonitObj = system.PacketmonitorApi(fw)
RPackageMonitObj = system.PacketmonitorApi(rt)
LMulticast = firewallsettings.MulticastApi(fw)
RMulticast = firewallsettings.MulticastApi(rt)
scapyPacketObj = trafficGen.ScapyPacketSend()
natPolicyObj = network.NatpolicyApi(fw)
arpObj = network.ArpApi(fw)
LiphelperObj = network.IpHelperApi(fw)
RiphelperObj = network.IpHelperApi(rt)
LNetMonitObj = network.NetworkMonitorApi(fw)
LArpObj = network.ArpApi(fw)
LBWMObj = firewall.BandwidthObjectApi(fw)
LHASet = highavailability.SettingsApi(fw)

####add new 
Linterface_v6 = network.InterfaceIPv6Api(fw)
Lsetting = system.SettingApi(fw)

#show cert cmds
show_cmds = ['show certificates status imported']

# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC1_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
PC2 = Host(Params.testbed + '-PC2')
new_pc_ip = "192.168.101.3"

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Numbered_TI/testplan/Numbered_TI.json'
TESTPATH = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/Numbered_TI'
#NI IP
VPN_IF_IP_LOCAL = '1.1.1.2'
VPN_IF_IP_REMOTE = '1.1.1.1'
VPN_IF_NET = '1.1.1.0/24'
VPN_BGP_IP_LOCAL = '2.2.2.3'
VPN_BGP_IP_REMOTE = '2.2.2.5'

# DUT local and remote object
local_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
#RemoteDUT local and remote object
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
}
# Add DUT NAT object
trans_net = {
    'name': 'translated_vpnnet',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '192.168.101.0,255.255.255.0',
}
#Add remote PC(PC2) address
remote_pc = {
    'name': 'vpn_host',
    'zone': 'VPN',
    'object_type': 'host',
    'value': '172.16.1.3',
}
#Config Remote and Local Interface x0,x1
Lx1 = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': Parameter.WANIP,
        'netmask': '255.255.255.0',
        'gateway': Parameter.WANGW,
        'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
Lx0 = {
        'if'     : 'X0',
        'zone'   : 'LAN',
        'mode'   : 'static',
        'ip'     : '192.168.168.168',
        'mask'   : '255.255.255.0',
        'gateway': '0.0.0.0',
        'mgmt_https': True,
        'mgmt_ssh'  : True,
        'mgmt_ping' : True,
        'mgmt_snmp': True,
        "multicast": True,
    }
Rx1 = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': Parameter.REMOTEX1,
        'netmask': '255.255.255.0',
        'gateway': Parameter.WANGW,
        'dns1': Params.G_DNS1,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
            
    }
Rx0 = {
        'if'     : 'X0',
        'zone'   : 'LAN',
        'mode'   : 'static',
        'ip'     : '172.16.1.101',
        'mask'   : '255.255.255.0',
        'gateway': '0.0.0.0',
        'mgmt_https': True,
        'mgmt_ssh'  : True,
        'mgmt_ping' : True,
        'mgmt_snmp': True,
        "multicast": True,
    }
#config snmp group,user,access 
snmp_user = {
            'snmp': {
                'user': [
                    {
                    'name': 'vpntc23user',
                    'security_level': {},
                    'group': 'g1'
                    }
                ]
            }
        }
snmp_access = {'snmp': {
                'access': [
                    {
                        'name': 'tc23_access',
                        'security_level': {},
                        'read_view': 'root',
                        'master_group': 'g1'
                    }
                ]
            }
        }
#config NAT access rule
nat_lan2vpn = {
            "name": "nat_lan2vpn",
            "action": "allow",
            "enable": True,
            "from": "LAN",
            "source": {"address": {"name": "X0 Subnet"}},
            "to": "VPN",
            "destination": {"address": {"name": trans_net["name"]}},
            "service": {"any": True},
            "geo_ip_filter": {"enable": False},
    }
nat_vpn2lan = {
            "name": "nat_vpn2lan",
            "action": "allow",
            "enable": True,
            "from": "VPN",
            "source": {"address": {"name": trans_net["name"]}},
            "to": "LAN",
            "destination": {"address": {"name": "X0 Subnet"}},
            "service": {"any": True},
            "geo_ip_filter": {"enable": False},
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
    'name'              : 'test',
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
    'ike_auth'          : 'sha-1', 
    'ike_dh_group'      : '2', 
    'ike_lifetime'      : '28800', 
    'ipsec_lifetime'    : '28800', 
    'ipsec_protocol'    : 'esp', 
    'ipsec_auth'        : 'sha_1', 
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}
Rvpn = {
    'type'              : 'tunnel_interface',
    'name'              : 'test',
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
    'ike_auth'          : 'sha-1', 
    'ike_dh_group'      : '2', 
    'ike_lifetime'      : '28800', 
    'ipsec_lifetime'    : '28800', 
    'ipsec_protocol'    : 'esp', 
    'ipsec_auth'        : 'sha_1', 
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}
Tunnel_Interface = {
            'zone'          : 'VPN',
            'type'          : "vpn_tunnel",
            'mode'          : 'static',
            'ip'            : VPN_IF_IP_LOCAL,
            'netmask'       : '255.255.255.0',
            "tunnel_name"   : "Ni",
            'comment'       : '',
            "vpn_policy"    :"test",
            'mgmt_https'    : True,
            'mgmt_ssh'      : True,
            'mgmt_ping'     : True,
            'mgmt_snmp'     : True,
            'flow_reporting': True,
            'multicast'     : True,
            'asymmetric_route': False,
            'fragment_packets': True,
            'ignore_df_bit'   :True,
        }
TI_modify = {
            'zone'          : 'VPN',
            'type'          : "vpn_tunnel",
            'mode'          : 'static',
            'ip'            : VPN_BGP_IP_LOCAL,
            'netmask'       : '255.255.0.0',
            "tunnel_name"   : "Ni",
            'comment'       : '',
            "vpn_policy"    :"test",
            'mgmt_https'    : True,
            'mgmt_ssh'      : True,
            'mgmt_ping'     : False,
            'mgmt_snmp'     : False,    
            'user_https'    : True,
            'user_http'     : True
        }
rip = {
        'interface': 'Ni',
        'type': 'TI',
        'num_id': '1',
        'DUT':'local',    
        'mode': 'send_and_receive',
        'receive': '2',
        'send': '2',
        'split_horizon': 'on',
        'poison_reverse': 'on',
        'password': '',
    }
ospf2 = {
        'interface': 'Ni',
        'type'     : 'TI',
        'num_id': '',
        'DUT':'local',    
        'mode': 'enable',  # enable,disable,passive
        'dead_interval': '40',
        'hello_interval': '10',
        'auth': 'disable',  # disable,message diagest,simple password
        'area': '112',
        'area_type': 'normal',  # normal, stub area, totally stubby area, not-so-stubby area,totally stubby nssa
        'auto': 'on',
        # 'cost': '0',
        'priority': '2',
        'mtu': 'off',
    }
rip_setting_dict = {
    'OriginateDefaultRoute':'on',
    'RedistributeConnectedNetworks': 'on',
    'RedistributeStaticRoutes': 'on',
    'RedistributeOSPFRoutes': 'on',
    'RedistributeRemoteVPNNetworks': 'on',
}
ospf_setting_dict = {
    'router_id': '10.0.0.1',
    'static_route': 'on',
    'connect_network': 'on',
    'rip_route': 'on',
    'vpn_network': 'on',
}
local_bgp_cmds = [
    'config',
    'routing',
    'bgp',
    'configure t',
    'router bgp 2',
    "network {}/24".format(Parameter.LOCALNET),
    "neighbor {} remote-as 2".format(VPN_BGP_IP_REMOTE),
    "neighbor {} update-source {}".format(VPN_BGP_IP_REMOTE,VPN_BGP_IP_LOCAL),
    'end',
    'exit',
    'commit',
    'end',
    'exit',
]
remote_bgp_cmds = [
    'config',
    'routing',
    'bgp',
    'configure t',
    'router bgp 2',
    "network {}/24".format(Parameter.REMOTENET),
    "neighbor {} remote-as 2".format(VPN_BGP_IP_LOCAL),
    "neighbor {} update-source {}".format(VPN_BGP_IP_LOCAL,VPN_BGP_IP_REMOTE),
    'end',
    'exit',
    'commit',
    'end',
    'exit',
]
local_bgp_cmds2 = [
    'config',
    'routing',
    'bgp',
    'configure t',
    'router bgp 2',
    "network {}/24".format(Parameter.LOCALNET),
    "neighbor {} remote-as 2".format(VPN_IF_IP_REMOTE),
    "neighbor {} update-source {}".format(VPN_IF_IP_REMOTE,VPN_IF_IP_LOCAL),
    'end',
    'exit',
    'commit',
    'end',
    'exit',
]
route_policy = [
    'config',
    'route-policy ipv4 interface Ni metric 10 source name X0\ Subnet destination name remote_net',
    'name ti_route',
    'auto-add-access-rules',
    'commit',
    'exit',
    'exit',
]
route_policy2 = [
    'config',
    'route-policy ipv4 interface Ni metric 10 source name X0\ Subnet destination any',
    'name ti_route2',
    'auto-add-access-rules',
    'commit',
    'exit',
    'exit',
]
packet_filter = {
    'monitor_filter': {
        'interfaces':Tunnel_Interface["tunnel_name"] ,
    },
    "display_filter": {
   "interfaces": Tunnel_Interface["tunnel_name"],
   }
}
Multicast_json = {
    'multicast': True,
    'timeout': 5,
}
filter_frag = {
            'IP' : {
            'src': PC1_IP,
            'dst': PC2_IP, 
            'flags': 'MF',
            }
        }
del_rule1 = {
        "from": "LAN",
        "to": "VPN",
        "action": "allow",
        "source": {
            "address": {"name": "X0 Subnet" },
            "port": { "any": True }
        },
        "destination": {
            "address": { "name": "remote_net" }
        }
    }
del_rule2 = {
        "from": "VPN",
        "to": "LAN",
        "action": "allow",
        "source": {
            "address": {"name": "remote_net" },
            "port": { "any": True }
        },
        "destination": {
            "address": { "name": "X0 Subnet" }
        }
    }
del_rule3 = {
        "destination": {
            "address": { "name": "Ni IP" }
        }
    }
nat_policy = {
            "nat_policies":[
                {
                    "ipv4":{
                        "name": "tc_nat_rule",
                        "enable": True,
                        "dns_doctoring":False,
                        "reflexive":True,
                        "comment": "test",
                        "inbound": "any",
                        "outbound": "any",
                        "source": {"any": True},
                        "translated_source":  {'original': True},
                       'destination': {'name': trans_net["name"]},
                        'translated_destination':{'name': local_r["name"]},
                        'service': {"any": True},
                         'translated_service': {'original': True}, 
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": ""
                        }
                        #"source_port_remap": True  ###this option can be enabled only when "translated source" is not Original
                    }
                }
            ]
        }
# Nat_reflexive_name = "tc_nat_rule (Reflexive)"
Nat_name = nat_policy["nat_policies"][0]["ipv4"]["name"]
Nat_reflexive_name = nat_policy["nat_policies"][0]["ipv4"]["name"]+" (Reflexive)"
iphelper_policy1 = {
        "protocol":"NetBIOS",
        "source":{"name":"X0 Subnet"},
        "destination":{"name":"remote_net"},
        "enable":True,
        "comment":""
        }
iphelper_policy2 = {
        "protocol":"DHCP",
        "source":{"interface":"X0"},
        "destination":{"name":Tunnel_Interface['tunnel_name']+" IP"},
        "enable":True,
        "comment":""
        }
udp_packet = {
    'IP': {
        'version': '4',
        'src': PC1_IP,
        'dst': PC2_IP,
    },
    'UDP': {
        'sport': '137',
        'dport' : '137',
    },
    'data': "QQQQQOOOPPPP"
}
netmonit_policy={
        "network_monitors": [{
            "policy": {
                "ipv4": {
                    "name": "monitor_policy",
                    'probe': {
                        "target":{"name":remote_pc["name"]}, 
                        "type":{"ping":"explicit"}, 
                        'interval': 2
                        },
                    'reply_timeout': 1,
                    'interval': {'missed': 3, 'successful': 3},
                    'must_respond': False,
                    "comment": "",
                    "local_ip":{"name":"X0 IP"},
                    "outbound_interface":Tunnel_Interface['tunnel_name']
                }
            }
        }]
        }
arp_json = { "arp": {
            "entry": [
            {
                "ip": '1.1.1.3',
                "mac": 'FA:16:3E:9A:1A:26',
                "interface": Tunnel_Interface['tunnel_name'],
                "publish": False,
                "bind_mac": False,
            }]}}
bwm_obj1 = {
        'name'         : 'bwm1',
        'guaranteed' : {
            "kbps": { "value": 100 }
        },
        'maximum' : {
            "kbps": 200,
        },
        'priority'  : 'realtime',
        'action' : 'delay',
        'comment'     : 'bwm1'
    }
HA_set = {
    'mode':'active_standby',
    'control_interface':'Ni',
    'secondary_serial':'000000000099',
}
Connetion_Filter = {
    'dstIf' : 'X0', 
    }


route_policy3 = {
    "route_policies":[{
        "ipv6":{
            "name":"test",
            "comment":"",
            "interface":"Ni",
            "metric":3,
            "service":{"any":True},
            "gateway":{"default":True},
            "source":{"any":True},
            "destination":{"any":True},
            "disable_on_interface_down":True,
            "probe":"",
            "distance":{"auto":True},
            "tos":"0x00",
            "mask":"0x00",
            "type":"standard",
            "vpn_precedence":False,
        }
    }]
}



def icmp_packet_check(PackageMonitObj, scapyPacketObj, filter_frag ):
    PackageMonitObj.start_capture()
    PackageMonitObj.clear_packets()
    PC1.send_command("ping {}  -s 1460 -c 1 -W 1".format(PC2_IP))
    PackageMonitObj.stop_capture()
    logger.info("export captured packets in libpcap format")
    PackageMonitObj.export_captured_packets_libpcap()
    logger.info(" captured packets in decoding and filtering....")
    p = scapyPacketObj.analyze_packet(file = '/tmp/packet-c.pcap')
    packets = scapyPacketObj.filter_packets(p, filter_frag)
    logger.info(packets)
    if len(packets) >= 1:
        rc = True
    else:
        rc = False
    return rc
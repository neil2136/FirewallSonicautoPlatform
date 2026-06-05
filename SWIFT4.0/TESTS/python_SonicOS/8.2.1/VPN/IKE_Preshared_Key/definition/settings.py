import os
import sys
import time
import copy

from runner.settings import logger, Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IKE_Preshared_Key')
from bin.global_settings import *

from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info

from lib.modules.API import network
from lib.modules.API import log
from lib.modules.API import vpn
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.CLI.system import LicenseCli

fw = Firewall(
    '192.168.168.168',
    user='admin',
    password='sonicauto',
    supported_config_mode='api')
fw_cli = Firewall(
    '192.168.168.168',
    user='admin',
    password='sonicauto',
    supported_config_mode='cli-ssh')

licensecli = LicenseCli(fw_cli)
failoverapi = network.FailoverLbApi(fw)
interfaceapi = network.InterfaceIPv4Api(fw)


OpenS  = Openstack(Params.testbed)

LocalObj1 = {
        'name': 'remote_net',
        'zone': 'VPN',
        'object_type': 'network',
        'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
    }
RemoteObj1 = {
        'name': 'local_net',
        'zone': 'VPN',
        'object_type': 'network',
        'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
    }

LocalAddrList = [
        LocalObj1,
        {
            'name' : 'local_net',
            'zone' : 'LAN',
            'object_type' : 'network',
            'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
        },
        {
            'name' : 'local_host',
            'zone' : 'LAN',
            'object_type' : 'host',
            'value': Parameter.LOCALHOST,
        },
        {
            'name': 'remote_host',
            'zone': 'VPN',
            'object_type': 'host',
            'value': Parameter.REMOTEHOST,
        },
        {
            'name': 'remote_range',
            'zone': 'VPN',
            'object_type': 'range',
            'value': '172.16.1.0,172.16.1.255',
        },
        {
            'name': 'local_range',
            'zone': 'LAN',
            'object_type': 'range',
            'value': '192.168.168.0,192.168.168.255',
        },

    ]
RemoteAddrList = [
        RemoteObj1,
        {
            'name': 'remote_net',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
        },
        {
            'name': 'remote_host',
            'zone': 'LAN',
            'object_type': 'host',
            'value': Parameter.REMOTEHOST,
        },
        {
            'name': 'local_host',
            'zone': 'VPN',
            'object_type': 'host',
            'value': Parameter.LOCALHOST,
        },
        {
            'name': 'local_range',
            'zone': 'VPN',
            'object_type': 'range',
            'value': '192.168.168.0,192.168.168.255',
        },
        {
            'name': 'remote_range',
            'zone': 'LAN',
            'object_type': 'range',
            'value': '172.16.1.0,172.16.1.255',
        },
    ]

TESTPLAN 		= os.environ["PYTHON_SONICOS_HOME"]+'/VPN/IKE_Preshared_Key/testplan/IKE_Preshared_Keys.json'

# need add
RM_PREF = os.environ["PYTHON_COMMON_HOME"] + "/data/prefs/OS_REMOTE.exp"
GW_PREF = os.environ["PYTHON_COMMON_HOME"] + "/data/prefs/OS_GW.exp"

LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)

PC1 = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2 = OpenS.get_node_interface_ip('PC2', 'eth0')
PC3_IP = OpenS.get_node_interface_ip('PC3', 'eth1')
PC4_IP = OpenS.get_node_interface_ip('PC4', 'eth1')

LObj1 = LocalObj1
RObj1 = RemoteObj1

LaddrList = LocalAddrList
RaddrList = RemoteAddrList

Lvpn = {
    'type'              : 'site_to_site',
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
    'remote_net_name'   : LObj1['name'],
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_encryption'  : 'aes_128',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'bound_to'          :['zone', 'WAN'],
    'keep_alive'        : True,
}
Rvpn = {
    'type'              : 'site_to_site',
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
    'remote_net_name'   : RObj1['name'],
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_encryption'  : 'aes_128',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'bound_to'          :['zone', 'WAN'],
    'keep_alive'        : True,
}

vpn_raw = {
    "local_net"  : Parameter.LOCALNET,
    "local_mask" : "255.255.255.0",
    "remote_net" : Parameter.REMOTENET,
    "remote_mask": "255.255.255.0",
    "remote_gw"  : Parameter.REMOTEX1,
}




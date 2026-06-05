import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/IKEv2_Sec_GW_Part2')

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
from lib.modules.API import system
from lib.modules.CLI.vpn import VpnBaseSettingsCli


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
Rinterface_ipv4 = network.InterfaceIPv4Api(rt)
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
LRestartObj = system.RestartApi(fw)
Lsetting_obj = system.SettingApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LogObj = log.LogMonitorApi(fw)
Rlog_set = log.LogCategoryApi(rt)
RLogObj = log.LogMonitorApi(rt)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
LAdv_obj = vpn.VpnAdvancedsettingApi(fw)
RAdv_obj = vpn.VpnAdvancedsettingApi(rt)

# PC SSH
PC1_eth0 = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/IKEv2_Sec_GW_Part2/testplan/IKEv2_Sec_GW.json'


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
    'pri_gate'          : Parameter.REMOTEX2,
    'sec_gate'          : Parameter.REMOTEX1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : Parameter.DUT,
    'peer_ike_id'       : Parameter.REMOTEX0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'ike_exchange'      : 'ikev2',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : False,
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
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : False,
    'bound_to'          : ['zone', 'WAN'],
}

Ldpd = {
    'enable': True,
    'ike_dpd': True,
    'dpd_interval': '10',
    'dpd_trigger': '3',
    'idle_dpd': True,
    'idle_dpd_interval': '60',
}

Rdpd = {
    'enable': True,
    'ike_dpd': True,
    'idle_dpd': True,
}

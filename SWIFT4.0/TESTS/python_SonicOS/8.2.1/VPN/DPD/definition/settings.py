import sys
import os
import time
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/DPD')

from inspect import Parameter
import paramunittest
from nose_parameterized import parameterized
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
from lib.modules.CLI.system import LicenseCli


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
LRestartObj = system.RestartApi(fw)
Lsetting_obj = system.SettingApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LintfaceObj = network.InterfaceIPv4Api(fw)
RintfaceObj = network.InterfaceIPv4Api(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)
LAdv_obj = vpn.VpnAdvancedsettingApi(fw)
RAdv_obj = vpn.VpnAdvancedsettingApi(rt)
license_obj = LicenseCli(fw_cli)


# PC SSH
PC1_eth0 = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
PC2_login = Host(PC2_IP, user='root', password='password')
PC2_eth0 = OpenS.get_node_interface_ip('PC2', 'eth0')
PC4_IP = OpenS.get_node_interface_ip('PC4', 'eth1')
PC4_login = Host(PC4_IP, user='root', password='password')
PC5_eth0 = OpenS.get_node_interface_ip('PC5', 'eth0')
PC3_eth0 = OpenS.get_node_interface_ip('PC3', 'eth0')


TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/DPD/testplan/DPD.json'
conf_path = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/DPD/bin/'

# DUT object
remote_l = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
remote_l_2 = {
    'name': 'remote_net_2',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTEX3NET),
}

#RemoteDUT object
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
}
remote_r_2 = {
    'name': 'remote_net_2',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.DUTX3NET),
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
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.LOCALSUBNET,
    'remote_net_name'   : remote_l['name'],
    'ike_exchange'      : 'aggressive',
    # 'keep_alive'        : False,
    'bound_to'          :['interface', 'X1'],
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
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : Parameter.REMOTESUBNET,
    'remote_net_name'   : remote_r['name'],
    'ike_exchange'      : 'aggressive',
    # 'keep_alive'        : False,
    'bound_to'          : ['interface', 'X1'],

}

Lvpn_2 = {
    'type'              : 'site_to_site',
    'name'              : 'vpn3',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.REMOTEX2,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : 'X3 Subnet',
    'remote_net_name'   : remote_l_2['name'],
    'ike_exchange'      : 'aggressive',
    'bound_to'          :['interface', 'X2'],
}
Rvpn_2 = {
    'type'              : 'site_to_site',
    'name'              : 'vpn4',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Parameter.DUTX2,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : 'X3 Subnet',
    'remote_net_name'   : remote_r_2['name'],
    'ike_exchange'      : 'aggressive',
    'bound_to'          : ['interface', 'X2'],

}

En_dpd = {
    'enable': True,
    'ike_dpd': True,
    'dpd_interval': '10',
    'dpd_trigger': '3',
    'idle_dpd': True,
    'idle_dpd_interval': '60',
}

Dis_dpd = {
    'ike_dpd': False,
    'idle_dpd': True,
}

import sys
import os
import time
import copy
import pprint

from inspect import Parameter
import paramunittest
from nose_parameterized import parameterized

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'VPN/MOBIKE_TP2581')
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
from lib.modules.API import accessrule
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.CLI.system import DiagnosticsCli


OpenS = Openstack(Params.testbed)
fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
LCACertObj = system.CertificateApi(fw)
RCACertObj = system.CertificateApi(rt)
LTimeObj = system.TimeApi(fw)
RTimeObj = system.TimeApi(rt)
LRestartObj = system.RestartApi(fw)
Lpacket_obj = system.PacketmonitorApi(fw)
Linterface = network.InterfaceIPv4Api(fw)
Lacrule_obj = accessrule.AccessRuleIPv4Api(fw)
tsr_obj = DiagnosticsCli(fw_cli)
setting_obj = system.SettingApi(fw)

LAddrOBJ = network.AddressobjectsApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
RAddrGroupOBJ = object.AddressObjectGroupApi(rt)
LRoutePolicyObj = network.RoutePolicyApi(fw)
RRoutePolicyObj = network.RoutePolicyApi(rt)
LogObj = log.LogMonitorApi(fw)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)


TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/MOBIKE_TP2581/testplan/MOBIKE_TP2581.json'
ca_cert = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/MOBIKE_TP2581/cert/rootca.pem'
local_cert = os.environ["PYTHON_SONICOS_HOME"]+'/VPN/MOBIKE_TP2581/cert/my_cert.pfx'

# add ao
rm_host = {
    "name":'remote_host',
    "zone":'VPN',
    "object_type":'host',
    "value":  '172.17.1.100',
}

rm_net = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}

rm_range = {
    'name': 'remote_range',
    'zone': 'VPN',
    'object_type': 'range',
    'value': '172.18.1.1,172.18.1.15',
}

rm_range_2 = {
    'name': 'remote_range_2',
    'zone': 'VPN',
    'object_type': 'range',
    'value': '172.19.1.1,172.19.1.15',
}

rm_range_3 = {
    'name': 'remote_range_3',
    'zone': 'VPN',
    'object_type': 'range',
    'value': '172.20.1.1,172.20.1.15',
}


# VPN policy
#########################################
#                Notice!                #
#          Key:"_"      Value:"-"       #
#       site_to_site & site-to-site     #
#         triple_des & triple-des       #
#########################################
Lvpn_rmhost = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn_rmhost',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': 'my_cert',  # add local cert
    'local_ike_type': 'distinguished-name',
    'peer_ike_type': 'distinguished_name',
    'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate': Parameter.REMOTEX1,
    'local_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_type': 'name',
    'remote_net_name': rm_host['name'],
    'ike_exchange': 'ikev2',
}

Lvpn = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': 'my_cert',  # add local cert
    'local_ike_type': 'distinguished-name',
    'peer_ike_type': 'distinguished_name',
    'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate': Parameter.REMOTEX1,
    'local_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_type': 'name',
    'remote_net_name': rm_net['name'],
    'ike_exchange': 'ikev2',
}

Lvpn_1 = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn1',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': 'my_cert',  # add local cert
    'local_ike_type': 'distinguished-name',
    'peer_ike_type': 'distinguished_name',
    'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate': Parameter.REMOTEX1,
    'local_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_type': 'pool',
    'remote_net_name': rm_range['name'],
    'ike_exchange': 'ikev2',

}

Lvpn_2 = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn2',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': 'my_cert',  # add local cert
    'local_ike_type': 'distinguished-name',
    'peer_ike_type': 'distinguished_name',
    'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate': Parameter.REMOTEX1,
    'local_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_type': 'pool',
    'remote_net_name': rm_range_2['name'],
    'ike_exchange': 'ikev2',

}

Lvpn_3 = {
    'type': 'site_to_site',  # site-to-site, tunnel_interface
    'name': 'vpn3',
    'enable': True,
    'auth_mode': 'certificate',  # certificate or shared-secret
    'local_cert': 'my_cert',  # add local cert
    'local_ike_type': 'distinguished-name',
    'peer_ike_type': 'distinguished_name',
    'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate': Parameter.REMOTEX1,
    'local_net_type': 'name',
    'local_net_name': 'X0 Subnet',
    'remote_net_type': 'pool',
    'remote_net_name': rm_range_3['name'],
    'ike_exchange': 'ikev2',

}

signreq = {
    "certificates": {
        "generate_signing_request": [{
            "signature_algorithm": "sha-1",
            "key": {
                "type": "rsa",
                "size": "1024"
            },
            "generate": True,
            "alias": "my_cert",
            "distinguished_name": {
                "element1": {
                    "country": "CHINA"
                },
                "element2": {
                    "state": "SH"
                },
                "element3": {
                    "locality": "ShangHai"
                },
                "element4": {
                    "organization": "SNWL"
                },
                "element5": {
                    "department": "AUTO"
                },
                "element6": {
                    "group": "AUTO"
                },
                "element7": {
                    "team": "AUTO"
                },
                "element8": {
                    "common_name": "AUTO"
                }
            }
        }]
    }
}


import sys
import os
import re
import copy
import time
import subprocess
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion


# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall


# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.API.log import LogMonitorApi, LogCategoryApi
from lib.modules.API.system import CertificateApi


suite_path = os.environ['PYTHON_SONICOS_HOME']+'/VPN/NAT_Traversal_TP374/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/nat_traversal_tp374.json'
restore_path = os.environ['PYTHON_COMMON_HOME'] + '/config/restore_tel.py'
cfg_if_path = os.environ['PYTHON_COMMON_HOME'] + '/config/cfg_if_tel.py'
cert_path = os.environ['PYTHON_COMMON_HOME']+'/util/vpn_cert/my_cert.pfx'
ca_cert_path = os.environ['PYTHON_COMMON_HOME']+'/util/vpn_cert/rootca.pem'

os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')

logger.info(f"""
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
""")
pc1_login = Host(PC1_ETH1_IP)
pc2_login = Host(PC2_ETH2_IP)


# Params on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.168'
    X1_NET = '172.16.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    NATD_X0_IP = '172.16.1.101'
    NATD_X1_IP = '12.12.1.101'
    REM_X1_IP = '12.12.1.102'
    REM_X2_IP = '12.12.2.102'


# Instantiate objects including API import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_nat = Firewall(
    Parameter.NATD_X1_IP,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_rem = Firewall(
    Parameter.REM_X1_IP,
    user='admin',
    password='password',
    supported_config_mode='api'
)
if_v4_api = network.InterfaceIPv4Api(fw)
ao_api = network.AddressobjectsApi(fw)
vpn_api = VpnbasesettingApi(fw)
route_api = network.RoutePolicyApi(fw)
log_mon_api = LogMonitorApi(fw)
log_set_api = LogCategoryApi(fw)
cert_api = CertificateApi(fw)

if_nat_api = network.InterfaceIPv4Api(fw_nat)
ao_nat_api = network.AddressobjectsApi(fw_nat)
nat_dev_api = network.NatpolicyApi(fw_nat)
acl_nat_api = AccessRuleApi(fw_nat)

if_rem_api = network.InterfaceIPv4Api(fw_rem)
ao_rem_api = network.AddressobjectsApi(fw_rem)
vpn_rem_api = VpnbasesettingApi(fw_rem)
route_rem_api = network.RoutePolicyApi(fw_rem)
log_mon_rem_api = LogMonitorApi(fw_rem)
log_set_rem_api = LogCategoryApi(fw_rem)
cert_rem_api = CertificateApi(fw_rem)

acl_base_dict = {
            "name": "",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "group": ""
            },
            "destination": {
                "address": {
                    "any": True
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }

nat_base_dict = {
            "name": 'translate_rem_x1_to_local_x1',
            "enable": True,
            "comment": "",
            "inbound": "any",
            "outbound": "any",
            "source": {
                "any": True
            },
            "translated_source": {
                "original": True
            },
            "destination": {
                "name": "X1 IP"
            },
            "translated_destination": {
                "name": "local_fw_x1"
            },
            "service": {
                "any": True
            },
            "translated_service": {
                "original": True
            },
            "ticket": {
                "tag1": "",
                "tag2": "",
                "tag3": ""
            }
        }

ti_vpn_local = {
            "type": "tunnel_interface",
            "name": "ti_local",
            "enable": True,
            "auth_mode": "shared_secret",
            'pri_gate':  Parameter.REM_X1_IP,
            'secret': "1111",
            'local_ike_type': "ipv4",
            'peer_ike_type': "ipv4",
            'local_ike_id': "1.1.1.1",
            'peer_ike_id': "2.2.2.2",
            'ipversion': "ipv4",
            'ike_exchange': "",
            'ike_encryption': "aes-256",
            "ike_dh_group": "2",
            "ike_auth": "sha-256",
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            'keep_alive': True
        }

ti_vpn_remote = {
            "type": "tunnel_interface",
            "name": "ti_remote",
            "enable": True,
            "auth_mode": "shared_secret",
            'pri_gate': Parameter.NATD_X1_IP,
            'secret': "1111",
            'local_ike_type': "ipv4",
            'peer_ike_type': "ipv4",
            'local_ike_id': "2.2.2.2",
            'peer_ike_id': "1.1.1.1",
            'ipversion': "ipv4",
            'ike_exchange': "",
            'ike_encryption': "aes-256",
            "ike_dh_group": "2",
            "ike_auth": "sha-256",
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            'keep_alive': True
        }

route_vpn = {
            "route_policies": [{
                "ipv4": {
                    "name": "test",
                    "comment": "",
                    "interface": "",
                    "metric": 6,
                    "service": {"any": True},
                    "gateway": {"default": True},
                    "source": {"name": ""},
                    "destination": {"name": ""},
                    "disable_on_interface_down": True,
                    "probe": "",
                    "distance": {"auto": True},
                    "tos": "0x00",
                    "mask": "0x00",
                    "type": "standard",
                    "auto_add_access_rules": True
                }
            }]
        }

s2s_local = {
            "type": "site_to_site",
            "name": "",
            "enable": True,
            "pri_gate": Parameter.REM_X1_IP,
            "sec_gate": "",
            #auth
            "auth_mode": 'shared_secret',
            'secret': "1111",
            'local_ike_type': "ipv4",
            'peer_ike_type': "ipv4",
            'local_ike_id': "1.1.1.1",
            'peer_ike_id': "2.2.2.2",
            #network
            "ipversion": "ipv4",
            "local_net_type": "name",
            'local_net_name': "X0 Subnet",
            'remote_net_type': "name",
            "remote_net_name": "rem_sub_net",
            #protocol
            'ike_exchange': "",
            'ike_encryption': "aes-256",
            "ike_dh_group": "2",
            "ike_auth": "sha-256",
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            #advanced
            'keep_alive': True
        }

s2s_remote = {
            "type": "site_to_site",
            "name": "",
            "enable": True,
            "pri_gate": Parameter.NATD_X1_IP,
            "sec_gate": "",
            # auth
            "auth_mode": 'shared_secret',
            'secret': "1111",
            'local_ike_type': "ipv4",
            'peer_ike_type': "ipv4",
            'local_ike_id': "2.2.2.2",
            'peer_ike_id': "1.1.1.1",
            # network
            "ipversion": "ipv4",
            "local_net_type": "name",
            'local_net_name': "X2 Subnet",
            'remote_net_type': "name",
            "remote_net_name": "local_sub_net",
            # protocol
            'ike_exchange': "",
            'ike_encryption': "aes-256",
            "ike_dh_group": "2",
            "ike_auth": "sha-256",
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # advanced
            'keep_alive': True
        }

cert_local = {
            'type': 'site_to_site',
            'name': 'local',
            'enable': True,
            'auth_mode': 'certificate',
            'local_cert': 'my_cert',
            'local_ike_type': 'distinguished-name',
            'peer_ike_type': 'distinguished_name',
            'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
            'pri_gate': Parameter.REM_X1_IP,
            'local_net_type': 'name',
            'local_net_name': 'X0 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'rem_sub_net',
            'ike_exchange': 'main',
            'ike_encryption': 'triple-des',
            'ike_auth': 'sha-1',
            'ike_lifetime': '28800',
            'ipsec_encryption': 'triple_des',
            'ipsec_auth': 'sha_1',
            'ipsec_lifetime': '28800',
            'keep_alive': True,
            'bound_to': ['zone', 'WAN'],
        }

cert_remote = {
            'type': 'site_to_site',
            'name': 'remote',
            'enable': True,
            'auth_mode': 'certificate',
            'local_cert': 'my_cert',
            'local_ike_type': 'distinguished-name',
            'peer_ike_type': 'distinguished_name',
            'peer_ike_id': '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
            'pri_gate': Parameter.NATD_X1_IP,
            'local_net_type': 'name',
            'local_net_name': "X2 Subnet",
            'remote_net_type': 'name',
            'remote_net_name': "local_sub_net",
            'ike_exchange': 'main',
            'ike_encryption': 'triple-des',
            'ike_auth': 'sha-1',
            'ike_lifetime': '28800',
            'ipsec_encryption': 'triple_des',
            'ipsec_auth': 'sha_1',
            'ipsec_lifetime': '28800',
            'keep_alive': True,
            'bound_to': ['zone', 'WAN'],
        }

import os
import sys
import copy
import re
import time
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_SSH')
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from lib.modules.API import network,system
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API.users import UserLocalApi
from utm import Firewall
from lib.modules.CLI.system import LicenseCli,DiagnosticsCli
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI,SSLVPNClientSettingsAPI,SSLVPNVirtualOfficeAPI
from lib.modules.API import vpn

OpenS = Openstack(Params.testbed)
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_SSH/testplan/ipv6_ssh.json'
ui_file = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_SSH/definition/ui_user.py'
DUT_X0_IPV4 = '192.168.168.168'
DUT_X0_IPV6 = '2001:db0::193'
DUT_X1_IPV4 = '13.0.0.10'
DUT_X1_IPV6 = '2001:db1::193'
PC1_ETH0_IPV6 = '2001:db0::1096'

fw_api = Firewall(DUT_X0_IPV4, user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='api')
fw_cli = Firewall(DUT_X0_IPV4, user='admin', password=Params.G_NEW_PASSWORD,ssh_version=2, supported_config_mode='cli-ssh')
fw_ipv6_cli = Firewall(DUT_X0_IPV6, user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='cli-ssh')
fw_cli_option = Firewall(DUT_X0_IPV6, user='admin', password=Params.G_NEW_PASSWORD, option='KexAlgorithms=diffie-hellman-group-exchange-sha256', supported_config_mode='cli-ssh')
fw_cli_encr = Firewall(DUT_X0_IPV6, user='admin', password=Params.G_NEW_PASSWORD, cli_encr='aes128-gcm@openssh.com', supported_config_mode='cli-ssh')
fw_cli_mac = Firewall(DUT_X0_IPV6, user='admin', password=Params.G_NEW_PASSWORD, mac_spec='hmac-sha1', supported_config_mode='cli-ssh')

interfacev4api = network.InterfaceIPv4Api(fw_api)
interfacev6api = network.InterfaceIPv6Api(fw_api)
interface_cli = InterfaceCli(fw_cli)
license_obj = LicenseCli(fw_cli)
diag_cli = DiagnosticsCli(fw_ipv6_cli)
diag_api = system.DiagnosticApi(fw_api)
sslvpnserver = SSLVPNServerSettingsAPI(fw_api)
sslvpnvirtual = SSLVPNVirtualOfficeAPI(fw_api)
user_local = UserLocalApi(fw_api)
clientsetobj = SSLVPNClientSettingsAPI(fw_api)
address_objects = network.AddressobjectsApi(fw_api)
Lvpn = vpn.VpnbasesettingApi(fw_api)
admin_api = system.AdminApi(fw_api)

x0_ipv6 = {'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': DUT_X0_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'ra_max': 30
        }
x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUT_X1_IPV4,
            'netmask': '255.255.255.0',
            'gateway': '13.0.0.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }
x1_ipv6 = {'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': DUT_X1_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'ra_max': 30
            }
ssl_vpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': False,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
address_object = {
            "object_type": "range",
            "name": "sslvpn_range",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
address_ipv6 = {
            "object_type": "range",
            "name": "sslvpn_ipv6",
            "zone": "SSLVPN",
            "begin": "2001:db0::193",
            "end":"2001:db0::1930"
        }
enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
add_user = {
            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': Params.G_NEW_PASSWORD,
        }
uesr_access1 = {
            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': Params.G_NEW_PASSWORD,
            'vpn_client_access': ['LAN Subnets','WAN Subnets','WAN IPv6 Subnets','LAN IPv6 Subnets']
        }
user_member1 = {
            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services','SonicWALL Administrators'],
            'vpn_client_access': ['LAN Subnets','WAN Subnets','WAN IPv6 Subnets','LAN IPv6 Subnets']
        }
ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'ipv6_network_address_name':'sslvpn_ipv6',
            'ipv6_network_address_zone':'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets','WAN Subnets'],
            'route_ipv6': ['WAN IPv6 Subnets','LAN IPv6 Subnets']
        }
sshv2_bookmark = {
              'name': 'test2',
              'host': PC1_ETH0_IPV6,
              'service_type': 'sshv2',
              'automatic_accept_host_key' : True,
              'display_on_mobile' : False,
            }
vpn_dict ={
            'ipversion':'ipv6',
            'type': 'site_to_site',
            'name': 'vpn_ipv6',
            'pri_gate': DUT_X1_IPV6,
            'sec_gate': '0::0',
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'local_ike_type': 'ipv6',
            'peer_ike_type': 'ipv6',
            'local_ike_id': '1::1',
            'peer_ike_id': '2::2',
            'local_net_type': 'group',
            'local_net_group': 'LAN IPv6 Subnets',
            'remote_net_type': 'name',
            'remote_net_name':'sslvpn_ipv6' ,
            'keep_alive': True,
            'management_ssh':True
        } 
option_dict = {
                "ssh": {
                    'port':111
                }
            }
        
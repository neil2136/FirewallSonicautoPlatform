import os
import re
import sys
import copy
import json
import time
import unittest
import urllib3
import requests
import paramiko

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Ula_TP88_3')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Ula_TP88_3/definition')

from lib.modules.CLI.system import LicenseCli, AdminCli
from lib.modules.API.network import InterfaceIPv4Api, ZoneObjectsApi, DHCPServerApi, AddressobjectsApi
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.CLI.vpn import VpnBaseSettingsCli
from lib.modules.API.users import SSOApi, UsersettingApi, UserStatusApi, UserLocalApi, LdapApi
from lib.modules.API.system import DiagnosticApi, RestartApi, SettingApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.log import LogSettingsApi, LogCategoryApi, LogMonitorApi
from lib.modules.API.securityservices import IPSApi, AntiSpywareApi
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from ui_user import FWPage

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_GW = '192.168.168.1'
    X0_SUBNET = '192.168.168.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_SUBNET = '12.12.1.0'
    X2_IP = '192.168.3.168'
    X2_GW = '192.168.3.1'
    X2_SUBNET = '192.168.3.0'
    MASK = '255.255.255.0'
    WAN_IP = '12.12.1.110'
    LAN_IP = '192.168.168.120'
    VPN_IP = '172.16.1.140'
    DMZ_IP = '192.168.3.130'
    R_X0_IP = '172.16.1.101'
    R_X0_SUBNET = '172.16.1.0'
    R_X1_IP = '12.12.1.201'
    R_X1_GW = X1_GW

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/testplan/ula.json'
    HTTP_CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Firewall/Access_Rule_Enh_6.5/Access_rule_new_2/definition/config/httpserver'
    certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
    configPath = os.environ["PYTHON_SONICOS_HOME"] + '/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/'

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
r_fw_api = Firewall(Parameter.R_X1_IP, user='admin', password='sonicauto', supported_config_mode='api')
r_fw_cli = Firewall(Parameter.R_X1_IP, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

os_obj = Openstack(Params.testbed)
pc1 = Host('localhost')
static_pc2 = Params.testbed + '-PC2'
pc2 = Host(static_pc2)
static_pc3 = Params.testbed + '-PC3'
pc3 = Host(static_pc3)
static_pc4 = Params.testbed + '-PC4'
pc4 = Host(static_pc4)

license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
user_sso = SSOApi(fw_api)
user_setting = UsersettingApi(fw_api)
user_status = UserStatusApi(fw_api)
accessrule = AccessRuleIPv4Api(fw_api)
r_accessrule = AccessRuleIPv4Api(r_fw_api)
diag_api = DiagnosticApi(fw_api)
user_ldap = LdapApi(fw_api)
user_local = UserLocalApi(fw_api)
log_settings = LogSettingsApi(fw_api)
log_category = LogCategoryApi(fw_api)
log_monitor = LogMonitorApi(fw_api)
ips_api = IPSApi(fw_api)
antispyware_api = AntiSpywareApi(fw_api)
zone_object = ZoneObjectsApi(fw_api)
restart_api = RestartApi(fw_api)
dhcpserverapi = DHCPServerApi(fw_api)
r_dhcpserverapi = DHCPServerApi(r_fw_api)
address_objects = AddressobjectsApi(fw_api)
r_address_objects = AddressobjectsApi(r_fw_api)
address_objects_cli = AddressObjectCli(fw_cli)
r_address_objects_cli = AddressObjectCli(r_fw_cli)
r_address_groups = AddressObjectGroupApi(r_fw_api)
vpn_cli = VpnBaseSettingsCli(fw_cli)
r_vpn_cli = VpnBaseSettingsCli(r_fw_cli)
r_admin_cli = AdminCli(r_fw_cli)
settings = SettingApi(r_fw_api)
r_accessrules = AccessRuleApi(r_fw_api)

x2_static = {
            'if': 'x2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_http': False,
            'user_https': True,
            'https_redirect': True
        }
x2_cus = {
            'if': 'x2',
            'zone': 'zone1',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_http': False,
            'user_https': True,
            'https_redirect': True
        }


local_vpn_obj = {
    "object_type": "network",
    "name": "local_vpn",
    "zone": "VPN",
    "value": Parameter.R_X0_SUBNET+','+Parameter.MASK,
}
remote_vpn_lan = {
    "object_type": "network",
    "name": "remote_vpn_lan",
    "zone": "VPN",
    "value": Parameter.X0_SUBNET+','+Parameter.MASK,
}
# local_group = {
#     "name": "local_group",
#     "version": "ipv4",
#     "objects": ['ipv4 "X0 Subnet"']
# }
# remote_group = {
#     "name": "remote_group",
#     "version": "ipv4",
#     "objects": ['ipv4 ' + remote_vpn_lan['name']]
# }

local_vpn = {
    'type'                     : 'site-to-site',
    'name'                     : 'local_vpn_1',
    'mode'                     : 'shared-secret',
    'secret'                   : 'password',
    'pri_gate'                 :  Parameter.R_X1_IP,
    'local_ike_id'             : 'ipv4 1.1.1.1',
    'peer_ike_id'              : 'ipv4 2.2.2.2',
    'local_net_type'           : 'group',
    'remote_net_type'          : 'name',
    'local_network'            : 'LAN\ Subnets',
    'remote_network'           : local_vpn_obj['name'],
    'proposal ike exchange'    : 'ikev2',
    'proposal ike encryption'  : 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'keep_alive'               : True,
}
local_lan_vpn_cmds = ['configure']
local_lan_vpn_cmds.append('vpn policy ' + local_vpn['type'] + ' ' + local_vpn['name'])
local_lan_vpn_cmds.append('network local ' + local_vpn['local_net_type'] + ' ' + local_vpn['local_network'])
local_lan_vpn_cmds.append('network remote destination-network ' + \
                          local_vpn['remote_net_type'] + ' ' + local_vpn['remote_network'])
local_lan_vpn_cmds.append('gateway primary ' + local_vpn['pri_gate'])
local_lan_vpn_cmds.append('proposal ike exchange ' + local_vpn['proposal ike exchange'])
local_lan_vpn_cmds.append('proposal ike encryption ' + local_vpn['proposal ike encryption'])
local_lan_vpn_cmds.append('proposal ike authentication ' + local_vpn['proposal ike authentication'])
local_lan_vpn_cmds.append('proposal ipsec encryption ' + local_vpn['proposal ipsec encryption'])
local_lan_vpn_cmds.append('proposal ipsec authentication ' + local_vpn['proposal ipsec authentication'])
local_lan_vpn_cmds.append('keep-alive')
local_lan_vpn_cmds.append('user-login https')
local_lan_vpn_cmds.append('management https')
local_lan_vpn_cmds.append('auth-method ' + local_vpn['mode'])
local_lan_vpn_cmds.append('ike-id local ' + local_vpn['local_ike_id'])
local_lan_vpn_cmds.append('ike-id peer ' + local_vpn['peer_ike_id'])
local_lan_vpn_cmds.append('shared-secret ' + local_vpn['secret'])
local_lan_vpn_cmds.append('exit')
local_lan_vpn_cmds.append('keep-alive')
local_lan_vpn_cmds.append('commit')
local_lan_vpn_cmds.append('end')
local_lan_vpn_cmds.append('end')

remote_vpn = {
    'type'                     : 'site-to-site',
    'name'                     : 'remote_vpn_1',
    'mode'                     : 'shared-secret',
    'secret'                   : 'password',
    'pri_gate'                 :  Parameter.X1_IP,
    'local_ike_id'             : 'ipv4 2.2.2.2',
    'peer_ike_id'              : 'ipv4 1.1.1.1',
    'local_net_type'           : 'group',
    'remote_net_type'          : 'name',
    'local_network'            : 'LAN\ Subnets',
    'remote_network'           : remote_vpn_lan['name'],
    'proposal ike exchange'    : 'ikev2',
    'proposal ike encryption'  : 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ipsec encryption': 'aes-128', 
    'proposal ipsec authentication': 'sha-1',
    'keep_alive'               : False,
}
remote_lan_vpn_cmds = ['configure']
remote_lan_vpn_cmds.append('vpn policy ' + remote_vpn['type'] + ' ' + remote_vpn['name'])
remote_lan_vpn_cmds.append('network local ' + remote_vpn['local_net_type'] + ' ' + remote_vpn['local_network'])
remote_lan_vpn_cmds.append('network remote destination-network ' + \
                          remote_vpn['remote_net_type'] + ' ' + remote_vpn['remote_network'])
remote_lan_vpn_cmds.append('gateway primary ' + remote_vpn['pri_gate'])
remote_lan_vpn_cmds.append('proposal ike exchange ' + remote_vpn['proposal ike exchange'])
remote_lan_vpn_cmds.append('proposal ike encryption ' + remote_vpn['proposal ike encryption'])
remote_lan_vpn_cmds.append('proposal ike authentication ' + remote_vpn['proposal ike authentication'])
remote_lan_vpn_cmds.append('proposal ipsec encryption ' + remote_vpn['proposal ipsec encryption'])
remote_lan_vpn_cmds.append('proposal ipsec authentication ' + remote_vpn['proposal ipsec authentication'])
remote_lan_vpn_cmds.append('auth-method ' + remote_vpn['mode'])
remote_lan_vpn_cmds.append('ike-id local ' + remote_vpn['local_ike_id'])
remote_lan_vpn_cmds.append('ike-id peer ' + remote_vpn['peer_ike_id'])
remote_lan_vpn_cmds.append('shared-secret ' + remote_vpn['secret'])
remote_lan_vpn_cmds.append('commit')
remote_lan_vpn_cmds.append('end')
remote_lan_vpn_cmds.append('end')
import os
import re
import sys
import copy
import time
import unittest
import json
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from runner.settings import Params, logger
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, repeat_method
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network, system, users, log
import paramunittest
import paramiko

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Encryption_Username_and_Password/definition')
print(sys.path)

from lib.modules.API.accesspoint import AccessPointApi
from lib.modules.API.aws import AwsConnection
from lib.modules.API.diag import DiagApi
from lib.modules.API.log import LogAutomationApi
from lib.modules.API.network import DDNSApi, InterfaceIPv4Api, DnsSettingsApi, DynamicRoutingApi, AddressobjectsApi, ZoneObjectsApi
from lib.modules.API.object import DynamicGroupApi
from lib.modules.API.securityservices import Botnet
from lib.modules.API.system import DiagnosticApi, SettingApi, PacketmonitorApi, TimeApi, StatusApi
from lib.modules.API.users import UserLocalApi, RadiusApi
from lib.modules.API.users import UserGuestApi
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.CLI.system import LicenseCli


class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '13.0.0.100'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Encryption_Username_and_Password/testplan/testplan_encrypt_username_password.json'

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

interface = InterfaceIPv4Api(fw_api)
ddnsapi = DDNSApi(fw_api)
user_local = UserLocalApi(fw_api)
guest_local = UserGuestApi(fw_api)
diagnostic = DiagnosticApi(fw_api)
packetmonitorapi = PacketmonitorApi(fw_api)
logautomationapi = LogAutomationApi(fw_api)
dnssettingapi = DnsSettingsApi(fw_api)
radius_user = RadiusApi(fw_api)
edagapi = DynamicGroupApi(fw_api)
aws_connection = AwsConnection(fw_api)
time_api = TimeApi(fw_api)
dyrouteapi = DynamicRoutingApi(fw_api)
vpnObj = VpnbasesettingApi(fw_api)
diag = DiagApi(fw_api)
settingapi = SettingApi(fw_api)
botnet = Botnet(fw_api)
address_obj = AddressobjectsApi(fw_api)
zone_obj = ZoneObjectsApi(fw_api)
accesspoint = AccessPointApi(fw_api)
license = LicenseCli(fw_cli)
status_api = StatusApi(fw_api)
localhost = Host('localhost')

logger.info("The Firewall LAN IP is {}".format(ip))

sonicwave = {'sonicpoint': {
    'profile': [{
    'wave2': {
        'name_prefix': 'SonicWave'
        }, 
        'enable': True, 
        'radius': {
        'retries': 4, 
        'retry_interval': {}, 
        'server': {
        'server1': {
        'ip': '1.1.1.1', 
        'port': {'value': 1812}, 
        'secret': '11111111'}, 
        'server2': {
            'ip': '0.0.0.0', 
            'port': {
                'value': 1812
                }, 
                'secret': '11111111'
                }}, 
        'accouting': {
        'server1': {
        'ip': '0.0.0.0', 
        'port': {
            'value': 1813
            }, 
            'secret': ''
            }, 
            'server2': {
                'ip': '0.0.0.0', 
                'port': {'value': 1813}, 
                'secret': '0'
                }}, 
        'nas': {
        'identifier': {}, 
        'ip': '0.0.0.0'
        }}, 
        'rf_monitoring': False, 
        'led': True, 
        'country_code':'United States', 
        'eapol_version': 'v2', 
        'poe_out': False, 
        'low_power': False, 
        'band_steering': {}, 
        'sslvpn': {
            'server': '1.1.1.1', 
            'user_name': 'sslvpntest', 
            'password': 'sslvpntest', 
            'domain': 'test.com', 
            'auto_reconnect': False
            }, 
        'administrator': {
            'name': 'testuser2', 
            'password': 'testuser2'
            }, 'retain': {}, 
            'radio_2400mhz': {
                'virtual_access_point': {'group': ''}, 
                'enable': False, 
                'ssid': 'sonicwall-4D6C-1', 
                'short_guard_interval': True, 
                'aggregation': True, 
                'schedule': {'always_on': True}, 
                'band': 'auto', 
                'channel': {'primary': 'auto', 'secondary': 'auto'}, 
                'mode': {'n_only': True}, 
                'access_list': {}, 
                'mic_failure': {'acl_blacklist': False, 'frequency': 3}, 
                'dynamic_vlan': False, 
                'authentication_type': {
            'wpa3': {'eap_192b': True}
            }, 
            'wpa': {
            'cipher_type': 'gcmp', 
            'group_key_interval': 86400, 
            'auth_balance_method': 'remote-radius-only'
            }, 
            'hide_ssid': False, 
            'data_rate': 'best', 
            'transmit_power': 'full', 
            'interval': {'beacon': 100, 'dtim': 1}, 
            'threshold': {'rts': 2346}, 
            'max_clients': 32, 
            'station_inactivity_timeout': 300, 
            'wmm': '', 
            'airtime_fairness': False, 
            'wds_ap': False, 
            'green_ap': {'enable': False, 'timeout': 20}, 
            'ids_scan': {'schedule': {}}, 
            'rssi': {'enable': False, 'threshold': -95}, 
            '80211r': {
                'enable': False, 
                'ft_over_ds': False, 
                'mix_mode': False
                }, 
                '80211k': {'neighbour_report': False}, 
                '80211v': {'bss_trans_mgmt': False, 'wnm_sleep': False}, 
                'preamble_length': 'long'
                }, 
            'radio_5000mhz': {
            'virtual_access_point': {'group': ''}, 
            'enable': True, 
            'ssid': 'sonicwall-4D6C', 
            'short_guard_interval': True, 
            'aggregation': True, 
            'schedule': {'always_on': True}, 
            'band': '40', 
            'channel': {'primary': '40', 'secondary': 'auto'}, 
            'dfs_channel': False, 
            'mode': {'5000mhz': 'na-mixed'}, 
            'access_list': {}, 
            'mic_failure': {'acl_blacklist': False, 'frequency': 3}, 
            'authentication_type': {"wpa2":{"auto":"psk"}},
            'wep_key': {'type': 'none'}, 
            'hide_ssid': False, 
            'data_rate': 'best', 
            'transmit_power': 'full', 
            'interval': {'beacon': 100, 'dtim': 1}, 
            'threshold': {'rts': 2346}, 
            'max_clients': 32, 
            'station_inactivity_timeout': 300, 
            'wmm': '', 
            'airtime_fairness': False, 
            'wds_ap': False, 
            'green_ap': {'enable': False, 'timeout': 20}, 
            'ids_scan': {'schedule': {}}, 
            'rssi': {'enable': False, 'threshold': -95}, 
            '80211r': {
                'enable': False, 
                'ft_over_ds': False, 
                'mix_mode': False
                }, 
            '80211k': {
                'neighbour_report': False
                }, 
                '80211v': {'bss_trans_mgmt': False, 'wnm_sleep': False}},
                'widp_sensor': {}, 
                'wwan': {'enable': False, 'bound_to': ''}, 
                'connection_profile': {
                'enable': False, 
                'country': '', 
                'service_provider': '', 
                'plan_type': '', 
                'dialed_number': '', 
                'user_name': '', 
                'user_password': '', 
                'apn': ''
                }, 
                'ble': {
                    'advertisement': False, 
                    'ibeacon': {'enable': False, 'uuid': '', 'major': {}, 'minor': {}}}, 
                    'mesh': {'2400mhz': {'enable': False}, '5000mhz': {'enable': False}
                    }
                }
]}}
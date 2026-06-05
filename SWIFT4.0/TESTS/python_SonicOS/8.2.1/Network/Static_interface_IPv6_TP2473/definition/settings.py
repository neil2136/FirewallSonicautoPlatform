import sys
import os
import time
import re
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


#import form branch lib contents for testsuite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.API.system import PacketmonitorApi, SettingApi, AdminApi
from lib.modules.CLI.network import InterfaceCli


suite_path = os.environ['PYTHON_SONICOS_HOME'] + \
    '/Network/Static_interface_IPv6_TP2473/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/static_interface_ipv6.json'


# parameters on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
localhost = Host(PC1_ETH1_IP)
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
pc2_login = Host(PC2_ETH2_IP)


# parameters on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X2_IP = '12.12.2.168'
    REM_X3_IP = '12.12.3.201'
    REM_X2_IP = '12.12.2.201'
    REM_X2_NET = '12.12.2.0'
    REM_X2_V6_IP = '2102::169'
    X0_V6_IP = '2000::168'
    X2_V6_IP = '2102::168'
    X1_V6_IP = '2002::168'
    PREFIX_LEN = 64
    V6_DNS = REM_X2_V6_IP
    UNREACH_V6_ADDR = '2003::100'
    PC1_ETH1_V6 = "2000::100"
    X0_TEM_IP = ""


# Instantiate objects including API, CLI import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)
rem_fw = Firewall(
    Parameter.REM_X3_IP,
    user='admin',
    password='password',
    supported_config_mode='api'
)
rem_fw_cli = Firewall(
    Parameter.REM_X3_IP,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')


iface_v4_api = network.InterfaceIPv4Api(fw)
iface_cli = InterfaceCli(fw_cli)
iface_v6_api = network.InterfaceIPv6Api(fw)
pkt_api = PacketmonitorApi(fw)
setting_api = SettingApi(fw)
dns_api = network.DnsSettingsApi(fw)
ao_api = network.AddressobjectsApi(fw)
wlb_api = network.FailoverLbApi(fw)
route_api = network.RoutePolicyApi(fw)
nat_v6_api = network.NatpolicyApi(fw)
admin_api = AdminApi(fw)

rm_ifacev6_api = network.InterfaceIPv6Api(rem_fw)
rm_ifacev4_api = network.InterfaceIPv4Api(rem_fw)
rm_dhcpv6_api = network.DHCPServerApi(rem_fw)
rm_ao_api = network.AddressobjectsApi(rem_fw)
rm_iface_cli = InterfaceCli(rem_fw_cli)



class CaseParams:
    rem_x2_linklocal = ''


# Parameters on case
x0_v6_dict = {
    'name': 'X0',
    'mode': 'static',
    'zone': 'LAN',
    'ip': Parameter.X0_V6_IP,
    'prefix_length': 64,
    'mgmt_ping': True,
    'mgmt_https': True
}

rem_x2v6_dict = {
        'name': 'X2',
        'mode': 'static',
        'zone': 'WAN',
        'ip': Parameter.REM_X2_V6_IP,
        'prefix_length': 64,
        'router_adv': True,
        'ra_min': 20,
        'ra_max': 60,
        'managed': True,
        'other_config': True,
        'mgmt_ping': True,
        'mgmt_https': True,
        'mgmt ssh': True
    }

x2v6_static_dict = {
        'name': 'X2',
        'mode': 'static',
        'zone': 'WAN',
        'ip': Parameter.X2_V6_IP,
        "gateway": Parameter.REM_X2_V6_IP,
        'ra_min': 20,
        'ra_max': 60,
        'prefix_length': 64,
        'mgmt_ping': True,
        'mgmt_https': True
    }

rem_x2v6_update = {'ip': "2102::170"}

x2v6_update_dict = {"gateway": "2102::170"}

x1v6_static_dict = {
    'name': 'X1',
    'mode': 'static',
    'zone': 'WAN',
    'ip': Parameter.X1_V6_IP,
    'prefix_length': 64,
    'mgmt_ping': True,
    'mgmt_https': True
}

x1_dhcpv6_dict = {
    'name': 'X1',
    'mode': 'dhcpv6',
    'zone': 'WAN',
    'dhcpv6': {
        'mode': 'manual'
    },
    'mgmt_ping': True,
    'mgmt_https': True,
    'listen_router_advertisement': True
}

x0v6_update_dict = {
    'name': 'X0',
    'mode': 'static',
    'zone': 'LAN',
    'ip': '100::12',
    'prefix_length': 32,
    'mgmt_ping': True,
    'mgmt_https': True
}

extra_dict = {
    'name': 'x0',
    'type': 'static',
    "subnet_prefix_adv": True,
    'ip': "1000::1",
    'prefix_length': 64
}

v6_nat_dict = {
            "nat_policies": [{
                "ipv6": {
                    "name": "test for case39",
                    "reflexive": False,
                    "comment": "",
                    "enable": True,
                    "inbound": "X0",
                    "outbound": "any",
                    "source": {
                        "name": "X0 IPv6 Primary Static Address Subnet"
                    },
                    "translated_source": {
                        "name": "X2 IPv6 Primary Static Address"
                    },
                    "destination": {
                        "any": True
                    },
                    "translated_destination": {
                        "original": True
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
            }]
        }

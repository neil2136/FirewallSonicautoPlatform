import os
import sys
import copy
import re
import time
import base64
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_PBR_TP2518_Part2')
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from lib.modules.API import network,policy,object
from utm import Firewall
from lib.modules.CLI.system import LicenseCli

OpenS = Openstack(Params.testbed)
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_PBR_TP2518_Part2/testplan/IPv6_PBR_TP2518_Part2.json'

DUT_X0_IPV4 = '192.168.168.168'
DUT_X0_IPV6 = '2001:db0::193'
DUT_X0_NET_IPV6 = '2001:db0::0'
DUT_X1_IPV4 = '13.0.0.10'
DUT_X1_NET_IPV4 = '13.0.0.0'
DUT_X2_IPV4 = '23.0.0.10'
DUT_X1_IPV6 = '2001:db1::193'
DUT_X1_GW= '2001:db1::1'
DUT_X1_NET_IPV6 = '2001:db1::0'
DUT_X2_IPV6 = '2001:db2::193'
DUT_X2_GW= '2001:db2::1'
DUT_X2_NET_IPV6 = '2001:db2::0'
PC2_ETH0_IPV6 = '2001:db1::1093'
PC2_ETH2_IPV6 = '2001:db4::183'

# result = {}

fw_api = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto',ssh_version=2, supported_config_mode='cli-ssh')

interfacev4api = network.InterfaceIPv4Api(fw_api)
interfacev6api = network.InterfaceIPv6Api(fw_api)
license_obj = LicenseCli(fw_cli)
route_obj = policy.RoutePolicyApi(fw_api)
addr_obj = network.AddressobjectsApi(fw_api)
addrGroup_obj = object.AddressObjectGroupApi(fw_api)

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
            'gateway':PC2_ETH0_IPV6,
            'ra_max': 30
            }
x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUT_X2_IPV4,
            'netmask': '255.255.255.0',
            'gateway': '23.0.0.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }
x2_ipv6 = {'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': DUT_X2_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            # 'gateway':PC3_ETH0_IPV6,
            'ra_max': 30
            }

ipv4_ao1 = {
    'name': 'ipv4_ao',
    'zone': 'WAN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(DUT_X1_NET_IPV4),
}
ipv4_ao2 = {
    'name': 'ipv4_ao2',
    'zone': 'WAN',
    'object_type': 'host',
    'value':DUT_X2_IPV4 ,
}
ipv6_ao1 = {
    'name': 'ipv6_ao1',
    'zone': 'WAN',
    'object_type': 'network',
    'subnet': DUT_X0_NET_IPV6,
    'mask': '/64',
}
ipv6_ao2 = {
    'name': 'ipv6_ao2',
    'zone': 'WAN',
    'object_type': 'network',
    'subnet': DUT_X1_NET_IPV6,
    'mask': '/64',
}
ipv6_ao3 = {
    'name': 'ipv6_ao3',
    'zone': 'WAN',
    'object_type': 'host',
    'ip': DUT_X2_IPV6,
}

ipv6_group =  {
    "address_groups":[{
        "ipv6":{
            "address_object":{
                "ipv6":[{
                    "name":"ipv6_ao1"
                    },
                    {
                    "name":"ipv6_ao2"
                    }]},
            "name":"ipv6_group"
        }
    }]
}
ipv4_route = {
    "route_policies":
    [{"ipv4":{
        "name":"test_ipv4",
        "comment":"",
        "interface":"X1",
        "metric":4,
        "service":{"any":True},
        "gateway":{"name":"ipv4_ao2"},
        "source":{"name":"ipv4_ao"},
        "destination":{"name":"ipv4_ao2"},
        "disable_on_interface_down":True,
        "vpn_precedence":False,
        "probe":"",
        "distance":{"auto":True},
        "tos":"0x00",
        "mask":"0x00",
        "type":"standard"
        }
    }]
}
ipv6_route = {
    "route_policies":
    [{"ipv6":{
        "name":"test1",
        "comment":"",
        "interface":"X1",
        "metric":3,
        "service":{"any":True},
        "gateway":{"name":"ipv6_ao3"},
        "source":{"name":"ipv6_ao2"},
        "destination":{"name":"ipv6_ao1"},
        "disable_on_interface_down":True,
        "vpn_precedence":False,
        "probe":"",
        "distance":{"auto":True},
        "tos":"0x00",
        "mask":"0x00",
        "type":"standard"
        }
    }]
}

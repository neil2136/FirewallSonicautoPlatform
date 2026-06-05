import sys
import os
import re
import time
import paramunittest

from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from tools.trafficGen import ScapyPacketSend

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/ECMP/')
from lib.modules.API.network import InterfaceIPv4Api, RoutePolicyApi, AddressobjectsApi
from lib.modules.API.system import PacketmonitorApi, DiagnosticApi, RestartApi
from lib.modules.CLI.network import RouteCli, InterfaceCli
from lib.modules.CLI.system import LicenseCli


class Parameter:
    DUT_X0_IP = "192.168.168.168"
    DUT_X1_IP = "13.0.11.110"
    DUT_X1_GW = "13.0.11.120"
    X1_GW_MGMT = "172.168.0.110"
    DUT_X2_IP = "13.0.12.110"
    DUT_X2_GW = "13.0.12.120"
    X2_GW_MGMT = "172.168.0.120"
    DUT_X3_IP = "13.0.13.110"
    DUT_X3_GW = "13.0.13.120"
    X3_GW_MGMT = "172.168.0.130"
    DUT_X4_IP = "13.0.14.110"
    DUT_X4_GW = "13.0.14.120"
    X4_GW_MGMT = "172.168.0.140"
    DUT_X5_IP = "12.12.1.168"
    DUT_X5_GW = "12.12.1.1"
    X5_GW_MGMT = "172.168.0.150"
    VPN2_IP = '12.12.1.201'
    VPN2_Host = '172.16.1.3'
    VPN2_X0_IP = '172.16.1.101'
    VPN2_X0_Net = '172.16.1.0,255.255.255.0'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/ECMP/testplan/ecmp_auto.json'

    SRC_HOST = '192.168.168.60/27'
    DST_HOST = "100.100.10.200"
    DST_NET = "100.100.10.0/24"
    SRC_RANGE = '192.168.168.160/27'
    DST_NETWORK = "100.100.10.192/27"
    SRC_NETWORK = '192.168.168.192/27'

    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


icmp_dict = {
    'IP': {
        'version': '4',
        'src': Parameter.SRC_HOST,
        'dst': Parameter.DST_HOST,
    },
    'ICMP': {
        'type': '8'
    },
    'conf': {
        'iface': 'eth0',
        'route': {
            'net': Parameter.DST_NET,
            'gw': Parameter.DUT_X0_IP
        }
    }
}

gw1_ao_dict = {
    "object_type": "host",
    "name": "gw1_ao",
    "zone": "WAN",
    "value": "13.0.11.121"
}

gw2_ao_dict = {
    "object_type": "host",
    "name": "gw2_ao",
    "zone": "WAN",
    "value": "13.0.11.122"
}

gw3_ao_dict = {
    "object_type": "host",
    "name": "gw3_ao",
    "zone": "WAN",
    "value": "13.0.11.123"
}

gw4_ao_dict = {
    "object_type": "host",
    "name": "gw4_ao",
    "zone": "WAN",
    "value": "13.0.11.124"
}

dns_server_ao_dict = {
    "object_type": "host",
    "name": "dns_server",
    "zone": "WAN",
    "value": "10.190.202.200"
}

server_pc_ao_dict = {
    "object_type": "host",
    "name": "server_pc",
    "zone": "WAN",
    "value": "100.100.10.200"
}

client_range_ao_dict = {
    "object_type": "range",
    "name": "client_range",
    "zone": "LAN",
    "value": "192.168.168.161,192.168.168.191"
}

client_network_ao_dict = {
    "object_type": "network",
    "name": "client_network",
    "zone": "LAN",
    "value": "192.168.168.192,255.255.255.224"
}

server_network_ao_dict = {
    "object_type": "network",
    "name": "server_network",
    "zone": "WAN",
    "value": "100.100.10.192,255.255.255.224"
}

ecmp_1gw_api_rt_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "ecmp_1gw_api",
                "comment": "",
                "interface": "X1",
                "metric": 10,
                "service": {
                    "any": True
                },
                "gateway": {
                    "name": "gw1_ao"
                },
                "nexthop_number": 4,
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "dns_server"
                },
                "disable_on_interface_down": True,
                "vpn_precedence": False,
                "probe": "",
                "interface2": "X1",
                "gateway2": {
                    "name": "gw2_ao"
                },
                "interface3": "X1",
                "gateway3": {
                    "name": "gw3_ao"
                },
                "interface4": "X1",
                "gateway4": {
                    "name": "gw4_ao"
                },
                "distance": {
                    "auto": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "type": "multi-path"
            }
        }
    ]
}

ecmp_4gw_api_rt_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "ecmp_4gw_api",
                "comment": "",
                "interface": "X1",
                "metric": 10,
                "service": {
                    "any": True
                },
                "gateway": {
                    "name": "X1 Default Gateway"
                },
                "nexthop_number": 4,
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "server_pc"
                },
                "disable_on_interface_down": True,
                "vpn_precedence": False,
                "probe": "",
                "interface2": "X2",
                "gateway2": {
                    "name": "X2 Default Gateway"
                },
                "interface3": "X3",
                "gateway3": {
                    "name": "X3 Default Gateway"
                },
                "interface4": "X4",
                "gateway4": {
                    "name": "X4 Default Gateway"
                },
                "distance": {
                    "auto": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "type": "multi-path"
            }
        }
    ]
}

ecmp_4gw_range_rt_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "ecmp_4gw_range",
                "comment": "",
                "interface": "X1",
                "metric": 10,
                "service": {
                    "any": True
                },
                "gateway": {
                    "name": "X1 Default Gateway"
                },
                "nexthop_number": 4,
                "source": {
                    "name": "client_range"
                },
                "destination": {
                    "name": "server_network"
                },
                "disable_on_interface_down": True,
                "vpn_precedence": False,
                "probe": "",
                "interface2": "X2",
                "gateway2": {
                    "name": "X2 Default Gateway"
                },
                "interface3": "X3",
                "gateway3": {
                    "name": "X3 Default Gateway"
                },
                "interface4": "X4",
                "gateway4": {
                    "name": "X4 Default Gateway"
                },
                "distance": {
                    "auto": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "type": "multi-path"
            }
        }
    ]
}

ecmp_4gw_network_rt_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "ecmp_4gw_network",
                "comment": "",
                "interface": "X1",
                "metric": 10,
                "service": {
                    "any": True
                },
                "gateway": {
                    "name": "X1 Default Gateway"
                },
                "nexthop_number": 4,
                "source": {
                    "name": "client_network"
                },
                "destination": {
                    "name": "server_network"
                },
                "disable_on_interface_down": True,
                "vpn_precedence": False,
                "probe": "",
                "interface2": "X2",
                "gateway2": {
                    "name": "X2 Default Gateway"
                },
                "interface3": "X3",
                "gateway3": {
                    "name": "X3 Default Gateway"
                },
                "interface4": "X4",
                "gateway4": {
                    "name": "X4 Default Gateway"
                },
                "distance": {
                    "auto": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "type": "multi-path"
            }
        }
    ]
}

ecmp_cli_rt_dict = {
    "version": "ipv4",
    "if": "X1",
    "metric": 10,
    "gateway": 'name "X1 Default Gateway"',
    "destination": 'name "server_pc"',
    "name": "ecmp_cli",
    "nexthop-number": 4,
    "interface2": "X2",
    "gateway2": 'name "X2 Default Gateway"',
    "interface3": "X3",
    "gateway3": 'name "X3 Default Gateway"',
    "interface4": "X4",
    "gateway4": 'name "X4 Default Gateway"'
}

ecmp_cli_new_rt_dict = {
    "name-new": "ecmp_cli_new",
    "nexthop-number-new": 3,
    "interface2": "X2",
    "gateway2": 'name "X2 Default Gateway"',
    "interface3": "X4",
    "gateway3": 'name "X4 Default Gateway"',
}

pkt_setting_dict = {
    'display_filter': {
        'bidirectional': True,
        'destination_ips': '',
        'destination_ports': '',
        'ip_types': 'icmp',
    }
}

expect_pkt_dict = {
    'src': '192.168.168.',
    'dst': '100.100.10.200',
    'in': 'X0',
    'out': '',
    'proto': 'ICMP',
}


ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fwcli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

interfaceipv4api = InterfaceIPv4Api(fw)
interfacecli = InterfaceCli(fwcli)
aoapi = AddressobjectsApi(fw)
routeapi = RoutePolicyApi(fw)
routecli = RouteCli(fwcli)
pkgmonitorapi = PacketmonitorApi(fw)
diagapi = DiagnosticApi(fw)
restartapi = RestartApi(fw)
licensecli = LicenseCli(fwcli)
scapysend = ScapyPacketSend(iface='eth0', count=5)

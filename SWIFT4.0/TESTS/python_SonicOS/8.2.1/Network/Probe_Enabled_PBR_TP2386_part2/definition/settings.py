import os
import sys
import copy
import ast
import re
import time
import json
import requests
import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from contextvars import ContextVar


# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, FirewallCLI
from util.enhancedinfo import show_testcase_info

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, NetworkMonitorApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.CLI.network import NetworkMonitorCli, RouteCli
from lib.modules.API.system import DiagnosticApi
from lib.modules.API.policy import NatPolicyApi, RoutePolicyApi

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Probe_Enabled_PBR_TP2386_part2'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/probe_enabled_pbr_tp2386_part2.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH0_IP = os_obj.get_node_interface_ip('PC3', 'eth0')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')


logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            f"\n PC2_ETH2_IP : {PC2_ETH2_IP}"
            f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            )

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)

#################################################################################################################
#
#                                                                                                              #
#  PC1(eth1)---------(192.168.168.168)DUT x1(12.12.1.101)---------x1_gw(12.12.1.1)                             #
#                    x3(193.168.1.101)|  |
#                                   PC2  PC3
#                        (193.168.1.20)  (193.168.1.22)
#
#################################################################################################################


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X2_IP = '193.168.1.168'
    X1_NET = '12.12.1.0'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

interfacev4api = InterfaceIPv4Api(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
routepolicyapi = RoutePolicyApi(fw_api)
ne_routepolicyapi = RoutePolicyApi(fw_api)
networkmonitorapi = NetworkMonitorApi(fw_api)
networkmonitorcli = NetworkMonitorCli(fw_cli)
routecli = RouteCli(fw_cli)
addressobjectgroupapi = AddressObjectGroupApi(fw_cli)
natpolicyapi = NatPolicyApi(fw_api)
diagnosticapi = DiagnosticApi(fw_api)


initial_pbr_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "test",
                "comment": "",
                "interface": "Nii",
                "metric": 20,
                "service": {
                    "any": True
                },
                "gateway": {
                    "default": True
                },
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "130.1.1.0"
                },
                "disable_on_interface_down": True,
                "probe": "",
                "distance": {
                    "auto": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "type": "standard",
                "auto_add_access_rules": True
            }
        }
    ]
}

nm_ping_explicit_dict = {
    "network_monitors": [
        {
            "policy": {
                "ipv4": {
                    "name": "nm_ping_explicit",
                    "probe": {
                        "target": {
                            "name": "pc2_eth1"
                        },
                        "type": {
                            "ping": "explicit"
                        },
                        "interval": 5
                    },
                    "reply_timeout": 1,
                    "interval": {
                        "missed": 3,
                        "successful": 3
                    },
                    "must_respond": False,
                    "comment": "",
                    "next_hop": {
                        "name": "x1_gw"
                    },
                    "outbound_interface": "X1"
                }
            }
        }
    ]
}

nm_ping_non_explicit_dict = {
    "network_monitors": [
        {
            "policy": {
                "ipv4": {
                    "name": "nm_ping_non_explicit",
                    "probe": {
                        "target": {
                            'name': 'pc2_eth2'
                        },
                        "type": {
                            'ping': 'non-explicit'
                        },
                        "interval": 5
                    },
                    "reply_timeout": 1,
                    "interval": {
                        "missed": 3,
                        "successful": 3
                    },
                    "must_respond": False,
                    "comment": "",
                }
            }
        }
    ]
}

nm_tcp_non_explicit_dict = {
    "network_monitors": [
        {
            "policy": {
                "ipv4": {
                    "name": "nm_tcp_non_explicit",
                    "probe": {
                        "target": {
                            'name': 'pc2_eth1'
                        },
                        "type": {
                            "tcp": {
                                "port": 80,
                                "non_explicit": True
                            }
                        },
                        "interval": 5
                    },
                    "reply_timeout": 1,
                    "interval": {
                        "missed": 3,
                        "successful": 3
                    },
                    "must_respond": False,
                    "comment": "",
                    "rst_as_miss": False
                }
            }
        }
    ]
}

nm_tcp_explicit_dict = {
    "network_monitors": [
        {
            "policy": {
                "ipv4": {
                    "name": "nm_tcp_explicit",
                    "probe": {
                        "target": {
                            'name': 'pc2_eth1'
                        },
                        "type": {
                            "tcp": {
                                "port": 80,
                                "explicit": True
                            }
                        },
                        "interval": 5
                    },
                    "reply_timeout": 1,
                    "interval": {
                        "missed": 3,
                        "successful": 3
                    },
                    "must_respond": False,
                    "comment": "",
                    "next_hop": {
                        "name": "X1 Default Gateway"
                    },
                    "outbound_interface": "X1",
                    "rst_as_miss": False
                }
            }
        }
    ]
}

add_nat_policy_with_probe_dict = {
    "nat_policies": [
        {
            "ipv4": {
                "name": "nat_policy_with_probe",
                "nat_method": "sticky-ip",
                "dns_doctoring": False,
                "reflexive": False,
                "inbound": "any",
                "outbound": "any",
                "comment": "",
                "enable": True,
                "translated_destination": {
                    "name": "x0_range"
                },
                "translated_source": {
                    "original": True
                },
                "translated_service": {
                    "original": True
                },
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "X1 IP"
                },
                "service": {
                    "any": True
                },
                "priority": {
                    "auto": True
                },
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                },
                "high_availability": {
                    "probing": {
                        "probe_type": {
                            "icmp_ping": True
                        },
                        "probe_every": 5,
                        "reply_timeout": 1,
                        "deactivate_after": 3,
                        "reactivate_after": 3
                    }
                }
            }
        }
    ]
}

edit_nat_policy_with_probe_dict = {
    "nat_policies": [
        {
            "ipv4": {
                "name": "nat_policy_with_probe",
                "nat_method": "sticky-ip",
                "dns_doctoring": False,
                # "reflexive": False,
                "inbound": "any",
                "outbound": "any",
                "comment": "",
                "enable": True,
                "translated_destination": {
                    "name": "x0_range"
                },
                "translated_source": {
                    "original": True
                },
                "translated_service": {
                    "original": True
                },
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "X1 IP"
                },
                "service": {
                    "any": True
                },
                "priority": {
                    "auto": True
                },
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                },
                "high_availability": {
                    "probing": {
                        "probe_type": {
                            "tcp": 80
                        },
                        "probe_every": 5,
                        "reply_timeout": 1,
                        "deactivate_after": 3,
                        "reactivate_after": 3
                    }
                }
            }
        }
    ]
}

route_policy_with_probe_dict = {
    "route_policies": [
        {
            "ipv4": {
                "name": "pbr_with_probe",
                "comment": "",
                "interface": "X1",
                "metric": 20,
                "service": {
                    "any": True
                },
                "gateway": {
                    "name": "X1 Default Gateway"
                },
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "10.103.202.200"
                },
                "disable_on_interface_down": False,
                "vpn_precedence": False,
                "probe": "nm_ping_non_explicit",
                "distance": {
                    "auto": True
                },
                "disable_when_probes_succeed": True,
                "default_probe_state_up": False,
                "tos": "0x00",
                "mask": "0x00",
                "type": "standard"
            }
        }
    ]
}

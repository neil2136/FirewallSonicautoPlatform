import os
import sys
import copy
import ast
import re
import time
import json
import winrm
import requests
import unittest
import paramunittest
from nose_parameterized import parameterized
from contextvars import ContextVar

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, FirewallCLI
from util.enhancedinfo import show_testcase_info
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, NetworkMonitorApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.CLI.network import NetworkMonitorCli, RouteCli
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.system import RestartApi, SettingApi
from lib.modules.API.policy import RoutePolicyApi, NatPolicyApi

# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Network_Monitor'
sys.path.append(suite_path)
TESTPLAN = suite_path + '/testplan/network_monitor.json'

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
PC4_ETH0_IP = os_obj.get_node_interface_ip('PC4', 'eth0')
PC4_ETH1_IP = os_obj.get_node_interface_ip('PC4', 'eth1')
PC5_ETH0_IP = os_obj.get_node_interface_ip('PC5', 'eth0')
PC5_ETH1_IP = os_obj.get_node_interface_ip('PC5', 'eth1')

logger.info(f"\n PC1_ETH0_IP : {PC1_ETH0_IP}"
            f"\n PC1_ETH1_IP : {PC1_ETH1_IP}"
            f"\n PC1_ETH2_IP : {PC1_ETH2_IP}"
            f"\n PC2_ETH0_IP : {PC2_ETH0_IP}"
            f"\n PC2_ETH1_IP : {PC2_ETH1_IP}"
            f"\n PC2_ETH2_IP : {PC2_ETH2_IP}"
            f"\n PC3_ETH0_IP : {PC3_ETH0_IP}"
            f"\n PC3_ETH1_IP : {PC3_ETH1_IP}"
            f"\n PC4_ETH0_IP : {PC4_ETH0_IP}"
            f"\n PC4_ETH1_IP : {PC4_ETH1_IP}"
            f"\n PC5_ETH0_IP : {PC5_ETH0_IP}"
            f"\n PC5_ETH1_IP : {PC5_ETH1_IP}"
            )

PC1_Login = Host(PC1_ETH1_IP)
PC2_Login = Host(PC2_ETH0_IP)
PC3_Login = Host(PC3_ETH0_IP)
PC4_Login = Host(PC4_ETH0_IP)
PC5_Login = Host(PC4_ETH0_IP)


#################################################################################################################
#
#
#  PC1(eth1)--------x0(192.168.168.168)DUT x1(12.12.1.101)---------(12.12.1.201) X1 remote DUT(X3)---------PC4
#                    x2(193.168.1.101)|  |                                                         --------pc5
#                                   PC2  PC3
#
#
#################################################################################################################


class Parameter:
    FIREWALL = '192.168.168.168'
    X0_NET = '192.168.168.0'
    X0_IP = '192.168.168.168'
    X1_IP = '12.12.1.200'
    X1_GW = '12.12.1.1'
    X2_IP = '193.168.1.168'
    X0_REMOTE_IP = '172.16.1.101'
    X1_REMOTE_IP = '12.12.1.201'
    X2_REMOTE_IP = '12.12.2.201'
    X3_REMOTE_IP = '12.12.3.201'
    X3_REMOTE_NET = '12.12.3.0'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2


ip = Parameter.FIREWALL
r_ip = Parameter.X0_REMOTE_IP
fw_api = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
r_fw_api = Firewall(r_ip, user='admin', password='sonicauto', supported_config_mode='api')

interfacev4api = InterfaceIPv4Api(fw_api)
addressobjectsapi = AddressobjectsApi(fw_api)
routepolicyapi = RoutePolicyApi(fw_api)
restartapi = RestartApi(fw_api)
settingapi = SettingApi(fw_api)
networkmonitorapi = NetworkMonitorApi(fw_api)
networkmonitorcli = NetworkMonitorCli(fw_cli)
routecli = RouteCli(fw_cli)
addressobjectgroupapi = AddressObjectGroupApi(fw_cli)
vpnbasesettingapi = VpnbasesettingApi(fw_api)
accessruleipv4api = AccessRuleIPv4Api(fw_api)
natpolicyapi = NatPolicyApi(fw_api)
r_vpnbasesettingapi = VpnbasesettingApi(r_fw_api)
r_interfacev4api = InterfaceIPv4Api(r_fw_api)
r_addressobjectsapi = AddressobjectsApi(r_fw_api)
r_accessruleipv4api = AccessRuleIPv4Api(r_fw_api)

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
                            "name": "x1_gw"
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
                        "name": "X1 Default Gateway"
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

nm_ping_explicit_with_ti_dict = {
    "network_monitors": [
        {
            "policy": {
                "ipv4": {
                    "name": "",
                    "probe": {
                        "target": {
                            'name': 'pc4_eth1'
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
                    "local_ip": {
                        "name": "X0 IP"
                    },
                    "outbound_interface": ""
                }
            }
        }
    ]
}

nat_policy_dict = {
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
                "disable_on_interface_down": True,
                "vpn_precedence": False,
                "probe": "nm_ping_non_explicit",
                "distance": {
                    "auto": True
                },
                "disable_when_probes_succeed": False,
                "default_probe_state_up": False,
                "tos": "0x00",
                "mask": "0x00",
                "type": "standard"
            }
        }
    ]
}

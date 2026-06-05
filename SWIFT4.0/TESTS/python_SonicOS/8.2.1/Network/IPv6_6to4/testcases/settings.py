import sys
import re
import os
import time
import json
import ipaddress
import unittest
import paramunittest
import unittest
from nose_parameterized import parameterized
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_6to4')
from runner.unittest.setup import Test, repeat_method
from lib.modules.CLI.network import InterfaceCli
from lib.modules.CLI.network import DhcpServerCli
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import network
from lib.modules.API import firewall
from lib.modules.API import system
from lib.modules.API import vpn
from utm import Firewall,FirewallAPI
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from tools import trafficGen


class Parameter():
    DUT_X0_IP = "192.168.168.168" 
    DUT_X1_IP = "12.12.1.168"  
    DUT_X1_GW = "12.12.1.1"  
    DUT_X2_IP = "12.12.2.168"    
    DUT_X2_GW = "12.12.2.1"    
    DUT_X2_IP_NEW = "12.12.2.100"
    DUT_X3_IP = "12.12.3.168"   
    DUT_X3_GW = "12.12.3.1"   
    DUT_X3_NETWORK = "12.12.3.0"
    TUNNEL_IP = '100::100'
    TUNNEL_IP_2 = '101::101'
    TUNNEL_IP_3 = '102::102'
    IP_6RD = '2022::100'
    REMOTE_X0 = '176.16.1.169'
    REMOTE_X1 = '12.12.1.201' 
    REMOTE_X2 = '12.12.2.201' 
    REMOTE_X3 = '176.16.2.169' 
    REMOTE_X1_GW = '12.12.1.1'
    NETMASK = '255.255.255.0'
    PC1_LAN = '192.168.168.101'
    PC1_WAN = '12.12.1.101'
    PC1_ETH0_V6 = '2012::100'
    MCAST_V4= '224.0.0.2'
    BCAST_V4 = '255.255.255.255'
    LOCAL_V6 = 'fe80::217:c5ff:fe17:4cd'
    BCAST_V6 = 'ff02::1'
    REMOTE_X1_IP_new = "12.12.1.248"
    REMOTE_X0_IPv6_Network_new = "2001:444::"
    REMOTE_X0_IPv6_new = "2001:444::1"
    PC2_X0_IPv6_new = "2001:444::2"
    rem_gw_new = "2001:444::1"

    DUT_X0_IPv6  = {
        "6to4"        : "2002:c0c:1a8::100",
        "6to4-relay"  : "2002:c0c:1a8::100",
        "manual"      : "2001:678::100",
        "gre"         : "2001:678::100",
    }
    REMOTE_X0_IPv6= {
        "6to4"        : "2002:c0c:1c9::200",
        "6to4-relay"  : "2003::200",
        "manual"      : "2001:789::200",
        "gre"         : "2001:789::200",
    }
    DUT_X3_IPv6  = {
        "6to4"        : "2002:c0c:2a8::100",
        "manual"      : "2001:123::100",
        "gre"         : "2001:123::100",
    }
    REMOTE_X3_IPv6= {
        "6to4"        : "2002:c0c:2c9::200",
        "manual"      : "2001:456::200",
        "gre"         : "2001:456::200",
    }
    PC1_X0_IPv6  = {
        "6to4"        : "2002:c0c:1a8::101",
        "6to4-relay"  : "2002:c0c:1a8::101",
        "manual"      : "2001:678::101",
        "gre"         : "2001:678::101",
    }
    PC2_X0_IPv6= {
        "6to4"        : "2002:c0c:1c9::201",
        "6to4-relay"  : "2003::201",
        "manual"      : "2001:789::201",
        "gre"         : "2001:789::201",
    }
    PC3_X3_IPv6  = {
        "6to4"        : "2002:c0c:2a8::101",
        "manual"      : "2001:123::101",
        "gre"         : "2001:123::101",
    }
    PC4_X3_IPv6= {
        "6to4"        : "2002:c0c:2c9::201",
        "manual"      : "2001:456::201",
        "gre"         : "2001:456::201",
    }

    DUT_X0_IPv6_Network = {
        "6to4"        : "2002:c0c:1a8::",
        "manual"      : "2001:678::",
        "gre"         : "2001:678::",
    }
    REMOTE_X0_IPv6_Network = {
        "6to4"        : "2002:c0c:1c9::",
        "manual"      : "2001:789::",
        "gre"         : "2001:789::",
    }
    DUT_X3_IPv6_Network = {
        "6to4"        : "2002:c0c:2a8::",
        "manual"      : "2001:123::",
        "gre"         : "2001:123::",
    }
    REMOTE_X3_IPv6_Network = {
        "6to4"        : "2002:c0c:2c9::",
        "manual"      : "2001:456::",
        "gre"         : "2001:456::",
    }
    PC1_INTERFACE = {
        "LAN"         : "eth0",
        "WAN"         : "eth1",
    }
    PC2_INTERFACE = "eth1"
    PC3_INTERFACE = "eth1"
    PC4_INTERFACE = "eth1"

    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + "/Network/IPv6_6to4/testplan/6to4.json"

ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
interface = network.InterfaceIPv4Api(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
ao = network.AddressobjectsApi(fw)
acl = firewall.AccessRuleApi(fw)
acl_ipv6 = firewall.AccessRuleIPv6Api(fw)
failover = network.FailoverLbApi(fw)
route = network.RoutePolicyApi(fw)
setting = system.SettingApi(fw)
diag =system.DiagnosticApi(fw)
Lvpn = vpn.VpnbasesettingApi(fw)
license_obj = LicenseCli(fw_cli)

if Params.openstack:
    osstack = Openstack(Params.testbed)
    consvr, conport = osstack.get_console_info(dut='RemoteGEN6')
# rem_fw = Firewall(Parameter.REMOTE_X1, user='admin', password='password', console_ip=consvr, console_port=conport, supported_config_mode = 'cli-console')
rem_fw_api = FirewallAPI(Parameter.REMOTE_X1, user='admin', password='password')
rem_fw_new = Firewall(Parameter.REMOTE_X1_IP_new, user='admin', password='password')
rem_interface = InterfaceCli(rem_fw_api)
rem_interface_api = network.InterfaceIPv4Api(rem_fw_api)
rem_interface_new = network.InterfaceIPv4Api(rem_fw_new)
rem_interface_v6 = network.InterfaceIPv6Api(rem_fw_api)
rem_interface_v6_new = network.InterfaceIPv6Api(rem_fw_new)
rem_dhcp = DhcpServerCli(rem_fw_api)
rem_ao = network.AddressobjectsApi(rem_fw_api)
rem_acl = firewall.AccessRuleApi(rem_fw_api)
rem_acl_ipv6 = firewall.AccessRuleIPv6Api(rem_fw_api)
rem_vpn = vpn.VpnbasesettingApi(rem_fw_api)
rem_route = network.RoutePolicyApi(rem_fw_api)

pc1 = Host('localhost')
pc2 = Host(Params.testbed + '-PC2')
pc3 = Host(Params.testbed + '-PC3')
pc4 = Host(Params.testbed + '-PC4')

lb = {
    "failover_lb": {
        "group": [
            {
                "name": " Default LB Group",
                "type": "basic",
                "probing": {
                    "health_check": 5,
                    "missed_intervals": 6,
                    "successful_intervals": 3,
                    "global_responder": False
                },
                "interface": [
                    {
                        "name": "X1",
                        "rank": 1,
                        "probe_type": "logical",
                        "probe_condition": "both",
                        "main_target":{
                            "protocol":{"ping":True},
                            "host":"0.0.0.0"
                        },
                        "alternate_target":{
                            "protocol":{"ping":True},
                            "host":"0.0.0.0"
                        },
                        "default_target":{"value":Parameter.DUT_X1_GW}
                    },
                    {
                        "name": "TC8",
                        "rank": 2,
                        "probe_type": "logical",
                        "probe_condition": "both",
                        "main_target":{
                            "protocol":{"ping":True},
                            "host":"0.0.0.0"
                        },
                        "alternate_target":{
                            "protocol":{"ping":True},
                            "host":"0.0.0.0"
                        },
                        "default_target":{"value":Parameter.DUT_X2_GW}

                    },
                ]
            }
        ]
    }
}
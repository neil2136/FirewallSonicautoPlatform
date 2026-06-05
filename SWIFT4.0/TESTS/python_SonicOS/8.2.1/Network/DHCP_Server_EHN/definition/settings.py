import os
import sys
import re
import time
import copy
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion


# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host


# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API.system import PacketmonitorApi, SettingApi
from lib.modules.API.network import DHCPServerApi, InterfaceIPv4Api, DnsSettingsApi



suite_path = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Network/DHCP_Server_EHN'
sys.path.append(suite_path)
sys.path.append(suite_path+'/testcases')
TESTPLAN = suite_path + "/testplan/DHCP_Server_EHN.json"
DHCP_SERVER_CONF_FILE = suite_path + '/definition/conf_file/dhcpd.conf'
PPPOE_SERVER_CONF_FILE = suite_path + '/definition/conf_file/pppoe_confs'
EXP_FILE = '/tmp/cyuan_dhcp_test.exp'
DHCLIEN_LEASE_FILE = '/var/lib/dhclient/dhclient.leases'


# params on openstack
os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')  
PC2_ETH3_IP = os_obj.get_node_interface_ip('PC2', 'eth3')  
PC4_ETH2_IP = os_obj.get_node_interface_ip('PC4', 'eth2')  
PC5_ETH2_IP = os_obj.get_node_interface_ip('PC5', 'eth2')  
logger.info('#'*20)
logger.info(f'pc1 eth1 ip addr is {PC1_ETH1_IP}')
logger.info(f'pc3 eth1 ip addr is {PC3_ETH2_IP}')
logger.info(f'pc2 eth1 ip addr is {PC2_ETH3_IP}')
logger.info(f'pc4 eth1 ip addr is {PC4_ETH2_IP}')
logger.info(f'pc5 eth1 ip addr is {PC5_ETH2_IP}')
logger.info('#'*20)

pc1_login = Host('localhost')
pc2_login = Host(PC2_ETH3_IP)
pc3_login = Host(PC3_ETH2_IP)
pc4_login = Host(PC4_ETH2_IP)
pc5_login = Host(PC5_ETH2_IP)


# params on fw
class Parameter:
    FIREWALL = "192.168.168.168"
    X1_IP = '172.17.1.10'
    X1_GW = '172.17.1.1'
    X1_DNS_1 = Params.G_DNS1
    X1_DNS_2 = Params.G_DNS2
    X2_IP = '2.2.2.168'
    X3_IP = '3.3.3.168'
    PPPOE_SERVER = '172.17.2.1'
    pppoe_pool_start = '172.17.2.2'
    pppoe_pool_end = '172.17.2.20'
    PPPOE_DNS = '156.154.54.200'


# Instance Objects
fw = Firewall(Parameter.FIREWALL,
              user='admin',
              password='password',
              supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL,
                  user='admin',
                  password='password',
                  supported_config_mode='cli-ssh')
dhcpserverapi = DHCPServerApi(fw)
interfacev4api = InterfaceIPv4Api(fw)
interfacev4cli = InterfaceCli(fw_cli)
packetapi = PacketmonitorApi(fw)
settingsapi = SettingApi(fw)
dnsapi = DnsSettingsApi(fw)


# Params on case
class CaseParams:
    tc14_res = False
    tc14_pc2_ip = ''
    tc28_pc3_eth1_ip = ''
    tc16_res1 = False
    tc16_res2 = False
    tc29_res = False
    tc38_res = False
    pc3_eth1_mac = ''
    pc2_eth2_mac = ''
    pc4_eth1_mac = ''
    pc5_eth1_mac = ''

dynamic_scope_base = {
    "dhcp_server":
        {"ipv4": {
            "scope": {
                "dynamic": [
                    {
                        "from": "",
                        "to": "",
                        "enable": True,
                        "lease_time": 60,
                        "default_gateway": "",
                        "netmask": "255.255.255.0",
                        "comment": "",
                        # "allow_bootp":False,
                        "domain_name": "",
                        "dns": {"server": {"inherit": True}},
                    }
                ]
            }
        }
        }
}

static_scope_base = {
    "dhcp_server":
        {"ipv4": {
            "scope": {
                "static": [
                    {
                        "ip": "",
                        "mac": "",
                        "name": "",
                        "enable": True,
                        "lease_time": 60,
                        "default_gateway": "",
                        "netmask": "255.255.255.0",
                        "comment": "",
                        "domain_name": "test.com",
                        "dns": {"server": {"static": {"primary": "1.1.1.1", "secondary": "2.2.2.2", "tertiary": "0.0.0.0"}}},
                    }
                ]
            }
        }
    }
}

# case 10
tc10_x2_dhcp_dict = {
    "from": "2.2.2.6",
    "to": "2.2.2.10",
    "default_gateway": "2.2.2.168",
    "comment": "test for domain with maximun numbers",
    "domain_name": "12345678901234567890123456789012345678901qazxsw23edcvfr45tg.com"
}
tc10_edit_dict1 = {
    "from": "2.2.2.6",
    "to": "2.2.2.10",
    "default_gateway": "2.2.2.168",
    "comment": "test for domain with upper cases",
    "domain_name": 'SonicWall.com'
}
tc10_edit_dict2 = {
    "from": "2.2.2.6",
    "to": "2.2.2.10",
    "default_gateway": "2.2.2.168",
    "comment": "test for domain with multi level",
    'domain_name': '123.abc.efg.com'
}

# case 14
tc14_dynamic_dict = {
    "from": "2.2.2.6",
    "to": "2.2.2.10",
    "default_gateway": "2.2.2.168",
    "comment": "dhcp lease for x2 interface",
    "domain_name": "example.com"
}

# case 16
tc16_static_dict = {
    "ip": "3.3.3.200",
    "mac": '',
    "enable": True,
    "name": "test_tc16",
    "lease_time": 5,
    "default_gateway": "3.3.3.168",
    "comment": "test for case 16",
    "dns": {"server": {"static": {"primary": "1.1.1.1", "secondary": "2.2.2.2", "tertiary": "0.0.0.0"}}},
}

# case 27
tc27_dynamic_dict = {
    "from": "2.2.2.6",
    "to": "2.2.2.7",
    "default_gateway": "2.2.2.168",
    "comment": "dhcp range for case 27",
}

# case 30
tc30_dynamic_dict = {
    "from": "2.2.2.41",
    "to": "2.2.2.50",
    "default_gateway": "2.2.2.168",
    "comment": "dhcp range for case 30",
}

# case 28
tc28_dynamic_dict = {
    "from": "3.3.3.6",
    "to": "3.3.3.7",
    "lease_time": 2,
    "default_gateway": "3.3.3.168",
    "comment": "dhcp lease for x3 interface",
}

# case 29
tc29_static_dict1 = {
    "ip": "2.2.2.200",
    "mac": '',
    "name": "static_range_1 for case 29",
    "default_gateway": "2.2.2.168",
    "comment": "static_range_1 for case 29",
}
tc29_static_dict2 = {
    "ip": "2.2.2.201",
    "mac": '',
    "name": "static_range_2 for case 29",
    "default_gateway": "2.2.2.168",
    "comment": "static_range_2 for case 29",
}

# case 34
tc34_dynamic_dict1 = {
    "from": "192.168.168.170",
    "to": "192.168.168.172",
    "default_gateway": "192.168.168.168",
    "comment": "dynamic_range_1 for case 34",
}
tc34_dynamic_dict2 = {
    "from": "192.168.168.175",
    "to": "192.168.168.179",
    "default_gateway": "192.168.168.168",
    "comment": "dynamic_range_2 for case 34",
}


# case 35
tc35_dynamic_dict1 = {
    "from": "2.2.2.170",
    "to": "2.2.2.192",
    "default_gateway": "2.2.2.168",
    "comment": "dynamic_range_1 for case 35",
}
tc35_dynamic_dict2 = {
    "from": "3.3.3.170",
    "to": "3.3.3.192",
    "default_gateway": "3.3.3.168",
    "comment": "dynamic_range_2 for case 35",
}

# case 36
tc36_static_dict1 = {
    "ip": "2.2.2.200",
    "mac": '',
    "name": "static_range_1 for case 36",
    "default_gateway": "2.2.2.168",
    "comment": "static_range_1 for case 36",
}
tc36_static_dict2 = {
    "ip": "2.2.2.202",
    "mac": '',
    "default_gateway": "2.2.2.168",
    "name": "static_range_2 for case 36",
    "comment": "static_range_2 for case 36",
}

# case 37
tc37_dynamic_dict1 = {
    "from": "2.2.2.6",
    "to": "2.2.2.10",
    "default_gateway": "2.2.2.168",
    "comment": "dynamic_range_1 for case 37",
}
tc37_dynamic_dict2 = {
    "from": "3.3.3.175",
    "to": "3.3.3.179",
    "default_gateway": "3.3.3.168",
    "comment": "dynamic_range_2 for case 37",
}
tc37_static_dict1 = {
    "ip": "2.2.2.200",
    "mac": '',
    "name": "static_range_1",
    "default_gateway": "2.2.2.168",
    "comment": "static_range_1 for case 37",
}
tc37_static_dict2 = {
    "ip": "2.2.2.201",
    "mac": '',
    "name": "static_range_2",
    "default_gateway": "2.2.2.168",
    "comment": "static_range_2 for case 37",
}

# case 91
tc91_x2_dict = {
    "from": "2.2.2.6",
    "to": "2.2.2.26",
    "default_gateway": "2.2.2.168",
    "comment": "dynamic range for x2",
}

# case 95
tc95_dns_dict = {
    "dns": {
        "server": {
            "inherit": False,
            "static": {
                "primary": "2.2.2.2",
                "secondary": "4.4.4.4",
                "tertiary": "8.8.8.8"
            },
            "ipv6": {
                "preferred": True,
                "inherit": True,
                "static": {
                    "primary": "::",
                    "secondary": "::",
                    "tertiary": "::"
                }
            }
        },
        "rebinding": {
            "enable": False,
            "action": "log-attack-only",
            "allowed_domains": {}
        },
        "fqdn_binding": False,
        "fqdn_over_tcp_dns": False,
        "split_servers": True
    }
}
tc95_dns_inhert_dict = {
    "dns": {
        "server": {
            "inherit": True,
            "static": {
                "primary": "",
                "secondary": "",
                "tertiary": ""
            },
            "ipv6": {
                "preferred": True,
                "inherit": True,
                "static": {
                    "primary": "::",
                    "secondary": "::",
                    "tertiary": "::"
                }
            }
        },
        "rebinding": {
            "enable": False,
            "action": "log-attack-only",
            "allowed_domains": {}
        },
        "fqdn_binding": False,
        "fqdn_over_tcp_dns": False,
        "split_servers": True
    }
}

# case 78
tc78_dynamic_dict1 = {
    "from": "192.168.168.170",
    "to": "192.168.168.172",
    "default_gateway": "192.168.168.168",
    "comment": "dynamic_range_1",
}
tc78_dynamic_dict2 = {
    "from": "192.168.168.175",
    "to": "192.168.168.179",
    "default_gateway": "192.168.168.168",
    "comment": "dynamic_range_2",
}
tc78_static_dict1 = {
    "ip": "192.168.168.200",
    "mac": '000d568d4eca',
    "name": "static_range_1",
    "default_gateway": "192.168.168.168",
    "comment": "static_range_1",
}
tc78_static_dict2 = {
    "ip": "192.168.168.201",
    "mac": '000d568d4ecc',
    "name": "static_range_2",
    "default_gateway": "192.168.168.168",
    "comment": "static_range_2",
}
tc78_dynamic_dict3 = {
    "from": "2.2.2.170",
    "to": "2.2.2.172",
    "default_gateway": "2.2.2.168",
    "netmask": "255.255.255.0",
    "comment": "dynamic_range_3",
}
tc78_dynamic_dict4 = {
    "from": "2.2.2.31",
    "to": "2.2.2.35",
    "default_gateway": "2.2.2.168",
    "netmask": "255.255.255.0",
    "comment": "dynamic_range_4",
}

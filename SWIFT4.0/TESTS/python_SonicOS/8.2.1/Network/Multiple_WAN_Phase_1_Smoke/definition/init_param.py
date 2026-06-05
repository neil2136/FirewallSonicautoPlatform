import os
import sys
import re
import subprocess

import unittest
import paramunittest
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from time import sleep


sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Multiple_WAN_Phase_1_Smoke')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/Multiple_WAN_Phase_1_Smoke/testcases')

from lib.modules.API import network
from lib.modules.API import system

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_IP = FIREWALL
    X0_GW = '192.168.168.1'
    X1_IP = '13.0.11.110'
    X1_GW = '13.0.11.120'
    X1_GW_MGMT = '172.168.0.110'
    X2_IP = '13.0.12.110'
    X2_GW = '13.0.12.120'
    X2_GW_MGMT = '172.168.0.120'
    X3_IP = '13.0.13.110'
    X3_GW = '13.0.13.120'
    X3_GW_MGMT = '172.168.0.130'
    X4_IP = '13.0.14.110'
    X4_GW = '13.0.14.120'
    X4_GW_MGMT = '172.168.0.140'
    X5_IP = '13.0.15.110'
    X5_GW = '13.0.15.120'
    X5_GW_MGMT = '172.168.0.150'
    X5_VIf1_IP = '13.3.0.1'
    X5_VIf1_gw = '13.3.0.2'
    X5_VIf1_GW_MGMT = '172.168.0.160'
    X5_VIf2_IP = '13.4.0.1'
    X5_VIf2_GW = '13.4.0.2'
    X5_VIf2_GW_MGMT = '172.168.0.170'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'

    PC1_ETH0 = '192.168.4.3'
    PC1_ETH1 = '192.168.5.2'
    PC1_ETH2 = '192.168.168.158'
    PC1_ETH3 = '172.168.0.100'
    
    SERVER_ETH0 = '192.168.2.3'
    SERVER_ETH1 = '100.100.10.200'
    SERVER_ETH2 = '192.168.3.2'
    SERVER_ETH3 = '172.168.0.200'
    
    GW1_ETH0 = '192.168.6.3'
    GW1_ETH1 = '100.100.11.11'
    GW1_ETH2 = '13.0.11.120'
    GW1_ETH3 = '172.168.0.110'

    GW2_ETH0 = '192.168.7.3'
    GW2_ETH1 = '100.100.12.12'
    GW2_ETH2 = '13.0.12.120'
    GW2_ETH3 = '172.168.0.120'

    GW3_ETH0 = '192.168.8.3'
    GW3_ETH1 = '100.100.13.13'
    GW3_ETH2 = '13.0.13.120'
    GW3_ETH3 = '172.168.0.130'

    GW4_ETH0 = '192.168.9.3'
    GW4_ETH1 = '100.100.14.14'
    GW4_ETH2 = '13.0.14.120'
    GW4_ETH3 = '172.168.0.140'

    GW5_ETH0 = '192.168.10.3'
    GW5_ETH1 = '100.100.15.15'
    GW5_ETH2 = '13.0.15.120'
    GW5_ETH3 = '172.168.0.150'
    
    TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/Multiple_WAN_Phase_1_Smoke/testplan/Multiple_WAN_Phase_1_Smoke.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1','eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1','eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1','eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1','eth3')

PC_Server_ETH0_IP = os_obj.get_node_interface_ip('PC-Server','eth0')
PC_Server_ETH1_IP = os_obj.get_node_interface_ip('PC-Server','eth1')
PC_Server_ETH2_IP = os_obj.get_node_interface_ip('PC-Server','eth2')
PC_Server_ETH3_IP = os_obj.get_node_interface_ip('PC-Server','eth3')

logger.info('\n' + '-' * 30 + '\n' \
    + 'PC1_ETH0_IP :' + PC1_ETH0_IP + '\n' \
    + 'PC1_ETH1_IP :' + PC1_ETH1_IP + '\n' \
    + 'PC1_ETH2_IP :' + PC1_ETH2_IP + '\n' \
    + 'PC1_ETH3_IP :' + PC1_ETH3_IP + '\n' \

    + 'PC_Server_ETH0_IP :' + PC_Server_ETH0_IP + '\n' \
    + 'PC_Server_ETH1_IP :' + PC_Server_ETH1_IP + '\n' \
    + 'PC_Server_ETH2_IP :' + PC_Server_ETH2_IP + '\n' \
    + 'PC_Server_ETH3_IP :' + PC_Server_ETH3_IP + '\n' \
    + '-' * 30
)
TESTPATH= os.environ['PYTHON_SONICOS_HOME']  + '/Network/Multiple_WAN_Phase_1_Smoke'


binPath = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Multiple_WAN_Phase_1_Smoke/bin'
toolPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissh/tools'




X1_IP_DHCP = '13.0.11.150'
X2_IP_DHCP = '13.0.12.150'
X3_IP_DHCP = '13.0.13.150'
X4_IP_DHCP = '13.0.14.150'
HTTP_Server = '100.100.10.200'
Server_MGMT = '172.168.0.200'
IP_Responser_SNWL = HTTP_Server
Host_Responser_SNWL = HTTP_Server
Port_Responser_SNWL = '80'


ip_pool_start_X2 = '13.0.12.200'
ip_pool_end_X2 = '13.0.12.210'
ip_pool_start_X3 = '13.0.13.200'
ip_pool_end_X3 = '13.0.13.210'
ip_pool_start_X4 = '13.0.14.200'
ip_pool_end_X4 = '13.0.14.210'

dhcpdcfg_1 = '''
ddns-update-style interim;
ignore client-updates;
subnet 13.0.11.0 netmask 255.255.255.0 { 
''' + \
f'''
option routers {Parameter.GW1_ETH2};
''' + \
'''
option subnet-mask 255.255.255.0;
option time-offset -18000;
range dynamic-bootp 13.0.11.150 13.0.11.200;
default-lease-time 21600;
max-lease-time 43200;
}
'''

dhcpdcfg_2 = '''
ddns-update-style interim;
ignore client-updates;
subnet 13.0.12.0 netmask 255.255.255.0 {
''' + \
f'''
option routers {Parameter.GW2_ETH2};
''' + \
'''
option subnet-mask 255.255.255.0;
option time-offset -18000;
range dynamic-bootp 13.0.12.150 13.0.12.200;
default-lease-time 21600;
max-lease-time 43200;
}
'''
dhcpdcfg_3 = '''
ddns-update-style interim;
ignore client-updates;
subnet 13.0.13.0 netmask 255.255.255.0 {
''' + \
f'''
option routers {Parameter.GW3_ETH2};
''' + \
'''
option subnet-mask 255.255.255.0;
option time-offset -18000;
range dynamic-bootp 13.0.13.150 13.0.13.200;
default-lease-time 21600;
max-lease-time 43200;
}
'''

dhcpdcfg_4 = '''
ddns-update-style interim;
ignore client-updates;
subnet 13.0.14.0 netmask 255.255.255.0 {
''' + \
f'''
option routers {Parameter.GW4_ETH2};
'''+ \
'''
option subnet-mask 255.255.255.0;
option time-offset -18000;
range dynamic-bootp 13.0.14.150 13.0.14.200;
default-lease-time 21600;
max-lease-time 43200;
}
'''

dhcpdcfg_5 = '''
ddns-update-style interim;
ignore client-updates;
subnet 13.0.15.0 netmask 255.255.255.0 {
''' + \
f'''
option routers {Parameter.GW5_ETH2};
''' + \
'''
option subnet-mask 255.255.255.0;
option time-offset -18000;
range dynamic-bootp 13.0.15.150 13.0.15.200;
default-lease-time 21600;
max-lease-time 43200;
}
'''


tc27_json = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X2",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {}
                        ]
                    }
                ]
            }
        }

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')



interfaceObj = network.InterfaceIPv4Api(fw)
failoverlbObj = network.FailoverLbApi(fw)
routeObj = network.RoutePolicyApi(fw)
natObj = network.NatpolicyApi(fw)
addrObj = network.AddressobjectsApi(fw)
packetObj = system.PacketmonitorApi(fw)

#pc
local_host = Host('localhost')
server_ssh = Host(Server_MGMT, user='root', password='password')
gw1_ssh = Host(Parameter.GW1_ETH3, user='root', password='password')
gw2_ssh = Host(Parameter.GW2_ETH3, user='root', password='password')
gw3_ssh = Host(Parameter.GW3_ETH3, user='root', password='password')
gw4_ssh = Host(Parameter.GW4_ETH3, user='root', password='password')
gw5_ssh = Host(Parameter.GW5_ETH3, user='root', password='password')

import os
import re
from runner.settings import Params
from util.openstack import Openstack


class Parameter():
    DNS1 = '10.9.1.40'
    LAN_INTERFACE="eth0"
    WAN_INTERFACE="eth1"
    DMZ_INTERFACE="eth2"
    MY_LAN_PC_IP="192.168.168.169"
    MY_DMZ_PC_IP="2.2.2.169"
    MY_WAN_PC_IP="11.11.11.169"
    X0_IP="192.168.168.168"
    X1_IP="11.11.11.168"
    X1_IPv6 = "2001::168"
    MY_WAN_PC_IPv6="2001::169"
    X1_GW="11.11.11.1"
    X2_IP="2.2.2.168"
    ZONES=['Public','Trusted']
    DESTINATION = Params.G_DNS1
    DNS_SERVER = MY_WAN_PC_IP
    REGISTER_DNS = Params.G_DNS1
    REACH_WEB = "www.baidu.com"
    UNREACH_WEB = "www.unreach.com"
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + "/Network/DNS_Proxy/testplan/dnsproxy.json"
    DNS_MAP={
        REACH_WEB: '2.2.2.2',
    }
    TC58_CACHE_V4 = '58.58.58.58'
    TC58_CACHE_V6 = '58::58'
    MY_WAN_PC_IPv6= '2001::169'
    DNS_SERVER_V6 = MY_WAN_PC_IPv6


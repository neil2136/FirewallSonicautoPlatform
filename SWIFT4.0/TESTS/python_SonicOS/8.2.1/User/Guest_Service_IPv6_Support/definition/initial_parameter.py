import os
import sys
import re
import copy
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network,firewall,system,users
from lib.modules.CLI.system import LicenseCli


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Service_IPv6_Support/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Service_IPv6_Support')
print(sys.path)
import dibbler,ui_guest

os_obj = Openstack(Params.testbed)
httpserver_pc = Params.testbed + '-PC2'
pc1_defaultgw = os_obj.get_pc_default_gw_ip('PC1')




tc_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Service_IPv6_Support/testcases'
lib_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Service_IPv6_Support/lib'


ip = '192.168.168.168'
dhcpv6_server = '11.11.11.101'
dhcpv6_server_v6 = "3000::11"
X1_Prefix = "3000::"
X2_Prefix = "2012::"

class Parameter():
    FIREWALL = '192.168.168.168'
    LAN_PC_IPv6 = '2001:db0::1096'
    LAN_PC_IPv6_GW = '2001:db0::1'
    X0_IPv6 = "2001:db0::193"

    #connected to external windows auth server
    X1_IP = '12.0.0.10'
    X1_GW = '12.0.0.1'
    X1_IPv6 = '2002:db0::193'

    #linux http server
    LINUX_SERVER_IPv6 = '2001:db1::1093'
    LINUX_SERVER_IPv6_GW = '2001:db1::1'
    X2_IPv6 = '2001:db1::193'
    X2_IP = '13.0.0.10'

    #static client
    static_PC_IPv6 = "2001:1100::200"
    static_PC_IPv6_GW = "2001:1100::1"
    X3_IPv6 = "2001:1100::193"
    X3_IP = '20.2.2.20'

    #dynamic client
    Dynamic_PC_IPv6_GW = "2003:db93::1"
    X4_IPv6 = "2003:db93::193"
    X4_IP = '30.2.2.20'

    #lhm server of windows
    lhm_server_v6 = "2002:db0::199"
    lhm_server_v4 = '12.0.0.100'

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Service_IPv6_Support/testplan/Guest_Service_IPv6_Support.json'
    DIBBLER_SERVER_CONF = os.environ['PYTHON_SONICOS_HOME'] + '/User/Guest_Service_IPv6_Support/confs/server.conf'
    DIBBLER_CLIENT_CONF = os.environ['PYTHON_SONICOS_HOME'] + '/User/Guest_Service_IPv6_Support/confs/client.conf'


ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

licenseObj = LicenseCli(fw_cli)
interface_ipv4 = network.InterfaceIPv4Api(fw)
interface_ipv6 = network.InterfaceIPv6Api(fw)
guest_obj = users.UserGuestApi(fw)

zone_obj = network.ZoneObjectsApi(fw)
access_rules_obj = firewall.AccessRuleApi(fw)
ao_obj = network.AddressobjectsApi(fw)
service_obj = network.ServiceObjectApi(fw)
natpolicy_obj = network.NatpolicyApi(fw)
packet_obj = system.PacketmonitorApi(fw)
natpolicy_obj = network.NatpolicyApi(fw)
dhcp_server_obj = network.DHCPServerApi(fw)
localhost = Host('localhost')
linux_http_server = Params.testbed + '-PC2'
http_server = Host(linux_http_server)
dibbler_pc = Params.testbed + '-PC4'
dibbler_client = Host(dibbler_pc)
static_pc = Params.testbed + '-PC3'
static_client = Host(static_pc)


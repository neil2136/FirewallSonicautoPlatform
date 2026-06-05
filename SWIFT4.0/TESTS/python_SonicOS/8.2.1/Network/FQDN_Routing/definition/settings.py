import os
import sys
import re
import time
import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from networkdevice import Host

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/FQDN_Routing')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/FQDN_Routing/testcases')
CONFPATH = os.environ["PYTHON_SONICOS_HOME"] + '/Network/FQDN_Routing/definition'

from utm import Firewall
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, DynamicRoutingApi, \
                                    DnsProxyApi, DnsSettingsApi
from lib.modules.API.system import AdminApi, SettingApi, DiagnosticApi
from lib.modules.API.policy import RoutePolicyApi
from lib.modules.API.object import AddressObjectGroupApi
from lib.modules.CLI.network import RouteCli
from lib.modules.CLI.diag import DiagCli
from lib.modules.CLI.system import LicenseCli

# parameters on the openstack
class Parameter():
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/FQDN_Routing/testplan/FQDN_Routing.json'
    FIREWALL = '192.168.168.168'
    MASK = '255.255.255.0'
    FWUSER = 'admin'
    FWPASS = 'password'

    PC1_E0_X0 = '192.168.168.169'
    ROUTER_E0_X1 = '172.16.1.169'
    ROUTER_E1_X2 = '172.16.2.169'
    ROUTER_E2_X3 = '172.16.3.169'
    ROUTER_MGMT = '172.17.1.201'

    PORT_NET = '172.16.0.0'
    UNREACH_NET = '172.18.0.0'

    X1_IP    = '172.16.1.168'
    X1_GW    = ROUTER_E0_X1
    X1_DNS1  = ROUTER_E0_X1
    X1_DNS2  = Params.G_DNS1
    X1_IF    = 'eth0'

    X2_IP    = '172.16.2.168'
    X2_GW    = ROUTER_E1_X2
    X2_IF    = 'eth1'

    X3_IP    = '172.16.3.168'
    X3_GW    = ROUTER_E2_X3
    X3_IF    = 'eth2'

#Instantiate objects including API,CLI
ip = Parameter.FIREWALL
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')

if_api = InterfaceIPv4Api(fw_api)
ao_api = AddressobjectsApi(fw_api)
ao_group_api = AddressObjectGroupApi(fw_api)
route_api = RoutePolicyApi(fw_api)
route_cli = RouteCli(fw_cli)
dynamic_route_api = DynamicRoutingApi(fw_api)
diag_cli = DiagCli(fw_cli)
dns_setting_api = DnsSettingsApi(fw_api)
dns_proxy_api = DnsProxyApi(fw_api)
setting_api = SettingApi(fw_api)
diagnostic_api = DiagnosticApi(fw_api)
license_cli = license = LicenseCli(fw_cli)

# parameters used in test
dn_file = '/var/named/chroot/var/named/sonicwall-fqdn-test.com.zone'
named_conf = '/var/named/chroot/etc/named.conf'
fqdn_policy = 'fqdn_policy'
fqdn_group_name = 'fqdn_group'

router = Host(Parameter.ROUTER_MGMT, user='root', password='password')
local_host = Host('localhost')

def verify(**opt):
    fqdn_dn = opt['fqdn']
    fqdn_ip = opt['fqdn_ip']
    src_ip = opt['src_ip']
    dst_if = opt['dst_if']

    cmd1 = 'ping ' + str(fqdn_dn) + ' -c 4 -w 1'
    cmd2 = "nohup tshark -f 'icmp[icmptype]=icmp-echo " + \
           " and dst host " + str(fqdn_ip) + " and src host " + str(src_ip) + \
           "' -i " + str(dst_if) + " -c 1 > /tmp/capture.txt 2>&1 &"
    cmd3 = 'rm -rf /tmp/capture.txt'
    cmd4 = 'cat /tmp/capture.txt'

    logger.info(cmd1)
    logger.info(cmd2)
    logger.info(cmd3)
    logger.info(cmd4)

    router.send_command(cmd3)
    router.send_command(cmd2)
    time.sleep(2)
    os.system(cmd1)
    time.sleep(3)
    router.send_command('pkill tshark')
    out = router.send_command(cmd4)
    print(out)

    if '1 packet captured' in out:
        return True
    else:
        return False

def show_nsm_db(fw_obj=fw_cli):
    cmds = ['configure', 'routing', 'nsm', 'show ip route database', 'exit', 'end', 'end']
    output = ''
    if not fw_obj.cli_login():
        print("Login FW failed.")
        return ""
    for cmd in cmds:
        if 'show' not in cmd:
            fw_obj.do_cli_command(cmd)
        else:
            fw_obj.prompt='NSM>'
            output = fw_obj.do_cli_command(cmd, customPrompt='#')
            fw_obj.prompt='>'
    fw_obj.cli_logout()
    return output

x1_static = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': True,
}
x2_static = {
    'if': 'X2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X2_GW,
}
x3_static = {
    'if': 'X3',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X3_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X3_GW,
}
domain_list = {
    'dns.sonicwall-fqdn-test.com': '172.18.1.201',
    'www.sonicwall-fqdn-test.com': '172.18.2.201',
    'ftp.sonicwall-fqdn-test.com': '172.18.3.201',
    'smb.sonicwall-fqdn-test.com': '172.18.4.201',
    'test.sonicwall-fqdn-test.com': '172.18.6.201'
}

# # # TC8 to TC12 definitions
ipv4_fqdn_www = {
    'name': 'ipv4_fqdn_www',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': 'www.sonicwall-fqdn-test.com',
}
ipv4_fqdn_ftp = {
    'name': 'ipv4_fqdn_ftp',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': 'ftp.sonicwall-fqdn-test.com',
}
ipv4_fqdn_smb = {
    'name': 'ipv4_fqdn_smb',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': 'smb.sonicwall-fqdn-test.com',
}
ipv4_fqdn_static = {
    'name': 'ipv4_fqdn_static',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': 'static.sonicwall-fqdn-test.com',
}
ipv4_fqdn_maxip = {
    'name': 'ipv4_fqdn_maxip',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': 'maxip.sonicwall-fqdn-test.com',
}
ipv4_fqdn_test = {
    'name': 'ipv4_fqdn_test',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': 'test.sonicwall-fqdn-test.com',
}
ipv4_fqdn_wildcard = {
    'name': 'ipv4_fqdn_wildcard',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': '*.sonicwall-fqdn-test.com',
}
ipv4_host = {
    'name': 'ipv4_host',
    'zone': 'WAN',
    'object_type': 'host',
    'value' : '172.18.7.201',
}
ipv4_network = {
    'name': 'ipv4_network',
    'zone': 'WAN',
    'object_type': 'network',
    'value' : '172.18.8.0,255.255.255.0',
}

tc8_13_result = {
    '08': [],
    '10': [],
    '11': [],
    '12': [],
    '13': []
}
tc18_19_26_result = {
    '18': [],
    '19': [],
    '26': []
}
tc28_29_result = {
    '28': [],
    '29': []
}

# # # ----------------- Var used in test
test_01_fqdn_group_name = 'ipv4_fqdn_group'
test_01_mixed_group_name = 'ipv4_mixed_group'
test_01_ao_policy = 'ao_policy'
test_01_group_policy = 'group_policy'
test_01_mixed_policy = 'mixed_policy'

test_13_new_name = 'ipv4_fqdn_new'
test_13_new_zone = 'DMZ'
test_13_new_host = 'ftp.sonicwall-fqdn-test.com'

ao_start_time = 0
ao_cur_time = 0

test_17_ipaddr1 = domain_list[ipv4_fqdn_www['value']]
test_17_ipaddr2 = '172.18.2.222'

test_22_newip = '172.18.10.201'

test_23_policy1 = 'policy1'
test_23_policy2 = 'policy2'
test_23_pref_file = '/tmp/pref.exp'

test_24_policy1 = 'policy1'
test_24_policy2 = 'policy2'

test_25_tsr_file = '/tmp/tsr.wri'

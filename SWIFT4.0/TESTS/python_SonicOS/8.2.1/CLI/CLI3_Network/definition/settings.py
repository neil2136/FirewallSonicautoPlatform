import os
import sys

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])

from lib.modules.CLI import network
# from definition import network
from lib.modules.API.network import InterfaceIPv4Api

from util.enhancedinfo import show_testcase_info
from utm import Firewall
from util.openstack import Openstack

import unittest
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                'CLI/CLI3_Nework/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    'CLI/CLI3_Network')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
    '/CLI/CLI3_Network/testplan/network_cli.json'
  
           
# configure fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.168'
    MASK = '255.255.255.0'
    X1_GW = '172.16.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


# Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fwcli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

interfaceapi = InterfaceIPv4Api(fw)
interfacecli = network.InterfaceCli(fwcli)
zonecli = network.ZonesCli(fwcli)
failoverlbcli = network.FailoverLBCli(fwcli)
dhcpservercli = network.DhcpServerCli(fwcli)
aocli = network.AddressObjectCli(fwcli)
ddnscli = network.DDNSCli(fwcli)
routecli = network.RouteCli(fwcli)
iphelpercli = network.IpHelperCli(fwcli)
networkmonitorcli = network.NetworkMonitorCli(fwcli)
natcli = network.NatpolicyCli(fwcli)
arp_cli = network.ARPCli(fwcli)

# case 1 parameter
X2_STATIC_dict = {
    'if': 'x2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': '20.20.20.1',
    'management https': True,
    'management ping': True,
    'management snmp': True,
    'management ssh': True,
    'comment': 'TestOnInterfaceX2',
    'user_login_https': True,
    'link-speed': 'auto',
    'flow-reporting': True,
    'mtu': '1460',
    'fqdn-assignment': '"aaa.com"'
}
tunnel_interface_dict = {
    'name': 'test_gre',
    'type': 'gre4to6',
    'bound-if': 'X1',
    'ip': '10.10.10.10',
    'netmask': '255.255.255.0',
    'local-ipv6': 'dynamic',
    'remote': '88::88',
    'flow-reporting': True,
    'fragment-packets': True,
    'ignore-df-bit': True,
    'send-icmp-fragmentation': True
}

#case 2 parameter
zone_dict = {
    'name': 'test1',
    'security-type': 'trusted',
    'allow-from-lower': True,
    'guest-services': True,
    'bypass-guest-auth': 'all',
    'bypass-guest-auth-type': '',
    'smtp-redirect': 'X0 IP',
    'smtp-redirect-type': 'name',
    'deny-networks': 'LAN Interface IP',
    'deny-networks-type': 'group',
    'pass-networks': 'All WAN IP',
    'pass-networks-type': 'group'
}
zone_new_dict = {
    'name': 'test1',
    'security-type': 'trusted',
    'name-new': 'edit-test1',
    'allow-from-lower': False,
    'guest-services': True,
}
del_zone_list = ['edit-test1']

#case 3 parameter
wlb_basic_dict = {
    'type': 'basic',
    'preempt': True,
    'global-responder': True,
    'missed-intervals': '6',
    'successful-intervals': '7'
}
#case 4 parameters
dhcpserver_scope_static_dict = {
    'name': 'test1',
    'type': 'static',
    'ip': '192.168.168.170',
    'mac': '11:22:33:44:55:66',
    'gateway': '192.168.168.168',
    'netmask': '255.255.255.0',
    'lease-time': '100',
    'dns1': '1.1.1.1',
    'dns2': '2.2.2.2',
    'wins1': '1.1.1.1',
    'voip1': '1.1.1.1',
}
dhcpserver_scope_dynamic_dict = {
    'name': 'test2',
    'type': 'dynamic',
    'start': '192.168.168.171',
    'end': '192.168.168.200',
    'netmask': '255.255.255.0',
    'gateway': '192.168.168.168'
}
old_scope_dict = {
    'name': 'test2',
    'type': 'dynamic',
    'start': '192.168.168.171',
    'end': '192.168.168.200',
    'netmask': '255.255.255.0',
    'gateway': '192.168.168.168'
}
new_scope_dict = {
    'start-new': '192.168.168.172',
    'end-new': '192.168.168.210',
}

del_scope_dict = {
    'version': 'ipv4',
    'type': 'dynamic',
    'start': '192.168.168.172',
    'end': '192.168.168.210'
}

# case5 parameter
host_ao_dict = {
    'version': 'ipv4',
    'type': 'host',
    'name': 'test-host',
    'host': '1.1.1.1',
    'zone': 'WAN'
}
range_ao_dict = {
    'name': 'test-range',
    'version': 'ipv4',
    'type': 'range',
    'range': '2.2.2.1 2.2.2.10',
    'zone': 'WAN'
}
network_ao_dict = {
    'name': 'test-network',
    'version': 'ipv4',
    'type': 'network',
    'network': '3.3.3.0 255.255.255.0',
    'zone': 'WAN'
}
mac_ao_dict = {
    'name': 'test-mac',
    'type': 'mac',
    'zone': 'WAN',
    'address': '11:22:33:44:55:66',
    'multi-homed': True
}
fqdn_ao_dict = {
    'name': 'test-fqdn',
    'type': 'fqdn',
    'zone': 'WAN',
    'domain': 'www.aaa.com',
    'dns-ttl': '150'
}

#case 6 parameter
ddns_profile_dict = {
    'name': 'test-ddns',
    'domain': 'sonic.com',
    'user-name': 'auto1',
    'password': 'auto1'
}
ddns_profile_new_dict = {
    'name': 'test-ddns',
    'domain-new': 'bbb.com'
}

#case 7 parameter
add_route_dict = {
    'if': 'X1',
    'metric': 12,
    'source': 'name "X0 Subnet"',
    'dest': 'any',
    'name': 'add_route',
    'version': 'ipv4',
    'gateway': 'name "X1 Default Gateway"',
}
new_route_dict = {
    'metric-new': 6,
    'source-new': 'any',
    'name-new': 'edit-route'
}
del_route_dict = {
    'if': 'X1',
    'metric': 6,
    'source': 'any',
    'dest': 'any',
    'name': 'edit-route',
    'version': 'ipv4',
    'gateway': 'name "X1 Default Gateway"',
}

# case 8 parameter
relay_protocol_dict = {
    'name': 'iph-v4',
    'port1': '30',
    'port2': '40'
}
policy_dhcp_dict = {
    'name': 'policy_dhcp',
    'protocol': 'DHCP',
    'from': 'LAN',
    'to': 'name "X1 IP"',
    'comment': 'testIphelperPolicy_dhcp'
}

# case 9 parameter
nat_v4_dict = {
    'version': 'ipv4',
    'orig_source_type': 'name',
    'orig_source': 'X0 Subnet',
    'trans_source_type': 'name',
    'trans_source': 'X1 IP',
    'orig_dest_type': 'name',
    'orig_dest': 'X2 Subnet',
    'trans_dest_type': 'name',
    'trans_dest': 'X2 IP',
    'name': 'ipv4_nat',
    'comment': 'add ipv4 nat policy'
}
natv4_new_dict = {
    'trans_source_type': 'name',
    'trans_source_new': '"X2 IP"',
    'name': 'edit_ipv4_nat',
    'comment': 'edit ipv4 nat policy'
}
nat_del_list = ['ipv4:name:edit_ipv4_nat']
nat_v6_dict = {
    'version': 'ipv6',
    'orig_source_type': 'name',
    'orig_source': 'X0 IPv6 Primary Static Address Subnet',
    'trans_source_type': 'name',
    'trans_source': 'X1 IPv6 Primary Static Address',
    'name': 'ipv6 nat policy',
    'comment': 'add ipv6 nat policy'
}
nat_64_dict = {
    'version': 'nat64',
    'orig_source_type': 'any',
    'trans_source_type': 'name',
    'trans_source': 'X1 IP',
    'pref64_type': 'name',
    'pref64': 'Well-Known\ Pref64',
    'name': 'nat64 policy',
    'comment': 'add nat64 policy'
}

# case 10 parameter
nm_icmp_dict = {
    'name': 'nm_ipv4',
    'probe-target': 'name "X1 IP"',
    'outbound-interface': 'X1',
    'next-hop': 'name "X0 IP"',
    'probe-type': 'ping explicit',
    'comment': 'add nm_icmp policy'
}

# case 11 parameter
x0_ipv6_static_dict = {
    'if': 'X0',
    'mode': 'static',
    'zone': 'LAN',
    'ip': '100::1',
    'prefix-length': 64,
    'mgmt-https': True,
    'mgmt-snmp': True,
    'mgmt-ping': True,
    'mgmt-ssh': True,
    'user-https': True,
    'https-redirect': True
}

# case 12 parameter
vlan_interface_dict = {
    'if': 'x0',
    'type': 'vlan',
    'vlan-tag': 200,
    'zone': 'lan',
    'mode': 'static',
    'ip': '200.1.1.1'
}

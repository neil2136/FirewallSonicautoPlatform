from definition.settings import *
from definition.utils import *

@paramunittest.parametrized(
    {'check_list1': ["'Comments for this interface object' , X2, changed from .*? changed to \[modify x2 interfance\]"],'check_list2':["X2.*?'Comments for this interface object'.*?modify x2 interfance"], 'uuid': '1526147'},
    {'check_list1': ["'Allow SSH Management on this interface' , X2, changed from \[enabled\], changed to \[disabled\]"],'check_list2':["X2.*?'Allow SSH Management on this interface'.*?enabled.*?disabled"], 'uuid': '1526148'},
    {'check_list1': ["'Port Grouping' , X2, changed from .*? changed to \[Port Redundancy\]"],'check_list2':["X2.*?'Port Grouping'.*?None.*?Port Redundancy"], 'uuid': '1526149'},
    {'check_list1': ["'LAN/DMZ/WLAN IP Address' , X2.*? changed to \[1\.1\.1\.1\]"],'check_list2':["X2.*?'LAN/DMZ/WLAN IP Address'.*?1\.1\.1\.1"], 'uuid': '1526150'},
    {'check_list1': ["'IPv6 Interface SSH management' , X2.*? changed from \[enabled\], changed to \[disabled\]"],'check_list2':["X2.*?'IPv6 Interface SSH management'.*?enabled.*?disabled"], 'uuid': '1526151'},
    {'check_list1': ["'IPv6 Interface Static IP' , X2.*? changed from \[2004::1\], changed to \[3001::1\]"],'check_list2':["X2.*?'IPv6 Interface Static IP'.*?2004::1.*?3001::1"], 'uuid': '1526152'},
    {'check_list1': ["'IPv6 Interface number' , x2_ti"],'check_list2':["x2_ti.*?'IPv6 Interface number'"], 'uuid': '1526153'},
    {'check_list1': ["Interface Portshield To' , X5, changed from .*? changed to \[X2\]"],'check_list2':["X5.*?'Interface Portshield To'.*?X2"], 'uuid': '1526154'},
    {'check_list1': ["'Ethernet Link Ability: Auto Negotiate/Force 10/100 Mbps' , X5, changed from .*? changed to \[100Mbps - Half Duplex\]"],'check_list2':["X5.*?'Ethernet Link Ability: Auto Negotiate/Force 10/100 Mbps'.*? 100Mbps - Half Duplex"], 'uuid': '1526155'},
    {'check_list1': ["Added 'LB-Type Member Display Name' , X3, changed to \[X3\]"],'check_list2':["X3.*?Added 'LB-Type Member Display Name'.*?X3"], 'uuid': '1526156'},
    {'check_list1': ["'LB Type' ,  Default LB Group, changed from .*? changed to \[Round Robin\]"],'check_list2':["Default LB Group.*?'LB Type'.*?Round Robin"], 'uuid': '1526157'},
    {'check_list1': ["Added 'LB-Type Member Display Name' , X3, changed to \[X3\]"],'check_list2':["X3.*?Added 'LB-Type Member Display Name'.*?X3"], 'uuid': '1526158'},
    {'check_list1': ["'LB Type' ,  Default LB Group IPv6, changed from .*? changed to \[Round Robin\]"],'check_list2':["Default LB Group IPv6.*?'LB Type'.*?Round Robin"], 'uuid': '1526159'},
    {'check_list1': ["'Zone Name' , test, changed to \[test\]"],'check_list2':["test.*?'Zone Name'"], 'uuid': '1526160'},
    {'check_list1': ["'Security Type' , test, changed from \[Public\], changed to \[Trusted\]"],'check_list2':["test.*?'Security Type'.*?Public.*?Trusted"], 'uuid': '1526162'},
    {'check_list1': ["Deleted 'Zone Name' , test, changed from \[test\]"],'check_list2':["test.*?Deleted 'Zone Name'"], 'uuid': '1526161'},
    {'check_list1': ["Added 'Wiremode Vlan configuration Source Interface' , X2/1/X4/3"],'check_list2':["X2/1/X4/3.*?Added 'Wiremode Vlan configuration Source Interface'"], 'uuid': '1526163'},
    {'check_list1': ["Deleted 'Wiremode Vlan configuration Source Interface' , X2/1/X4/3"],'check_list2':["X2/1/X4/3.*?Deleted 'Wiremode Vlan configuration Source Interface'"], 'uuid': '1526164'},
    {'check_list1': ["'Enable DNS query over TCP'.*?disabled.*?enabled"],'check_list2':["'Enable DNS query over TCP'.*?disabled.*?enabled"], 'uuid': '1526165'},
    {'check_list1': ["'Split DNS Domain Name' , test, changed to \[test\]"],'check_list2':["test.*?'Split DNS Domain Name'"], 'uuid': '1526166'},
    {'check_list1': ["Deleted 'Split DNS Domain Name' , test, changed from \[test\]"],'check_list2':["test.*?Deleted 'Split DNS Domain Name'"], 'uuid': '1526167'},
    {'check_list1': ["'Split DNS Domain Name' , mail.126.com, changed to \[mail.126.com\]"],'check_list2':["mail.126.com.*?'Split DNS Domain Name'"], 'uuid': '1526168'},
    {'check_list1': ["Deleted 'Split DNS Domain Name' , mail.126.com, changed from \[mail.126.com\]"],'check_list2':["mail.126.com.*?Deleted 'Split DNS Domain Name'"], 'uuid': '1526169'}, 
    {'check_list1': ["'Enforce DNS Proxy' , changed from \[disabled\], changed to \[enabled\]"],'check_list2':["'Enforce DNS Proxy'.*?disabled.*?enabled"], 'uuid': '1526170'},
    {'check_list1': ["'Enable DNS Cache' , changed from \[enabled\], changed to \[disabled\]"],'check_list2':["'Enable DNS Cache'.*?enabled.*?disabled"], 'uuid': '1526171'},
    {'check_list1': ["'Static DNS Cache Domain Name' , www.baidu.com"],'check_list2':["www.baidu.com.*?'Static DNS Cache Domain Name'"], 'uuid': '1526172'},
    {'check_list1': ["Deleted 'Static DNS Cache Domain Name' , www.baidu.com"],'check_list2':["www.baidu.com.*?Deleted 'Static DNS Cache Domain Name'"], 'uuid': '1526173'},
    {'check_list1': ["'Custom Malicious Domain Name' , custom.test.com"],'check_list2':["custom.test.com.*?'Custom Malicious Domain Name'"], 'uuid': '1526174'},
    {'check_list1': ["'White Entry Name' , white.test.com"],'check_list2':["white.test.com.*?'White Entry Name'"], 'uuid': '1526175'},
    {'check_list1': ["'DNS Tunnel White Entry' , 1.1.1.1"],'check_list2':["1.1.1.1.*?'DNS Tunnel White Entry'"], 'uuid': '1526176'},
    {'check_list1': ["'Policy Name' , Src 'Any', Dst 'Any', Srv 'Any', App 'Any', , changed to \[test1_route"],'check_list2':["Src 'Any', Dst 'Any', Srv 'Any', App 'Any'.*?Added 'The Property of the route policy'"], 'uuid': '1526177'},
    {'check_list1': ["Deleted 'The ID of the route policy' , Src 'Any', Dst 'Any', Srv 'Any', App 'Any'"],'check_list2':["Deleted 'The ID of the route policy'"], 'uuid': '1526180'},
    {'check_list1': ["Policy Name' , Src 'Any', Dst 'remote_net', Srv 'Any', App 'Any', , changed to \[test2_route"],'check_list2':["Src 'Any', Dst 'remote_net', Srv 'Any', App 'Any'.*?test2_route"], 'uuid': '1526178'},
    {'check_list1': ["'Policy Name' , Src 'Any', Dst 'Any', Srv 'Any', App 'Any', , changed to \[test3_route\]"],'check_list2':["Src 'Any', Dst 'Any', Srv 'Any', App 'Any'.*?test3_route "], 'uuid': '1526179'},
    {'check_list1': ["'Policy Name' , Src 'Any', Dst 'Any', Srv 'Any', App 'Any', , changed to \[test_ipv6"],'check_list2':["Src 'Any', Dst 'Any', Srv 'Any', App 'Any'.*?Added 'IPv6 Network Object Time Created'"], 'uuid': '1526181'},
    {'check_list1': ["Deleted 'IPv6 PBR Object ID' , Src 'Any', Dst 'Any', Srv 'Any', App 'Any'"],'check_list2':["Src 'Any', Dst 'Any', Srv 'Any', App 'Any'.*?Deleted 'IPv6 PBR Object ID'"], 'uuid': '1526182'},
    {'check_list1': ["'OSPF: OSPF Mode' , OSPFv2, changed from \[Disabled\], changed to \[Enabled\]"],'check_list2':["OSPFv2.*?'OSPF: OSPF Mode'.*?Disabled.*?Enabled"], 'uuid': '1526183'},
    {'check_list1': ["'RIP: RIP Mode' , RIP, changed from \[Disabled\], changed to \[Send and Receive\]"],'check_list2':["RIP.*?'RIP: RIP Mode'.*?Disabled.*?Send and Receive"], 'uuid': '1526184'},
    {'check_list1': ["'Ospf3 Interface mode' , OSPFv3, changed from \[Disabled\], changed to \[Enabled\]"],'check_list2':["OSPFv3.*?'Ospf3 Interface mode'.*?Disabled.*?Enabled"], 'uuid': '1526185'},
    {'check_list1': ["'Ripng mode' , changed from \[Disabled\], changed to \[Enabled\]"],'check_list2':["'Ripng mode'.*?Disabled.*?Enabled"], 'uuid': '1526186'},
    {'check_list1': ["'NAT Policy Name' , test_nat"],'check_list2':["test_nat.*?'NAT Policy Name'"], 'uuid': '1526187'},
    {'check_list1': ["Deleted 'Original Source' , test_nat"],'check_list2':["test_nat.*?Deleted 'Original Source'"], 'uuid': '1526188'},
    {'check_list1': ["'IPv6NAT Policy Name' , test_nat_ipv6"],'check_list2':["test_nat_ipv6.*?'IPv6NAT Policy Name'"], 'uuid': '1526189'},
    {'check_list1': ["Deleted 'IPv6 Original Source' , test_nat_ipv6"],'check_list2':["test_nat_ipv6.*?Deleted 'IPv6 Original Source'"], 'uuid': '1526190'},
    {'check_list1': ["'Static ARP IP Address' , 13.0.0.5"],'check_list2':["13.0.0.5.*?'Static ARP IP Address'"], 'uuid': '1526191'},
    {'check_list1': ["Deleted 'Static ARP IP Address' , 13.0.0.5,"],'check_list2':["13.0.0.5.*?Deleted 'Static ARP IP Address'"], 'uuid': '1526192'},
    {'check_list1': ["'ARP Cache entry timeout \(minutes\)' , changed from \[10\], changed to \[22\]"],'check_list2':["'ARP Cache entry timeout \(minutes\)'.*?10.*?22"], 'uuid': '1526193'},
    {'check_list1': ["'NDP static IP' , 48::48"],'check_list2':["48::48.*?'NDP static IP'"], 'uuid': '1526194'},
    {'check_list1': ["Deleted 'NDP static IP' , 2CB8ED6D7FF6"],'check_list2':["2CB8ED6D7FF6.*?Deleted 'NDP static IP' "], 'uuid': '1526195'},
    {'check_list1': ["'Enable MAC-IP anti-spoofing' , X2, changed from \[disabled\], changed to \[enabled\]"],'check_list2':["X2.*?'Enable MAC-IP anti-spoofing'.*?disabled.*?enabled"], 'uuid': '1526196'},
    {'check_list1': ["'Mac-IP Spoof Static Interface Index' , X2/23.0.0.10/2c:b8:ed:6d:7f:f6"],'check_list2':["X2/23.0.0.10/2c:b8:ed:6d:7f:f6.*?'Mac-IP Spoof Static Interface Index'"], 'uuid': '1526197'},
    {'check_list1': ["Deleted 'Mac-IP Spoof Static Interface Index' , X2/23.0.0.10/2c:b8:ed:6d:7f:f6"],'check_list2':["X2/23.0.0.10/2c:b8:ed:6d:7f:f6.*?Deleted 'Mac-IP Spoof Static Interface Index'"], 'uuid': '1526198'},
    {'check_list1': ["'Enable IPv6 Mac-IP anti-spoofing' , X2, changed from \[disabled\], changed to \[enabled\]"],'check_list2':["X2.*?'Enable IPv6 Mac-IP anti-spoofing'.*?disabled.*?enabled"], 'uuid': '1526199'},
    {'check_list1': ["'IPv6 Mac-IP Spoof Static Interface Index' , 2c:b8:ed:6d:7f:f6.*?X2"],'check_list2':["2c:b8:ed:6d:7f:f6.*?'IPv6 Mac-IP Spoof Static Interface Index'.*?X2"], 'uuid': '1526200'},
    {'check_list1': ["Deleted 'IPv6 Mac-IP Spoof Static Interface Index' , 2c:b8:ed:6d:7f:f6.*?X2"],'check_list2':["2c:b8:ed:6d:7f:f6.*?Deleted 'IPv6 Mac-IP Spoof Static Interface Index'.*?X2"], 'uuid': '1526201'},
    {'check_list1': ["'Enable DHCP Persistence' , changed from \[disabled\], changed to \enabled\]"],'check_list2':["'Enable DHCP Persistence'.*?disabled.*?enabled"], 'uuid': '1526202'},
    {'check_list1': ["'DHCP Dynamic Range Begin' , 23.0.0.1/23.0.0.9"],'check_list2':["23.0.0.1/23.0.0.9.*?'DHCP Dynamic Range Begin'"], 'uuid': '1526203'},
    {'check_list1': ["'DHCP Dynamic Comment' , 23.0.0.1/23.0.0.9, changed to \[test\]"],'check_list2':["23.0.0.1/23.0.0.9.*?'DHCP Dynamic Comment'.*?test"], 'uuid': '1526204'},
    {'check_list1': ["'DHCP Static IP' , 23.0.0.11/000102030471"],'check_list2':["23.0.0.11/000102030471.*?'DHCP Static IP'"], 'uuid': '1526205'},
    {'check_list1': ["'DHCP Static Comment' , 23.0.0.11/000102030471, changed to \[static\]"],'check_list2':["23.0.0.11/000102030471.*?'DHCP Static Comment'.*?static"], 'uuid': '1526206'},
    {'check_list1': ["Deleted 'DHCP Static IP' , 23.0.0.11/000102030471","Deleted 'DHCP Dynamic Range Begin' , 23.0.0.1/23.0.0.9"],'check_list2':["23.0.0.1/23.0.0.9.*?Deleted 'DHCP Dynamic Range Begin'","23.0.0.11/000102030471.*?Deleted 'DHCP Static IP'"], 'uuid': '1526207'},
    {'check_list1': ["Delete DHCP Object"],'check_list2':["Delete DHCP Object"], 'uuid': '1526208'},
    {'check_list1': ["'Enable DHCPv6' , changed from \[enabled\], changed to \[disabled\]"],'check_list2':[" 'Enable DHCPv6'.*?enabled.*?disabled"], 'uuid': '1526209'},
    {'check_list1': ["'DHCPv6 dynamic scope object ID' , scope_ipv6"],'check_list2':["'DHCPv6 dynamic scope object ID'.*?scope_ipv6"], 'uuid': '1526210'},
    {'check_list1': ["'DHCPv6 dynamic scope object ID' , TEST_IPV6"],'check_list2':["'DHCPv6 dynamic scope object ID'.*?TEST_IPV6"], 'uuid': '1526211'},
    {'check_list1': ["'DHCPv6 Server static entry' , static_ipv6"],'check_list2':["static_ipv6.*?'DHCPv6 Server static entry'"], 'uuid': '1526212'},
    {'check_list1': ["'DHCPv6 Server static object comment' , static_ipv6, changed to \[test\]"],'check_list2':["static_ipv6.*?'DHCPv6 Server static object comment'.*?test"], 'uuid': '1526213'},
    {'check_list1': ["del dhcps6 Lease"],'check_list2':["del dhcps6 Lease"], 'uuid': '1526215'},
    {'check_list1': ["Deleted 'DHCPv6 dynamic scope object ID' , TEST_IPV6","Deleted 'DHCPv6 Server static entry' , static_ipv6"],'check_list2':["Deleted 'DHCPv6 dynamic scope object ID'.*?TEST_IPV6","Deleted 'DHCPv6 Server static entry'.*?static_ipv6"], 'uuid': '1526214'},
) 

class Test_Config_Auditing_GUI_Network_01(Test):

    def setParameters(self, check_list1,check_list2, uuid):
        self.check_list1 = check_list1
        self.check_list2 = check_list2
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        if self.uuid == '1526191' or self.uuid == '1526192':
            self.jira = 'GEN7-42086'
    
    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True , True , "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_01_clear_log(self):
        if self.uuid == '1526171':
            logger.info('no need clear log')
        else:
            rc = clear_log_and_snmp_msg()
            Assertion.assert_equal(rc , True , "ERR: clear log and snmp server message failed")

    def test_01_02_config_DUT(self):
        if self.uuid == '1526147':
            ref = copy.deepcopy(Lx2)
            ref['comment'] = 'modify x2 interfance'
            rc = Linterface.config_interface(**ref)
            Assertion.assert_equal(rc, True , "ERR: configure x2 failed")
        elif self.uuid == '1526148':
            ref = copy.deepcopy(Lx2)
            ref['mgmt_ssh'] = False
            rc = Linterface.config_interface(**ref)
            Assertion.assert_equal(rc, True , "ERR: configure ax2 failed")
        elif self.uuid == '1526149':
            ref1 = copy.deepcopy(redundant_port)
            ref2 = copy.deepcopy(Lx2)
            ref2.update(ref1)
            rc = Linterface.config_interface(**ref2)
            Assertion.assert_equal(rc, True , "ERR: configure x2 failed")
        elif self.uuid == '1526150':
            rc = Linterface.add_interface(**Lx2_vlan)
            Assertion.assert_equal(rc, True , "ERR: add vlan x2 failed")
        elif self.uuid == '1526151':
            ref = copy.deepcopy(Lx2_ipv6)
            ref['mgmt_ssh'] = False
            rc = Linterface_ipv6.config_interface_ipv6(**ref)
            Assertion.assert_equal(rc, True , "ERR: edit x2 ipv6 failed")
        elif self.uuid == '1526152':
            ref = copy.deepcopy(Lx2_ipv6)
            ref['ip'] = '3001::1'
            rc = Linterface_ipv6.config_interface_ipv6(**ref)
            Assertion.assert_equal(rc, True , "ERR: edit x2 ipv6 failed")
        elif self.uuid == '1526153':
            rc = Linterface_ipv6.add_tunnel_interface(**Lx2_ti)
            Assertion.assert_equal(rc, True , "ERR: edit x2 ti failed")
        elif self.uuid == '1526154':
            rc = Linterface.config_interface(**Lx5)
            Assertion.assert_equal(rc, True , "ERR: config x5 portsheild failed")
        elif self.uuid == '1526155':
            ref = copy.deepcopy(Lx5)
            ref['link_speed'] = '100_half'
            rc = Linterface.config_interface(**ref)
            Assertion.assert_equal(rc, True , "ERR: edit x5 linkspeed failed")
        elif self.uuid == '1526156':
            rc = failover_obj.config_failover_groups_by_multi(**lb_group)
            Assertion.assert_equal(rc, True , "ERR: add x3 to failover group failed")
        elif self.uuid == '1526157':
            ref = copy.deepcopy(lb_group)
            ref['failover_lb']['group'][0]['type'] = 'round-robin'
            del ref['failover_lb']['group'][0]['preempt']
            rc = failover_obj.config_failover_groups_by_multi(**ref)
            Assertion.assert_equal(rc, True , "ERR: edit failover group type failed")
        elif self.uuid == '1526158':
            ref = copy.deepcopy(lb_group)
            ref['failover_lb']['group'][0]['name'] = " Default LB Group IPv6"
            rc = failover_obj.config_failover_groups_by_multi(**ref)
            Assertion.assert_equal(rc, True , "ERR: add x3 to failover group ipv6 failed")
        elif self.uuid == '1526159':
            ref = copy.deepcopy(lb_group)
            ref['failover_lb']['group'][0]['name'] = " Default LB Group IPv6"
            ref['failover_lb']['group'][0]['type'] = 'round-robin'
            del ref['failover_lb']['group'][0]['preempt']
            rc = failover_obj.config_failover_groups_by_multi(**ref)
            Assertion.assert_equal(rc, True , "ERR: edit failover group type ipv6 failed")
        elif self.uuid == '1526160':
            rc = zones_obj.add_zone_object(**customer_zone)
            Assertion.assert_equal(rc, True , "ERR: add custom zone failed")
        elif self.uuid == '1526162':
            ref = copy.deepcopy(customer_zone)
            ref['zones'][0]['security_type'] = 'trusted'
            rc = zones_obj.edit_zone_object(name = 'test',**ref)
            Assertion.assert_equal(rc, True , "ERR: edit custom zone failed")
        elif self.uuid == '1526161':
            rc = zones_obj.delete_zone_object(name = 'test')
            Assertion.assert_equal(rc, True , "ERR: del custom zone failed")
        elif self.uuid == '1526163':
            rc =Linterface.config_interface(**Lx2_wiremode)
            rc &= vlan_translation.add_vlan_translation(**vlan_trans_json)
            Assertion.assert_equal(rc, True , "ERR: add vlan translation failed")
        elif self.uuid == '1526164':
            rc = vlan_translation.del_vlan_translation(**vlan_trans_json)
            Assertion.assert_equal(rc, True , "ERR: del vlan translation failed")
        elif self.uuid == '1526165':
            ref = copy.deepcopy(dns_set)
            ref['dns']['fqdn_over_tcp_dns'] = True
            rc = dns_setting.set_dns(**ref)
            Assertion.assert_equal(rc, True , "ERR: edit dns setting failed")
        elif self.uuid == '1526166':
            rc = dns_setting.add_split_dns(**dns_dict_ipv4)
            Assertion.assert_equal(rc, True , "ERR: Add IPv4 Split DNS Entry  failed")
        elif self.uuid == '1526167':
            rc = dns_setting.delete_split_dns(domain='test')
            Assertion.assert_equal(rc, True , "ERR: delete IPv4 Split DNS Entry  failed")
        elif self.uuid == '1526168':
            rc = dns_setting.add_split_dns(**dns_dict_ipv6)
            Assertion.assert_equal(rc, True , "ERR: Add IPv6 Split DNS Entry  failed")
        elif self.uuid == '1526169':
            rc = dns_setting.delete_split_dns(domain='mail.126.com')
            Assertion.assert_equal(rc, True , "ERR: delete IPv6 Split DNS Entry  failed")
        elif self.uuid == '1526170':
            rc = dns_proxy.config_dnsproxy(**dns_proxy_json)
            Assertion.assert_equal(rc, True , "ERR: Modify DNS Proxy Settings  failed")
        elif self.uuid == '1526172':
            rc = dns_proxy.add_dns_proxy_entry(**dns_proxy_entry)
            Assertion.assert_equal(rc, True , "ERR: Add Static DNS Proxy Cache Entry failed")
        elif self.uuid == '1526173':
            rc = dns_proxy.delete_static_dns_cache_entry(domain=['www.baidu.com'])
            Assertion.assert_equal(rc, True , "ERR: del Static DNS Proxy Cache Entry failed")
        elif self.uuid == '1526174':
            rc = dns_security.enable_dns_sinkhole(**dns_security_enable)
            rc &= dns_security.add_dns_custom_list(domain = 'custom.test.com')
            Assertion.assert_equal(rc, True , "ERR: Add  DNS Security - Custom Malicious Domain Name failed")
        elif self.uuid == '1526175':
            rc = dns_filter.add_dns_whitelist(name = 'white.test.com')
            Assertion.assert_equal(rc, True , "ERR: Add  DNS Security - White Domain Name failed")
        elif self.uuid == '1526176':
            rc = dns_security.set_dns_tunnel(enable=True, block=True)
            rc &= dns_security.add_dns_tunnel_white_list(ip = '1.1.1.1')
            Assertion.assert_equal(rc, True , "ERR: Add DNS Security - White List for DNS Tunnel Detection failed")
        elif self.uuid == '1526177':
            rc = route_obj.add_route_policy(**route_policies)
            Assertion.assert_equal(rc, True , "ERR: Add Standard Route Policy failed")
        elif self.uuid == '1526180':
            rc = route_obj.del_route_policy_by_name(name = 'test1_route')
            Assertion.assert_equal(rc, True , "ERR: del Standard Route Policy failed")
        elif self.uuid == '1526178':
            ref = copy.deepcopy(route_policies)
            ref['route_policies'][0]['ipv4']['name'] = 'test2_route'
            ref['route_policies'][0]['ipv4']['type'] = "multi-path"
            ref['route_policies'][0]['ipv4']['nexthop_number'] = 2
            ref['route_policies'][0]['ipv4']['gateway2'] = {"default":True}
            ref['route_policies'][0]['ipv4']['interface2'] = "X2"
            ref['route_policies'][0]['ipv4']['destination'] = {"name":"remote_net"}
            rc = route_obj.add_route_policy(**ref)
            Assertion.assert_equal(rc, True , "ERR: Add multi-path Route Policy failed")
        elif self.uuid == '1526179':
            rc = sdwan_group.configure_sdwan_group(**sdwan_group_json)
            rc &= sdwan_probe.configure_sdwan_probes(**sdwan_probe_json)
            rc &= sdwan_obj.configure_sdwan_perf_class(**sdwan_object_json)
            rc &= sdwan_path.configure_sdwan_psp(**sdwan_psp)
            rc &= sdwan_rt_obj.add_sdwan_route(**sdwan_route)
        elif self.uuid == '1526181':
            rc = route_obj.add_route_policy(**route_ipv6)
            Assertion.assert_equal(rc, True , "ERR: Add IPv6 Standard Route Policy failed")
        elif self.uuid == '1526182':
            rc = route_obj.del_route_policy_by_name(name = 'test_ipv6',version = 'ipv6')
            Assertion.assert_equal(rc, True , "ERR: del ipv6 Standard Route Policy failed")
        elif self.uuid == '1526183':
            rc = dynamic_route.set_ospf2(**ospfv2_dict)
            Assertion.assert_equal(rc, True , "ERR: Modify Interface OSPFv2 Configuration failed")
        elif self.uuid == '1526184':
            rc = dynamic_route.set_rip(**rip_dict)
            Assertion.assert_equal(rc, True , "ERR:  Modify Interface RIP Configuration failed")
        elif self.uuid == '1526185':
            rc = dynamic_route.set_ospf3(**ospfv3_dict)
            Assertion.assert_equal(rc, True , "ERR:  Modify Interface OSPFv3 Configuration failed")
        elif self.uuid == '1526186':
            rc = dynamic_route.set_ripng(**ripng_dict)
            Assertion.assert_equal(rc, True , "ERR:  Modify Interface RIPng Configuration failed")
        elif self.uuid == '1526187':
            rc = nat_policy.add_nat_policy(**nat_dict)
            Assertion.assert_equal(rc, True , "ERR:  add IPv4 nat policies  failed")
        elif self.uuid == '1526188':
            rc = nat_policy.del_nat_policy_by_name(name = 'test_nat',version = 'ipv4')
            Assertion.assert_equal(rc, True , "ERR:  del IPv4 nat policies  failed")
        elif self.uuid == '1526189':
            rc = nat_policy.add_nat_policy(**nat_ipv6_dict)
            Assertion.assert_equal(rc, True , "ERR:  add IPv6 nat policies  failed")
        elif self.uuid == '1526190':
            rc = nat_policy.del_nat_policy_by_name(name = 'test_nat_ipv6',version = 'ipv6')
            Assertion.assert_equal(rc, True , "ERR:  del IPv6 nat policies  failed")
        elif self.uuid == '1526191':
            rc = arp_obj.add_static_arp(**static_arp_dict)
            Assertion.assert_equal(rc, True , "ERR:   Add Static ARP Entries  failed")
        elif self.uuid == '1526192':
            rc = arp_obj.del_static_arp(**static_arp_dict)
            Assertion.assert_equal(rc, True , "ERR:   del Static ARP Entries  failed")
        elif self.uuid == '1526193':
            rc = arp_obj.arp_setting(timeout=22)
            Assertion.assert_equal(rc, True , "ERR:    Modify ARP Settings  failed")
        elif self.uuid == '1526194':
            rc = ndp_obj.add_static_entry(**ndp_dict)
            Assertion.assert_equal(rc, True , "ERR:   Add Static NDP Entries  failed")
        elif self.uuid == '1526195':
            rc = ndp_obj.delete_static_entry(**ndp_dict)
            Assertion.assert_equal(rc, True , "ERR:   Del Static NDP Entries  failed")
        elif self.uuid == '1526196':
            rc = mac_spoof.edit_mac_anti_spoof_settings(version = 4, name = 'X2',**mac_set_ipv4)
            Assertion.assert_equal(rc, True , "ERR:   Modify IPv4 Settings for Interface - Anti-Soof Settings  failed")
        elif self.uuid == '1526197':
            rc = mac_spoof.add_anti_spoof_cache(version = 4,**mac_cache_ipv4)
            Assertion.assert_equal(rc, True , "ERR:   Add Static IPv4 Cache Entries  failed")
        elif self.uuid == '1526198':
            rc = mac_spoof.delete_anti_spoof_cache(ip=DUT_X2, mac='2CB8ED6D7FF6', interface='X2',version = 'ipv4')
            Assertion.assert_equal(rc, True , "ERR:   del Static IPv4 Cache Entries  failed")
        elif self.uuid == '1526199':
            rc = mac_spoof.edit_mac_anti_spoof_settings(version = 6, name = 'X2',**mac_set_ipv6)
            Assertion.assert_equal(rc, True , "ERR:   Modify IPv6 Settings for Interface - Anti-Soof Settings  failed")
        elif self.uuid == '1526200':
            rc = mac_spoof.add_anti_spoof_cache(version = 6,**mac_cache_ipv6)
            Assertion.assert_equal(rc, True , "ERR:   Add Static IPv6 Cache Entries  failed")
        elif self.uuid == '1526201':
            rc = mac_spoof.delete_anti_spoof_cache(ip='28::28', mac='2CB8ED6D7FF6', interface='X2',version = 'ipv6')
            Assertion.assert_equal(rc, True , "ERR:   del Static IPv6 Cache Entries  failed")
        elif self.uuid == '1526202':
            rc = dhcp_obj.config_dhcp_server_settings(**dhcp_server_settings)
            Assertion.assert_equal(rc, True , "ERR:   Modify DHCPv4 Server Settings  failed")
        elif self.uuid == '1526203':
            rc = dhcp_obj.add_dhcp_server_scope_dynamic(**dhcp_scope_dynamic)
            Assertion.assert_equal(rc, True , "ERR:   Add Dynamic DHCPv4  Range  failed")
        elif self.uuid == '1526204':
            ref1 = copy.deepcopy(dhcp_scope_dynamic)
            ref1['dhcp_server']['ipv4']['scope']['dynamic'][0]['comment'] = 'test'
            rc = dhcp_obj.edit_dhcp_server_scope_v4(scope = 'dynamic',p1 = '23.0.0.1', p2 = '23.0.0.9',**ref1)
            Assertion.assert_equal(rc, True , "ERR:   edit Dynamic DHCPv4  Range  failed")
        elif self.uuid == '1526205':
            rc = dhcp_obj.add_dhcp_server_scope_static(**dhcp_scope_static)
            Assertion.assert_equal(rc, True , "ERR:   Add static DHCPv4  Range  failed")
        elif self.uuid == '1526206':
            ref1 = copy.deepcopy(dhcp_scope_static)
            ref1['dhcp_server']['ipv4']['scope']['static'][0]['comment'] = 'static'
            rc = dhcp_obj.edit_dhcp_server_scope_v4(scope = 'static',p1 = '23.0.0.11', p2 = '000102030471',**ref1)
            Assertion.assert_equal(rc, True , "ERR:   edit static DHCPv4  Range  failed")
        elif self.uuid == '1526207':
            rc = dhcp_obj.delete_dhcp_server_scope_v4(scope = 'static',p1 = '23.0.0.11', p2 = '000102030471')
            rc &= dhcp_obj.delete_dhcp_server_scope_v4(scope = 'dynamic',p1 = '23.0.0.1', p2 = '23.0.0.9')
            Assertion.assert_equal(rc, True , "ERR:   del static and dynamic DHCPv4  Range  failed")
        elif self.uuid == '1526208':
            cmds = ['pkill dhclient',
            'ifconfig eth0 0.0.0.0 0.0.0.0',
            'dhclient eth0',
            'ifconfig eth0']
            rc = dhcp_obj.edit_dhcp_server_scope_v4(scope = 'dynamic',p1 = '192.168.168.1', p2 = '192.168.168.167',**dhcp_scope_dynamic_x0)
            PC1.send_commands(cmds)
            res = dhcp_obj.get_dhcp_server_leases()
            pc1_eth0 = res[0]['ip_address']
            rc = dhcp_obj.delete_target_dhcp_server_lease(ip = pc1_eth0)
            Assertion.assert_equal(rc, True , "ERR:   del current dhcpv4 leases  failed")
        elif self.uuid == '1526209':
            rc = dhcp_obj.config_dhcp_server_settings(**dhcp_server_settings_v6)
            Assertion.assert_equal(rc, True , "ERR:   Modify DHCPv6 Server Settings  failed")
        elif self.uuid == '1526210':
            rc = dhcp_obj.add_dhcp_server_scope_dynamic(**dhcp_scope_dynamic_v6)
            Assertion.assert_equal(rc, True , "ERR:   Add Dynamic DHCPv6  Range  failed")
        elif self.uuid =='1526211':
            ref = copy.deepcopy(dhcp_scope_dynamic_v6)
            ref['dhcp_server']['ipv6']['scope']['dynamic'][0]['name'] = 'TEST_IPV6'
            rc = dhcp_obj.edit_dhcp_server_scope_v6(scope = 'dynamic',name = 'scope_ipv6',**ref)
            Assertion.assert_equal(rc, True , "ERR:   modify Dynamic DHCPv6  Range  failed")
        elif self.uuid == '1526212':
            rc = dhcp_obj.add_dhcp_server_scope_static(**dhcp_scope_static_v6)
            Assertion.assert_equal(rc, True , "ERR:   Add static DHCPv6   failed")
        elif self.uuid =='1526213':
            ref = copy.deepcopy(dhcp_scope_static_v6)
            ref['dhcp_server']['ipv6']['scope']['static'][0]['comment'] = 'test'
            rc = dhcp_obj.edit_dhcp_server_scope_v6(scope = 'static',name = 'static_ipv6',**ref)
            Assertion.assert_equal(rc, True , "ERR:  modify static DHCPv6  Range  failed")
        elif self.uuid =="1526214":
            rc = dhcp_obj.delete_dhcp_server_scope_v6(scope = 'dynamic',name = 'TEST_IPV6')
            rc &= dhcp_obj.delete_dhcp_server_scope_v6(scope = 'static',name = 'static_ipv6')
            Assertion.assert_equal(rc, True , "ERR:   del static and dynamic DHCPv6  Range  failed")
        elif self.uuid == '1526215':
            ret = DibblerStart()
            logger.info(f'---****{ret}')
            res = dhcp_obj.get_dhcp_server_leases(version=6)
            time.sleep(5)
            pc1_eth0_ipv6 = res[0]['ipv6_address']
            rc = dhcp_obj.delete_target_dhcp_server_lease(ip = pc1_eth0_ipv6,version=6)
            logger.info(f'------{res}')
            Assertion.assert_equal(rc & (not ret), True , "ERR:   del current dhcpv6 leases  failed")

    def test_01_03_verify_syslog(self):
        msg = os.popen('cat /var/log/messages', 'r')
        info = msg.read().replace(' ','').replace('\n','')
        if info == '':
            logger.info('the syslog message is null!!!')
            pass
        else:
            time.sleep(10)
            rc =check_log_msg(mode ='syslog',check_list=self.check_list1)
            Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_01_04_verify_snmp(self):
        rc =check_log_msg(mode ='snmp',check_list=self.check_list1)
        Assertion.assert_equal(rc, True , "ERR: check snmp trap failed")

    def test_01_05_verify_audit_log(self):
        rc =check_log_msg(mode ='audit',check_list=self.check_list2)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_01_06_verify_log(self):
        rc =check_log_msg(mode ='log',check_list=self.check_list1)
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_01_07_restore_env(self):
        if self.uuid in ['1526147','1526148','1526149'] :
            ref1 = copy.deepcopy(Lx2)
            ref2 = copy.deepcopy(remove_redundancy)
            ref2.update(ref1)
            rc = Linterface.config_interface(**ref2)
            Assertion.assert_equal(rc, True , "ERR: configure x6 failed")
        elif self.uuid == '1526150':
            rc = Linterface.del_interface(**Lx2_vlan)
            Assertion.assert_equal(rc, True , "ERR: del vlan x2 failed")
        elif self.uuid  in ['1526151','1526152']:
            rc = Linterface_ipv6.config_interface_ipv6(**Lx2_ipv6)
            Assertion.assert_equal(rc, True , "ERR: config x2 ipv6 failed")
        elif self.uuid == '1526153':
            rc = Linterface_ipv6.delete_tunnel_interface(name='x2_ti')
            Assertion.assert_equal(rc, True , "ERR: del x2 ti failed")
        elif self.uuid == '1526155':
            rc = Linterface.unassign_interface(interface="X5")
            Assertion.assert_equal(rc, True, f"ERR: restore Local X5 unassign failed")
        elif self.uuid == '1526157':
            ref = copy.deepcopy(lb_group)
            ref['failover_lb']['group'][0]['interface'].pop(1)
            rc = failover_obj.config_failover_groups_by_multi(**ref)
            Assertion.assert_equal(rc, True , "ERR: restore failover group  failed")
        elif self.uuid == '1526159':
            ref = copy.deepcopy(lb_group)
            ref['failover_lb']['group'][0]['name'] = " Default LB Group IPv6"
            ref['failover_lb']['group'][0]['interface'].pop(1)
            rc = failover_obj.config_failover_groups_by_multi(**ref)
            Assertion.assert_equal(rc, True , "ERR: restore failover group ipv6 failed")
        elif self.uuid == '1526164':
            rc = Linterface.config_interface(**Lx2)
            Assertion.assert_equal(rc, True , "ERR: restore Lx2 failed")
        elif self.uuid == '1526165':
            rc = dns_setting.set_dns(**dns_set)
            Assertion.assert_equal(rc, True , "ERR: edit dns setting failed")
        elif self.uuid == '1526171':
            ref = copy.deepcopy(dns_proxy_json)
            ref['enable'] = False
            ref['dns_cache'] = True
            rc = dns_proxy.config_dnsproxy(**ref)
            Assertion.assert_equal(rc, True , "ERR: Modify DNS Proxy Settings  failed")
        elif self.uuid == '1526174':
            rc = dns_security.delete_dns_custom_list(domains = ['custom.test.com'])
            Assertion.assert_equal(rc, True , "ERR: del  DNS Security - Custom Malicious Domain Name failed")
        elif self.uuid == '1526175':
            rc = dns_filter.del_dns_whitelist(name_list = ['white.test.com'])
            Assertion.assert_equal(rc, True , "ERR: del  DNS Security - White Domain Name failed")
        elif self.uuid == '1526176':
            rc = dns_security.delete_dns_tunnel_white_list(ips = ['1.1.1.1'])
            Assertion.assert_equal(rc, True , "ERR: del DNS Security - White List for DNS Tunnel Detection failed")
        elif self.uuid == '1526178':
            rc = route_obj.del_route_policy_by_name(name = 'test2_route')
            Assertion.assert_equal(rc, True , "ERR: del  Route Policy failed")
        elif self.uuid == '1526179':
            rc = route_obj.del_route_policy_by_name(name = 'test3_route')
            rc &= sdwan_path.delete_sdwan_psp(name = 'test')
            rc &= sdwan_obj.delete_sdwan_perf_class(name = 'test')
            rc &= sdwan_probe.delete_sdwan_probes(name = 'test')
            rc &= sdwan_group.delete_sdwan_group(name='test')
            Assertion.assert_equal(rc, True , "ERR: del  Route Policy failed")
        elif self.uuid == '1526183':
            ref = copy.deepcopy(ospfv2_dict)
            ref['mode'] = 'disable'
            rc = dynamic_route.set_ospf2(**ref)
            Assertion.assert_equal(rc, True , "ERR: Modify Interface OSPFv2 Configuration failed")
        elif self.uuid == '1526184':
            ref = copy.deepcopy(rip_dict)
            ref['mode'] = 'disable'
            rc = dynamic_route.set_rip(**ref)
            Assertion.assert_equal(rc, True , "ERR:  Modify Interface RIP Configuration failed")
        elif self.uuid == '1526185':
            ref = copy.deepcopy(ospfv3_dict)
            ref['mode'] = 'disable'
            rc = dynamic_route.set_ospf3(**ref)
            Assertion.assert_equal(rc, True , "ERR:  Modify Interface OSPFv3 Configuration failed")
        elif self.uuid == '1526186':
            ref = copy.deepcopy(ripng_dict)
            ref['mode'] = 'disable'
            rc = dynamic_route.set_ripng(**ref)
            Assertion.assert_equal(rc, True , "ERR:  Modify Interface RIPng Configuration failed")
        elif self.uuid == '1526193':
            rc = arp_obj.arp_setting(timeout=10)
            Assertion.assert_equal(rc, True , "ERR:  Modify ARP Settings  failed")
        elif self.uuid == '1526198':
            ref = copy.deepcopy(mac_set_ipv4)
            ref['mac_ip_anti_spoof']['interface'][0]['enable'] = False
            rc = mac_spoof.edit_mac_anti_spoof_settings(version = 4, name = 'X2',**ref)
            Assertion.assert_equal(rc, True , "ERR:   Modify IPv4 Settings for Interface - Anti-Soof Settings  failed")
        elif self.uuid == '1526201':
            ref = copy.deepcopy(mac_set_ipv6)
            ref['mac_ip_anti_spoof']['ipv6']['interface'][0]['enable'] = False
            rc = mac_spoof.edit_mac_anti_spoof_settings(version = 6, name = 'X2',**ref)
            Assertion.assert_equal(rc, True , "ERR:   Modify IPv6 Settings for Interface - Anti-Soof Settings  failed")
        elif self.uuid == '1526202':
            ref = copy.deepcopy(dhcp_server_settings)
            ref['dhcp_server']['ipv4']['persistence'] = False
            rc = dhcp_obj.config_dhcp_server_settings(**ref)
            Assertion.assert_equal(rc, True , "ERR:   Modify DHCPv4 Server Settings  failed")
        elif self.uuid == '1526208':
            ref = copy.deepcopy(dhcp_scope_dynamic_x0)
            ref['dhcp_server']['ipv4']['scope']['dynamic'][0]['from'] = '192.168.168.1'
            ref['dhcp_server']['ipv4']['scope']['dynamic'][0]['to'] = '192.168.168.167'
            rc = dhcp_obj.edit_dhcp_server_scope_v4(scope = 'dynamic',p1 = '192.168.168.200', p2 = '192.168.168.200',**ref)
            Assertion.assert_equal(rc, True , "ERR:   edit Dynamic DHCPv4  Range  failed")
        elif self.uuid == '1526209':
            ref = copy.deepcopy(dhcp_server_settings_v6)
            ref['dhcp_server']['ipv6']['enable'] = True
            rc = dhcp_obj.config_dhcp_server_settings(**ref)
            Assertion.assert_equal(rc, True , "ERR:   Modify DHCPv6 Server Settings  failed")
        elif self.uuid == '1526215':
            ret = DibblerStop()
            logger.info('------------------')
            logger.info(ret)
            Assertion.assert_equal(ret, False, "ERR: stop dibbler client failed")
        else:
            logger.info('This case not need restore env')


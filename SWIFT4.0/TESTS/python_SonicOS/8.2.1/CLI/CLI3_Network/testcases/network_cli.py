from definition.settings import *


class Test_01_Configure_Interface(Test):
    uuid = "SOSAIOT-TC-48515"
    description = show_testcase_info(TESTPLAN, "1", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_config_x2_interface(self):
        rs = interfacecli.config_interface(**X2_STATIC_dict)
        logger.info(f'configure x2 interface result:{rs}')
        show_result = interfacecli.show_interface_status(
            interface='x2', version='ipv4')
        logger.info(f'show x2 interface status: {show_result}')
        output = True if 'ip ' + \
                         X2_STATIC_dict['ip'] and X2_STATIC_dict['comment'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: configure X2 interface failed")

    def test_02_unassign_x2_interface(self):
        output = False
        rs = interfacecli.unassign_interface(interface='x2')
        logger.info(f'unassgin x2 interface result: {rs}')
        show_result = interfaceapi.get_interface_status('X2')
        logger.info(show_result)
        try:
            output = True if show_result['interfaces'][0]['ipv4']['ip_assignment'] == {
            } else False
        except BaseException:
            Assertion.assert_equal(
                False, True, "ERR: show interface x0 failed")
        Assertion.assert_equal(
            output, True, "ERR: unassign X2 interface failed")

    def test_03_add_tunnel_interface(self):
        rs = interfacecli.add_tunnel_interface_4to6(**tunnel_interface_dict)
        logger.info(f'show add 4to6 tunnel interface result: {rs}')
        show_result = interfacecli.show_tunnel_interface_status(
            type='4to6', name='test_gre')
        logger.info(f'show added tunnel interface result: {show_result}')
        output = True if 'ip ' + \
                         tunnel_interface_dict['ip'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: add tunnel interface failed")


class Test_02_Configure_Zone(Test):
    uuid = "SOSAIOT-TC-48526"
    description = show_testcase_info(TESTPLAN, "2", description=True)['title']

    def test_00__show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_zone(self):
        rs = zonecli.add_zone(**zone_dict)
        logger.info(f'show add zone result: {rs}')
        show_result = zonecli.show_zones()
        output = True if 'zone test1' in show_result else False
        Assertion.assert_equal(output, True, "ERR: add zone failed")

    def test_02_edit_zone(self):
        rs = zonecli.edit_zone(**zone_new_dict)
        logger.info(f'show edit zone result: {rs}')
        show_result = zonecli.show_zones()
        output = True if 'zone edit-test1' in show_result else False
        Assertion.assert_equal(output, True, "ERR: add zone failed")

    def test_03_del_zone(self):
        rs = zonecli.del_zone(*del_zone_list)
        logger.info(f'show delete zone result: {rs}')
        show_result = zonecli.show_zones()
        output = True if 'zone edit-test1' not in show_result else False
        Assertion.assert_equal(output, True, "ERR: delete zone failed")


class Test_03_Configure_WLB(Test):
    uuid = "SOSAIOT-TC-48528"
    description = show_testcase_info(TESTPLAN, "3", description=True)['title']

    def test_00__show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_configure_wlb(self):
        rs = failoverlbcli.edit_default_LB(**wlb_basic_dict)
        logger.info(f'show edit default LB result: {rs}')
        show_result = failoverlbcli.show_failover()
        logger.info(f'show failover result: {show_result}')
        output = True if 'missed-intervals 6' and 'successful-intervals 7' in show_result else False
        Assertion.assert_equal(output, True, "ERR: configure WLB failed")


class Test_04_Configure_DHCP_Server(Test):
    uuid = "SOSAIOT-TC-48529"
    description = show_testcase_info(TESTPLAN, "4", description=True)['title']
    jira = "GEN7-30038"

    def test_00__show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_dhcpserver_static_scope_v4(self):
        rs = dhcpservercli.add_dhcpserver_scope_v4(
            **dhcpserver_scope_static_dict)
        logger.info(f'show add static dhcpserver scope result: {rs}')
        show_result = dhcpservercli.show_dhcpserver_v4()
        logger.info(f'show dhcpserver status: {show_result}')
        output = True if '192.168.168.170 112233445566' in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: add dhcpserver static scope ipv4 failed")

    def test_02_add_dhcpserver_dynamic_scope_v4(self):
        range = old_scope_dict['start'] + ' ' + old_scope_dict['end']

        rs = dhcpservercli.add_dhcpserver_scope_v4(
            **dhcpserver_scope_dynamic_dict)
        logger.info(f'show add dynanic scope result: {rs}')
        show_result = dhcpservercli.show_dhcpserver_v4()
        logger.info(f'show dhcpserver status: {show_result}')
        output = True if range in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: add dhcpserver dynamic scope ipv4 failed")

    def test_03_edit_dhcpserver_scope_v4(self):
        res = dhcpservercli.edit_dhcpserver_scope_v4(old_scope_dict, new_scope_dict)
        Assertion.assert_equal(
            res, True, "ERR: edit dhcpserver scope ipv4 failed")

    def test_04_del_scope(self):
        res = dhcpservercli.delete_dynmaic_scope(**del_scope_dict)
        Assertion.assert_equal(
            res, True, "ERR: delete dhcpserver scope ipv4 failed")


class Test_05_Add_Address_Object(Test):
    uuid = "SOSAIOT-TC-48530"
    description = show_testcase_info(TESTPLAN, "5", description=True)['title']

    def test_00__show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_host_ao(self):
        rs = aocli.add_address_object(**host_ao_dict)
        logger.info(f'add host address object result: {rs}')
        show_result = aocli.show_address_object(
            name='test-host', version='ipv4')
        logger.info(f'show the added host ao result: {show_result}')
        output = True if 'host ' + \
                         host_ao_dict['host'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: add a host type address object failed")

    def test_02_add_range_ao(self):
        rs = aocli.add_address_object(**range_ao_dict)
        logger.info(f'add range address object result: {rs}')
        show_result = aocli.show_address_object(
            name='test-range', version='ipv4')
        logger.info(f'show the added range ao result: {show_result}')
        output = True if 'range ' + \
                         range_ao_dict['range'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: add a range type address object failed")

    def test_03_add_network_ao(self):
        rs = aocli.add_address_object(**network_ao_dict)
        logger.info(f'add network address object result: {rs}')
        show_result = aocli.show_address_object(
            name='test-network', version='ipv4')
        logger.info(f'show the added network ao result: {show_result}')
        output = True if 'network ' + \
                         network_ao_dict['network'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: add a network type address object failed")

    def test_04_add_mac_ao(self):
        rs = aocli.add_address_object(**mac_ao_dict)
        logger.info(f'add mac address object result: {rs}')
        show_result = aocli.show_address_object(name='test-mac', type='mac')
        logger.info(f'show the added mac ao result: {show_result}')
        output = True if 'address 112233445566' in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: add a mac address object failed")

    def test_05_add_fqdn_address_object(self):
        rs = aocli.add_address_object(**fqdn_ao_dict)
        logger.info(f'add fqdn address object result: {rs}')
        show_result = aocli.show_address_object(name='test-fqdn', type='fqdn')
        output = True if 'domain ' + \
                         fqdn_ao_dict['domain'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: add a fqdn address object failed")


class Test_06_Configure_DDNS(Test):
    uuid = "SOSAIOT-TC-48531"
    description = show_testcase_info(TESTPLAN, "6", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_ddns_profile(self):
        rs = ddnscli.add_ddns_profile(**ddns_profile_dict)
        logger.info(f'show add ddns profile result: {rs}')
        show_result = ddnscli.show_ddns('ipv4')
        output = True if 'domain ' + \
                         ddns_profile_dict['domain'] in show_result else False
        Assertion.assert_equal(output, True, "ERR: add DDNS profile failed")

    def test_02_edit_dns_profile(self):
        rs = ddnscli.edit_ddns_profile(**ddns_profile_new_dict)
        logger.info(f'show edit ddns profile result: {rs}')
        show_result = ddnscli.show_ddns('ipv4')
        output = True if 'domain ' + \
                         ddns_profile_new_dict['domain-new'] in show_result else False
        Assertion.assert_equal(output, True, 'ERR, edit ddns profile failed')


class Test_07_Configure_Route(Test):
    uuid = "SOSAIOT-TC-48532"
    description = show_testcase_info(TESTPLAN, "7", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_route_policy(self):
        rs = routecli.add_route_policy(**add_route_dict)
        logger.info(f'show add route policy result: {rs}')
        show_result = routecli.show_route_policy(**add_route_dict)
        logger.info(f'show the added route policy result: {show_result}')
        output = True if 'metric 12' in show_result else False
        Assertion.assert_equal(output, True, "ERR:add a route policy failed")

    def test_02_edit_route_policy(self):
        rs = routecli.edit_route_policy(add_route_dict, new_route_dict)
        logger.info(f'show edit route policy result: {rs}')
        show_result = routecli.show_route_policy_by_name(name='edit-route')
        logger.info(f'show the edited route policy result: {show_result}')
        output = True if 'metric 6' in show_result else False
        Assertion.assert_equal(output, True, "ERR:edit a route policy failed")

    def test_03_del_route_policy(self):
        rs = routecli.del_route_policy(**del_route_dict)
        logger.info(f'show delete route policy result: {rs}')
        show_result = routecli.show_route_policies(
            version='ipv4', type='custom')
        logger.info(f'show the added route policy result: {show_result}')
        output = True if 'metric 6' not in show_result else False
        Assertion.assert_equal(output, True, "ERR:del a route policy failed")


class Test_08_Configure_IPHelper(Test):
    uuid = "SOSAIOT-TC-48533"
    description = show_testcase_info(TESTPLAN, "8", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_iphelper(self):
        rc = iphelpercli.enable_IPhelper()
        logger.info(f'enable iphelper settings result: {rc}')
        Assertion.assert_equal(rc, True, 'ERR: enable iphelper failed')

    def test_02_add_relay_protocol(self):
        rs = iphelpercli.add_relay_protocol(**relay_protocol_dict)
        logger.info(f'add relay protocol result: {rs}')
        show_result = iphelpercli.show_relay_protocol(name='iph-v4')
        output = True if 'port1 30' and 'port2 40' in show_result else False
        Assertion.assert_equal(output, True, "ERR: configure IPHelper failed")

    def test_03_add_policy(self):
        rs = iphelpercli.add_policy(**policy_dhcp_dict)
        logger.info(f'show add policy result: {rs}')
        show_result = iphelpercli.show_policies()
        output = True if policy_dhcp_dict['comment'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: failed to add iphelper policy")


class Test_09_Configure_NAT_Policy(Test):
    uuid = "SOSAIOT-TC-48534"
    description = show_testcase_info(TESTPLAN, "8", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_nat_policy_v4(self):
        rs = natcli.add_natpolicy(**nat_v4_dict)
        logger.info(f'show the add ipv4 nat policy result： {rs}')
        show_result = natcli.show_natpolicy(**nat_v4_dict)
        output = True if nat_v4_dict['comment'] in show_result else False
        Assertion.assert_equal(output, True, "ERR: add ipv4 NAT Policy failed")

    def test_02_edit_nat_policy_v4(self):
        rs = natcli.edit_natpolicy(nat_v4_dict, natv4_new_dict)
        logger.info(f'show edit the added nat policy result: {rs}')
        show_result = natcli.show_natpolicy(**natv4_new_dict)
        output = True if natv4_new_dict['comment'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: edit ipv4 NAT Policy failed")

    def test_03_del_natpolicy_v4(self):
        rc = natcli.del_natpolicy(*nat_del_list)
        logger.info(f'show delete the added vat policy result: {rc}')
        Assertion.assert_equal(rc, True, "ERR: delete ipv4 NAT Policy failed")

    def test_04_add_nat_policy_v6(self):
        rs = natcli.add_natpolicy(**nat_v6_dict)
        logger.info(f'show add ipv6 nat policy result: {rs}')
        show_result = natcli.show_natpolicy(**nat_v6_dict)
        output = True if nat_v6_dict['comment'] in show_result else False
        Assertion.assert_equal(output, True, "ERR: add ipv6 NAT Policy failed")

    def test_05_add_nat_policy_64(self):
        rs = natcli.add_natpolicy(**nat_64_dict)
        logger.info(f'show add nat64 policy result: {rs}')
        show_result = natcli.show_natpolicy(**nat_64_dict)
        output = True if nat_64_dict['comment'] in show_result else False
        Assertion.assert_equal(output, True, "ERR: add NAT64 Policy failed")


class Test_10_Configure_Network_Monitor(Test):
    uuid = "SOSAIOT-TC-48516"
    description = show_testcase_info(TESTPLAN, "10", description=True)['title']
    jira = 'GEN8-5321'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_network_monitor_policy(self):
        rs = networkmonitorcli.add_nm_policy(**nm_icmp_dict)
        logger.info(f'show add network monitor policy result: {rs}')
        show_result = networkmonitorcli.show_nm_policy(name='nm_ipv4')
        output = True if nm_icmp_dict['comment'] in show_result else False
        Assertion.assert_equal(output, True, "ERR: add network monitor failed")


class Test_11_Configure_Interface_IPV6(Test):
    uuid = "SOSAIOT-TC-48517"
    description = show_testcase_info(TESTPLAN, "10", description=True)['title']
    jira = 'GEN7-37892'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_configure_interface_ipv6(self):
        rs = interfacecli.config_interface_ipv6(**x0_ipv6_static_dict)
        logger.info(f'show x0 ipv6 interface result: {rs}')
        show_result = interfacecli.show_interface_status(
            interface='x0', version='ipv6')
        logger.info(f'show x2 interface status: {show_result}')
        output = True if 'ip ' + \
                         x0_ipv6_static_dict['ip'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: configure ipv6 interface general failed")


class Test_12_Add_Vlan_Interface(Test):
    uuid = "SOSAIOT-TC-48518"
    description = show_testcase_info(TESTPLAN, "12", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_configure_vlan_interface(self):
        rs = interfacecli.add_interface(**vlan_interface_dict)
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = interfacecli.show_interface_status(
            interface='x0 vlan 200')
        logger.info(f'show x2 interface status: {show_result}')
        output = True if 'ip ' + \
                         vlan_interface_dict['ip'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: configure vlan interface failed")


class Test_13_Edit_Vlan_Interface(Test):
    uuid = "SOSAIOT-TC-48519"
    description = show_testcase_info(TESTPLAN, "13", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_vlan_interface(self):
        vlan_dict = {
            'if': "x0 vlan 200",
            'zone': 'lan',
            'mode': "static",
            'ip': "200.1.1.2"
        }
        rc = interfacecli.config_interface(**vlan_dict)
        Assertion.assert_equal(rc, True, 'ERR: edit vlan interface failed!')


class Test_14_Del_Vlan_Interface(Test):
    uuid = "SOSAIOT-TC-48520"
    description = show_testcase_info(TESTPLAN, "14", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_del_vlan_interface(self):
        vlan_dict = {
            'if': "x0",
            'type': 'vlan',
            'vlan-tag': 200
        }
        rc = interfacecli.del_interface(**vlan_dict)
        Assertion.assert_equal(rc, True, 'ERR: del vlan interface failed!')


class Test_15_Del_Multi_Vlan_Interface(Test):
    uuid = "SOSAIOT-TC-48521"
    description = show_testcase_info(TESTPLAN, "15", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_create_multi_vlan(self):
        params = [{
            'if': 'x0',
            'type': 'vlan',
            'vlan-tag': int(tag),
            'zone': 'lan',
            'mode': 'static',
            'ip': f'{tag}.1.1.1'
        } for tag in (100, 101, 102, 103, 104)]
        for iface in params:
            rc = interfacecli.add_interface(**iface)
            if not rc:
                logger.error(f"add vlan interface <{iface['vlan-tag']}> failed")
                break
        Assertion.assert_equal(rc, True, 'ERR: add multi vlan interfaces failed!')

    def test_01_del_multi_vlan(self):
        params = [{'if': "x0", "type": "vlan", "vlan-tag": tag} for tag in (100, 101)]
        for iface in params:
            rc = interfacecli.del_interface(**iface)
            if not rc:
                logger.error(f'del vlan interface <{iface["vlan-tag"]}> failed!')
                break
        Assertion.assert_equal(rc, True, "ERR: del multi vlan interface failed!")


class Test_16_Del_All_Vlan_Interface(Test):
    uuid = "SOSAIOT-TC-48522"
    description = show_testcase_info(TESTPLAN, "16", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_del_all_vlan_ifaces(self):
        rc = interfacecli.del_all_vlan_interfaces()
        Assertion.assert_equal(rc, True, 'ERR: del all vlan interface failed!')


class Test_17_Add_Arp_Entry(Test):
    uuid = "SOSAIOT-TC-48523"
    description = show_testcase_info(TESTPLAN, "17", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_ary_entry(self):
        arp_dict = {
            'ip': '10.11.12.13',
            'mac': '00:11:22:33:44:55',
            'interface': 'x0'
        }
        rc = arp_cli.add_arp_entry(**arp_dict)
        Assertion.assert_equal(rc, True, 'ERR: add arp entry failed!')


class Test_18_Edit_Arp_Entry(Test):
    uuid = "SOSAIOT-TC-48524"
    description = show_testcase_info(TESTPLAN, "18", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_arp_entry(self):
        old_dict = {
            'ip': '10.11.12.13',
            'mac': '00:11:22:33:44:55',
            'interface': 'x0'
        }
        new_dict = {
            'ip': '10.11.12.14',
            'mac': '00:11:22:33:44:55',
            'interface': 'x0'
        }
        rc = arp_cli.edit_arp_entry(old_dict, new_dict)
        Assertion.assert_equal(rc, True, 'ERR: edit arp entry failed!')


class Test_19_Del_Arp_Entry(Test):
    uuid = "SOSAIOT-TC-48525"
    description = show_testcase_info(TESTPLAN, "19", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_del_arp_entry(self):
        arp_dict = {
            'ip': '10.11.12.13',
            'mac': '00:11:22:33:44:55',
            'interface': 'x0'
        }
        rc = arp_cli.del_arp_entry(**arp_dict)
        Assertion.assert_equal(rc, True, 'ERR: del arp entry failed!')


class Test_20_Del_All_Arp_Entry(Test):
    uuid = "SOSAIOT-TC-48527"
    description = show_testcase_info(TESTPLAN, "20", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_arp_entries(self):
        for i in range(3):
            arp_dict = {
                'ip': f'10.11.12.1{i}',
                'mac': f'00:11:22:33:44:5{i}',
                'interface': 'x0'
            }
            rc = arp_cli.add_arp_entry(**arp_dict)
            if not rc:
                logger.error(f'add ARP <{arp_dict}> failed')
        Assertion.assert_equal(rc, True, 'ERR: add arp entry failed!')

    def test_02_del_all_ar(self):
        rc = arp_cli.del_all_arp_entries()
        Assertion.assert_equal(rc, True, 'ERR: del all arp entries failed')


class Test_21_Conf_IPv6_Prefix(Test):
    uuid = "SOSAIOT-TC-48535"
    description = show_testcase_info(TESTPLAN, "2025633", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2025633')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_config_x3_ipv4(self):
        x3_dict = {
            'if': 'x3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': "13.13.1.168"
        }
        rc = interfacecli.config_interface(**x3_dict)
        Assertion.assert_equal(rc, True, 'ERR: config x3 interface failed!')

    def test_02_config_x3_ipv6(self):
        x3_v6_dict = {
            'if': 'x3',
            'zone': 'lan',
            'ip': '2003::168',
            'router-advertisement': True,
            'add_prefix': {
                'ip': '1001::',
                'autonomou': True
            }
        }
        rc = interfacecli.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc, True, 'ERR: config ipv6 x3 failed!')

    def test_03_show_ipv6_prefix(self):
        resp = interfacecli.show_interface_prefix('x3')
        rc = 'prefix 1001::' in resp
        Assertion.assert_equal(rc, True, 'ERR: show added ipv6 prefix failed!')

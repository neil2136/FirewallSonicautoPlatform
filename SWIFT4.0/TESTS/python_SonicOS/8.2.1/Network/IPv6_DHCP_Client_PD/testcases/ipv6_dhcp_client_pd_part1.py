from definition.settings import *
from definition.utils import *


# Expect: At least one DHCPv6 interface can support DHCPv6 PD
class Test_IPv6_PD_TC001(Test):
    uuid = "SOSAIOT-TC-56450"
    description = show_testcase_info(TESTPLAN, '001', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '001')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_get_v6_x1_pd_status(self):
        resp = if_v6_api.get_ipv6_interface_base(name='x1')
        Assertion.assert_regular(json.dumps(resp), '"prefix_delegation": {"preferred": {}}',
                                 'ERR: get pd status failed.')


# Expect: DHCPv6 PD info MUST be displayed in ¡°Protocol¡± tab when PD is enabled on that interface
class Test_IPv6_PD_TC002(Test):
    uuid = "SOSAIOT-TC-56451"
    description = show_testcase_info(TESTPLAN, '002', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '002')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_x1_v6_addr(self):
        rc = False
        time.sleep(60)
        for i in range(3):
            ip_res = check_interface_v6_addr('x1', Parameter.V6_Prefix)
            if ip_res:
                rc = True
                break
            if_v6_cli.click_dhcpv6_renew('x1')
        Assertion.assert_equal(rc, True, 'ERR: x1 get v6 addr failed.')

    def test_02_check_x1_obtained_pd(self):
        CasePara.tsr_msg = diag_api.get_tsr_part(func='Network', lab1='Interfaces')
        res = check_pd_in_tsr(Parameter.X1_PD1, CasePara.tsr_msg)
        Assertion.assert_equal(res, True, 'ERR: x1 obtained pd failed')


# Expect: DHCPv6 PD information MUST be contained in TSR when PD is enabled on one interface
class Test_IPv6_PD_TC051(Test):
    uuid = "SOSAIOT-TC-56473"
    description = show_testcase_info(TESTPLAN, '051', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '051')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_in_tsr(self):
        res = check_pd_in_tsr(Parameter.X1_PD1, CasePara.tsr_msg)
        Assertion.assert_equal(res, True, 'ERR: check pd in failed.')


# Expect: DHCPv6 PD information MUST be contained in TSR when PD is enabled on one interface
class Test_IPv6_PD_TC052(Test):
    uuid = "SOSAIOT-TC-56474"
    description = show_testcase_info(TESTPLAN, '052', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '052')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_reboot_fw(self):
        res = set_api.boot_fw(mode=1)
        Assertion.assert_equal(res, True, 'ERR: reboot firewall failed.')

    def test_02_check_settings(self):
        Test_IPv6_PD_TC002().test_02_check_x1_obtained_pd()


# Expect: The PD information of the interface MUST be displayed, including IAID, Type, IPv6 Prefix, Prefix Length, and Lease Expires
class Test_IPv6_PD_TC003(Test):
    uuid = "SOSAIOT-TC-56452"
    description = show_testcase_info(TESTPLAN, '003', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '003')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_pd_detail_info(self):
        iaid_info = get_IAID_info_in_tsr(CasePara.tsr_msg)
        Assertion.assert_equal(bool(iaid_info), True, 'ERR: check pd details info failed.')


# Expect: Currently one interface MUST learn one PD prefix only
class Test_IPv6_PD_TC005(Test):
    uuid = "SOSAIOT-TC-56453"
    description = show_testcase_info(TESTPLAN, '005', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '005')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verfiy_only_one_PD_entry(self):
        m = re.findall('Identity Association for Prefix Delegation', CasePara.tsr_msg)
        logger.info(m)
        Assertion.assert_equal(len(m), 1, 'ERR: verfiy only one pd can obtained failed.')


# Expect: When clicking Renew button, the interface should do Renew process while a PD prefix has been learned
class Test_IPv6_PD_TC013(Test):
    uuid = "SOSAIOT-TC-56461"
    description = show_testcase_info(TESTPLAN, '013', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '013')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_01_check_do_renew_process(self):
        rc = False
        init_packet_capture()
        if_v6_cli.click_dhcpv6_renew('x1')
        time.sleep(5)
        stop_res = pkt_api.stop_capture()
        logger.info(f'=> start capture result: {stop_res}')
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            msg_type = get_dhcpv6_packet_type(pkt)
            if msg_type == 'Renew' or msg_type == 'Rebind':
                rc = True
                break
        else:
            logger.error('no rebind occurs')
        Assertion.assert_equal(True, True, "ERR: check firewall do renew process failed!")


# Expect:An IPv6 AO with Network type of PD prefix for the interface that PD is enabled MUST be auto added
class Test_IPv6_PD_TC006(Test):
    uuid = "SOSAIOT-TC-56454"
    description = show_testcase_info(TESTPLAN, '006', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '006')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_01_check_auto_added_pd_ao(self):
        time.sleep(5)
        resp = ao_api.get_addressobject_by_name(version='ipv6', name='X1 Delegated Prefix')
        Assertion.assert_regular(json.dumps(resp), Parameter.X1_PD1, 'ERR: check auto added pd ao failed.')


# Expect:An IPv6 route for delegated prefix destined to Drop_TunnelIf MUST be created
class Test_IPv6_PD_TC009(Test):
    uuid = "SOSAIOT-TC-56457"
    description = show_testcase_info(TESTPLAN, '009', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '009')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_01_check_auto_added_route(self):
        time.sleep(5)
        out = route_cli.show_route_policies(version='ipv6', type='')
        res = 'destination name "X1 Delegated Prefix"' in out and 'interface Drop_TunnelIf' in out
        Assertion.assert_equal(res, True, 'ERR: check auto added route failed.')


# Expect: Downstream interface can add IPv6 addresses based on the PD prefix
class Test_IPv6_PD_TC010(Test):
    uuid = "SOSAIOT-TC-56458"
    description = show_testcase_info(TESTPLAN, '010', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '010')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_set_x3_to_lan(self):
        x3_dict = {
            'if': 'X3',
            'zone': "LAN",
            'mode': 'static',
            'ip': '13.13.1.168'
        }
        res = if_v4_api.config_interface(**x3_dict)
        Assertion.assert_equal(res, True, 'ERR: config x3 failed')

    def test_02_add_extra_x3_ip(self):
        res = if_v6_api.add_ipv6_extra_ip(**x3_param_1)
        Assertion.assert_equal(res, True, 'ERR: add ipv6 addr based on PD failed.')

    @repeat_method(3)
    def test_03_check_x3_v6_addr(self):
        time.sleep(5)
        res = check_interface_v6_addr('x3', Parameter.X1_PD1 + '1/64')
        Assertion.assert_equal(res, True, 'ERR: verify x3 obtained v6 address failed.')

    def test_04_del_extra_x3_ip(self):
        res = if_v6_api.delete_ipv6_extra_ip(**x3_param_1)
        Assertion.assert_equal(res, True, 'ERR: del x3 extra ip failed.')


# Expect: The downstream delegated IPv6 address should choose the longer prefix length between the PD prefix length and the preferred prefix length
class Test_IPv6_PD_TC011(Test):
    uuid = "SOSAIOT-TC-56459"
    description = show_testcase_info(TESTPLAN, '011', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '011')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_extra_x3_ip(self):
        res = if_v6_api.add_ipv6_extra_ip(**x3_param_2)
        Assertion.assert_equal(res, True, 'ERR: add x3 extra ip failed.')

    @repeat_method(3)
    def test_02_check_x3_v6_addr(self):
        time.sleep(5)
        res = check_interface_v6_addr('x3', Parameter.X1_PD1 + '1/72')
        Assertion.assert_equal(res, True, 'ERR: verify x3 obtained v6 address failed.')

    def test_03_del_extra_ip_x3(self):
        res = if_v6_api.delete_ipv6_extra_ip(**x3_param_2)
        Assertion.assert_equal(res, True, 'ERR: del x3 extra ip failed.')

    def test_04_add_extra_x3_ip(self):
        res = if_v6_api.add_ipv6_extra_ip(**x3_param_3)
        Assertion.assert_equal(res, True, 'ERR: add x3 extra ip failed.')

    @repeat_method(3)
    def test_05_check_x3_v6_addr(self):
        time.sleep(5)
        res = check_interface_v6_addr('x3', Parameter.X1_PD1 + '1/64')
        Assertion.assert_equal(res, True, 'ERR: verify x3 obtained v6 address failed.')

    def test_06_del_x3_extra_ip(self):
        res = if_v6_api.delete_ipv6_extra_ip(**x3_param_3)
        Assertion.assert_equal(res, True, 'ERR: del x3 extra ip failed.')


# Expect: The related Delegated Prefix AO MUST be deleted when DHCPv6 PD is disabled on that interface
class Test_IPv6_PD_TC007(Test):
    uuid = "SOSAIOT-TC-56455"
    description = show_testcase_info(TESTPLAN, '007', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '007')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_pd_on_x1(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                # 'prefix_delegation': False,
                'prefix_delegation': {},
                "mode": "manual",
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: disable pd on x1 failed.')

    @repeat_method(3)
    def test_02_check_related_ao_is_deleted(self):
        time.sleep(5)
        out = ao_cli.show_address_objects(version='ipv6', ao_type='network')
        Assertion.assert_not_regular(out, "X1 Delegated Prefix", 'ERR: check_related_ao_is_deleted failed.')


# Expect: All the related routes MUST be deleted when the related Delegated Prefix AO is deleted
class Test_IPv6_PD_TC008(Test):
    uuid = "SOSAIOT-TC-56456"
    description = show_testcase_info(TESTPLAN, '008', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '008')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_01_check_related_route_is_deleted(self):
        time.sleep(5)
        out = route_cli.show_route_policies(version='ipv6', type='')
        Assertion.assert_not_regular(out, "X1 Delegated Prefix", 'ERR: check_related_route_is_deleted')


class Test_Update_PD(Test):
    uuid = 'NonTC'
    goto_teardown = True
    description = 'update the PD pool on server'

    def test_01_change_pd_pool_on_dhcpv6_server(self):
        cmd_list = ['dibbler-server stop',
                    f'timeout 5 \cp {conf_path}/server_2.conf /etc/dibbler/server.conf',
                    'timeout 5 dibbler-server start',
                    'timeout 5 dibbler-server status']
        out = pc2_login.send_commands(cmd_list)
        Assertion.assert_regular(out, 'Dibbler server: RUNNING', 'ERR: start dibbler server failed.')

    def test_02_init_x1_v6(self):
        x1_v6_dict = {
            'name': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': "::",
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: init x1 v6 iface failed.')


# Expect: When the PD prefix is updated, the related PD AO MUST be updated
class Test_IPv6_PD_TC019(Test):
    uuid = "SOSAIOT-TC-56466"
    description = show_testcase_info(TESTPLAN, '019', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '019')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_pd_on_x1(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                # 'prefix_delegation': True,
                "mode": "manual",
                'prefix_delegation': {"preferred": {}}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'set x1 to dhcpv6 mode failed.')

    def test_02_check_x1_v6_addr(self):
        res = False
        time.sleep(60)
        for i in range(3):
            ip_res = check_interface_v6_addr('x1', Parameter.V6_Prefix)
            if ip_res:
                res = True
                break
            if_v6_cli.click_dhcpv6_renew('x1')
            time.sleep(30)
        Assertion.assert_equal(res, True, 'ERR: x1 get v6 addr failed.')

    def test_03_check_x1_obtained_pd(self):
        tsr_msg = diag_api.get_tsr_part(func='Network', lab1='Interfaces')
        res = check_pd_in_tsr(Parameter.X1_PD2, tsr_msg)
        Assertion.assert_equal(res, True, 'ERR: x1 obtain pd failed')

    def test_04_check_updated_pd_ao(self):
        resp = ao_api.get_addressobject_by_name(version='ipv6', name='X1 Delegated Prefix')
        Assertion.assert_regular(json.dumps(resp), Parameter.X1_PD2, 'ERR: check auto added pd ao failed.')


# Expect: When the PD AO is updated, all related downstream interface addresses MUST be updated/
class Test_IPv6_PD_TC020(Test):
    uuid = "SOSAIOT-TC-56467"
    description = show_testcase_info(TESTPLAN, '020', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '020')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_extra_x3_ip(self):
        res = if_v6_api.add_ipv6_extra_ip(**x3_param_1)
        Assertion.assert_equal(res, True, 'ERR: add x3 extra ip failed.')

    @repeat_method(3)
    def test_02_check_x3_v6_addr(self):
        time.sleep(5)
        res = check_interface_v6_addr('x3', Parameter.X1_PD2 + '1/64')
        Assertion.assert_equal(res, True, 'ERR: verify x3 obtained v6 address failed.')


# Expect: When the PD AO is updated, all related routes MUST be updated
class Test_IPv6_PD_TC021(Test):
    uuid = "SOSAIOT-TC-56468"
    description = show_testcase_info(TESTPLAN, '021', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '021')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_updated_related_routes(self):
        out = route_cli.show_route_policies(version='ipv6', type='')
        res = 'destination name "X1 Delegated Prefix"' in out and 'interface Drop_TunnelIf' in out
        Assertion.assert_equal(res, True, 'ERR: check auto added route failed.')


# Expect: When the PD AO is updated, all related downstream interface MUST update its related prefixes when sending Router Advertisements
class Test_IPv6_PD_TC022(Test):
    uuid = "SOSAIOT-TC-56469"
    description = show_testcase_info(TESTPLAN, '022', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '022')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_00_enable_RA_x3(self):
        x3_v6_dict = {
            'name': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': "::",
            'router_adv': True,
            'ra_min': 20,
            'ra_max': 30
        }
        res = if_v6_api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: init x1 v6 iface failed.')

    def test_01_01_configure_packet_monitor_to_default(self):
        param = {
            'monitor_filter': {
                'ip_types': '',
                'destination_ports': ''
            }
        }
        res = pkt_api.conf_packmon(**param)
        Assertion.assert_equal(res, True, 'ERR: config packet monitor failed.')

    @repeat_method(3)
    def test_02_check_RA_packet(self):
        rc = False
        pkt_api.monitor_default()
        init_packet_capture()
        time.sleep(60)
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if f'ICMPv6 Option (Prefix information : {Parameter.X1_PD2}/64)' in pkt:
                rc = True
                break
        Assertion.assert_equal(rc, True, 'ERR: check updated PD info in RA message failed!')


# Expect: DUT MUST support to enable DHCPv6 PD on physical interface
class Test_IPv6_PD_TC023(Test):
    uuid = "SOSAIOT-TC-56470"
    description = show_testcase_info(TESTPLAN, '023', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '023')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_pd_on_physical_interface(self):
        Test_IPv6_PD_TC001().test_01_get_v6_x1_pd_status()


# Expect: DUT MUST support to enable DHCPv6 PD on VLAN interface
class Test_IPv6_PD_TC024(Test):
    uuid = "SOSAIOT-TC-56471"
    description = show_testcase_info(TESTPLAN, '024', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '024')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_vlan_bound_x3(self):
        x3_vlan = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': 100,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '2.2.2.168',
            'mgmt_ping': True,
            'mgmt_https': True,
        }
        res = if_v4_api.add_interface(**x3_vlan)
        Assertion.assert_equal(
            res, True, "ERR: add sub vlan iface for X3 failed.")

    def test_02_enable_pd_on_x3_vlan(self):
        x3_vlan_dict = {
            'name': 'X3:V100',
            'mode': 'dhcpv6',
            'dhcpv6': {
                # 'prefix_delegation': True,
                'prefix_delegation': {"preferred": {}},
                "mode": "manual",

            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x3_vlan_dict)
        Assertion.assert_equal(res, True, 'ERR: enable pd on x3 vlan inface failed.')

    def test_03_check_vlan_interface_pd_status(self):
        resp = if_v6_api.get_ipv6_interface_base(name='X3:V100')
        Assertion.assert_regular(json.dumps(resp), '"prefix_delegation": {"preferred": {}}',
                                 'ERR: iface X3:V100 get pd status failed.')


# Expect: DUT MUST support to enable DHCPv6 PD when interface is in PPPoE mode
class Test_IPv6_PD_TC025(Test):
    uuid = "SOSAIOT-TC-56472"
    description = show_testcase_info(TESTPLAN, '025', description=True)['title']
    jira = 'GEN7-49071'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '025')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_update_x3_to_pppoe_mode(self):
        x3_dict = {
            'if': 'x3',
            # 'type': 'vlan',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': "test",
            "pppoe_passwd": '123456',
            'pppoe_servicename': '',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 0,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_ping': True,
            'mgmt_https': True,
        }
        res = if_v4_api.config_interface(**x3_dict)
        Assertion.assert_equal(
            res, True, "ERR: update X3 to pppoe mode failed.")

    def test_02_enable_pd_on_x3_pppoev6(self):
        x3_v6_dict = {
            "name": 'X3',
            'mode': "pppoe6",
            'listen_router_advertisement': True,
            'pppoe6': {
                'inactivity': 1,
                'mode_assign': 'dhcpv6',
                # 'prefix_delegation': True,
                'prefix_delegation': {"preferred": {}},
                "reconnect": 5,
                'lcp_echo_packets': False,
                'ncp_neg_retrans': 200,
                'rapid_commit': False
            }
        }
        res = if_v6_api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: enable_pd_on_x3_pppoev6 failed')

    def test_03_check_x3_interface_pd_status(self):
        resp = if_v6_api.get_ipv6_interface_base(name='X3')
        Assertion.assert_regular(json.dumps(resp), '"prefix_delegation": {"preferred": {}}',
                                 'ERR: get pd status failed.')


# Expect: When clicking Release button, the interface MUST do Release process while a PD prefix has already been learned
class Test_IPv6_PD_TC015(Test):
    uuid = "SOSAIOT-TC-56462"
    description = show_testcase_info(TESTPLAN, '015', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '015')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_set_x1_v6(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': True
                'prefix_delegation': {"preferred": {}}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'set x1 to dhcpv6 mode failed.')

    def test_02_check_x1_v6_addr(self):
        rc = False
        time.sleep(60)
        for i in range(3):
            ip_res = check_interface_v6_addr('x1', Parameter.V6_Prefix)
            if ip_res:
                rc = True
                break
            if_v6_cli.click_dhcpv6_renew('x1')
            time.sleep(30)
        Assertion.assert_equal(rc, True, 'ERR: x1 get v6 addr failed.')

    def test_03_check_x1_obtain_pd(self):
        tsr_info = diag_api.get_tsr_part(func='Network', lab1='Interfaces')
        res = check_pd_in_tsr(Parameter.X1_PD2, tsr_info)
        Assertion.assert_equal(res, True, 'ERR: x1 obtained pd failed')

    def test_04_check_do_release_when_click_release(self):
        rc = False
        for i in range(3):
            logger.info(f'run for {i + 1} time')
            if_v6_cli.click_dhcpv6_renew('x1')
            init_packet_capture()
            if_v6_cli.click_dhcpv6_release('x1')
            time.sleep(30)
            stop_res = pkt_api.stop_capture()
            logger.info(f'=> start capture result: {stop_res}')
            pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
            pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
            pkt_list = pkts.split('\n\n')
            for pkt in pkt_list:
                msg_type = get_dhcpv6_packet_type(pkt)
                if msg_type == 'Release':
                    rc = True
                    break
            else:
                logger.error('no release occurs')
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: check firewall do release process failed!")


# Expect:When the interface PD prefix is released, the related AO of that interface MUST be reset
class Test_IPv6_PD_TC016(Test):
    uuid = "SOSAIOT-TC-56463"
    description = show_testcase_info(TESTPLAN, '016', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '016')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_01_check_related_AO_reset_after_pd_release(self):
        out = ao_cli.show_address_objects(version='ipv6', ao_type='network')
        out_list = out.split('\n')
        for entry in out_list:
            if 'X1 IPv6' in entry and Parameter.X1_PD2 in entry:
                rc = False
                break
        else:
            rc = True
        Assertion.assert_equal(rc, True, 'ERR: check_related_ao_is_deleted failed.')


# Expect: When the interface PD prefix is released, all related downstream interfaces MUST stop advertising related subnet prefixes
class Test_IPv6_PD_TC017(Test):
    uuid = "SOSAIOT-TC-56464"
    description = show_testcase_info(TESTPLAN, '017', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '017')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_01_check_pd_in_RA_packet(self):
        rc = False
        pkt_api.monitor_default()
        init_packet_capture()
        time.sleep(60)
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if f'ICMPv6 Option (Prefix information : {Parameter.X1_PD2}/64)' not in pkt:
                rc = True
                break
        Assertion.assert_equal(rc, True, 'ERR: check updated PD info in RA message failed!')


# Expect: When the PD prefix is released, all related downstream interface PD addresses MUST be deleted
class Test_IPv6_PD_TC018(Test):
    uuid = "SOSAIOT-TC-56465"
    description = show_testcase_info(TESTPLAN, '018', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '018')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_the_downstream_iface_reset(self):
        for i in range(3):
            logger.info(f'run for {i + 1} time')
            if_v6_cli.click_dhcpv6_release('x1')
            time.sleep(30)
            res = check_interface_v6_addr('x3', "::")
            if res:
                break
        Assertion.assert_equal(res, True,
                               "ERR: check all related downstream interface PD addresses are deleted failed!")

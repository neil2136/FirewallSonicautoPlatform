from definition.settings import *
from definition.utils import *


# Expect:[GUI]Same parent interface and different zone
class TestV6Vlan_TC1(Test):
    uuid = "SOSAIOT-TC-56689"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_addsubif_in_zones(self):
        cfg_opt = {
            'LAN': {
                'vlan_tag': 100,
                'ip': '100.1.1.1'
            },
            'WAN': {
                'vlan_tag': 101,
                'ip': '101.1.1.1'
            },
            'WLAN': {
                'vlan_tag': 102,
                'ip': '102.1.1.1'
            },
            'DMZ': {
                'vlan_tag': 103,
                'ip': '103.1.1.1'
            }
        }
        for zone in cfg_opt:
            vlan_if = {
                'if': 'x0',
                'type': 'vlan',
                'vlan_tag': cfg_opt[zone]['vlan_tag'],
                'zone': zone,
                'mode': 'static',
                'ip': cfg_opt[zone]['ip']
            }
            res = interfacev4api.add_interface(**vlan_if)
            if not res:
                logger.error(f"config interface X0 to <{zone}> with vlan <{vlan_if['vlan_tag']}> failed!")
                break
        Assertion.assert_equal(res, True, 'ERR: add vlan if in different zones failed.')

    def test_02_config_v6addr_for_vlan_subif(self):
        cfg_opt_v6 = {
            'LAN': {
                'vlan_tag': 100,
                'ip': '1000::1'
            },
            'WAN': {
                'vlan_tag': 101,
                'ip': '1001::1'
            },
            'WLAN': {
                'vlan_tag': 102,
                'ip': '1002::1'
            },
            'DMZ': {
                'vlan_tag': 103,
                'ip': '1003::1'
            }
        }
        for zone in cfg_opt_v6:
            vlan_ifv6 = {
                'name': 'X0',
                'vlan': cfg_opt_v6[zone]['vlan_tag'],
                'mode': 'static',
                'zone': zone,
                'ip': cfg_opt_v6[zone]['ip']
            }
            res = interfacev6api.config_interface_ipv6(**vlan_ifv6)
            if not res:
                logger.error(f"config vlan <{vlan_ifv6['vlan']}> failed!")
                break
        Assertion.assert_equal(res, True, 'ERR: config v6 addr for vlan sub if failed.')


# Expect: [FUN]Static IPv6 Assignment
class TestV6Vlan_TC13(Test):
    uuid = "SOSAIOT-TC-56690"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_static_v6addr_for_X1_vlan(self):
        x1v6_vlan_static = {
            'name': 'X1',
            'vlan': X1_VLAN_ID,
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_V1_V6IP,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh': True,
        }
        res = interfacev6api.config_interface_ipv6(**x1v6_vlan_static)
        Assertion.assert_equal(
            res, True, "ERR: config v6 address for x1 vlan if failed")

    @repeat_method(3)
    def test_02_check_pingres_of_x1_vlan(self):
        out = pc2_login.send_command('ping6 2022::168 -c 5')
        Assertion.assert_not_regular(out, '100% packet loss', 'check ping result of x1 vlan if failed.')


# Expect: [FUN]Management traffic - HTTP
class TestV6Vlan_TC16(Test):
    uuid = "SOSAIOT-TC-56693"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_http_result(self):
        out = pc2_login.send_command(
            f'curl -k http://[{Parameter.X1_V1_V6IP}]')
        rc = f"https://[{Parameter.X1_V1_V6IP}]/sonicui/7/login/" in str(out)
        Assertion.assert_equal(rc, True, 'ERR: check http management traffic failed.')


# Expect: [FUN]Management traffic - HTTPS
class TestV6Vlan_TC17(Test):
    uuid = "SOSAIOT-TC-56694"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_https_result(self):
        TestV6Vlan_TC16().test_01_check_http_result()


# Expect: [FUN]Management traffic - PING
class TestV6Vlan_TC19(Test):
    uuid = "SOSAIOT-TC-56696"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_ping_result(self):
        res = pc2_login.ping6(Parameter.X1_V1_V6IP)
        Assertion.assert_equal(
            res, True, 'check ping result of x1 vlan if failed.')


# Expect: [FUN]DHCPV6 IP Assignment
class TestV6Vlan_TC14(Test):
    uuid = "SOSAIOT-TC-56691"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x1_vlanif_to_dhcpv6_mode(self):
        x1v6_vlan_dhcpv6 = {
            'name': 'X1',
            'vlan': X1_VLAN_ID,
            'mode': 'dhcpv6',
            'zone': 'WAN',
            'dhcpv6': {
                'mode': 'manual'
            },
            'mgmt_ping': True,
            'mgmt_https': True,
            'listen_router_advertisement': True
        }
        res = interfacev6api.config_interface_ipv6(**x1v6_vlan_dhcpv6)
        Assertion.assert_equal(
            res, True, "ERR: Configure X1 dhcpv6 mode failed")

    def test_02_X1_vlanif_get_dhcpv6_addr(self):
        rc = False
        time.sleep(15)
        for i in range(5):
            logger.info(f'run for {i + 1} time')
            resp = interfacev6api.get_interface_address(
                name=f'X1/vlan/{X1_VLAN_ID}')
            if '2022::' in str(resp):
                rc = True
                break
            else:
                interfacecli.click_dhcpv6_renew(f'X1 vlan {X1_VLAN_ID}')
                time.sleep(3)
        Assertion.assert_equal(rc, True, 'ERR: x1 vlan if get dhcpv6 address failed')


# Expect: [FUN]auto IP Assignment
class TestV6Vlan_TC15(Test):
    uuid = "SOSAIOT-TC-56692"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x1_vlan_if_to_auto_mode(self):
        x1vlan_auto = {
            'name': 'X1',
            'vlan': X1_VLAN_ID,
            'mode': 'auto',
            'zone': 'WAN',
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res = interfacev6api.config_interface_ipv6(**x1vlan_auto)
        Assertion.assert_equal(
            res, True, "ERR: Configure X1 dhcpv6 mode failed")

    @repeat_method(5)
    def test_02_check_if_get_autov6_addr(self):
        time.sleep(15)
        resp = interfacev6api.get_interface_address(
            name=f'X1/vlan/{X1_VLAN_ID}')
        Assertion.assert_regular(
            str(resp), '2001:1:2:3:', 'ERR: x1 vlan if get v6 address in auto mode failed')


# Expect: [FUN] Router Advertisement settings & Advertise Subnet Prefix of IPV6 Primary static address for VLAN
class TestV6Vlan_TC23(Test):
    uuid = "SOSAIOT-TC-56697"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_prefix(self):
        resp = interfacev6api.get_ipv6_prefixes()
        Assertion.assert_regular(
            str(resp), '2013:1::', "ERR: verfiy Advertise Subnet Prefix failed")

    @repeat_method(3)
    def test_02_check_RA_msg_info(self):
        res = False
        clear_res = packetapi.clear_packets()
        logger.info(f'=> clear packet result: {clear_res}')
        start_res = packetapi.start_capture()
        logger.info(f'=> start capture result: {start_res}')
        time.sleep(60)
        stop_res = packetapi.stop_capture()
        logger.info(f'=> start capture result: {stop_res}')
        pc1_login.send_command('rm -rf /tmp/*.pcapng')
        packetapi.export_captured_packets_pcapng()
        packets = pc1_login.send_command('tshark -V -r /tmp/packet-c.pcapng')
        packet_list = packets.split('Packet comments')
        for packet in packet_list:
            if f'X3:V{X3_VLAN_ID1}*,Generated' in packet:
                if 'Dst: ff02::1' in packet:
                    if 'Router Advertisement (134)' in packet:
                        logger.info('RA packet is generated')
                        if 'Managed address configuration: Not set' in packet:
                            if 'Other configuration: Not set' in packet:
                                logger.info('M and O flag not set')
                                logger.info(
                                    '=' * 10 + "captured RA packet as follow:" + "=" * 10)
                                logger.info(packet)
                                res = True
                            else:
                                logger.error(
                                    'sent wrong RA message due to M or O flag is set.')
                    else:
                        logger.error('RA packet not generated')
        Assertion.assert_equal(res, True, 'ERR: verify RA message failed.')

    def test_03_check_client_ipv6_addr(self):
        for i in range(3):
            logger.info(f'run for {i+1} time')
            time.sleep(15)
            out = pc3_login.send_command("ifconfig eth1 | grep inet6")
            res = "prefixlen 64" in out and '2013:1::' in out
            if res:
                break
        Assertion.assert_equal(res, True, 'client get v6 addr failed.')


# Expect: [FUN]Routing between different VLAN
class TestV6Vlan_TC24(Test):
    uuid = "SOSAIOT-TC-56698"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_check_traffic_between_vlan(self):
        pc3_v6_addr = get_client_global_v6_addr(pc3_login)
        pc4_v6_addr = get_client_global_v6_addr(pc4_login)
        logger.info(f'pc3 ipv6 addr is: {pc3_v6_addr}')
        logger.info(f'pc4 ipv6 addr is: {pc4_v6_addr}')
        if pc4_v6_addr and pc3_v6_addr:
            pc4_login.config_IPv6_route(
                route='2013:1::', prefix=64, gw=Parameter.X3_V2_V6)
        res = pc4_login.ping6(pc3_v6_addr)
        Assertion.assert_equal(
            res, True, 'ERR: verify traffic between vlan interfaces failed.')


# Expect: [FUN]VLAN Preference support
class TestV6Vlan_TC35(Test):
    uuid = "SOSAIOT-TC-56699"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_prefs(self):
        res = settingapi.export_setting_exp('/tmp/cyuan_ipv6_vlan_test.exp')
        Assertion.assert_equal(res, True, "ERR: export prefs file failed")

    def test_02_restore_fw(self):
        res = settingapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_03_import_prefs_file(self):
        res = settingapi.import_setting_exp(
            filepath='/tmp/cyuan_ipv6_vlan_test.exp')
        Assertion.assert_equal(res, True, "ERR: import prefs file failed")

    def test_04_check_settings(self):
        check_tumple = [('100', "1000::1"), ('101', "1001::1"), ('102', "1002::1"),
                        ('103', "1003::1")]
        for tumple in check_tumple:
            resp = interfacev6api.get_interface_address(
                name=f'X0/vlan/{tumple[0]}')
            res = tumple[1] in str(resp)
            if not res:
                logger.error(f"check vlan ID <{tumple[0]}>'s ipv6 addr failed!")
                break
        Assertion.assert_equal(res, True, 'check settings after import prefs file failed.')


# Expect: [GUI]Delete IPv6 Vlan sub interface
class TestV6Vlan_TC40(Test):
    uuid = "SOSAIOT-TC-56700"
    description = show_testcase_info(TESTPLAN, '40', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '40')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_delete_vlan_sub_if(self):
        x3_del_vlan1_dict = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': str(X3_VLAN_ID1)
        }

        x3_del_vlan2_dict = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': str(X3_VLAN_ID2)
        }
        res1 = interfacev4api.del_interface(**x3_del_vlan1_dict)
        res2 = interfacev4api.del_interface(**x3_del_vlan2_dict)
        Assertion.assert_equal(
            res1 & res2, True, 'ERR: del vlan sub interface failed.')


# Expect: [FUN]Management for VLAN trunk interface
class TestV6Vlan_TC41(Test):
    uuid = "SOSAIOT-TC-56701"
    description = show_testcase_info(TESTPLAN, '41', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vlan_trunk_port(self):
        trunk_port_dict = {"port": "X3"}
        res = vlanTrunkApi.add_trunk_ports(**trunk_port_dict)
        Assertion.assert_equal(res, True, 'ERR: add trunk port failed.')

    def test_02_enable_vlan(self):
        res1 = vlanTrunkApi.enable_vlan(interface='X3', vlan=str(X3_VLAN_ID1))
        res2 = vlanTrunkApi.enable_vlan(interface='X3', vlan=str(X3_VLAN_ID2))
        Assertion.assert_equal(res1 & res2, True, 'ERR: enabl vlan failed.')

    def test_03_set_trunk_vlan_interface_addr_v4(self):
        x3_vlan1 = {
            'name': 'X3',
            'vlan': X3_VLAN_ID1,
            'ip_assignment': {
                "mode": {
                    "static": {
                        "ip": Parameter.X3_V1_IP,
                        "netmask": "255.255.255.0"
                    }
                },
                "zone": "LAN"
            },
            'management': {
                'https': True,
                'ping': True,
            }
        }
        x3_vlan2 = {
            'name': 'X3',
            'vlan': X3_VLAN_ID2,
            'ip_assignment': {
                "mode": {
                    "static": {
                        "ip": Parameter.X3_V2_IP,
                        "netmask": "255.255.255.0"
                    }
                },
                "zone": "LAN"
            },
            'management': {
                'https': True,
                'ping': True,
            }
        }
        res1 = interfacev4api.edit_vlan_interface(**x3_vlan1)
        res2 = interfacev4api.edit_vlan_interface(**x3_vlan2)
        Assertion.assert_equal(
            res1 & res2, True, "ERR: set v4 addr for trunk vlan interface failed")

    def test_04_set_trunk_vlan_interface_addr_v6(self):
        x3_vlan1_v6 = {
            'name': 'X3',
            'vlan': X3_VLAN_ID1,
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_V1_V6,
            'mgmt_https': True
        }
        x3_vlan2_v6 = {
            'name': 'X3',
            'vlan': X3_VLAN_ID2,
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_V2_V6,
            'mgmt_https': True
        }
        res1 = interfacev6api.config_interface_ipv6(**x3_vlan1_v6)
        res2 = interfacev6api.config_interface_ipv6(**x3_vlan2_v6)
        Assertion.assert_equal(
            res1 & res2, True, 'ERR: set v4 addr for trunk vlan interface failed')

    @repeat_method(3)
    def test_05_check_https_for_vlan_trunk_interface(self):
        out = pc3_login.send_command(
            f'curl -k https://[{Parameter.X3_V1_V6}]')
        rc = f"https://[{Parameter.X3_V1_V6}]/sonicui/7/login/" in str(out)
        Assertion.assert_equal(rc, True, 'ERR: check https management failed.')


# Expect [FUN]Passing traffic through VLAN trunk interface
class TestV6Vlan_TC42(Test):
    uuid = "SOSAIOT-TC-56702"
    description = show_testcase_info(TESTPLAN, '42', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_routes_for_pc(self):
        pc3_login.config_IPv6_route(
            route='2013:2::', prefix=64, gw=Parameter.X3_V1_V6)
        pc4_login.config_IPv6_route(
            route='2013:1::', prefix=64, gw=Parameter.X3_V2_V6)
        Assertion.assert_equal(True, True, 'ERR: add routes for pc3 and pc4 failed!')

    @repeat_method(3)
    def test_02_check_traffic(self):
        time.sleep(3)
        pc3_v6_addr = get_client_global_v6_addr(pc3_login)
        pc4_v6_addr = get_client_global_v6_addr(pc4_login)
        logger.info(f'pc3 ipv6 addr is: {pc3_v6_addr}')
        logger.info(f'pc4 ipv6 addr is: {pc4_v6_addr}')
        res1 = pc3_login.ping6(pc4_v6_addr)
        res2 = pc4_login.ping6(pc3_v6_addr)
        Assertion.assert_equal(
            res1&res2, True, 'ERR: verify traffic between vlan interfaces failed.')

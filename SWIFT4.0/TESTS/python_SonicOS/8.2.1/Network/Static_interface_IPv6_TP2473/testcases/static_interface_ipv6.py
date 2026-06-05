from definition.settings import *
from definition.utils import *


# Expect: Verify the function after change IPV6 WAN static gateway address
class TestV6If_TC39(Test):
    uuid = "SOSAIOT-TC-57213"
    description = show_testcase_info(TESTPLAN, '39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_remote_FW_x2v6(self):
        res = rm_ifacev6_api.config_interface_ipv6(**rem_x2v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 IPv6 to static failed")

    def test_02_config_x2v6_to_static(self):
        res = iface_v6_api.config_interface_ipv6(**x2v6_static_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 IPv6 to static failed")

    @repeat_method(3)
    def test_03_check_generated_default_route(self):
        time.sleep(10)
        rules = route_api.get_default_route_policy_v6()
        res = False
        try:
            for rule in rules:
                if rule['destination'] == '::/0':
                    if rule['gateway'] == Parameter.REM_X2_V6_IP:
                        res = True
                        break
            else:
                logger.error('get the default route failed!')
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(
            res, True, "ERR: check generated default route failed")

    def test_04_configure_packet_monitor(self):
        pkt_api.monitor_default()
        mon_conf_dict = {
            'monitor_filter': {
                'ip_types': 'icmpv6'
            }
        }
        res, _ = pkt_api.conf_packmon(mon_conf_dict)
        Assertion.assert_equal(res, True, 'ERR: config packet monitor failed')

    @repeat_method(3)
    def test_05_check_forwarded_mac(self):
        localhost.send_command('ifconfig eth1 inet6 add 2000::100/64')
        localhost.send_command('ip -6 route add 2003::/64 via 2000::168')
        packets = packets_process_for_ping6(Parameter.UNREACH_V6_ADDR)
        res = check_forwarded_mac(
            packets, src_ip=Parameter.PC1_ETH1_V6, trs_src_ip=Parameter.X2_V6_IP, dst_ip=Parameter.UNREACH_V6_ADDR)
        Assertion.assert_equal(res, True, 'check forwarded MAC address failed.')

    def test_06_update_remote_FW_x2v6(self):
        rem_x2v6_dict.update(rem_x2v6_update)
        res = rm_ifacev6_api.config_interface_ipv6(**rem_x2v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure remote FW X2 IPv6 to static failed")

    def test_07_update_X2_GW(self):
        x2v6_static_dict.update(x2v6_update_dict)
        res = iface_v6_api.config_interface_ipv6(**x2v6_static_dict)
        Assertion.assert_equal(res, True, "ERR: update X2 IPv6 GW failed")

    def test_08_check_updated_ipv6_default_route(self):
        rules = route_api.get_default_route_policy_v6()
        res = False
        try:
            for rule in rules:
                if rule['destination'] == '::/0':
                    if rule['gateway'] == x2v6_update_dict["gateway"]:
                        res = True
                        break
            else:
                logger.error('get the default route failed!')
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(
            res, True, "ERR: check updated default route failed")

    @repeat_method(3)
    def test_09_check_forwarded_mac(self):
        packets = packets_process_for_ping6(Parameter.UNREACH_V6_ADDR)
        res = check_forwarded_mac(
            packets, src_ip=Parameter.PC1_ETH1_V6, trs_src_ip=Parameter.X2_V6_IP, dst_ip=Parameter.UNREACH_V6_ADDR)
        Assertion.assert_equal(res, True, 'check forwarded MAC address failed.')


# Expect: IPv6 default route learned from RA, check its gateway.
class TestV6If_TC36(Test):
    uuid = "SOSAIOT-TC-57212"
    description = show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_pkt_monitor(self):
        pkt_api.monitor_default()
        pkt_mon_dict = {
            'monitor_filter': {
                'ip_types': "ICMPv6",
                'interfaces': "x2"
            }
        }
        res = pkt_api.conf_packmon(**pkt_mon_dict)
        Assertion.assert_equal(res, True, "ERR: config packet monitor failed")

    def test_02_enable_listen_to_RA_on_FW(self):
        iface_v4_api.disable_interface('x2')
        init_packet_capture()
        x2v6_static_dict.update({'listen_router_advertisement': True})
        res = iface_v6_api.config_interface_ipv6(**x2v6_static_dict)
        time.sleep(3)
        iface_v4_api.enable_interface('x2')
        Assertion.assert_equal(res, True, "ERR: enbale listening RA on FW X2 failed")

    @repeat_method(3)
    def test_03_check_if_generate_default_route_v6(self):
        res = False
        time.sleep(10)
        output = rm_ao_api.get_addressobject_by_name(
            name='X2 IPv6 Link-Local Address', version='ipv6')
        try:
            CaseParams.rem_x2_linklocal = output['address_objects'][0]['ipv6']['host']['ip']
            rules = route_api.get_default_route_policy_v6()
            for rule in rules:
                if rule['destination'] == '::/0' and rule['metric'] == 50:
                    if rule['gateway'] == CaseParams.rem_x2_linklocal:
                        logger.info(rule)
                        res = True
                        break
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(
            res, True, "ERR: check generated default route v6 failed")

    def test_04_check_if_received_RA_from_remX2(self):
        res = False
        for i in range(5):
            logger.info(f'check RA packet for the {i + 1} time')
            time.sleep(30)
            packets = pkt_api.export_captured_packets()
            logger.info(packets)
            (res, packet) = check_RA_packet(packets, 'X2', src_ip=CaseParams.rem_x2_linklocal)
            if res:
                logger.info(packet)
                break
        pkt_api.stop_capture()
        Assertion.assert_equal(res, True, 'check if received RA packet failed.')

    def test_05_shutdown_remote_x2(self):
        res = rm_ifacev4_api.disable_interface('x2')
        Assertion.assert_equal(res, True, "ERR: shutdown remote X2 failed")

    def test_06_check_if_receive_RA_packet(self):
        init_packet_capture()
        packets = pkt_api.export_captured_packets()
        logger.info(packets)
        res, packet = check_RA_packet(
            packets, 'X2', src_ip=CaseParams.rem_x2_linklocal, dst_ip='ff02::1')
        logger.info(packet)
        pkt_api.stop_capture()
        Assertion.assert_equal(
            res, False, 'check if received RA packet failed.')

    def test_07_check_if_generate_default_route_v6(self):
        rules = route_api.get_default_route_policy_v6()
        res = True
        try:
            for rule in rules:
                if rule['destination'] == '::/0' and rule['metric'] == 50:
                    if rule['gateway'] == CaseParams.rem_x2_linklocal:
                        logger.info(rule)
                        res = False
                        break
            else:
                logger.error('find the ipv6 default route that GW is the remote fw link local address')
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(res, False, "ERR: check generated default route v6 failed")

    def test_08_up_remote_x2(self):
        res = rm_ifacev4_api.enable_interface('x2')
        Assertion.assert_equal(res, True, "ERR: up remote X2 failed")


# Expect: show ipv6 settings correctly including IP, prefix
class TestV6If_TC01(Test):
    uuid = "SOSAIOT-TC-57201"
    description = show_testcase_info(TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_X1_to_static_mode(self):
        res = iface_v6_api.config_interface_ipv6(**x1v6_static_dict)
        Assertion.assert_equal(
            res, True, "ERR: Configure X1 IPv6 to static failed")

    def test_02_check_static_result(self):
        res = False
        x1_status = iface_v6_api.get_interface_address('x1')
        if (Parameter.X1_V6_IP and str(x1v6_static_dict['prefix_length'])) in x1_status['ip_address']:
            if x1_status['ip_mode'] == 'Static':
                res = True
        Assertion.assert_equal(res, True, "ERR: check static X1 result failed")

    def test_03_configure_x1_to_dhcpv6_mode(self):
        res = iface_v6_api.config_interface_ipv6(**x1_dhcpv6_dict)
        Assertion.assert_equal(
            res, True, "ERR: Configure X1 to dhcpv6 mode failed")

    def test_04_check_dhcpv6_result(self):
        res = False
        for i in range(3):
            ipv6_addr = get_interface_ipv6_addr('x1')
            if ipv6_addr:
                res = '2001:1:2:4' in ipv6_addr
                break
            iface_cli.click_dhcpv6_renew('X1')
            time.sleep(5)
        else:
            logger.error('x1 get dhcpv6 address failed!!')
        Assertion.assert_equal(
            res, True, "ERR: check X1 in dhcpv6 mode failed")


# Expect: verify "Disable all ipv6 traffic on interface" option
class TestV6If_TC10(Test):
    uuid = "SOSAIOT-TC-57202"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_disable_option(self):
        res = False
        x0_v6_dict.update({"ipv6_traffic": False})
        conf_res = iface_v6_api.config_interface_ipv6(**x0_v6_dict)
        if conf_res:
            output = localhost.send_command(f'ping6 -c 5 {Parameter.X0_V6_IP}')
            res = "100% packet loss" in output
        else:
            logger.error('disable ipv6 traffic option failed!')
        Assertion.assert_equal(
            res, True, "ERR: verify disable ipv6 traffic option failed")

    def test_02_verify_enable_option(self):
        res = False
        x0_v6_dict.update({"ipv6_traffic": True})
        conf_res = iface_v6_api.config_interface_ipv6(**x0_v6_dict)
        if conf_res:
            res = localhost.ping6(ip=Parameter.X0_V6_IP)
        else:
            logger.error('enable ipv6 traffic option failed!')
        Assertion.assert_equal(
            res, True, "ERR: verify enable ipv6 traffic option failed")


# Expect: verify "Enable Listening to RA" option
class TestV6If_TC11(Test):
    uuid = "SOSAIOT-TC-57203"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_packet_monitor(self):
        pkt_api.monitor_default()
        pkt_mon_dict = {
            'monitor_filter': {
                'ip_types': "ICMPv6",
                'interfaces': "x1"
            }
        }
        init_packet_capture()
        res = pkt_api.conf_packmon(**pkt_mon_dict)
        Assertion.assert_equal(res, True, "ERR: config packet monitor failed")

    def test_02_diable_RA_option(self):
        x1_dhcpv6_dict.update({'listen_router_advertisement': False})
        res = iface_v6_api.config_interface_ipv6(**x1_dhcpv6_dict)
        Assertion.assert_equal(res, True, "ERR: disable RA option failed")

    def test_03_verify_disable_listening_RA_option(self):
        init_packet_capture()
        packets = pkt_api.export_captured_packets()
        logger.info(packets)
        res, packet = check_RA_packet(packets, in_if='X1')
        logger.info(packet)
        Assertion.assert_equal(
            res, False, "ERR: verify disable RA option failed")

    def test_04_verify_enable_listening_RA_option(self):
        res = False
        init_packet_capture()
        x1_dhcpv6_dict.update({'listen_router_advertisement': True})
        iface_v6_api.config_interface_ipv6(**x1_dhcpv6_dict)
        for i in range(5):
            time.sleep(30)
            logger.info(f'check RA packet for the {i + 1} time')
            packets = pkt_api.export_captured_packets()
            logger.info(packets)
            res, packet = check_RA_packet(packets, in_if='X1')
            if res:
                logger.info(packet)
                break
        pkt_api.stop_capture()
        Assertion.assert_equal(res, True, "ERR: verify enable RA option failed")


# Expect: HTTPS management for interface including static, dhcpv6, auto mode
class TestV6If_TC25(Test):
    uuid = "SOSAIOT-TC-57208"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x1v6_to_dhcp_mode(self):
        TestV6If_TC01().test_03_configure_x1_to_dhcpv6_mode()

    def test_02_check_dhcpv6_result(self):
        TestV6If_TC01().test_04_check_dhcpv6_result()

    @repeat_method(3)
    def test_03_verify_https_dhcpv6_mode(self):
        rc = False
        x1_v6_addr = get_interface_ipv6_addr('x1')
        if x1_v6_addr:
            out = pc2_login.send_command(f'curl -k https://[{x1_v6_addr}]')
            rc = f'https://[{x1_v6_addr}]/sonicui/7/login/' in str(out)
        Assertion.assert_equal(rc, True, "ERR: verify dhcpv6 mode https management failed")

    def test_04_config_x1v6_to_auto_mode(self):
        x1_auto_dict = {
            'name': 'X1',
            'mode': 'auto',
            'zone': 'WAN',
            'mgmt_ping': True,
            'mgmt_https': True,
        }
        rc = iface_v6_api.config_interface_ipv6(**x1_auto_dict)
        Assertion.assert_equal(rc, True, "ERR: config x1 ipv6 interface to auto mode failed!")

    def test_05_check_x1_in_auto_mode_addr(self):
        res = False
        for i in range(5):
            time.sleep(10)
            ipv6_addr = get_interface_ipv6_addr('x1')
            if ipv6_addr:
                res = '2001:1:2:3' in ipv6_addr
                break
        else:
            logger.error('x1 get auto address failed!!')
        Assertion.assert_equal(
            res, True, "ERR: check X1 in auto mode failed")

    @repeat_method(3)
    def test_06_verify_https_in_auto_mode(self):
        rc = False
        x1_v6_addr = get_interface_ipv6_addr('x1')
        if x1_v6_addr:
            out = pc2_login.send_command(f'curl -k https://[{x1_v6_addr}]')
            rc = f'https://[{x1_v6_addr}]/sonicui/7/login/' in str(out)
        Assertion.assert_equal(rc, True, "ERR: verify auto mode https management failed")

    def test_07_config_x1v6_static_mode(self):
        TestV6If_TC01().test_01_configure_X1_to_static_mode()

    @repeat_method(3)
    def test_08_verify_https_static_mode(self):
        time.sleep(10)
        out = pc2_login.send_command(f'curl -k https://[{Parameter.X1_V6_IP}]')
        rc = f'https://[{Parameter.X1_V6_IP}]/sonicui/7/login/' in str(out)
        Assertion.assert_equal(rc, True, "ERR: verify static mode https management failed")


# Expect: Preference support for ipv6
class TestV6If_TC33(Test):
    uuid = "SOSAIOT-TC-57211"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_exp_file(self):
        logger.info('=> export exp file.')
        res = setting_api.export_setting_exp('/tmp/cyuan_ipv6_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_02_restore_fw(self):
        res = setting_api.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_03_import_exp_file(self):
        logger.info('=> import exp file.')
        res = setting_api.import_setting_exp(
            filepath='/tmp/cyuan_ipv6_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_04_check_config(self):
        logger.info('=> check settings.')
        x0_v6_addr = get_interface_ipv6_addr('x0')
        x1_v6_addr = get_interface_ipv6_addr('x1')
        res = x0_v6_addr == x0_v6_dict['ip'] and x1_v6_addr == Parameter.X1_V6_IP
        Assertion.assert_equal(
            res, True, "ERR: check imported settings failed")


# Expect: IP assignment as Static mode
class TestV6If_TC4(Test):
    uuid = "SOSAIOT-TC-57214"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_invalid_ipv6_address(self):
        logger.info('=> configure invalid v6 addr for x0.')
        invalid_x0_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': '2001:12',
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res, err_msg = iface_v6_api.config_interface_ipv6(**invalid_x0_dict, msg=True)
        rc = not res and 'invalid format' in json.dumps(err_msg)
        Assertion.assert_equal(rc, True, "ERR: verify invalid ipv6 address failed")

    def test_02_config_X2_V6(self):
        logger.info('=> configure X2 valid v6 addr/prefix/gw/dns.')
        x2_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X2_V6_IP,
            'prefix_length': Parameter.PREFIX_LEN,
            'dns': {'primary': Parameter.V6_DNS, 'secondary': '::', 'tertiary': '::'},
            'gateway': Parameter.REM_X2_V6_IP,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res = iface_v6_api.config_interface_ipv6(**x2_dict)
        Assertion.assert_equal(res, True, "ERR: configure X2 valid v6 addr/prefix/gw/dns failed")

    def test_03_verify_valid_x2(self):
        logger.info(
            '=> check settings including X2 valid v6 addr/prefix/gw/dns.')
        x2_v6_addr = get_interface_ipv6_addr('x2')
        x2_status = iface_v6_api.get_ipv6_interface_base('x2')
        res = x2_v6_addr == x2v6_static_dict['ip'] and Parameter.X2_V6_IP in str(
            x2_status) and Parameter.V6_DNS in str(x2_status)
        Assertion.assert_equal(res, True, "ERR: verify invalid ipv6 address failed")

    def test_04_verify_update_x0_ip(self):
        logger.info('=> update x0 settings.')
        res = False
        conf_res = iface_v6_api.config_interface_ipv6(**x0v6_update_dict)
        time.sleep(3)
        if conf_res:
            x0_ip = get_interface_ipv6_addr('x0')
            if x0_ip == x0v6_update_dict['ip']:
                res = True
        Assertion.assert_equal(res, True, "ERR: verify update x0 ipv6 address failed")

    def test_05_verify_related_ao(self):
        logger.info('=> check related address object')
        res = False
        resp = ao_api.get_addressobject_by_name(
            name='X0 IPv6 Primary Static Address', version='ipv6')
        try:
            resp_ip = resp['address_objects'][0]['ipv6']['host']['ip']
            if resp_ip == x0v6_update_dict['ip']:
                res = True
        except Exception as e:
            logger.error(e)
        Assertion.assert_equal(res, True, "ERR: verify related address object failed")


# Expect: IPV6 Address configuration on Advanced table
class TestV6If_TC9(Test):
    uuid = "SOSAIOT-TC-57220"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_extra_ipv6_addr(self):
        logger.info('=> add extra v6 addr for X0.')
        res = False
        conf_res = iface_v6_api.add_ipv6_extra_ip(**extra_dict)
        if conf_res:
            resp = iface_v6_api.get_ipv6_extra_ip()
            res = extra_dict['ip'] in str(resp) and str(extra_dict['prefix_length']) in str(resp)
        else:
            logger.error('add extra ipv6 address for X0 interface failed!')
        Assertion.assert_equal(res, True, "ERR: add additional static ipv6 address failed")

    def test_02_verify_Advertise_Subnet_Prefix_option(self):
        output = iface_v6_api.get_ipv6_prefixes()
        Assertion.assert_regular(
            str(output), '1000::', "ERR: verfiy Advertise Subnet Prefix Option failed")

    def test_03_delete_extra_ipv6_addr(self):
        res = False
        del_res = iface_v6_api.delete_ipv6_extra_ip(**extra_dict)
        logger.info('check if extra ip is deleted')
        if del_res:
            output = iface_v6_api.get_ipv6_extra_ip()
            res = extra_dict['ip'] not in output
        else:
            logger.error('delete extra ipv6 address failed!')
        Assertion.assert_equal(
            res, True, "ERR: delete additional static ipv6 address failed")

    def test_04_add_maximum_static_address(self):
        extra_dict = {
            'name': 'x0',
            'type': 'static',
            'ip': "",
            'prefix_length': 64
        }
        ip_addrs = ["3000::1", "4000::1", "4001::1", "4002::1",
                    "4006::1", "4003::1", "4004::1", "4005::1", "4007::1"]
        rc = False
        for ip_addr in ip_addrs:
            extra_dict.update({'ip': ip_addr})
            addres = iface_v6_api.add_ipv6_extra_ip(**extra_dict)
            if not addres:
                logger.error(f'add the {ip_addrs.index(ip_addr) + 1} ip_addr failed!')
                break
        else:
            extra_dict.update({'ip': '2008::1'})
            addres, err_msg = iface_v6_api.add_ipv6_extra_ip(**extra_dict, msg=True)
            logger.info(json.dumps(err_msg))
            rc = not addres and 'Reach maximum number of IPv6 static address for one interface' in json.dumps(err_msg)
        Assertion.assert_equal(rc, True, "ERR: add maximun extra ipv6 addr failed")


# HTTP Management for interface
class TestV6If_TC24(Test):
    uuid = "SOSAIOT-TC-57207"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_http_on_administration(self):
        rc = admin_api.conf_admin(**{"web_management": {"allow_http": True}})
        Assertion.assert_equal(rc, True, "ERR: enable http management on Administration page failed!")

    def test_02_enable_http_on_X0_v6(self):
        x0_v6_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_V6_IP,
            'prefix_length': 64,
            # 'mgmt_ping': True,
            'mgmt_http': True
        }
        rc = iface_v6_api.config_interface_ipv6(**x0_v6_opt)
        Assertion.assert_equal(rc, True, 'ERR: enable http management on ipv6 x0 interface failed!')

    def test_03_check_http_management(self):
        out = localhost.send_command(f'curl http://[{Parameter.X0_V6_IP}]')
        rc = f'http://[{Parameter.X0_V6_IP}]/sonicui/7/login/' in out
        Assertion.assert_equal(rc, True, 'ERR: check X0 interface http management failed!')


# Address object/Group support for Static Mode
class TestV6If_TC31(Test):
    uuid = "SOSAIOT-TC-57210"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_related_addr_obj(self):
        #     Xi IPv6 Link-Local Address / Xi IPv6 Primary Static Address / Xi IPv6 Primary Static Address Subnet.
        _, out1 = fw_cli.do_cli_commands(['show address-object ipv6 X0\ IPv6\ Link-Local\ Address'], tag=1)
        _, out2 = fw_cli.do_cli_commands(['show address-object ipv6 X0\ IPv6\ Primary\ Static\ Address'], tag=1)
        _, out3 = fw_cli.do_cli_commands(['show address-object ipv6 X0\ IPv6\ Primary\ Static\ Address\ Subnet'], tag=1)
        logger.info(out1)
        logger.info(out2)
        logger.info(out3)
        rc = 'host fe80::' in out1 and Parameter.X0_V6_IP in out2 and 'network 2000:: /64' in out3
        Assertion.assert_equal(rc, True,
                               'ERR: check related Link-Local Address, Primary Static Address, Primary Static Address Subnet failed')

    def test_02_check_related_addr_grp(self):
        # Firewalled IPv6 Subnets / Zone Interface IPv6 Addresses / Zone IPv6 Subnets / Xi IPv6 addresses / Xi Management IPv6 Addresses
        _, out1 = fw_cli.do_cli_commands(['show address-group ipv6 Firewalled\ IPv6\ Subnets'], tag=1)
        _, out2 = fw_cli.do_cli_commands(['show address-group ipv6 LAN\ IPv6\ Subnets'], tag=1)
        _, out3 = fw_cli.do_cli_commands(['show address-group ipv6 X1\ IPv6\ Addresses'], tag=1)
        _, out4 = fw_cli.do_cli_commands(['show address-group ipv6 X1\ Management\ IPv6\ Addresses'], tag=1)
        logger.info(out1)
        logger.info(out2)
        logger.info(out3)
        logger.info(out4)
        check1 = ("LAN IPv6 Subnets", "DMZ IPv6 Subnets", "WLAN IPv6 Subnets")
        check2 = ("X0 IPv6 Primary Dynamic Address Subnet", "X0 IPv6 Primary Static Address Subnet")
        check3 = ("X1 IPv6 Primary Dynamic Address", "X1 IPv6 Primary Static Address", "X1 IPv6 Link-Local Address")
        check4 = ("X1 IPv6 Primary Dynamic Address", "X1 IPv6 Primary Static Address", "X1 IPv6 Link-Local Address")
        rc = all([all(x in out1 for x in check1), all(x in out2 for x in check2), all(x in out3 for x in check3),
                  all(x in out4 for x in check4)])
        Assertion.assert_equal(rc, True, 'ERR: check related address group failed')


# no errors with https management when managed IP is a temporary IPV6 address
class TestV6If_TC41(Test):
    uuid = "SOSAIOT-TC-57215"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x0_temporary_ipv6_addr(self):
        x0_v6_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': generate_temporary_ipv6_addr('x0'),
            'prefix_length': 64,
            'mgmt_https': True,
            'mgmt_http': False,
            'mgmt_ping': True,
        }
        rc = iface_v6_api.config_interface_ipv6(**x0_v6_opt)
        Assertion.assert_equal(rc, True, "ERR: config X0 temporary ipv6 addr failed!")

    def test_02_check_https_management(self):
        localhost.send_command('ip -6 r add 2000::/64 dev eth1')
        ip = generate_temporary_ipv6_addr('X0')
        out = localhost.send_command(f'curl -k https://[{ip}]')
        logger.info(out)
        rc = 'This page is redirecting!' in str(out)
        Assertion.assert_equal(rc, True, "ERR: verify https management failed!")


# Check IPv6 Link-Local Address after disable/enable IPv6
class TestV6If_1533076(Test):
    uuid = "SOSAIOT-TC-57221"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_ipv6_in_admin_page(self):
        rc = admin_api.conf_admin(**{"ipv6": False})
        Assertion.assert_equal(rc, True, "ERR: diable ipv6 on Administration page failed!")

    def test_02_check_traffic(self):
        out = localhost.send_command(f'ping6 -c 5 {generate_temporary_ipv6_addr("x0")}')
        Assertion.assert_regular(out, '100% packet loss', 'ERR: check traffic failed!')

    def test_03_restore_DUT(self):
        res = setting_api.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_04_check_ipv6_stat_in_admin_page(self):
        out = admin_api.show_admin_setting()
        Assertion.assert_regular(json.dumps(out), '"ipv6": true',
                                 "ERR: check ipv6 stat in admin page after restore failed!")

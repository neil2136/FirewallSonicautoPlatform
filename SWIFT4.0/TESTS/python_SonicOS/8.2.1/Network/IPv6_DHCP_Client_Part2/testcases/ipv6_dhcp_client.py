from definition.settings import *
from definition.utils import *


# Expect:WAN interface--DHCP v6 Mode as Automatic, (don't) click 'Enable Listening to Router Advertisement'
class Test_IPv6_Client_TC3(Test):
    uuid = "SOSAIOT-TC-56433"
    description = show_testcase_info(TESTPLAN, '1512445', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512445')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_RA(self):
        x1_dict = copy.deepcopy(x1_v6_dict)
        x1_dict['dhcpv6'] = {"mode": "auto"}
        rc, err_msg = if_v6_api.config_interface_ipv6(**x1_dict, msg=True)
        logger.info(err_msg)
        if not rc:
            res = 'Listening to router advertisement option must be enabled when DHCPv6 is in automatic mode' in str(err_msg)
        Assertion.assert_equal(res, True, 'ERR: verify disable RA when x1 ipv6 is auto mode failed.')



# Expect: WAN interface--DHCPv6 Mode as manual, Only Request Stateless Information
class Test_IPv6_Client_TC6(Test):
    uuid = "SOSAIOT-TC-56446"
    description = show_testcase_info(TESTPLAN, '1512464', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512464')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_config_x1(self):
        if_v6_cli.click_dhcpv6_release('x1')
        x1_dict = copy.deepcopy(x1_v6_dict)
        x1_dict["dhcpv6"]["info_only"] = True
        rc = if_v6_api.config_interface_ipv6(**x1_dict)
        Assertion.assert_equal(rc, True, 'set x1 to dhcpv6 mode failed.')

    def test_02_check_ipv6_x1_status(self):
        if_v6_cli.click_dhcpv6_renew('x1')
        sleep(3)
        resp = if_v6_api.get_interface_address('x1')
        resp = json.dumps(resp)
        rc = '"primary_dns": "2000::ff"' in resp and f'{Parameter.V6_Prefix_1}' not in resp
        Assertion.assert_equal(bool(rc), True, 'ERR: check interface x1 ipv6 status failed!')


# Expect:WAN interface--DHCPv6 Mode as manual, Don't Click 'Only Request Stateless Information'
class Test_IPv6_Client_TC7(Test):
    uuid = "SOSAIOT-TC-56447"
    description = show_testcase_info(TESTPLAN, '1512465', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512465')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_config_x1(self):
        rc = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc, True, 'set x1 to dhcpv6 mode failed.')

    def test_02_check_ipv6_x1_status(self):
        rc = get_v6_addr('x1')
        Assertion.assert_equal(bool(rc), True, 'ERR: interface x1 get v6 addr failed!')


# Expect:WAN interface--DHCP v6 Mode as manual, (Don't) click Enable Listening to Router Advertisement
class Test_IPv6_Client_TC8(Test):
    uuid = "SOSAIOT-TC-56448"
    description = show_testcase_info(TESTPLAN, '1512466', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512466')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_ipv6_x1_status(self):
        resp = if_v6_api.get_interface_address('x1')
        resp = json.dumps(resp)
        rc = '"primary_dns": "2000::ff"' in resp and f'{Parameter.V6_Prefix_1}' in resp
        Assertion.assert_equal(rc, True, 'ERR: check ipv6 x1 status failed!')


# Expect: WAN interface-DHCP v6 Mode as manual, Rapid commit
class Test_IPv6_Client_TC9(Test):
    uuid = "SOSAIOT-TC-56449"
    description = show_testcase_info(TESTPLAN, '1512467', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512467')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_rapid_option_in_packet(self):
        rc = False
        pkt_list = capture_packets_from_fw()
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Solicit':
                if 'out:X1*' in pkt:
                    logger.info(pkt)
                    rc = 'Option: Rapid Commit' in pkt
                    break
        else:
            logger.error('not found the Solicit packet')

        Assertion.assert_equal(rc, True, 'ERR: check ia addr in Solicit packet failed!')


# Expect: Verify TSR
class Test_IPv6_Client_TC40(Test):
    uuid = "SOSAIOT-TC-56442"
    description = show_testcase_info(TESTPLAN, '1512457', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512457')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_tsr_info(self):
        rc = False
        down_rc = diag_api.download_tsr()
        logger.info(f'download tsr file result: {down_rc}')
        t1 = pc1_login.send_command("cat /tmp/techSupport | grep -n '#Network : Interfaces_START'")
        t2 = pc1_login.send_command("cat /tmp/techSupport | grep -n '#Network : Interfaces_END'")
        try:
            n1 = re.search(r'(\d+)', t1)
            n2 = re.search(r'(\d+)', t2)
            n = int(n2.group(1)) - int(n1.group(1))
            tsr_info = pc1_login.send_command(f"cat /tmp/techSupport | head -{n2.group(1)} | tail -{n}")
            x1_match = re.search(r'Interface Name\s+: X1(.*)\nInterface Name\s+: X2', tsr_info, re.S)
            if x1_match:
                x1_settings = x1_match.group(1)
                logger.info(x1_settings)
                rc = Parameter.V6_Prefix_1 in x1_settings
            else:
                logger.error('got interface x1 part failed!')
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(rc, True, "ERR: verify tsr info failed")


# Expect:Plug out/in the cable of DHCP client
class Test_IPv6_Client_TC41(Test):
    uuid = "SOSAIOT-TC-56443"
    description = show_testcase_info(TESTPLAN, '1512458', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512458')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_plug_out_in_x1(self):
        dis_rc = if_v4_api.disable_interface('x1')
        logger.info(f'disable interface result: {dis_rc}')
        sleep(30)
        en_rc = if_v4_api.enable_interface('x1')
        logger.info(f'enable interface result: {en_rc}')
        rc = get_v6_addr('x1')
        Assertion.assert_equal(bool(rc), True, 'ERR: X1 obtain ipv6 addr failed after plug out')


# Expect:Disable one DHCPv6 client will not take any effect to other DHCPv6 clients.
class Test_IPv6_Client_TC44(Test):
    uuid = "SOSAIOT-TC-56444"
    description = show_testcase_info(TESTPLAN, '1512461', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512461')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_set_x2_to_dhcpv6_mode(self):
        res = if_v6_api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(res, True, 'set x2 to dhcpv6 mode failed.')

    def test_02_check_x2_v6_addr(self):
        rc = get_v6_addr('x2')
        Assertion.assert_equal(bool(rc), True, 'ERR: interface x2 get v6 addr failed!')

    def test_03_disable_x1(self):
        rc = if_v4_api.disable_interface('x1')
        Assertion.assert_equal(rc, True, "ERR: disconnect x1 failed!")

    def test_04_check_no_solicit_packet_from_x1(self):
        pkt_list = capture_packets_from_fw(renewd=False)
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Solicit':
                logger.info(pkt)
                if 'out:X1*' in pkt:
                    logger.error('find Solicit packet sent from X1')
                    rc = False
                    break
        else:
            logger.info('not found the Solicit packet')
            rc = True
        Assertion.assert_equal(rc, True, 'ERR: check ia addr in Solicit packet failed.')

    def test_05_enable_x1(self):
        rc = if_v4_api.enable_interface('x1')
        Assertion.assert_equal(rc, True, "ERR: enable x1 failed!")


# Expect: WAN interface---Send hints for renewing previous IP on startup
class Test_IPv6_Client_TC10(Test):
    uuid = "SOSAIOT-TC-56413"
    description = show_testcase_info(TESTPLAN, '1512424', description=True)['title']
    x1_v6_addr = ''

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512424')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_x1_v6_addr(self):
        self.x1_v6_addr = get_v6_addr('x1')
        Assertion.assert_equal(bool(self.x1_v6_addr), True, 'ERR: interface x1 get v6 addr failed!')

    def test_02_restart_fw(self):
        init_packet_capture()
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: restart FW via GUI failed!')

    def test_03_check_IA_addr_in_packet_after_restart(self):
        rc = False
        pkt_list = capture_packets_from_fw(renewd=False, init=False)
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Advertise':
                logger.info(pkt)
                rc = f'IPv6 address: {self.x1_v6_addr}' in pkt
                break
        else:
            logger.error('not found the Advertise packet')

        Assertion.assert_equal(rc, True, 'ERR: check ia addr in Advertise packet failed.')


# Expect: LAN/DMZ/Customer zone ---Send hints for renewing previous IP on startup
class Test_IPv6_Client_TC22(Test):
    uuid = "SOSAIOT-TC-56426"
    description = show_testcase_info(TESTPLAN, '1512437', description=True)['title']
    x2_v6_addr = ''

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512437')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_x2_v6_addr(self):
        self.x2_v6_addr = get_v6_addr('x2')
        Assertion.assert_equal(bool(self.x2_v6_addr), True, 'ERR: interface x1 get v6 addr failed!')

    def test_02_restart_fw(self):
        init_packet_capture()
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: restart FW via GUI failed!')

    def test_03_check_IA_addr_in_packet_after_restart(self):
        rc = False
        pkt_list = capture_packets_from_fw(renewd=False, init=False)
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Advertise':
                logger.info(pkt)
                rc = f'IPv6 address: {self.x2_v6_addr}' in pkt
                break
        else:
            logger.error('not found the Advertise packet')

        Assertion.assert_equal(rc, True, 'ERR: check ia addr in Advertise packet failed.')


# Expect:  LAN/DMZ/Customer zone --DHCPv6 Mode as manual, Only Request Stateless Information
class Test_IPv6_Client_TC18(Test):
    uuid = "SOSAIOT-TC-56421"
    description = show_testcase_info(TESTPLAN, '1512432', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512432')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_edit_ipv6_x2(self):
        if_v6_cli.click_dhcpv6_release('x2')
        sleep(3)
        x2_dict = copy.deepcopy(x2_v6_dict)
        x2_dict['dhcpv6']["info_only"] = True
        res = if_v6_api.config_interface_ipv6(**x2_dict)
        Assertion.assert_equal(res, True, 'set x1 to dhcpv6 mode failed.')

    def test_02_check_ipv6_x2_status(self):
        if_v6_cli.click_dhcpv6_renew('x2')
        sleep(3)
        resp = if_v6_api.get_interface_address('x2')
        resp = json.dumps(resp)
        rc = '"primary_dns": "2000::ff"' in resp and f'{Parameter.V6_Prefix_2}' not in resp
        Assertion.assert_equal(rc, True, 'ERR: check ipv6 x1 status failed!')


# Expect:LAN/DMZ/Customer zone --DHCPv6 Mode as manual, Don't Click 'Only Request Stateless Information'
class Test_IPv6_Client_TC19(Test):
    uuid = "SOSAIOT-TC-56422"
    description = show_testcase_info(TESTPLAN, '1512433', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512433')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_edit_ipv6_x2(self):
        if_v6_cli.click_dhcpv6_release('x2')
        sleep(3)
        res = if_v6_api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(res, True, 'set x2 to dhcpv6 mode failed.')

    def test_02_check_ipv6_x2_status(self):
        if_v6_cli.click_dhcpv6_renew('x2')
        sleep(3)
        resp = if_v6_api.get_interface_address('x2')
        resp = json.dumps(resp)
        rc = '"primary_dns": "2000::ff"' in resp and f'{Parameter.V6_Prefix_2}' in resp
        Assertion.assert_equal(rc, True, 'ERR: check ipv6 x1 status failed!')


# Expect:LAN/DMZ/Customer zone --DHCP v6 Mode as manual, (Don't) click Enable Listening to Router Advertisement
class Test_IPv6_Client_TC20(Test):
    uuid = "SOSAIOT-TC-56424"
    description = show_testcase_info(TESTPLAN, '1512435', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512435')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_check_ipv6_x2_status(self):
        Test_IPv6_Client_TC19().test_02_check_ipv6_x2_status()



# Expect: LAN/DMZ/Customer zone ---DHCP v6 Mode as manual, Rapid commit
class Test_IPv6_Client_TC21(Test):
    uuid = "SOSAIOT-TC-56425"
    description = show_testcase_info(TESTPLAN, '1512436', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512436')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_rapid_option_in_packet(self):
        rc = False
        pkt_list = capture_packets_from_fw()
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Solicit':
                if 'out:X1*' in pkt:
                    logger.info(pkt)
                    rc = 'Option: Rapid Commit' in pkt
                    break
        else:
            logger.error('not found the Solicit packet')
        Assertion.assert_equal(rc, True, 'ERR: check Rapid Commit addr in Solicit packet failed.')


# Expect:DNS info
class Test_IPv6_Client_TC24(Test):
    uuid = "SOSAIOT-TC-56427"
    description = show_testcase_info(TESTPLAN, '1512439', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512439')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_x2_dns_info(self):
        resp = if_v6_api.get_interface_address('x1')
        Assertion.assert_regular(json.dumps(resp), '"primary_dns": "2000::ff"', 'ERR: check dns info failed!')


# Expect: Lease time info
class Test_IPv6_Client_TC25(Test):
    uuid = "SOSAIOT-TC-56428"
    description = show_testcase_info(TESTPLAN, '1512440', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512440')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_lease_time(self):
        rc = False
        pkt_list = capture_packets_from_fw(iface='x2')
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Advertise':
                logger.info(pkt)
                rc = 'T1: 50' in pkt and 'T2: 80' in pkt
                break
        else:
            logger.error('not found the Advertise packet')
        Assertion.assert_equal(rc, True, 'ERR: check lease time info failed.')


# Expect: Disable all IPv6 Traffic on the Interface
class Test_IPv6_Client_TC26(Test):
    uuid = "SOSAIOT-TC-56429"
    description = show_testcase_info(TESTPLAN, '1512441', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512441')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_ipv6_all_option(self):
        x2_dict = copy.deepcopy(x2_v6_dict)
        x2_dict['ipv6_traffic'] = False
        res = if_v6_api.config_interface_ipv6(**x2_dict)
        Assertion.assert_equal(res, True, 'ERR: disable ipv6 all option failed.')

    def test_02_check_can_not_obtain_v6_addr(self):
        click_dhcp_release_renew('x2')
        resp = if_v6_api.get_interface_address('x2')
        resp = json.dumps(resp)
        rc = '"primary_dns": "2000::ff"' not in resp and f'{Parameter.V6_Prefix_2}' not in resp
        Assertion.assert_equal(rc, True, 'ERR: check ipv6 x2 status failed!')

    def test_03_enable_ipv6_all_option(self):
        x2_dict = copy.deepcopy(x2_v6_dict)
        x2_dict['ipv6_traffic'] = True
        res = if_v6_api.config_interface_ipv6(**x2_dict)
        Assertion.assert_equal(res, True, 'ERR: enable ipv6 all option failed.')


# Expect:  DHCP client renews lease when current time reached
class Test_IPv6_Client_TC31(Test):
    uuid = "SOSAIOT-TC-56434"
    description = show_testcase_info(TESTPLAN, '1512447', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512447')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_lifetime_in_packet(self):
        rc = False
        pkt_list = capture_packets_from_fw(renewd=False)
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Reply':
                logger.info(pkt)
                rc = 'T1: 50' in pkt and 'T2: 80' in pkt
                break
        else:
            logger.error('not found the Reply packet')
        Assertion.assert_equal(rc, True, 'ERR: check lifetime in Reply packet failed.')


# Expect:DHCP client rebind lease when current time reached.
class Test_IPv6_Client_TC32(Test):
    uuid = "SOSAIOT-TC-56435"
    description = show_testcase_info(TESTPLAN, '1512448', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512448')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_lifetime_in_packet(self):
        rc = False
        init_packet_capture()
        dis_rc = if_v4_api.disable_interface('x1')
        logger.info(f'disable interface result: {dis_rc}')
        sleep(30)
        en_rc = if_v4_api.enable_interface('x1')
        logger.info(f'enable interface result: {en_rc}')

        pkt_list = capture_packets_from_fw(init=False, renewd=False)
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Reply':
                logger.info(pkt)
                rc = 'T1: 50' in pkt and 'T2: 80' in pkt
                break
        else:
            logger.error('not found the Reply packet')
        Assertion.assert_equal(rc, True, 'ERR: check lifetime in Renew packet failed.')


# Expect:Exchanging between static mode and DHCP mode
class Test_IPv6_Client_TC33(Test):
    uuid = "SOSAIOT-TC-56436"
    description = show_testcase_info(TESTPLAN, '1512449', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512449')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_update_x1_v6_to_static_mode(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': "2001::168",
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X1 IPv6 from dhcpv6 mode to static failed")

    def test_02_update_x1_v6_to_dhcpv6_mode(self):
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: update x1 ipv6 interface from static mode to dhcpv6 mode failed.')


# Expect:Exchanging between auto mode and DHCP mode
class Test_IPv6_Client_TC34(Test):
    uuid = "SOSAIOT-TC-56437"
    description = show_testcase_info(TESTPLAN, '1512450', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512450')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_upadte_x1_v6_to_auto_mode(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'auto',
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: update x1 ipv6 interface from dhcpv6 mode to auto mode failed.')

    def test_02_update_x1_v6_to_dhcpv6_mode(self):
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: update x1 ipv6 interface from auto mode to dhcpv6 mode failed.')


# Expect: Restart the firewall, the configuration are saved
class Test_IPv6_Client_TC38(Test):
    uuid = "SOSAIOT-TC-56439"
    description = show_testcase_info(TESTPLAN, '1512454', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512454')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_restart_firewall(self):
        res = restart_api.restart_now()
        Assertion.assert_equal(res, True, "ERR: restart unit failed")

    def test_02_check_settings(self):
        resp_x1 = if_v6_api.get_interface_address('x1')
        resp_x2 = if_v6_api.get_interface_address('x2')
        resp_x1 = json.dumps(resp_x1)
        resp_x2 = json.dumps(resp_x2)
        check_x1 = ['"ip_mode": "DHCPv6"', '"primary_dns": "2000::ff"', Parameter.V6_Prefix_1]
        check_x2 = ['"ip_mode": "DHCPv6"', '"primary_dns": "2000::ff"', Parameter.V6_Prefix_2]
        rc_x1 = all(x in resp_x1 for x in check_x1)
        rc_x2 = all(x in resp_x2 for x in check_x2)
        Assertion.assert_equal(rc_x1 & rc_x2, True, 'ERR: check settings after restart failed!')


# Expect: Export/import Exp file
class Test_IPv6_Client_TC39(Test):
    uuid = "SOSAIOT-TC-56440"
    description = show_testcase_info(TESTPLAN, '1512455', description=True)['title']
    jira = 'GEN7-48491'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512455')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_export_exp_file(self):
        logger.info('=> export exp file.')
        res = settings_api.export_setting_exp('/tmp/cyuan_ipv6_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_02_init_ipv6_settings(self):
        x1_dict = {
            'name': "x1",
            'mode': "static",
            'zone': "WAN",
        }
        x2_dict = {
            'name': "x2",
            'mode': "static",
            'zone': "LAN",
        }
        res_x1 = if_v6_api.config_interface_ipv6(**x1_dict)
        logger.info(f'reset ipv6 x1 result: {res_x1}')
        res_x2 = if_v6_api.config_interface_ipv6(**x2_dict)
        logger.info(f'reset ipv6 x1 result: {res_x2}')
        Assertion.assert_equal(res_x1 & res_x2, True, 'ERR: update x2 v6 failed')

    def test_03_import_exp_file(self):
        logger.info('=> import exp file.')
        res = settings_api.import_setting_exp(
            filepath='/tmp/cyuan_ipv6_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_04_check_config(self):
        Test_IPv6_Client_TC38().test_02_check_settings()

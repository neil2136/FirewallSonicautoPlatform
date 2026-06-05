from definition.utils import *


#  GUI-Current DHCPv6 relay lease displayed and shows correct info
class Test_DHCPv6_Relay_TC1514142(Test):
    uuid = "SOSAIOT-TC-56283"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_x2_client_get_dhcpv6_lease(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        pc3_login.send_command('killall dhclient')
        out = pc3_login.send_command('dhclient -6 -v eth1')
        time.sleep(10)
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
        rc = 'IAADDR 2001:1:2:3::' in out and 'Bound to lease' in out
        Assertion.assert_equal(rc, True, 'ERR: x2 client get dhcpvv6 lease failed!!!')

    def test_02_check_v6_lease_in_dhcpv6_relay_lease_table(self):
        out = ip_helper_api.get_dhcpv6_relay_lease()
        logger.info(json.dumps(out))
        rc = "2001:1:2:4::" in out[0].get("server_s_ip_address") if out else False
        Assertion.assert_equal(rc, True, 'ERR: check v6 lease in dhcpv6 relay lease table failed!!')


# Relay-forward Solicit message
class Test_DHCPv6_Relay_TC1514143(Test):
    uuid = "SOSAIOT-TC-56284"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_relay_forward_solicit_pkt(self):
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::168" in pkt and "Dst: 2001:1:2:4::169" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-forw', dhcpv6_type='Solicit', pkt=pkt)
                if rc:
                    logger.info(f'find the relay forward solicit packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay forward solicit packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay forward solicit packet failed!!!')


#  relay-reply Advertise message
class Test_DHCPv6_Relay_TC1514144(Test):
    uuid = "SOSAIOT-TC-56285"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_relay_reply_advertise_pkt(self):
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Advertise', pkt=pkt)
                if rc:
                    logger.info(f'find the relay-reply Advertise packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay reply advertise packet!!!')
        Assertion.assert_equal(rc, True, "ERR: check the relay reply Avertise packet failed!!!")


# Relay-forward Request message
class Test_DHCPv6_Relay_TC1514146(Test):
    uuid = "SOSAIOT-TC-56286"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_relay_forward_request_pkt(self):
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::168" in pkt and "Dst: 2001:1:2:4::169" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-forw', dhcpv6_type='Request', pkt=pkt)
                if rc:
                    logger.info(f'find the relay forward request packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay forward request packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay forward request packet failed!!!')


# relay-reply Reply message
class Test_DHCPv6_Relay_TC1514147(Test):
    uuid = "SOSAIOT-TC-56287"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_relay_forward_request_pkt(self):
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Reply', pkt=pkt)
                if rc:
                    logger.info(f'find the relay-reply reply packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay-reply reply packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay-reply reply packet failed!!!')


# Relay-forward Confirm message
class Test_DHCPv6_Relay_TC1514149(Test):
    uuid = "SOSAIOT-TC-56288"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_relay_forward_confirm_pkt(self):
        pc3_login.send_command('killall dhclient')
        pkt_api.clear_packets()
        pkt_api.start_capture()
        pc3_login.send_command('dhclient -6 -v eth1')
        time.sleep(10)
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng("/tmp/packet-c.pcapng_2")
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_2 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::168" in pkt and "Dst: 2001:1:2:4::169" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-forw', dhcpv6_type='Confirm', pkt=pkt)
                if rc:
                    logger.info(f'find the relay-forward Confirm packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay-forward Confirm packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay-forward Confirm packet failed!!!')


# Relay-reply reply message of Confirm message
class Test_DHCPv6_Relay_TC1514150(Test):
    uuid = "SOSAIOT-TC-56289"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_relay_reply_confirm_pkt(self):
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_2 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Reply', pkt=pkt)
                if rc:
                    logger.info(f'find the Relay-reply Reply packet:\n{pkt}')
                    break
        else:
            logger.error('not found the Relay-reply Reply packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check Relay-reply Reply packet failed!!!')


# Relay-forward Renew message
class Test_DHCPv6_Relay_TC1514151(Test):
    uuid = "SOSAIOT-TC-56290"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_relay_forward_renew_pkt(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        time.sleep(150)
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng("/tmp/packet-c.pcapng_3")
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_3 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::168" in pkt and "Dst: 2001:1:2:4::169" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-forw', dhcpv6_type='Renew', pkt=pkt)
                if rc:
                    logger.info(f'find the relay-forward Renew packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay-forward Renew packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay-forward Renew packet failed!!!')


#  Relay-reply reply message of Renew message
class Test_DHCPv6_Relay_TC1514152(Test):
    uuid = "SOSAIOT-TC-56291"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_relay_forward_reply_pkt(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_3 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Reply', pkt=pkt)
                if rc:
                    logger.info(f'find the Relay-reply Reply packet:\n{pkt}')
                    break
        else:
            logger.error('not found the Relay-reply Reply packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check Relay-reply Reply packet failed!!!')


# DNS Recursive Name Server option
class Test_DHCPv6_Relay_TC1514160(Test):
    uuid = "SOSAIOT-TC-56297"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dns_recursive_name_server_option_in_pkt(self):
        logger.info('check this option in relay_reply packet')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_3 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                res = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Reply', pkt=pkt)
                if res:
                    logger.info(f'find the Relay-reply Reply packet:\n{pkt}')
                    if 'Option: DNS recursive name server' in pkt and 'DNS server address: 100::1' in pkt:
                        logger.info('find the DNS Recursive Name Server option')
                        rc = True
                    else:
                        logger.info('not found the DNS Recursive Name Server option')
                        rc = False
                    break
        else:
            logger.error('not found the Relay-reply Reply packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check Relay-reply Reply packet failed!!!')


# DNS Domain Search List option
class Test_DHCPv6_Relay_TC1514161(Test):
    uuid = "SOSAIOT-TC-56298"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dns_domain_search_list_option_in_pkt(self):
        logger.info('check this option in relay_reply packet')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_3 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                res = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Reply', pkt=pkt)
                if res:
                    logger.info(f'find the Relay-reply Reply packet:\n{pkt}')
                    if 'Option: Domain Search List' in pkt and 'Domain: test.com' in pkt:
                        logger.info('find the DNS Recursive Name Server option')
                        rc = True
                    else:
                        logger.info('not found the DNS Recursive Name Server option')
                        rc = False
                    break
        else:
            logger.error('not found the Relay-reply Reply packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check Relay-reply Reply packet failed!!!')


# Relay-forward Rebind message
class Test_DHCPv6_Relay_TC1514153(Test):
    uuid = "SOSAIOT-TC-56292"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(10)
    def test_01_check_relay_forward_rebind_pkt(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        time.sleep(30)
        # disable server scope
        rc1 = rem_fw_cli.do_cli_commands(
            commands=['configure', 'dhcp-server ipv6', 'scope dynamic for_relay_x2', 'no enable', 'commit', 'end',
                      'exit'])
        logger.info(f'disable server scope result: {rc1}')
        time.sleep(45)
        # enable server scope
        rc2 = rem_fw_cli.do_cli_commands(
            commands=['configure', 'dhcp-server ipv6', 'scope dynamic for_relay_x2', 'enable', 'commit', 'end',
                      'exit'])
        logger.info(f'enable server scope result: {rc2}')
        time.sleep(45)
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng_4')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_4 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::168" in pkt and "Dst: 2001:1:2:4::169" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-forw', dhcpv6_type='Rebind', pkt=pkt)
                if rc:
                    logger.info(f'find the relay-forward Rebind packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay-reply Rebind packet!!')
        Assertion.assert_equal(True, True, 'ERR: check relay-reply Rebind packet failed!!!')


# Relay-reply reply message of Rebind message
class Test_DHCPv6_Relay_TC1514154(Test):
    uuid = "SOSAIOT-TC-56293"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_relay_reply_reply_pkt(self):
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_4 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Reply', pkt=pkt)
                if rc:
                    logger.info(f'find the relay-reply Reply packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay-reply Reply packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay-reply Reply packet failed!!!')


# Relay-forward Release message
class Test_DHCPv6_Relay_TC1514155(Test):
    uuid = "SOSAIOT-TC-56294"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_relay_forward_release_pkt(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        pc3_login.send_command('killall dhclient')
        pc3_login.send_command('dhclient -6 -r eth1')
        time.sleep(3)
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng_5')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_5 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::168" in pkt and "Dst: 2001:1:2:4::169" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-forw', dhcpv6_type='Release', pkt=pkt)
                if rc:
                    logger.info(f'find the relay-forward Release packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay-forward Release packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay-forward Release packet failed!!!')


# Relay-reply reply message of Release message
class Test_DHCPv6_Relay_TC1514156(Test):
    uuid = "SOSAIOT-TC-56295"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_relay_reply_reply(self):
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_5 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                rc = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Reply', pkt=pkt)
                if rc:
                    logger.info(f'find the relay-reply Reply packet:\n{pkt}')
                    break
        else:
            logger.error('not found the relay-reply Reply packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay-reply Reply packet failed!!!')


#  Relay a message from a client
class Test_DHCPv6_Relay_TC1514169(Test):
    uuid = "SOSAIOT-TC-56299"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_relay_message_from_client(self):
        Test_DHCPv6_Relay_TC1514143().test_01_check_relay_forward_solicit_pkt()


# Preference export/import
class Test_DHCPv6_Relay_TC1514182(Test):
    uuid = "SOSAIOT-TC-56300"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_exp_file(self):
        res = settings_api.export_setting_exp('/tmp/cyuan_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_02_restore_fw(self):
        res = settings_api.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_03_import_exp_file(self):
        logger.info('=> import exp file.')
        res = settings_api.import_setting_exp(
            filepath='/tmp/cyuan_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_04_check_config(self):
        out1 = ip_helper_api.get_iphelper_settings()
        logger.info(json.dumps(out1))
        rc1 = '"enable": true' in json.dumps(out1)
        out2 = ip_helper_api.get_protocol(protocol='DHCPv6')
        logger.info(json.dumps(out2))
        rc2 = '"enable": true' in json.dumps(out2)
        out3 = ip_helper_api.get_policy()
        logger.info(json.dumps(out3))
        rc3 = '"protocol": "DHCPv6"' in json.dumps(out3)
        out4 = ip_helper_api.get_dhcpv6_relay_lease()
        if not out4:
            pc3_login.send_command('killall dhclient')
            pc3_login.send_command('dhclient -6 -v eth1')
            out4 = ip_helper_api.get_dhcpv6_relay_lease()
        logger.info(json.dumps(out4))
        rc4 = bool(re.search(r'server_s_ip_address.*2001:1:2:4::', str(out4)))
        logger.info(f'rc4 result: {rc4}')
        Assertion.assert_equal(rc1 & rc2 & rc3 & rc4, True, 'ERR: check config after restore failed!!')


# Check TSR info
class Test_DHCPv6_Relay_TC1514184(Test):
    uuid = "SOSAIOT-TC-56301"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_settings_in_tsr(self):
        tsr_info = diag_api.get_tsr_part(func='Network', lab1='IP Helper')
        logger.info(tsr_info)
        rc1 = 'IP Helper is ON' in tsr_info
        m1 = re.search(r'Relay Policy-+\n(.*)-+DHCP Relay Lease Table', tsr_info, re.S)
        rc2 = 'Interface X2' in m1.group(1) and '2001:1:2:4::169' in m1.group(1) if m1 else False
        m2 = re.search(r'-+DHCPv6 Relay Lease Table-+\n(.*)\n', tsr_info, re.S)
        rc3 = '2001:1:2:3::' in m2.group(1) if m2 else False
        Assertion.assert_equal(rc1 & rc2 & rc3, True, 'ERR: check settings in tsr info failed!!')


# Replay-reply reply with code: nobinding(3)
class Test_DHCPv6_Relay_TC1514157(Test):
    uuid = "SOSAIOT-TC-56296"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_server_scope(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        dynamic_scope = {
            "name": "for_relay_x2",
            "range": {
                "from": "2001:1:2:3::100",
                "to": "2001:1:2:3::100"
            },
            "enable": True,
            "prefix": "2001:1:2:3::",
            "lifetime": {
                "valid": 2,
                "preferred": 1
            },
            "comment": "",
            "domain_name": "test.com",
            "dns": {
                "server":
                    {"static":
                        {
                            "primary": "100::1",
                            "secondary": "::",
                            "tertiary": "::"
                        }
                    }
            },
            "generic_option": {},
            "always_send_option": False
        }
        res = rem_dhcpv6_api.edit_dhcp_server_scope_v6(scope='dynamic', name="for_relay_x2",
                                                       **{"dhcp_server": {
                                                           "ipv6": {"scope": {"dynamic": [dynamic_scope]}}}})
        Assertion.assert_equal(res, True, 'ERR: update dynamic dhcpv6 scope on server failed!!!')

    @repeat_method(3)
    def test_02_check_relay_reply_reply_with_nobinding_code(self):
        pc1_login.send_command('rm -rf /tmp/packet-c.pcapng_6')
        rc = False
        logger.info('check this option in relay reply packet')
        time.sleep(60)
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng_6')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng_6 -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if "Src: 2001:1:2:4::169" in pkt and "Dst: 2001:1:2:4::168" in pkt:
                res = check_specified_dhcpv6_packet(pkt_type='Relay-reply', dhcpv6_type='Reply', pkt=pkt)
                if res:
                    logger.info(f'find the relay-reply Reply packet:\n{pkt}')
                    if 'Status Code: NoBinding (3)' in pkt:
                        logger.info(f'find the Nobinding status code')
                        rc = True
                        break
                    else:
                        logger.error('not found the Nobinding status code')
                        continue
        else:
            logger.error('not found the relay-reply Reply packet!!')
        Assertion.assert_equal(rc, True, 'ERR: check relay-reply Reply packet failed!!!')
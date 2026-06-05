from definition.utils import *


# enable "Send preferred delegated prefix" and set proper value
class TestV6PD_Hint_Opt_TC01(Test):
    uuid = "SOSAIOT-TC-56486"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_config_packet_monitor(self):
        param = {
            'monitor_filter': {
                'ip_types': 'udp',
                'destination_ports': '546,547'
            }
        }
        res = pkt_mon_api.conf_packmon(**param)
        Assertion.assert_equal(res, True, 'ERR: config packet monitor failed.')

    def test_02_set_ipv6_x1_to_dhcpv6(self):
        init_packet_capture()
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': True
                'prefix_delegation': {"preferred": {'addr': "2001:470:80B7:930::", 'prefix': 60}}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'set x1 to dhcpv6 mode failed.')

    def test_03_check_x1_v6_addr(self):
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

    def test_04_check_ip_prefix_in_packet(self):
        rc = False
        pkt_mon_api.stop_capture()
        pkt_mon_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if 'Identity Association for Prefix Delegation' in pkt:
                logger.info(f'find the IAPD info in pkt\n{pkt}')
                m = re.search(r'Prefix address: (2001:470:80b7:9[0-9a-f]0::)', pkt)
                # m = re.search(r'Prefix address: (2001:470:80b7:930::)', pkt)
                if m:
                    logger.info(f'============>get correct prefix:{m.group(1)}')
                    rc = True
                break

        else:
            logger.error('not find the IAPD info in packets')
        Assertion.assert_equal(rc, True, 'ERR: check ip prefix in packet failed!!')


# check PD HINT info in TSR
class TestV6PD_Hint_Opt_TC09(Test):
    uuid = "SOSAIOT-TC-56494"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_check_pd_hint_in_tsr(self):
        rc = False
        tsr_info = diag_api.get_tsr_part("Network", 'Interfaces')
        logger.info(f'get tsr info as follow:\n{tsr_info}')
        m = re.search(r'(IA Prefixes:\s+)(\d.+/60)', tsr_info, re.M)
        if m:
            logger.info(f'get obtained Prefix in TSR file success.\n{m.group(2)}')
            rc = bool(re.search(r'2001:470:80b7:9[0-9a-f]0::', str(m.group(2))))
        else:
            logger.error('get Prefix failed in tsr')
        Assertion.assert_equal(rc, True, 'ERR: check pd hint in tsr failed!!')


# restart test
class TestV6PD_Hint_Opt_TC10(Test):
    uuid = "SOSAIOT-TC-56495"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_restart_fw(self):
        res = set_api.boot_fw(mode=1)
        Assertion.assert_equal(res, True, 'ERR: reboot firewall failed.')

    def test_02_check_pd_hint_after_restart(self):
        TestV6PD_Hint_Opt_TC09().test_check_pd_hint_in_tsr()


# enable "Send preferred delegated prefix" and set improper value
class TestV6PD_Hint_Opt_TC02(Test):
    uuid = "SOSAIOT-TC-56487"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_pd_x1v6(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': {"preferred": {'addr': "2001:470:80B7:800::", 'prefix': 60}}
                'prefix_delegation': {}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        rc = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc, True, 'ERRL disable v6 x1 pd failed!!')

    def test_02_enable_x1v6_pd_and_set_hint_opt_to_improper_value(self):
        init_packet_capture()
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': True
                'prefix_delegation': {"preferred": {'addr': "2001:470:80B7:800::", 'prefix': 60}}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'set x1 hint opt to improper value failed.')

    def test_03_check_x1_v6_addr(self):
        TestV6PD_Hint_Opt_TC01().test_03_check_x1_v6_addr()

    def test_04_check_ip_prefix_in_pkt(self):
        rc = False
        pkt_mon_api.stop_capture()
        pkt_mon_api.export_captured_packets_pcapng('/tmp/packet-c_2.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c_2.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            if get_dhcpv6_packet_type(pkt) == 'Rebind':
                logger.info(f'This Rebind packets details: \n{pkt}')
                if 'Identity Association for Prefix Delegation' in pkt:
                    # logger.info(f'find the IAPD info in pkt\n{pkt}')
                    m = re.search(r'Prefix address: (2001:470:80b7:9[0-9a-f]0::)', pkt)
                    if m:
                        logger.info(f'get correct prefix:{m.group(1)}')
                        rc = True
                    break

        else:
            logger.error('not find the IAPD info in packets')
        Assertion.assert_equal(rc, True, 'ERR: check ip prefix in packet failed!!')


# [error test]enable "Send preferred delegated prefix" and set invalid value
class TestV6PD_Hint_Opt_TC03(Test):
    uuid = "SOSAIOT-TC-56488"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_set_v6x1_hint_opt_as_invalid_value(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': True
                'prefix_delegation': {"preferred": {'addr': "2001:470:80B7:ddd33::", 'prefix': 60}}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res, err_msg = if_v6_api.config_interface_ipv6(**x1_v6_dict, msg=True)
        logger.info(json.dumps(err_msg))
        rc = "Schema validation error: property 'addr': invalid format" in json.dumps(err_msg) and (not res)
        Assertion.assert_equal(rc, True, 'ERR: set_v6x1_hint_opt_as_invalid_value failed.')


# edit PD hint value in GUI
class TestV6PD_Hint_Opt_TC04(Test):
    uuid = "SOSAIOT-TC-56489"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_edit_hint_opt_value(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': True
                'prefix_delegation': {"preferred": {'addr': "2001:470:80B7:903::", 'prefix': 60}}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: edit_hint_opt_value failed.')


# disable PD HINT in GUI
class TestV6PD_Hint_Opt_TC05(Test):
    uuid = "SOSAIOT-TC-56490"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_hint_opt(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': True
                'prefix_delegation': {}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: disable_hint_opt failed.')


#  Enable PD Hint via CLI
class TestV6PD_Hint_Opt_TC06(Test):
    uuid = "SOSAIOT-TC-56491"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_pd_hint_via_cli(self):
        cmds = ['configure', 'interface ipv6 x1', 'ip-assignment dhcpv6', 'prefix-delegation', 'preferred 2001:: 64',
                'commit',
                'end', 'end']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: enable pd hint via CLI failed!!')


# Disable PD Hint via CLI
class TestV6PD_Hint_Opt_TC07(Test):
    uuid = "SOSAIOT-TC-56492"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_pd_hint_via_cli(self):
        cmds = ['configure', 'interface ipv6 x1', 'ip-assignment dhcpv6', 'prefix-delegation', 'no preferred', 'commit',
                'end', 'end']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: disable pd hint via CLI failed!!')


# Edit PD Hint via CLI which add in GUI
class TestV6PD_Hint_Opt_TC08(Test):
    uuid = "SOSAIOT-TC-56493"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_config_hint_opt_value(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': True
                'prefix_delegation': {"preferred": {'addr': "2001:470:80B7:903::", 'prefix': 60}}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'ERR: config_hint_opt_value failed.')

    def test_02_edit_hint_via_cli(self):
        cmds = ['configure', 'interface ipv6 x1', 'ip-assignment dhcpv6', 'prefix-delegation',
                'preferred 2001:470:80b7:907:: 60 ', 'commit',
                'end', 'end']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: edit_hint_via_cli failed!!')

from definition.utils import *


# DHCP leases are saved in to the Flash only when it is necessary
class Test_DHCP_Persistence_TC1825685(Test):
    uuid = "SOSAIOT-TC-55932"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_server_persistence_opt(self):
        dhcp_dict = {
            "dhcp_server": {
                "ipv4": {
                    "conflict_detection": True,
                    "enable": True,
                    "persistence": True,
                    "persistence_monitoring_interval": 30,
                    "recycle_expired_lease": 0,
                    "trusted_relay_agents": ""
                }
            }
        }
        rc = dhcp_api.config_dhcp_server_settings(**dhcp_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable persistence option for dhcp server failed!!')

    def test_02_add_dhcp_dynamic_scope_for_x2(self):
        rc = dhcp_api.add_dhcp_server_scope_dynamic(**dynamic_scope)
        Assertion.assert_equal(rc, True, 'ERR: add dhcp dynamic scope for x2 failed!!')

    def test_03_pc3_get_dhcp_lease(self):
        out = pc_renew_dynamic_addr()
        rc = bool(re.search(r'bound to 13.13.1.\d{2,3}.*renewal', out))
        Assertion.assert_equal(rc, True, "ERR: pc3 get dhcp lease failed!!")

    def test_04_check_DHCP_Flash_writes_count_in_TSR(self):
        tsr_info = diag_api.get_tsr_part2(func='Blade_1_DHCP_PERSISTENCE')
        logger.info(tsr_info)
        Assertion.assert_regular(tsr_info, 'Need to update flash : 1', 'ERR: ')

    def test_05_init_pc3_eth1(self):
        pc3_login.send_command('dhclient -r eth1')
        Assertion.assert_equal(True, True, 'ERR: init pc3 eth1 failed!!')


# Verify DHCP bindings
class Test_DHCP_Persistence_TC1825686(Test):
    uuid = "SOSAIOT-TC-55933"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_enable_dhcp_bindings_in_tsr(self):
        rc = diag_api.conf_tsr(**{"dhcp_bindings": True})
        Assertion.assert_equal(rc, True, 'ERR: enable dhcp bindings in tsr failed!!')

    def test_02_client_get_dhcp_lease(self):
        Test_DHCP_Persistence_TC1825685().test_03_pc3_get_dhcp_lease()

    def test_03_reboot_fw(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: restart fw failed!!')

    def test_04_check_dhcp_bindings_in_tsr(self):
        sleep(30)
        pkt_api.stop_capture()
        tsr_info = diag_api.get_tsr_part2(func='Blade_1_DHCP_BINDING')
        logger.info(tsr_info)
        Assertion.assert_regular(tsr_info, '13.13.1.\d', 'ERR: check dhcp bindings in tsr failed!!')

    def test_05_init_pc3_eth1(self):
        pc3_login.send_command('dhclient -r eth1')
        Assertion.assert_equal(True, True, 'ERR: init pc3 eth1 failed!!')


# Client sends discover after reboot
class Test_DHCP_Persistence_TC1825688(Test):
    uuid = "SOSAIOT-TC-55935"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_check_discover_packet_after_reboot(self):
        rc = False
        pc1_login.send_command('rm -f /tmp/packet-c.pcapng')
        pkt_api.export_captured_packets_pcapng(filepath='/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('\n\n')
        for pkt in pkt_list:
            check_list = ('Src: 0.0.0.0 (0.0.0.0)', 'Dst: 255.255.255.255', ' Protocol: UDP (17)')
            rc = all(x in pkt for x in check_list)
            if rc:
                logger.info(f'find the discover sent from client:\n{pkt}')
                break
        else:
            logger.error('not find the discover packet!')
        Assertion.assert_equal(rc, True, 'ERR: check discover sent from client failed!!')

    def test_02_init_pc3_eth1(self):
        pc3_login.send_command('dhclient -r eth1')
        Assertion.assert_equal(True, True, 'ERR: init pc3 eth1 failed!!')


# import works with DHCP Persistence configuration
class Test_DHCP_Persistence_TC1825690(Test):
    uuid = "SOSAIOT-TC-55937"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_export_exp_file(self):
        rc = set_api.export_setting_exp(filepath='/tmp/cyuan.exp')
        Assertion.assert_equal(rc, True, 'ERR: export exp file failed!!')

    def test_02_restore_fw(self):
        rc = set_api.boot_fw(mode=2)
        Assertion.assert_equal(rc, True, "ERR: restore fw failed!!")

    def test_03_import_exp_file(self):
        rc = set_api.import_setting_exp(filepath='/tmp/cyuan.exp')
        Assertion.assert_equal(rc, True, "ERR: import exp file failed!!")

    def test_04_check_dhcp_persistence_conf(self):
        out = dhcp_api.get_dhcp_server_settings()
        logger.info(json.dumps(out))
        rc = '"persistence": true' in json.dumps(out) and '"persistence_monitoring_interval": 30' in json.dumps(out)
        Assertion.assert_equal(rc, True, "ERR: check dhcp persistence settings failed!!")


# Funciton for DHCP Server Persistence Monitoring Interval testing
class Test_DHCP_Persistence_TC1825689(Test):
    uuid = "SOSAIOT-TC-55936"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    dhcp_lease1 = ''

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_set_persistence_interval(self):
        dhcp_dict = {
            "dhcp_server": {
                "ipv4": {
                    "conflict_detection": True,
                    "enable": True,
                    "persistence": True,
                    "persistence_monitoring_interval": 5,
                    "recycle_expired_lease": 0,
                    "trusted_relay_agents": ""
                }
            }
        }
        rc = dhcp_api.config_dhcp_server_settings(**dhcp_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable persistence option for dhcp server failed!!')

    def test_02_pc3_get_dhcp_lease(self):
        Test_DHCP_Persistence_TC1825685().test_03_pc3_get_dhcp_lease()

    def test_03_download_tsr_and_wait(self):
        tsr_info = diag_api.get_tsr_part2(func='Blade_1_DHCP_PERSISTENCE')
        logger.info(tsr_info)
        logger.info('wait 10 mins the persistence monitor timeout')
        sleep(10*60)
        out = dhcp_api.get_dhcp_server_leases()
        Test_DHCP_Persistence_TC1825689.dhcp_lease1 = out[0].get("ip_address") if out and out[0] else "-1"
        logger.info(f'dhcp lease1 is: {self.dhcp_lease1}')
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, "ERR: reboot firewall failed!!")

    def test_04_check_dhcp_lease_preserved(self):
        out = dhcp_api.get_dhcp_server_leases()
        dhcp_lease2 = out[0].get("ip_address") if out and out[0] else "-2"
        logger.info(f'dhcp lease1 is: {Test_DHCP_Persistence_TC1825689.dhcp_lease1}')
        logger.info(f'dhcp lease2 is: {dhcp_lease2}')
        rc = Test_DHCP_Persistence_TC1825689.dhcp_lease1 == dhcp_lease2
        Assertion.assert_equal(rc, True, "ERR: check_dhcp_lease_preserved failed!!")

    def test_05_check_client_get_same_lease_after_renew(self):
        pc3_login.send_command('dhclient -r eth1')
        pc3_login.send_command('dhclient -v eth1')
        out = pc3_login.send_command('ifconfig eth1')
        rc = Test_DHCP_Persistence_TC1825689.dhcp_lease1 in out
        Assertion.assert_equal(rc, True, "ERR: check_client_get_same_lease_after_renew failed!!")


# Restoring configuration to Factory default truncate DHCP lease file in the Flash
class Test_DHCP_Persistence_TC1825687(Test):
    uuid = "SOSAIOT-TC-55934"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    dhcp_lease1 = ''

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_check_lease_after_restore(self):
        rc = set_api.boot_fw(mode=2)
        if not rc:
            logger.error('restore firewall failed!!')
        out = dhcp_api.get_dhcp_server_leases()
        Assertion.assert_equal(bool(out), False, "ERR: check_lease_after_restore failed!!")

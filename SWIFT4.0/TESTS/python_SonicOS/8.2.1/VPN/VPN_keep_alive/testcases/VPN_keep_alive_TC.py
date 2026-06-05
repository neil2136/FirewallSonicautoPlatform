from definition.settings import *
from definition import check_traffic


class TestVPN_keep_alive_01(Test):
    uuid = "SOSAIOT-TC-54445"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_01_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_01_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_01_04_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_05_restart_dut(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        ret = LRestartObj.restart_now()
        Assertion.assert_equal(ret, True, "ERR: restart dut failed")

    def test_01_06_check_traffic_after_restart_dut(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc1 = check_traffic.ping_from_local_to_remote()
        rc2 = check_traffic.check_test_log()
        Assertion.assert_equal(rc1&rc2, True, "ERR: Ping failed")

    def test_01_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestVPN_keep_alive_02(Test):
    uuid = "SOSAIOT-TC-54447"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_02_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_03_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_02_04_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_02_05_modify_vpn_secret(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['edit_auth'] = True
        ref2['edit_auth'] = True
        ref1['secret'] = 'mysecret'
        ref2['secret'] = 'mysecret'
        logger.info(" {} ".center(20, '*').format('Modify Local VPN Policy secret'))
        rc1 = Lvpn_obj.edit_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Modify Remote VPN Policy secret'))
        rc2 = Rvpn_obj.edit_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Modify VPN Policy secret Failed.')

    def test_02_06_check_traffic_after_modify_both_secret(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc1 = check_traffic.ping_from_local_to_remote()
        rc2 = check_traffic.check_test_log()
        Assertion.assert_equal(rc1&rc2, True, "ERR: Ping failed")

    def test_02_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2, True, 'Remove VPN Policy Failed.')


class TestVPN_keep_alive_03(Test):
    uuid = "SOSAIOT-TC-54448"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_03_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_03_03_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_03_04_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_03_05_modify_vpn_secret_local(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['edit_auth'] = True
        ref1['secret'] = 'mysecret'
        logger.info(" {} ".center(20, '*').format('Modify Local VPN Policy secret'))
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Modify VPN Policy secret Failed.')

    def test_03_06_check_traffic_after_modify_local_secret(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_03_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2, True, 'Remove VPN Policy Failed.')


class TestVPN_keep_alive_04(Test):
    uuid = "SOSAIOT-TC-54446"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_04_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_04_03_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_04_04_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_04_05_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_04_06_check_traffic_again(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc1 = check_traffic.ping_from_local_to_remote()
        rc2 = check_traffic.check_test_log()
        Assertion.assert_equal(rc1&rc2, False, "ERR: Ping failed")

    def test_04_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2, True, 'Remove VPN Policy Failed.')


class TestVPN_keep_alive_05(Test):
    uuid = "SOSAIOT-TC-54449"
    description = show_testcase_info(TESTPLAN, '5', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_05_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_05_03_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_05_04_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_05_05_disconnected_x1(self):
        cmds = ['configure',
                'interface x1',
                'shutdown-port',
                'commit',
                'exit',
                'exit',
            ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_05_06_check_traffic_blocked(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_05_07_reconnected_x1(self):
        cmds = ['configure',
                'interface x1',
                'no shutdown-port',
                'commit',
                'exit',
                'exit',
            ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_05_08_check_traffic(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc1 = check_traffic.ping_from_local_to_remote()
        rc2 = check_traffic.check_test_log()
        Assertion.assert_equal(rc1&rc2, True, "ERR: Ping failed")

    def test_05_09_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2, True, 'Remove VPN Policy Failed.')


class TestVPN_keep_alive_06(Test):
    uuid = "SOSAIOT-TC-54450"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_06_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_06_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_06_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_06_03_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_06_04_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_06_05_modify_local_AO(self):
        ref1 = {
            "address_objects": [{
                "ipv4": {
                    "name": "remote_net",
                    "zone": "VPN",
                    "network": {
                        "subnet": "11.11.11.0",
                        "mask": "255.255.255.0"
                    }
                }
            }
            ]
        }
        logger.info(" {} ".center(20, '*').format('Modify Local AO'))
        rc = LAddrOBJ.edit_addressobject(ip_type='ipv4', object_type='network', object_path='name', obj_name_uuid=remote_l['name'], json_put=ref1)
        Assertion.assert_equal(rc, True, 'Modify local AO Failed.')

    def test_06_06_check_traffic_blocked(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_06_07_recover_local_AO(self):
        ref1 = {
            "address_objects": [{
                "ipv4": {
                    "name": "remote_net",
                    "zone": "VPN",
                    "network": {
                        "subnet": "172.16.1.0",
                        "mask": "255.255.255.0"
                    }
                }
            }
            ]
        }
        logger.info(" {} ".center(20, '*').format('Modify Local AO'))
        rc = LAddrOBJ.edit_addressobject(ip_type='ipv4', object_type='network', object_path='name', obj_name_uuid=remote_l['name'], json_put=ref1)
        Assertion.assert_equal(rc, True, 'recover local AO Failed.')

    def test_06_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2, True, 'Remove VPN Policy Failed.')

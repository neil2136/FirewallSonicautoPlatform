from definition.settings import *
from bin import check_traffic
from bin import packet_monitor


class TestTunnel_All_TP16_01(Test):
    uuid = "SOSAIOT-TC-54669"
    description= show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret1 = LLogObj.clear_log()
        ret2 = RLogObj.clear_log()
        if ret1 == None and ret2 == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor('ICMP')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_01_02_add_vpn_policy(self):
        global ref1, ref2
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'main'
        ref2['ike_exchange'] = 'main'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    @repeat_method(3)
    def test_01_03_ping_from_remote_to_baidu(self):
        global spe_ip
        rc, spe_ip = check_traffic.ping_from_remote_to_baidu()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor(spe_ip)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_05_test_log_on_local(self):
        time.sleep(10)
        rc = check_traffic.check_test_log('local', ref1)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_06_test_log_on_remote(self):
        time.sleep(10)
        rc = check_traffic.check_test_log('remote', ref1)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestTunnel_All_TP16_02(Test):
    uuid = "SOSAIOT-TC-54670"
    description= show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret1 = LLogObj.clear_log()
        ret2 = RLogObj.clear_log()
        if ret1 == None and ret2 == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor('ICMP')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_02_02_add_vpn_policy(self):
        global ref1, ref2
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    @repeat_method(3)
    def test_02_03_ping_from_remote_to_baidu(self):
        global spe_ip
        rc, spe_ip = check_traffic.ping_from_remote_to_baidu()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor(spe_ip)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_02_05_test_log_on_local(self):
        time.sleep(10)
        rc = check_traffic.check_test_log('local', ref1)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_02_06_test_log_on_remote(self):
        time.sleep(10)
        rc = check_traffic.check_test_log('remote', ref1)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_02_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestTunnel_All_TP16_03(Test):
    uuid = "SOSAIOT-TC-54673"
    description= show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret1 = LLogObj.clear_log()
        ret2 = RLogObj.clear_log()
        if ret1 == None and ret2 == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor('ESP')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_03_02_add_vpn_policy(self):
        global ref1, ref2
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'ikev2'
        ref2['ike_exchange'] = 'ikev2'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    @repeat_method(3)
    def test_03_03_ping_from_remote_to_baidu(self):
        global spe_ip
        rc, spe_ip = check_traffic.ping_from_remote_to_baidu()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_03_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor(spe_ip)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_03_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestTunnel_All_TP16_10(Test):
    uuid = "SOSAIOT-TC-54671"
    description= show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret1 = LLogObj.clear_log()
        ret2 = RLogObj.clear_log()
        if ret1 == None and ret2 == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor('ESP')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_10_02_add_vpn_policy(self):
        global ref1, ref2
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['pri_gate'] = 'primary.vpntestbed.com'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    @repeat_method(3)
    def test_10_03_ping_from_remote_to_baidu(self):
        global spe_ip
        rc, spe_ip = check_traffic.ping_from_remote_to_baidu()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_10_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor(spe_ip)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_05_test_log_on_local(self):
        time.sleep(10)
        rc = check_traffic.check_test_log('local', ref1)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_06_test_log_on_remote(self):
        time.sleep(10)
        rc = check_traffic.check_test_log('remote', ref1)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestTunnel_All_TP16_08(Test):
    uuid = "SOSAIOT-TC-54672"
    description= show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_08_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_08_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret1 = LLogObj.clear_log()
        if ret1 == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_08_02_add_vpn_policy(self):
        global ref1, ref2
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'main'
        ref2['ike_exchange'] = 'main'
        ref2['remote_net_type'] = 'name'
        ref2['remote_net_name'] = remote_r['name']
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_08_03_check_ping_from_remote_to_local_blocked(self):
        logger.info("ping from remote to local host")
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_08_04_test_failure_log_on_local(self):
        time.sleep(10)
        rc = check_traffic.check_failure_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_08_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')
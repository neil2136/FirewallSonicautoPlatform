from definition.settings import *
from bin import check_traffic
from bin import conf_pri_gw


class TestIKEv2_Sec_GW_01(Test):
    uuid = "SOSAIOT-TC-54422"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_01_01_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_02(Test):
    uuid = "SOSAIOT-TC-54429"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['sec_gate'] = 'primary.vpntestbed.com'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_02_01_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_04(Test):
    uuid = "SOSAIOT-TC-54437"
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
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_04_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_04_05_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_04_06_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_04_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_05(Test):
    uuid = "SOSAIOT-TC-54442"
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
        ref1['keep_alive'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_05_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_05_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    # def test_05_05_test_log(self):
    #     rc = check_traffic.check_test_log()
    #     Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_05_06_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_05_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_07(Test):
    uuid = "SOSAIOT-TC-54443"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_07_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_07_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_07_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['keep_alive'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_07_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_07_04_check_traffic_after_reboot_dut(self):
        rc = LRestartObj.restart_now()
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: block cipher1 failed")

    def test_07_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_08(Test):
    uuid = "SOSAIOT-TC-54444"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_08_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_08_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_08_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['keep_alive'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_08_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_08_04_Export_and_import_Perference(self):
        rc = Lsetting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        rc &= Lsetting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export and import the settings...")

    def test_08_05_check_traffic_after_ex_imp_pref(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: block cipher1 failed")

    def test_08_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_10(Test):
    uuid = "SOSAIOT-TC-54423"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_10_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = "120"
        ref1['ipsec_lifetime'] = "120"
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_10_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_10_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_10_05_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_10_06_wait_for_expire(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        out = os.popen("ping {} -c 123".format(PC2_eth0)).read()
        logger.info(out)
        Assertion.assert_equal(True, True, "ERR: Ping failed")

    def test_10_07_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_11(Test):
    uuid = "SOSAIOT-TC-54424"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_11_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_11_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = "120"
        ref1['ipsec_lifetime'] = "120"
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_11_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_11_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_11_05_wait_for_expire(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        out = os.popen("ping {} -c 123".format(PC2_eth0)).read()
        logger.info(out)
        Assertion.assert_equal(True, True, "ERR: Ping failed")

    def test_11_06_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_11_07_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_11_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_19(Test):
    uuid = "SOSAIOT-TC-54428"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_19_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_19_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_19_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = "120"
        ref1['ipsec_lifetime'] = "120"
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_19_03_ping_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_19_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_19_05_ping_from_remote_to_local_after_dis_pri_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_19_06_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_19_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_22(Test):
    uuid = "SOSAIOT-TC-54430"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_22_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_22_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_22_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = "120"
        ref1['ipsec_lifetime'] = "120"
        ref1['preempt_interval'] = "120"
        ref2['pri_gate'] = "0.0.0.0"
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_22_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_22_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_22_05_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_22_06_wait_for_expire(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        out = os.popen("ping {} -c 123".format(PC2_eth0)).read()
        logger.info(out)
        Assertion.assert_equal(True, True, "ERR: Ping failed")

    def test_22_07_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_22_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_23(Test):
    uuid = "SOSAIOT-TC-54431"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_23_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_23_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_23_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = "120"
        ref1['ipsec_lifetime'] = "120"
        ref2['pri_gate'] = "0.0.0.0"
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_23_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_23_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_23_05_wait_for_expire(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        out = os.popen("ping {} -c 123".format(PC2_eth0)).read()
        logger.info(out)
        Assertion.assert_equal(True, True, "ERR: Ping failed")

    def test_23_06_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_23_07_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_23_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')



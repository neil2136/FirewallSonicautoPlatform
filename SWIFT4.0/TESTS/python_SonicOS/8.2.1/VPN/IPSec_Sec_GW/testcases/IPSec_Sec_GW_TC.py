from definition.settings import *
from bin import check_traffic
from bin import conf_pri_gw


class TestIPSec_Sec_GW_02(Test):
    uuid = "SOSAIOT-TC-54630"
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
        # ref1['ike_lifetime'] = "120"
        # ref2['ipsec_lifetime'] = "120"
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_05_test_log_after_pri_gw_down(self):
        rc = check_traffic.check_test_log_after_pri_gw_down()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_02_06_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIPSec_Sec_GW_04(Test):
    uuid = "SOSAIOT-TC-54632"
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
        # ref1['ike_lifetime'] = "120"
        ref1['keep_alive'] = True
        # ref2['ike_lifetime'] = "120"
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

    def test_04_05_test_log_after_pri_gw_down(self):
        rc = check_traffic.check_test_log_after_pri_gw_down()
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


class TestIPSec_Sec_GW_09(Test):
    uuid = "SOSAIOT-TC-54633"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_09_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_09_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = "120"
        ref1['keep_alive'] = True
        ref1['pri_gate'] = "primary.vpntestbed.com"
        ref1['sec_gate'] = "secondary.vpntestbed.com"
        ref2['ike_lifetime'] = "120"
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_09_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_09_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_09_05_test_log_after_pri_gw_down(self):
        rc = check_traffic.check_test_log_after_pri_gw_down()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_09_06_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_09_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIPSec_Sec_GW_10(Test):
    uuid = "SOSAIOT-TC-54634"
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
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_10_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_10_04_check_traffic_after_reboot_dut(self):
        rc = LRestartObj.restart_now()
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: block cipher1 failed")

    def test_10_05_check_vpn_sec_gw(self):
        resp = Lvpn_obj.show_s2svpnpolicy()
        if resp['vpn']['policy'][0]['ipv4']['site_to_site']['gateway']['secondary'] == Parameter.REMOTEX2:
            rc = True
        else:
            rc = False
            logger.info(resp)
        Assertion.assert_equal(rc, True, "ERR: block cipher1 failed")

    def test_10_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIPSec_Sec_GW_11(Test):
    uuid = "SOSAIOT-TC-54628"
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
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_11_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_11_04_Export_and_import_Perference(self):
        rc = Lsetting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        rc &= Lsetting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export and import the settings...")

    def test_11_05_check_traffic_after_ex_imp_pref(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: block cipher1 failed")

    def test_11_06_check_vpn_sec_gw(self):
        resp = Lvpn_obj.show_s2svpnpolicy()
        if resp['vpn']['policy'][0]['ipv4']['site_to_site']['gateway']['secondary'] == Parameter.REMOTEX2:
            rc = True
        else:
            rc = False
            logger.info(resp)
        Assertion.assert_equal(rc, True, "ERR: block cipher1 failed")

    def test_11_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIPSec_Sec_GW_12(Test):
    uuid = "SOSAIOT-TC-54629"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_12_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_12_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_12_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = "120"
        ref2['ipsec_lifetime'] = "120"
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_12_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_12_04_check_secondary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_12_05_test_log_after_pri_gw_down(self):
        rc = check_traffic.check_test_log_after_pri_gw_down()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_12_06_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_12_07_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_12_08_wait_for_expire(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        out = os.popen("ping {} -c 123".format(PC2_eth0)).read()
        logger.info(out)
        Assertion.assert_equal(True, True, "ERR: Ping failed")

    def test_12_09_test_log_after_expire(self):
        rc = check_traffic.check_test_log_after_expire()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_12_10_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIPSec_Sec_GW_23(Test):
    uuid = "SOSAIOT-TC-54631"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_23_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
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
        ref1['ike_exchange'] = "aggressive"
        ref1['ike_lifetime'] = "120"
        ref2['ipsec_lifetime'] = "120"
        ref2['ike_exchange'] = "aggressive"
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

    def test_23_05_test_log_after_pri_gw_down(self):
        rc = check_traffic.check_test_log_after_pri_gw_down()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_23_06_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_23_07_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_23_08_wait_for_expire(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        out = os.popen("ping {} -c 123".format(PC2_eth0)).read()
        logger.info(out)
        Assertion.assert_equal(True, True, "ERR: Ping failed")

    def test_23_09_test_log_after_expire(self):
        rc = check_traffic.check_test_log_after_expire()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_23_10_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

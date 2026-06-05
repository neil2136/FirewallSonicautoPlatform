from definition.settings import *
from bin import check_traffic
from bin import conf_pri_gw


@paramunittest.parametrized(
    {'dpd_interval': '3', 'dpd_trigger': '3', 'uuid': '1705065', 'tcid': '9'},
)
class TestDPD_09(Test):
    def setParameters(self, dpd_interval, dpd_trigger, uuid, tcid):
        self.dpd_interval = dpd_interval
        self.dpd_trigger = dpd_trigger
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_09_01_conf_dpd(self):
        global sleep_time
        ref = copy.deepcopy(En_dpd)
        ref['dpd_interval'] = self.dpd_interval
        ref['dpd_trigger'] = self.dpd_trigger
        sleep_time = int(ref['dpd_interval'])*int(ref['dpd_trigger'])+30
        rc = LAdv_obj.config_vpnadvanced(**ref)
        rc &= RAdv_obj.config_vpnadvanced(**ref)
        Assertion.assert_equal(rc, True, 'Config Local DPD Failed.')

    def test_09_02_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_09_03_add_first_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_09_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_09_05_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_09_06_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_09_07_add_secondary_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_2)
        ref2 = copy.deepcopy(Rvpn_2)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_09_08_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_PC4_to_PC5()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_09_09_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_09_10_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_09_11_disable_remote_x1x2(self):
        logger.info('disable remote x1&x2 port')
        rc = conf_pri_gw.disable_device_port('X1')
        rc &= conf_pri_gw.disable_device_port('X2')
        Assertion.assert_equal(rc, True, "ERR: disable remote x1x2 failed")

    def test_09_12_ping_from_local_to_remote_blocked(self):
        time.sleep(int(self.dpd_interval))
        logger.info('ping traffic')
        rc = check_traffic.ping_traffic_blocked()
        rc &= check_traffic.ping_traffic2_blocked()
        Assertion.assert_equal(rc, True, "ERR: check Ping block failed")

    def test_09_13_test_log_with_enable_dpd(self):
        time.sleep(int(sleep_time))
        rc = check_traffic.check_test_log_with_enable_dpd()
        Assertion.assert_equal(rc, True, "ERR: Test log with dpd enable failed")

    def test_09_14_enable_remote_x1x2(self):
        logger.info('enable remote x1x2 port')
        rc = conf_pri_gw.enable_device_port('X1')
        rc &= conf_pri_gw.enable_device_port('X2')
        Assertion.assert_equal(rc, True, "ERR: recover remote x1x2 failed")

    def test_09_15_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc1 &= Lvpn_obj.del_s2svpn_policy(**Lvpn_2)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        rc2 &= Rvpn_obj.del_s2svpn_policy(**Rvpn_2)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

    def test_09_16_disable_dpd(self):
        logger.info('-'*10+'Config Local DPD'+'-'*10)
        rc = LAdv_obj.config_vpnadvanced(**Dis_dpd)
        rc &= RAdv_obj.config_vpnadvanced(**Dis_dpd)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')

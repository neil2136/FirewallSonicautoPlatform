from definition.settings import *
from bin import check_traffic
from bin import conf_pri_gw


@paramunittest.parametrized(
    {'dpd_interval': '10', 'dpd_trigger': '3', 'uuid': '1705062', 'tcid': '5'},
    {'dpd_interval': '3', 'dpd_trigger': '10', 'uuid': '1515024', 'tcid': '6'},
)
class TestDPD_05_06(Test):
    def setParameters(self, dpd_interval, dpd_trigger, uuid, tcid):
        self.dpd_interval = dpd_interval
        self.dpd_trigger = dpd_trigger
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_conf_dpd(self):
        global sleep_time
        ref = copy.deepcopy(En_dpd)
        ref['dpd_interval'] = self.dpd_interval
        sleep_time = int(ref['dpd_interval'])*int(ref['dpd_trigger'])+30
        rc = LAdv_obj.config_vpnadvanced(**ref)
        rc &= RAdv_obj.config_vpnadvanced(**ref)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')

    def test_05_02_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_05_03_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['keep_alive'] = True
        ref2['keep_alive'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_05_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_05_05_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_05_06_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_05_07_disable_remote_x1_and_ping(self):
        logger.info('disable remote x1 port')
        rc = conf_pri_gw.disable_device_port('X1')
        time.sleep(int(self.dpd_interval))
        logger.info('check ping from dut to remote is block')
        rc &= check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: disable remote x1 failed")

    def test_05_08_test_log_with_enable_dpd(self):
        time.sleep(int(sleep_time))
        rc = check_traffic.check_test_log_with_enable_dpd()
        Assertion.assert_equal(rc, True, "ERR: Test log with enable dpd failed")

    def test_05_09_enable_remote_x1(self):
        logger.info('enable remote x1 port')
        rc = conf_pri_gw.enable_device_port('X1')
        Assertion.assert_equal(rc, True, "ERR: recover remote x1 failed")

    def test_05_10_test_log(self):
        time.sleep(120)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_05_11_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

    def test_05_12_disable_dpd(self):
        logger.info('-'*10+'Config Local DPD'+'-'*10)
        rc = LAdv_obj.config_vpnadvanced(**Dis_dpd)
        rc &= RAdv_obj.config_vpnadvanced(**Dis_dpd)
        Assertion.assert_equal(rc, True, 'Config Local DPD Failed.')

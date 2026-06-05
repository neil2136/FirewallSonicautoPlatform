from definition.settings import *
from bin import check_traffic
from bin import conf_pri_gw


@paramunittest.parametrized(
    {'dis_rm_x1': False, 'uuid': '1515021', 'tcid': '1'},
    {'dis_rm_x1': True, 'uuid': '1515022', 'tcid': '2'},
 )
class TestDPD_01_02(Test):
    def setParameters(self, dis_rm_x1, uuid, tcid):
        self.dis_rm_x1 = dis_rm_x1
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_disable_dpd(self):
        rc = LAdv_obj.config_vpnadvanced(**Dis_dpd)
        rc &= RAdv_obj.config_vpnadvanced(**Dis_dpd)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')

    def test_01_02_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_01_03_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_01_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_05_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_06_disable_dut_x1_and_ping(self):
        if self.dis_rm_x1:
            logger.info('disable remote x1 port')
            rc1 = conf_pri_gw.disable_device_port('X1')
            logger.info('Clear log')
            ret = LogObj.clear_log()
            if ret == None:
                rc2 = True
            else:
                rc2 = False
            time.sleep(int(En_dpd['dpd_interval']))
            logger.info('check ping from dut to remote is block')
            rc3 = check_traffic.ping_traffic_blocked()
            rc = rc1 & rc2 & rc3
            logger.info('{},{},{}'.format(rc1,rc2,rc3))
        else:
            logger.info("testcase {} skip this step".format(self.tcid))
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_07_test_log_with_disable_dpd(self):
        time.sleep(90)
        rc = check_traffic.check_test_log_with_dis_dpd()
        Assertion.assert_equal(rc, True, "ERR: Test dpd disable log failed")

    def test_01_08_recover_remote_x1(self):
        rc = conf_pri_gw.enable_device_port('X1')
        Assertion.assert_equal(rc, True, "ERR: recover rm x1 failed")

    def test_01_09_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

from definition.settings import *
from definition import check_traffic


@paramunittest.parametrized(
    {'local_type': 'domain_name', 'peer_type': 'domain_name', 'local_id':'test1', 'peer_id': 'test2', \
        'uuid': 'SOSAIOT-TC-54575', 'tcid': '18'},
    {'local_type': 'email_address', 'peer_type': 'email_address', 'local_id': 'test1@test.com', 'peer_id': 'test2@test.com', \
     'uuid': 'SOSAIOT-TC-54576', 'tcid': '19'},
)
class TestVPN_Phase1_ID_18(Test):

    def setParameters(self, local_type, peer_type, local_id, peer_id, uuid, tcid):
        self.local_type = local_type
        self.peer_type = peer_type
        self.local_id = local_id
        self.peer_id = peer_id
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
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
        ref1['local_ike_type'] = self.local_type
        ref1['peer_ike_type'] = self.peer_type
        ref1['local_ike_id'] = self.local_id
        ref1['peer_ike_id'] = self.peer_id
        ref2['local_ike_type'] = self.peer_type
        ref2['peer_ike_type'] = self.local_type
        ref2['local_ike_id'] = self.local_id
        ref2['peer_ike_id'] = self.peer_id
        if self.tcid == '18':
            ref1['peer_ike_id'] = 'test'
        if self.tcid == '19':
            ref2['peer_ike_id'] = 'test@test.com'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_01_03_ping_from_local_to_remote_blocked(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_01_04_test_log_mismatch(self):
        rc = check_traffic.check_test_log_mismatch()
        Assertion.assert_equal(rc, True, "ERR: Test log mismatch failed")

    def test_01_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')



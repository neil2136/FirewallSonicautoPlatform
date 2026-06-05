from definition.settings import *
from definition import check_traffic


@paramunittest.parametrized(
    {'local_type': 'ipv4', 'peer_type': 'ipv4', 'local_id': Parameter.DUT, 'peer_id': Parameter.REMOTEX0, \
        'uuid': 'SOSAIOT-TC-54569', 'tcid': '1'},
    {'local_type': 'ipv4', 'peer_type': 'ipv4', 'local_id': '', 'peer_id': '', \
     'uuid': 'SOSAIOT-TC-54567', 'tcid': '2'},
    {'local_type': 'domain_name', 'peer_type': 'domain_name', 'local_id': 'test1', 'peer_id': 'test2', \
     'uuid': 'SOSAIOT-TC-54568', 'tcid': '3'},
    {'local_type': 'email_address', 'peer_type': 'email_address', 'local_id': 'test1@test.com', 'peer_id': 'test2@test.com', \
     'uuid': 'SOSAIOT-TC-54577', 'tcid': '4'},
    {'local_type': 'firewall_id', 'peer_type': 'firewall_id', 'local_id': local_fwid, 'peer_id': remote_fwid, \
     'uuid': 'SOSAIOT-TC-54578', 'tcid': '5'},
    {'local_type': 'ipv4', 'peer_type': 'domain_name', 'local_id': Parameter.DUT, 'peer_id': 'test', \
     'uuid': 'SOSAIOT-TC-54579', 'tcid': '6'},
    {'local_type': 'ipv4', 'peer_type': 'email_address', 'local_id': Parameter.DUT, 'peer_id': 'test@test.com', \
     'uuid': 'SOSAIOT-TC-54580', 'tcid': '7'},
    {'local_type': 'domain_name', 'peer_type': 'email_address', 'local_id': 'test', 'peer_id': 'test@test.com', \
     'uuid': 'SOSAIOT-TC-54581', 'tcid': '8'},
    {'local_type': 'ipv4', 'peer_type': 'ipv4', 'local_id': '10.10.10.10', 'peer_id': Parameter.REMOTEX0, \
     'uuid': 'SOSAIOT-TC-54573', 'tcid': '16'},
    {'local_type': 'firewall_id', 'peer_type': 'firewall_id', 'local_id': local_fwid, 'peer_id': '0017C5990000', \
     'uuid': 'SOSAIOT-TC-54574', 'tcid': '17'},
)
class TestVPN_Phase1_ID_01(Test):

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
        ref2['local_ike_id'] = self.peer_id
        ref2['peer_ike_id'] = self.local_id
        if self.tcid == '5' or self.tcid == '17':
            ref1['ike_exchange'] = 'aggressive'
            ref2['ike_exchange'] = 'aggressive'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_01_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: ping failed")

    @repeat_method(3)
    def test_01_04_test_log(self):
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")


    def test_01_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')



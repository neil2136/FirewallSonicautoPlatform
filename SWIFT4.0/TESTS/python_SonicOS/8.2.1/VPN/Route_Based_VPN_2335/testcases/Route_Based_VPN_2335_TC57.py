from definition.settings import *
from definition import check_traffic
from definition import conf_device_port


@paramunittest.parametrized(
    {'ike_exchange': 'main', 'uuid': '1506339', 'tcid': '57'},
    {'ike_exchange': 'ikev2', 'uuid': '1506339', 'tcid': '57'},
)
class Route_Based_VPN_2335_TC57(Test):
    def setParameters(self, ike_exchange, uuid, tcid):
        self.ike_exchange = ike_exchange
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = self.ike_exchange
        ref2['ike_exchange'] = self.ike_exchange
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_01_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy1)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")

    def test_01_05_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_06_del_Route_Policy_local(self):
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        rc &= check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_07_del_Route_Policy_remote(self):
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy on remote'))
        rc = RRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_01_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete tunnel VPN'))
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')




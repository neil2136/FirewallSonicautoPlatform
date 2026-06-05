from definition.settings import *
from definition import check_traffic
from definition import conf_device_port


@paramunittest.parametrized(
    {'ike_exchange': 'main', 'action': None, 'uuid': '1705079', 'tcid': '70'},
    {'ike_exchange': 'ikev2', 'action': None, 'uuid': '1705079', 'tcid': '70'},
    {'ike_exchange': 'main', 'action': 'dis_X1', 'uuid': '1705080', 'tcid': '72'},
    {'ike_exchange': 'ikev2', 'action': 'dis_X1', 'uuid': '1705080', 'tcid': '72'},
)
class Route_Based_VPN_2335_TC70_72(Test):
    def setParameters(self, ike_exchange, action, uuid, tcid):
        self.ike_exchange = ike_exchange
        self.action = action
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

    def test_01_02_add_vpn_policy2(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = self.ike_exchange
        ref1['name'] = 'vpn2'
        ref1['pri_gate'] = Parameter.REMOTEX2
        ref2['ike_exchange'] = self.ike_exchange
        ref2['name'] = 'vpn2'
        ref2['pri_gate'] = Parameter.DUTX2
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy2'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy2'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, 'Add VPN Policy2 Failed.')

    def test_01_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy1)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")

    def test_01_04_add_Route_Policy2(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy2'))
        rc = fw_cli.do_cli_commands(route_policy2)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy2'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy2 failed")

    def test_01_05_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_06_dis_vpn_or_dis_X1(self):
        if self.action == 'dis_X1':
            rc = conf_device_port.disable_x1_port('UTM')
            rc &= check_traffic.ping_traffic_blocked()
            rc &= conf_device_port.enable_x1_port('UTM')
        else:
            rc = True
            logger.info("do action: {}, skip this step".format(self.action))
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_07_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy on dut'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        rc &= LRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy on remote'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_01_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete tunnel VPN'))
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')




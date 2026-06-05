from definition.settings import *
from definition import check_traffic
from definition import conf_device_port


@paramunittest.parametrized(
    {'ike_exchange': 'main', 'action': None, 'uuid': '1705076', 'tcid': '56'},
    {'ike_exchange': 'ikev2', 'action': None, 'uuid': '1705076', 'tcid': '56'},
    {'ike_exchange': 'main', 'action': 'dis_vpn', 'uuid': '1506340', 'tcid': '58'},
    {'ike_exchange': 'ikev2', 'action': 'dis_vpn', 'uuid': '1506340', 'tcid': '58'},
    {'ike_exchange': 'main', 'action': 'check_log', 'uuid': '1705077', 'tcid': '62'},
    {'ike_exchange': 'ikev2', 'action': 'check_log', 'uuid': '1705077', 'tcid': '62'},
    {'ike_exchange': 'main', 'action': 'dis_X1', 'uuid': '1705078', 'tcid': '63'},
    {'ike_exchange': 'ikev2', 'action': 'dis_X1', 'uuid': '1705078', 'tcid': '63'},
)
class Route_Based_VPN_2335_TC56_58_62_63(Test):
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

    # def test_01_02_add_Tunnel_interface(self):
    #     ref1 = copy.deepcopy(Tunnel_Interface)
    #     ref2 = copy.deepcopy(Tunnel_Interface)
    #     ref1["ip"] = VPN_IF_IP_LOCAL
    #     ref2["ip"] = VPN_IF_IP_REMOTE
    #     logger.info(" {} ".center(20, '-').format('Add Local Vpn Tunnel Interface'))
    #     rc = LintfaceObj.add_interface(**ref1)
    #     logger.info(" {} ".center(20, '-').format('Add Remote Vpn Tunnel Interface'))
    #     rc &= RintfaceObj.add_interface(**ref2)
    #     Assertion.assert_equal(rc, True, "ERR: Add Vpn Tunnel Interface failed")

    def test_01_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy1)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")

    def test_01_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_05_dis_vpn_or_dis_X1(self):
        if self.action == 'dis_vpn':
            rc = Lvpn_obj.dis_tunnelvpn_policy(**Lvpn)
            rc &= check_traffic.ping_traffic_blocked()
        elif self.action == 'dis_X1':
            rc = conf_device_port.disable_x1_port(rm_device)
            rc &= check_traffic.ping_traffic_blocked()
            rc &= conf_device_port.enable_x1_port(rm_device)
        elif self.action == 'check_log':
            rc = check_traffic.check_test_log_regotiation()
        else:
            rc = True
            logger.info("do action: {}, skip this step".format(self.action))
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_06_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    # def test_01_07_remove_Tunnel_Interface(self):
    #     ref1 = copy.deepcopy(Tunnel_Interface)
    #     ref2 = copy.deepcopy(Tunnel_Interface)
    #     ref1["ip"] = VPN_IF_IP_LOCAL
    #     ref2["ip"] = VPN_IF_IP_REMOTE
    #     logger.info(" {} ".center(20, '-').format('Delete Vpn Tunnel Interface'))
    #     rc = LintfaceObj.del_interface(**ref1)
    #     rc &= RintfaceObj.del_interface(**ref2)
    #     Assertion.assert_equal(rc, True, 'Remove Vpn Tunnel Interface Failed.')

    def test_01_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete tunnel VPN'))
        rc1 = Lvpn_obj.del_tunnelvpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_tunnelvpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

from definition.settings import *
from definition import check_traffic
from definition import conf_device_port
from definition import ftp_transfer


class Route_Based_VPN_2335_TC40(Test):
    uuid = "SOSAIOT-TC-54594"
    description = show_testcase_info(TESTPLAN, '40', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 40)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_01_02_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy1)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")

    def test_01_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_04_Export_and_import_Perference(self):
        rc = Lsetting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        rc &= Lsetting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export and import the settings...")

    def test_01_05_check_traffic_after_ex_imp_pref(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: block cipher1 failed")

    def test_01_06_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_01_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete tunnel VPN'))
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

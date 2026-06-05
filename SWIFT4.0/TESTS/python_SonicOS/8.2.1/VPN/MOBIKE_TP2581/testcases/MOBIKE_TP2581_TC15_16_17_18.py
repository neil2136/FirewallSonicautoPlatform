from definition.settings import *
from bin import check_access_rule


class TestMOBIKE_TP2581_TC15(Test):
    uuid = "SOSAIOT-TC-54216"
    description = show_testcase_info(TESTPLAN, '1714213', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1714213')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_addObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**rm_range)
        Assertion.assert_equal(rc, True, 'Add AO for DUT Failed.')
    
    def test_03_add_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Add first VPN Policy Failed.')

    def test_04_show_auto_added_lan2vpn_rules(self):
        logger.info('check LAN to VPN auto added rule')
        rc = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range', True)
        rc &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range', 'X0 Subnet', True)
        Assertion.assert_equal(rc, True, 'check auto added rules Failed.')

    def test_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')
    
    def test_06_delete_addObj(self):
        logger.info('-'*10+'delete ao'+'-'*10)
        rc = LAddrOBJ.del_ao_by_name(rm_range['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete AO Failed.')


class TestMOBIKE_TP2581_TC16(Test):
    uuid = "SOSAIOT-TC-54217"
    description = show_testcase_info(TESTPLAN, '1714214', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1714214')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_multi_addObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**rm_range)
        rc &= LAddrOBJ.config_addressobject(**rm_range_2)
        rc &= LAddrOBJ.config_addressobject(**rm_range_3)
        Assertion.assert_equal(rc, True, 'Add AO for DUT Failed.')

    def test_03_add_multi_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**Lvpn_1)
        rc &= Lvpn_obj.add_vpn_policy(**Lvpn_2)
        rc &= Lvpn_obj.add_vpn_policy(**Lvpn_3)
        Assertion.assert_equal(rc, True, 'Add 3 VPN Policy Failed.')

    def test_04_show_auto_added_rules_enable(self):
        rc1 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range', True)
        rc1 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range', 'X0 Subnet', True)
        rc2 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range_2', True)
        rc2 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range_2', 'X0 Subnet', True)
        rc3 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range_3', True)
        rc3 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range_3', 'X0 Subnet', True)
        logger.info(rc1,rc2,rc3)
        Assertion.assert_equal(rc1&rc2&rc3, True, 'check auto added rules Failed.')

    def test_05_disable_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('disable S2S VPN'))
        rc = Lvpn_obj.dis_s2svpn_policy(**Lvpn_1)
        rc &= Lvpn_obj.dis_s2svpn_policy(**Lvpn_2)
        rc &= Lvpn_obj.dis_s2svpn_policy(**Lvpn_3)
        Assertion.assert_equal(rc, True, 'disable VPN Policy Failed.')

    def test_06_show_auto_added_rules_disable(self):
        rc1 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range', False)
        rc1 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range', 'X0 Subnet', False)
        rc2 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range_2', False)
        rc2 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range_2', 'X0 Subnet', False)
        rc3 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range_3', False)
        rc3 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range_3', 'X0 Subnet', False)
        Assertion.assert_equal(rc1&rc2&rc3, True, 'check auto added rules disabled Failed.')

    def test_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_08_delete_addObj(self):
        rc = LAddrOBJ.del_ao_by_name(rm_range['name'], version='ipv4')
        rc &= LAddrOBJ.del_ao_by_name(rm_range_2['name'], version='ipv4')
        rc &= LAddrOBJ.del_ao_by_name(rm_range_3['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete 3 VPN Policy Failed.')


class TestMOBIKE_TP2581_TC17(Test):
    uuid = "SOSAIOT-TC-54218"
    description = show_testcase_info(TESTPLAN, '1714215', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1714215')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_addObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**rm_range)
        Assertion.assert_equal(rc, True, 'Add AO for DUT Failed.')
    
    def test_03_add_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Add first VPN Policy Failed.')

    def test_04_show_auto_added_lan2vpn_rules(self):
        logger.info('check LAN to VPN auto added rule')
        rc = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range', True)
        rc &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range', 'X0 Subnet', True)
        Assertion.assert_equal(rc, True, 'check auto added rules Failed.')

    def test_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')
    
    def test_06_delete_addObj(self):
        logger.info('-'*10+'delete ao'+'-'*10)
        rc = LAddrOBJ.del_ao_by_name(rm_range['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete AO Failed.')

    def test_07_check_auto_added_lan2vpn_rules_deleted(self):
        logger.info('check LAN to VPN auto added rule')
        rc = check_access_rule.check_auto_access_rule_deleted('LAN', 'VPN', 'X0 Subnet', 'remote_range')
        rc &= check_access_rule.check_auto_access_rule_deleted('VPN', 'LAN', 'remote_range', 'X0 Subnet')
        Assertion.assert_equal(rc, True, 'check auto added rules Failed.')


class TestMOBIKE_TP2581_TC18(Test):
    uuid = "SOSAIOT-TC-54219"
    description = show_testcase_info(TESTPLAN, '1714216', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1714216')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_multi_addObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**rm_host)
        rc &= LAddrOBJ.config_addressobject(**rm_net)
        rc &= LAddrOBJ.config_addressobject(**rm_range)
        Assertion.assert_equal(rc, True, 'Add AO for DUT Failed.')

    def test_03_add_multi_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**Lvpn_rmhost)
        rc &= Lvpn_obj.add_vpn_policy(**Lvpn)
        rc &= Lvpn_obj.add_vpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Add 3 VPN Policy Failed.')

    def test_04_show_auto_added_rules_enable(self):
        rc1 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_host', True)
        rc1 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_host', 'X0 Subnet', True)
        rc2 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_net', True)
        rc2 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_net', 'X0 Subnet', True)
        rc3 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range', True)
        rc3 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range', 'X0 Subnet', True)
        logger.info(rc1,rc2,rc3)
        Assertion.assert_equal(rc1&rc2&rc3, True, 'check auto added rules Failed.')

    def test_05_disable_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('disable S2S VPN'))
        rc = Lvpn_obj.dis_s2svpn_policy(**Lvpn_rmhost)
        rc &= Lvpn_obj.dis_s2svpn_policy(**Lvpn)
        rc &= Lvpn_obj.dis_s2svpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'disable VPN Policy Failed.')

    def test_06_show_auto_added_rules_disable(self):
        rc1 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_host', False)
        rc1 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_host', 'X0 Subnet', False)
        rc2 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_net', False)
        rc2 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_net', 'X0 Subnet', False)
        rc3 = check_access_rule.check_auto_access_rule('LAN', 'VPN', 'X0 Subnet', 'remote_range', False)
        rc3 &= check_access_rule.check_auto_access_rule('VPN', 'LAN', 'remote_range', 'X0 Subnet', False)
        Assertion.assert_equal(rc1&rc2&rc3, True, 'check auto added rules disabled Failed.')

    def test_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_08_delete_addObj(self):
        rc = LAddrOBJ.del_ao_by_name(rm_host['name'], version='ipv4')
        rc &= LAddrOBJ.del_ao_by_name(rm_net['name'], version='ipv4')
        rc &= LAddrOBJ.del_ao_by_name(rm_range['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete 3 VPN Policy Failed.')

from definition.settings import *
from definition import check_traffic


class Test_SHA512_Support_VPN_TP2628_01(Test):
    uuid = "SOSAIOT-TC-54646"
    description = show_testcase_info(TESTPLAN, '1531193', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1531193')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(Lvpn)
        rc = Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        res = Lvpn_obj.show_s2svpnpolicy()
        ref = res['vpn']['policy'][0]['ipv4']['site_to_site']['proposal']
        if  ref['ipsec']['authentication']['sha_512'] and 'sha-512'== ref['ike']['authentication']:
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check auth Failed.')

    def test_02_add_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_auth'] = 'sha-384'
        ref1['ipsec_auth'] = 'sha_384'
        rc = Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        res = Lvpn_obj.show_s2svpnpolicy()
        ref = res['vpn']['policy'][0]['ipv4']['site_to_site']['proposal']
        if  ref['ipsec']['authentication']['sha_384'] and 'sha-384'== ref['ike']['authentication']:
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')
        Assertion.assert_equal(rc, True, 'add VPN Policy and check auth Failed.')

    def test_03_add_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(Lvpn_TI)
        ref1['ike_auth'] = 'sha-384'
        ref1['ipsec_auth'] = 'sha_384'
        rc = Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        res = Lvpn_obj.show_tunnelvpnpolicy()
        ref = res['vpn']['policy'][0]['ipv4']['tunnel_interface']['proposal']
        if  ref['ipsec']['authentication']['sha_384'] and 'sha-384'== ref['ike']['authentication']:
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')
        Assertion.assert_equal(rc, True, 'add VPN Policy and check auth Failed.')

    def test_04_edit_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(Lvpn_TI)
        logger.info(" {} ".center(20, '*').format('edit Local VPN Policy'))
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        res = Lvpn_obj.show_tunnelvpnpolicy()
        ref = res['vpn']['policy'][0]['ipv4']['tunnel_interface']['proposal']
        if  ref['ipsec']['authentication']['sha_512'] and 'sha-512'== ref['ike']['authentication']:
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')
        Assertion.assert_equal(rc, True, 'edit VPN Policy and check auth Failed.')

    
class Test_SHA512_Support_VPN_TP2628_02(Test):
    uuid = "SOSAIOT-TC-54647"
    description = show_testcase_info(TESTPLAN, '1531194', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1531194')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_02_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(LVPN_edit)
        ref2 = copy.deepcopy(RVPN_edit)
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        rc &= Rvpn_obj.edit_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_03_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_04_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(LVPN_edit)
        ref2 = copy.deepcopy(RVPN_edit)
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        rc &= Rvpn_obj.edit_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_05_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'main'
        ref2['ike_exchange'] = 'main'
        ref1['ipsec_auth'] = 'sha_384'
        ref2['ipsec_auth'] = 'sha_384'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_06_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(LVPN_edit)
        ref2 = copy.deepcopy(RVPN_edit)
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        rc &= Rvpn_obj.edit_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')


class Test_SHA512_Support_VPN_TP2628_03(Test):
    uuid = "SOSAIOT-TC-54648"
    description = show_testcase_info(TESTPLAN, '1531195', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1531195')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_02_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(LVPN_edit)
        ref2 = copy.deepcopy(RVPN_edit)
        ref1['auth_mode'] = 'certificate'
        ref2['auth_mode'] = 'certificate'
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        rc &= Rvpn_obj.edit_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_03_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_04_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(LVPN_edit)
        ref2 = copy.deepcopy(RVPN_edit)
        ref1['auth_mode'] = 'certificate'
        ref2['auth_mode'] = 'certificate'
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        rc &= Rvpn_obj.edit_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_05_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        ref1['ike_exchange'] = 'main'
        ref2['ike_exchange'] = 'main'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_06_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(LVPN_edit)
        ref2 = copy.deepcopy(RVPN_edit)
        ref1['auth_mode'] = 'certificate'
        ref2['auth_mode'] = 'certificate'
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        rc &= Rvpn_obj.edit_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')


class Test_SHA512_Support_VPN_TP2628_04(Test):
    uuid = "SOSAIOT-TC-54649"
    description = show_testcase_info(TESTPLAN, '1531196', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1531196')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI_Manual)
        ref2 = copy.deepcopy(Rvpn_TI_Manual)
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        ref1['authentication_key'] = '7023a13a19b79295daf059a2ca00f4db3b60114c'*3+'7023a13a'
        ref2['authentication_key'] = '7023a13a19b79295daf059a2ca00f4db3b60114c'*3+'7023a13a'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_02_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI_Manual)
        ref2 = copy.deepcopy(Rvpn_TI_Manual)
        ref1['ipsec_auth'] = 'sha_384'
        ref2['ipsec_auth'] = 'sha_384'
        ref1['authentication_key'] = '7023a13a19b79295daf059a2ca00f4db3b60114c7023a13a19b79295daf059a2ca00f4db3b60114c7023a13a19b79295'
        ref2['authentication_key'] = '7023a13a19b79295daf059a2ca00f4db3b60114c7023a13a19b79295daf059a2ca00f4db3b60114c7023a13a19b79295'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_03_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI)
        ref2 = copy.deepcopy(Rvpn_TI)
        ref1['ike_exchange'] = 'ikev2'
        ref2['ike_exchange'] = 'ikev2'
        ref1['ike_auth'] = 'sha-384'
        ref2['ike_auth'] = 'sha-384'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_04_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI)
        ref2 = copy.deepcopy(Rvpn_TI)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        ref1['ike_auth'] = 'sha-384'
        ref2['ike_auth'] = 'sha-384'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_05_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI)
        ref2 = copy.deepcopy(Rvpn_TI)
        ref1['ike_auth'] = 'sha-384'
        ref2['ike_auth'] = 'sha-384'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_06_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI_cert)
        ref2 = copy.deepcopy(Rvpn_TI_cert)
        ref1['ike_exchange'] = 'main'
        ref2['ike_exchange'] = 'main'
        ref1['ike_auth'] = 'sha-384'
        ref2['ike_auth'] = 'sha-384'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_07_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI_cert)
        ref2 = copy.deepcopy(Rvpn_TI_cert)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        ref1['ike_auth'] = 'sha-384'
        ref2['ike_auth'] = 'sha-384'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_08_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI_cert)
        ref2 = copy.deepcopy(Rvpn_TI_cert)
        ref1['ike_auth'] = 'sha-384'
        ref2['ike_auth'] = 'sha-384'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    
class Test_SHA512_Support_VPN_TP2628_05(Test):
    uuid = "SOSAIOT-TC-54650"
    description = show_testcase_info(TESTPLAN, '1531197', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1531197')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_group_edit_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(groupvpn_dict)
        ref1['ike_auth'] = 'sha-384'
        ref1['ipsec_auth'] = 'sha_384'
        logger.info(" {} ".center(20, '*').format('edit Local group VPN Policy'))
        rc = Lvpn_obj.edit_wangroup_vpn_policy(**ref1)
        res = Lvpn_obj.show_wangroup_vpn()
        ref = res['vpn']['policy'][0]['ipv4']['group_vpn']['proposal']
        if  ref['ipsec']['authentication']['sha_384'] and 'sha-384'== ref['ike']['authentication']:
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')
        Assertion.assert_equal(rc, True, 'edit group VPN Policy and check auth Failed.')

    def test_02_group_edit_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(groupvpn_dict)
        logger.info(" {} ".center(20, '*').format('edit Local group VPN Policy'))
        rc = Lvpn_obj.edit_wangroup_vpn_policy(**ref1)
        res = Lvpn_obj.show_wangroup_vpn()
        ref = res['vpn']['policy'][0]['ipv4']['group_vpn']['proposal']
        if  ref['ipsec']['authentication']['sha_512'] and 'sha-512'== ref['ike']['authentication']:
        # if 'sha_512' in str(res) and 'sha-512' in str(res):
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')
        Assertion.assert_equal(rc, True, 'edit group VPN Policy and check auth Failed.')
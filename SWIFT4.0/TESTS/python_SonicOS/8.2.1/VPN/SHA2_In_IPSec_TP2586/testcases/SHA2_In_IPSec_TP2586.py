from definition.settings import *
from definition import check_traffic


class Test_SHA2_In_IPSec_TP2586_01(Test):
    uuid = "SOSAIOT-TC-54635"
    description = show_testcase_info(TESTPLAN, '1511552', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1511552')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(Lvpn)
        rc = Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        res = Lvpn_obj.show_s2svpnpolicy()
        res2 = Lvpn_obj.get_vpn_all_status_info(policyname='vpn1')
        logger.info(f'-------{res2}')
        ref = res['vpn']['policy'][0]['ipv4']['site_to_site']['proposal']
        ref2 = res2['cryptoSuite']
        if 'AES-128/HMAC SHA256' in ref2 and ref['ipsec']['authentication']['sha_256'] and 'sha-256'== ref['ike']['authentication']:
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')

        Assertion.assert_equal(rc, True, 'Add VPN Policy and check auth Failed.')


    
class Test_SHA2_In_IPSec_TP2586_02(Test):
    uuid = "SOSAIOT-TC-54637"
    description = show_testcase_info(TESTPLAN, '1511554', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1511554')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES_CBC-128; HMAC_SHA256_128' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_02_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES-128; HMAC_SHA256' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_03_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'main'
        ref2['ike_exchange'] = 'main'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES-128; HMAC_SHA256' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')


class Test_SHA2_In_IPSec_TP2586_03(Test):
    uuid = "SOSAIOT-TC-54638"
    description = show_testcase_info(TESTPLAN, '1511555', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1511555')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES_CBC-128; HMAC_SHA256_128' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')


    def test_02_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES-128; HMAC_SHA256' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')


    def test_03_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        ref1['ike_exchange'] = 'main'
        ref2['ike_exchange'] = 'main'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES-128; HMAC_SHA256' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')


class Test_SHA2_In_IPSec_TP2586_04(Test):
    uuid = "SOSAIOT-TC-54639"
    description = show_testcase_info(TESTPLAN, '1511556', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1511556')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_TI_Manual)
        ref2 = copy.deepcopy(Rvpn_TI_Manual)
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
        ref1 = copy.deepcopy(Lvpn_TI_cert)
        ref2 = copy.deepcopy(Rvpn_TI_cert)
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

    def test_05_add_vpn_policy_and_check_traffic(self):
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

    def test_06_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_Manual)
        ref2 = copy.deepcopy(Rvpn_Manual)
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')


class Test_SHA2_In_IPSec_TP2586_05(Test):
    uuid = "SOSAIOT-TC-54641"
    description = show_testcase_info(TESTPLAN, '1511558', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1511558')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['ipsec_auth'] = 'aes_xcbc'
        rc = Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        res = Lvpn_obj.show_s2svpnpolicy()
        res2 = Lvpn_obj.get_vpn_all_status_info(policyname='vpn1')
        logger.info(f'-------{res2}')
        ref = res['vpn']['policy'][0]['ipv4']['site_to_site']['proposal']
        ref2 = res2['cryptoSuite']
        if 'AES-128/HMAC AES-XCBC-96' in ref2 and ref['ipsec']['authentication']['aes_xcbc'] :
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check auth Failed.')


class Test_SHA2_In_IPSec_TP2586_06(Test):
    uuid = "SOSAIOT-TC-54642"
    description = show_testcase_info(TESTPLAN, '1511559', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1511559')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(Lvpn)
        # ref1['ipsec_auth'] = 'aes_xcbc'
        rc = Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check auth Failed.')

    def test_02_Export_and_Import_Prefs(self):
        logger.info(" {} ".center(20, '-').format('Export and Import Prefs '))
        rc = Lsetting.export_setting_exp(filepath='/tmp/prefs_module')
        time.sleep(5)
        rc &= Lvpn_obj.edit_vpn_policy(**LVPN_edit)
        res = Lvpn_obj.show_s2svpnpolicy()
        ref = res['vpn']['policy'][0]['ipv4']['site_to_site']['proposal']
        if ref['ipsec']['authentication']['aes_xcbc']:
            rc &=True
        else:
            rc &= False
        rc &= Lsetting.import_setting_exp(filepath='/tmp/prefs_module')
        Assertion.assert_equal(rc, True, "ERR: Export and Import Prefs failed") 

    def test_03_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        ref = res['vpn']['policy'][0]['ipv4']['site_to_site']['proposal']
        rc = True if ref['ipsec']['authentication']['sha_256'] else False
        Assertion.assert_equal(rc, True, "ERR: Check VPN Policy  failed") 


class Test_SHA2_In_IPSec_TP2586_07(Test):
    uuid = "SOSAIOT-TC-54643"
    description = show_testcase_info(TESTPLAN, '1511560', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1511560')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES_CBC-128; HMAC_SHA256_128' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_02_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES-128; HMAC_SHA256' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')

    def test_03_add_vpn_policy_and_check_traffic(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        ref1['ike_exchange'] = 'main'
        ref2['ike_exchange'] = 'main'
        rc = Lvpn_obj.del_all_vpn_policies()
        rc &= Rvpn_obj.del_all_vpn_policies()
        logger.info('clear log')
        LogObj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        time.sleep(10)
        rc &= check_traffic.ping_from_local_to_remote()
        logger.info('check log ')
        res = LogObj.show_log()
        if 'negotiation complete' in str(res) and 'AES-128; HMAC_SHA256' in str(res):
            rc &= True
            logger.info('check log success!!')
        else:
            rc &= False
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check traffic Failed.')


class Test_SHA2_In_IPSec_TP2586_08(Test):
    uuid = "SOSAIOT-TC-54645"
    description = show_testcase_info(TESTPLAN, '1511562', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1511562')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_and_check_auth(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['pri_gate'] = '0.0.0.0'
        rc = Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        res = Lvpn_obj.show_s2svpnpolicy()
        ref = res['vpn']['policy'][0]['ipv4']['site_to_site']
        if  ref['proposal']['ipsec']['authentication']['sha_256'] and ref['gateway']['primary'] == '0.0.0.0' :
            rc &= True
        else:
            rc &= False
            logger.info('check auth failed !!!')
        Assertion.assert_equal(rc, True, 'Add VPN Policy and check auth Failed.')

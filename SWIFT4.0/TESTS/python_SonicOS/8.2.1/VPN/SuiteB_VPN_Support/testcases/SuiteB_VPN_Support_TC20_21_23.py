from definition.settings import *


class TestSuiteB_VPN_Support_20(Test):
    uuid = "SOSAIOT-TC-54659"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_20_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_20_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_presh)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_20_02_check_tsr(self):
        tsr_content = tsr_obj.get_tsr_part(func="VPN",lab1="Settings")
        logger.info(tsr_content)
        if not tsr_content:
            rc = False
        else:
            if re.search('VPN Policy Name\s+: "vpn1"; enabled', tsr_content, re.I | re.S | re.M):
                rc = True
            else:
                rc = False
            Assertion.assert_equal(rc, True, "ERR: VPN1 setting not in tsr.")


    def test_20_03_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn_presh)
        Assertion.assert_equal(rc,True,'Remove VPN Policy Failed.')


class TestSuiteB_VPN_Support_21(Test):
    uuid = "SOSAIOT-TC-54660"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_21_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_21_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_presh)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_21_02_export_preference(self):
        rc = setting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export the settings...")

    def test_21_03_import_Perference(self):
        rc = setting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to import the settings...")

    def test_21_04_show_vpn_policy(self):
        resp = Lvpn_obj.show_s2svpnpolicy()
        if re.search('vpn1', str(resp), re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "Error: show vpn policy failed.")

    def test_21_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn_presh)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestSuiteB_VPN_Support_23(Test):
    uuid = "SOSAIOT-TC-54661"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_23_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_23_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_23_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_presh)
        ref2 = copy.deepcopy(Rvpn_presh)
        ref1['ike_dh_group'] = '2'
        ref1['ipsec_encryption'] = 'aes_128'
        ref1['ipsec_pfs_dhgroup'] = '2'
        ref2['ike_dh_group'] = '19'
        ref2['ipsec_encryption'] = 'aes_256'
        ref2['ipsec_pfs_dhgroup'] = '19'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_23_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_23_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(5)
        log = str(LogObj.export_log_txt(log_switch=False))
        if re.search('NO_PROPOSAL_CHOSEN', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            rc = False
            logger.info(log)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_23_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn_presh)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn_presh)
        Assertion.assert_equal(rc1&rc2, True, 'Remove VPN Policy Failed.')


class TestSuiteB_VPN_Support_34(Test):
    uuid = "SOSAIOT-TC-52344"
    description = show_testcase_info(TESTPLAN, '34', description=True)['title']

    def test_34_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_34_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_34_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_presh)
        ref2 = copy.deepcopy(Rvpn_presh)
        ref1['ike_dh_group'] = '2'
        ref1['ipsec_encryption'] = 'aes_128'
        ref1['ipsec_pfs_dhgroup'] = '19'
        ref2['ike_dh_group'] = '2'
        ref2['ipsec_encryption'] = 'aes_128'
        ref2['ipsec_pfs_dhgroup'] = '19'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_34_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_34_04_reboot_fw(self):
        rc = LRestartObj.restart_now()
        Assertion.assert_equal(rc, True, "ERR: restart fw failed")

    def test_34_05_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = False
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_34_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn_presh)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn_presh)
        Assertion.assert_equal(rc1&rc2, True, 'Remove VPN Policy Failed.')


class TestSuiteB_VPN_Support_35(Test):
    uuid = "SOSAIOT-TC-52344"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_34_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_35_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret is None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_35_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_presh)
        ref2 = copy.deepcopy(Rvpn_presh)
        ref1['ike_dh_group'] = '2'
        ref1['ipsec_encryption'] = 'aes_128'
        ref1['ipsec_pfs_dhgroup'] = '19'
        ref2['ike_dh_group'] = '2'
        ref2['ipsec_encryption'] = 'aes_128'
        ref2['ipsec_pfs_dhgroup'] = '19'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_35_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = False
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_35_04_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn_presh)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn_presh)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')

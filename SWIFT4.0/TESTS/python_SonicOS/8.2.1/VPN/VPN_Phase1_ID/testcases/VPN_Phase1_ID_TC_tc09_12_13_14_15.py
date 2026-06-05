from definition.settings import *


class TestVPN_Phase1_ID_09(Test):
    uuid = "SOSAIOT-TC-54582"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
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
        ref1['local_ike_type'] = 'ipv4'
        ref1['peer_ike_type'] = 'ipv4'
        ref1['local_ike_id'] = 'test'
        ref1['peer_ike_id'] = Parameter.REMOTEX0
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        resp = Lvpn_obj.add_vpn_policy(**ref1, msg=True)
        logger.info(resp)
        if re.search('Schema validation error: property \'ipv4\': invalid format', str(resp[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')


class TestVPN_Phase1_ID_12(Test):
    uuid = "SOSAIOT-TC-54570"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
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
        ref1['local_ike_type'] = 'domain'
        ref1['peer_ike_type'] = 'domain'
        ref1['local_ike_id'] = 'test'
        ref1['peer_ike_id'] = ''
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        resp = Lvpn_obj.add_vpn_policy(**ref1, msg=True)
        logger.info(resp)
        if re.search('property \'local\' can\'t be empty object', str(resp[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')


class TestVPN_Phase1_ID_13(Test):
    uuid = "SOSAIOT-TC-54571"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
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
        ref1['local_ike_type'] = 'email_address'
        ref1['peer_ike_type'] = 'email_address'
        ref1['local_ike_id'] = ''
        ref1['peer_ike_id'] = 'test@test.com'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        resp = Lvpn_obj.add_vpn_policy(**ref1, msg=True)
        logger.info(resp)
        if re.search('Local IKE ID not configured', str(resp[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    # def test_01_03_remove_vpn_policy(self):
    #     logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
    #     rc = Lvpn_obj.del_s2svpn_policy(**Lvpn)
    #     Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_01_04_add_vpn_policy2(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['local_ike_type'] = 'email_address'
        ref1['peer_ike_type'] = 'email_address'
        ref1['local_ike_id'] = 'test@test.com'
        ref1['peer_ike_id'] = ''
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        resp = Lvpn_obj.add_vpn_policy(**ref1, msg=True)
        logger.info(resp)
        if re.search('Peer IKE ID not configured', str(resp[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')


class TestVPN_Phase1_ID_14(Test):
    uuid = "SOSAIOT-TC-54572"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
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
        ref1['local_ike_type'] = 'firewall_id'
        ref1['peer_ike_type'] = 'domain'
        ref1['local_ike_id'] = ''
        ref1['peer_ike_id'] = 'test@test.com'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        resp = Lvpn_obj.add_vpn_policy(**ref1, msg=True)
        logger.info(resp)
        if re.search('property \'peer\' can\'t be empty object', str(resp[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_01_03_add_vpn_policy2(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['local_ike_type'] = 'firewall_id'
        ref1['peer_ike_type'] = 'domain'
        ref1['local_ike_id'] = local_fwid
        ref1['peer_ike_id'] = ''
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        resp = Lvpn_obj.add_vpn_policy(**ref1, msg=True)
        logger.info(resp)
        if re.search('property \'peer\' can\'t be empty object', str(resp[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')


class TestVPN_Phase1_ID_15(Test):
    uuid = "SOSAIOT-TC-54566"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
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
        ref1['local_ike_type'] = 'ipv4'
        ref1['peer_ike_type'] = 'ipv4'
        ref1['local_ike_id'] = ''
        ref1['peer_ike_id'] = Parameter.REMOTEX0
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_01_03_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

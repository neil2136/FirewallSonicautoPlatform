from definition.settings import *
from bin import check_traffic
from bin import conf_pri_gw
from bin import packet_monitor


globals()
reg1 = 'IKEv2 Accept IKE SA Proposal'
reg2 = 'VPN Policy.*3DES.*HMAC_SHA1_96'
reg3 = 'IKEv2 InitSPI.*IKEv2 RespSPI'
reg4 = 'IKEv2 Accept IPSec SA Proposal'
reg5 = 'IKEv2 negotiation complete'
reg6 = 'Local Net.*Remote Net'
reg7 = 'IKEv2.*delete IPsec SA request'
reg8 = 'IKEv2.*delete IPsec SA response'
reg9 = 'IKEv2.*delete IKE SA request'
reg10 = 'IKEv2.*delete IKE SA response'
reg11 = 'IKEv2.*Initiator.*Send CREATE_CHILD_SA request'
reg12 = 'IKEv2.*Initiator.*Received CREATE_CHILD_SA response'
reg13 = 'IKEv2 Received notify error payload'
reg14 = 'IKEv2 Initiator: Remote party timeout - Retransmitting IKEv2 request'
reg15 = 'IKEv2.*Initiator: Send IKE_SA_INIT request'
reg16 = 'Tunnel Down'
reg17 = 'IKEv2 IKE proposal does not match'
reg18 = 'IKEv2 Payload processing error'
reg19 = 'Received notify. NO_PROPOSAL_CHOSEN'
reg20 = 'Encryption algorithm mismatch'
reg21 = 'IKEv2 Received Notify Error Payload'
check_list_1_2_14 = [reg1, reg2, reg3, reg4, reg5, reg6]
check_list_6_21 = [reg13]
check_list_7 = [reg1, reg2, reg3, reg4, reg5, reg6, reg11, reg12]
check_list_9_10_11 = [reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10]
check_list_15 = [reg1, reg2, reg3, reg4, reg5, reg6, reg14, reg15, reg16]
check_list_22 = [reg17, reg18]
check_list_23 = [reg19]
check_list_24 = [reg21]
check_list_25 = [reg17, reg18, reg21]


class TestIKEv2_TP778_01(Test):
    uuid = "SOSAIOT-TC-54345"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_01_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_01_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_05_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_1_2_14)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_02(Test):
    uuid = "SOSAIOT-TC-54353"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_02_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_03_ping_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_02_05_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_1_2_14)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_02_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_06(Test):
    uuid = "SOSAIOT-TC-54376"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_06_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_06_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_06_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_dh_group'] = '2'
        ref2['ike_dh_group'] = '5'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_06_03_check_ping_failed(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: check block ping failed")

    def test_06_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_6_21)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_06_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_07(Test):
    uuid = "SOSAIOT-TC-54377"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_07_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_07_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_07_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '120'
        ref1['ipsec_lifetime'] = '300'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_07_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_07_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(4)
    def test_07_05_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_7)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_07_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_09(Test):
    uuid = "SOSAIOT-TC-54366"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_09_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_09_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '140'
        ref1['ipsec_lifetime'] = '120'
        ref2['ike_lifetime'] = '140'
        ref2['ipsec_lifetime'] = '120'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_09_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_09_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(5)
    def test_09_05_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_9_10_11)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_09_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_10(Test):
    uuid = "SOSAIOT-TC-54346"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_10_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '120'
        ref1['ipsec_lifetime'] = '120'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_10_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(4)
    def test_10_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_9_10_11)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_11(Test):
    uuid = "SOSAIOT-TC-54347"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_11_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_11_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '120'
        ref1['ipsec_lifetime'] = '120'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_11_03_ping_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(4)
    def test_11_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_9_10_11)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_11_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_12(Test):
    uuid = "SOSAIOT-TC-54348"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_12_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_12_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_12_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '140'
        ref1['ipsec_lifetime'] = '140'
        ref2['ike_lifetime'] = '120'
        ref2['ipsec_lifetime'] = '120'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_12_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(4)
    def test_12_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_9_10_11)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_12_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_13(Test):
    uuid = "SOSAIOT-TC-54349"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_13_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_13_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_13_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '140'
        ref1['ipsec_lifetime'] = '140'
        ref2['ike_lifetime'] = '120'
        ref2['ipsec_lifetime'] = '120'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_13_03_ping_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(4)
    def test_13_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_9_10_11)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_13_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_14(Test):
    uuid = "SOSAIOT-TC-54350"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_14_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_14_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_14_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['keep_alive'] = True
        ref1['ike_lifetime'] = '600'
        ref1['ipsec_lifetime'] = '600'
        ref2['ike_lifetime'] = '600'
        ref2['ipsec_lifetime'] = '600'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_14_03_ping_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_14_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_1_2_14)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_14_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_15(Test):
    uuid = "SOSAIOT-TC-54351"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_15_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_15_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_15_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '600'
        ref1['ipsec_lifetime'] = '600'
        ref2['ike_lifetime'] = '600'
        ref2['ipsec_lifetime'] = '600'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_15_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_15_04_diable_remote_X1(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        time.sleep(60)
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_15_05_check_ping_failed(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: check block ping failed")

    def test_15_06_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_1_2_14)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_15_07_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_15_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_16(Test):
    uuid = "SOSAIOT-TC-54371"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_16_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_16_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_16_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['keep_alive'] = True
        ref1['ike_lifetime'] = '600'
        ref1['ipsec_lifetime'] = '600'
        ref2['ike_lifetime'] = '600'
        ref2['ipsec_lifetime'] = '600'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_16_03_ping_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_16_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_1_2_14)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_16_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_17(Test):
    uuid = "SOSAIOT-TC-54372"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_17_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_17_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_17_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '600'
        ref1['ipsec_lifetime'] = '600'
        ref2['ike_lifetime'] = '600'
        ref2['ipsec_lifetime'] = '600'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_17_03_ping_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_17_04_diable_remote_X1(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.disable_pri_gw()
        time.sleep(60)
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_17_05_check_ping_failed(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: check block ping failed")

    def test_17_06_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_1_2_14)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_17_07_recover_primary_gw(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = conf_pri_gw.enable_pri_gw()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_17_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_21(Test):
    uuid = "SOSAIOT-TC-54373"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_21_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_21_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_21_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_dh_group'] = '1'
        ref1['ipsec_pfs_dhgroup'] = '2'
        ref1['keep_alive'] = True
        ref2['ike_dh_group'] = '2'
        ref2['ipsec_pfs_dhgroup'] = '2'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_21_03_check_ping_failed(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: check block ping failed")

    def test_21_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_6_21)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_21_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_22(Test):
    uuid = "SOSAIOT-TC-54374"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_22_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_22_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_22_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_dh_group'] = '1'
        ref1['ike_auth'] = 'sha-1'
        ref1['ike_encryption'] = 'aes-128'
        ref2['ike_dh_group'] = '2'
        ref2['ike_auth'] = 'md5'
        ref2['ike_encryption'] = 'triple-des'
        ref2['keep_alive'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_22_03_check_ping_failed(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: check block ping failed")

    def test_22_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_22)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_22_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_23(Test):
    uuid = "SOSAIOT-TC-54375"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_23_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_23_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_23_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'main'
        ref1['keep_alive'] = True
        ref2['ike_exchange'] = 'ikev2'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_23_03_check_ping_failed(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: check block ping failed")

    def test_23_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_23)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_23_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_24(Test):
    uuid = "SOSAIOT-TC-54391"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_24_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_24_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_24_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_encryption'] = 'aes-128'
        ref1['ipsec_encryption'] = 'aes-128'
        ref1['keep_alive'] = True
        ref2['ike_encryption'] = 'triple-des'
        ref2['ipsec_encryption'] = 'triple-des'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_24_03_check_ping_failed(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: check block ping failed")

    def test_24_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_24)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_24_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_25(Test):
    uuid = "SOSAIOT-TC-54392"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_25_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_25_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_25_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_auth'] = 'sha-1'
        ref1['ipsec_auth'] = 'sha-1'
        ref2['ike_auth'] = 'md5'
        ref2['ipsec_auth'] = 'md5'
        ref2['keep_alive'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_25_03_check_ping_failed(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: check block ping failed")

    def test_25_04_test_log(self):
        rc = check_traffic.check_test_log_list(check_list_25)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_25_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

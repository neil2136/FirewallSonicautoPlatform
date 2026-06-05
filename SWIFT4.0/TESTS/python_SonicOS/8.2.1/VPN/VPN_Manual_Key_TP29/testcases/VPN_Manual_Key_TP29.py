from definition.settings import *
from definition import check_traffic


class TestVPN_Manual_Key_TP29_01(Test):
    uuid = "SOSAIOT-TC-54489"
    description = show_testcase_info(TESTPLAN, '1519043', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519043')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc , True, 'Add VPN Policy Failed.')

    @repeat_method(3)
    def test_02_check_traffic_and_pkg(self):
        LpacketObj.clear_packets()
        LpacketObj.start_capture()
        rc = check_traffic.ping_traffic(PC1,PC2_eth0)
        time.sleep(5)
        LpacketObj.stop_capture()
        res = LpacketObj.export_captured_packets()
        logger.info(f'-------{res}')
        if 'IP Type: ESP' in str(res):
            rc &= True
        else:
            rc &=False
        Assertion.assert_equal(rc, True, "ERR: check ping and  esp pkg failed")

    @repeat_method(3)
    def test_03_check_active_tunnel(self):
        time.sleep(10)
        res1 = Lvpn_obj.get_active_vpn_tunnels()
        if res1[0]['policyName'] =='vpn1':
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check active vpn tunnel  failed")

# ###bug GEN7-49324
# class TestVPN_Manual_Key_TP29_02(Test):
#     uuid = "1519045"
#     jira = 'GEN7-49324'
#     description = show_testcase_info(TESTPLAN, '1519045', description=True)['title']

#     def test_01_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '1519045')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_add_vpn_policy(self):
#         ref1 = copy.deepcopy(Lvpn)
#         ref2 = copy.deepcopy(Rvpn)
#         ref1['pri_gate']=''
#         rc = Rvpn_obj.del_all_vpn_policies()
#         rc &= Lvpn_obj.del_all_vpn_policies()
#         logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
#         rc &= Lvpn_obj.add_vpn_policy(**ref1)
#         logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
#         rc &= Rvpn_obj.add_vpn_policy(**ref2)
#         Assertion.assert_equal(rc , True, 'Add VPN Policy Failed.')

#     @repeat_method(3)
#     def test_02_check_traffic_and_pkg(self):
#         LpacketObj.clear_packets()
#         LpacketObj.start_capture()
#         rc = check_traffic.ping_traffic(PC2_login,PC1_eth0)
#         time.sleep(5)
#         LpacketObj.stop_capture()
#         res = LpacketObj.export_captured_packets()
#         logger.info(f'-------{res}')
#         if 'IP Type: ESP' in str(res):
#             rc &= True
#         else:
#             rc &=False
#         Assertion.assert_equal(rc, True, "ERR: check ping and  esp pkg failed")

#     @repeat_method(3)
#     def test_03_check_active_tunnel(self):
#         time.sleep(10)
#         res1 = Lvpn_obj.get_active_vpn_tunnels()
#         if res1[0]['policyName'] =='vpn1':
#             rc = True
#         else:
#             rc = False
#         Assertion.assert_equal(rc, True, "ERR: check active vpn tunnel  failed")


class TestVPN_Manual_Key_TP29_03(Test):
    uuid = "SOSAIOT-TC-54492"
    description = show_testcase_info(TESTPLAN, '1519046', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519046')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc , True, 'Add VPN Policy Failed.')

    @repeat_method(3)
    def test_02_check_traffic_and_pkg(self):
        LpacketObj.clear_packets()
        LpacketObj.start_capture()
        rc = check_traffic.ping_traffic(PC1,PC2_eth0)
        time.sleep(5)
        LpacketObj.stop_capture()
        res = LpacketObj.export_captured_packets()
        logger.info(f'-------{res}')
        if 'IP Type: ESP' in str(res):
            rc &= True
        else:
            rc &=False
        Assertion.assert_equal(rc, True, "ERR: check ping and  esp pkg failed")

    @repeat_method(3)
    def test_03_check_active_tunnel(self):
        time.sleep(10)
        res1 = Lvpn_obj.get_active_vpn_tunnels()
        if res1[0]['policyName'] =='vpn1':
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check active vpn tunnel  failed")

    def test_04_disable_vpn_policy(self):
        rc = Lvpn_obj.dis_s2svpn_policy(name=Lvpn['name'])
        Assertion.assert_equal(rc, True, "ERR: disable vpn policy failed")

    @repeat_method(3)
    def test_05_check_traffic_and_tunnel(self):
        time.sleep(10)
        rc = check_traffic.ping_traffic(PC1,PC2_eth0)
        rc &= bool(Lvpn_obj.get_active_vpn_tunnels())
        Assertion.assert_equal(rc, False, "ERR: check traffic and active vpn tunnel  failed")

    def test_06_enable_vpn_policy(self):
        rc = Lvpn_obj.en_s2svpn_policy(name=Lvpn['name'])
        Assertion.assert_equal(rc, True, "ERR: enable vpn policy failed")

    @repeat_method(3)
    def test_07_check_traffic_and_tunnel(self):
        time.sleep(10)
        rc = check_traffic.ping_traffic(PC1,PC2_eth0)
        res1 = Lvpn_obj.get_active_vpn_tunnels()
        if res1[0]['policyName'] =='vpn1':
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: check traffic and active vpn tunnel  failed")



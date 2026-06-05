from definition.settings import *
from definition import check_traffic


class Test_VPN_bound_to_VLAN_interface_TP2464_00(Test):
    uuid = "SOSAIOT-TC-54678"
    description = show_testcase_info(TESTPLAN, '1516903', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516903')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['bound_to'] = ['interface',f'X3:V{lx3_tag}']
        rc = Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, "ERR: Add Local VPN Policy failed")

    def test_02_check_bound_to(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        if f'X3:V{lx3_tag}' in str(res):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check vpn policy bound to failed")


class Test_VPN_bound_to_VLAN_interface_TP2464_01(Test):
    uuid = "SOSAIOT-TC-54679"
    description = show_testcase_info(TESTPLAN, '1516904', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516904')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['pri_gate'] = Remote_X2_IPV4
        ref1['sec_gate'] = Remote_X1_IPV4
        ref2['pri_gate'] = DUT_X2_IPV4
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc & rc1 & rc2, True, 'Add VPN Policy Failed.')   

    def test_02_enable_DPD(self):
        rc = Lvpn_adv.config_vpnadvanced(**dpd)
        Assertion.assert_equal(rc , True, 'enable dpd Failed.')  

    def test_03_check_traffic(self):
        rc = check_traffic.ping_traffic(PC2_eth1)
        Assertion.assert_equal(rc, True, "ERR: check ping failed")


class Test_VPN_bound_to_VLAN_interface_TP2464_02(Test):
    uuid = "SOSAIOT-TC-54681"
    description = show_testcase_info(TESTPLAN, '1516906', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516906')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['pri_gate'] = Remote_X2_IPV4
        ref1['sec_gate'] = Remote_X4_IPV4
        ref2['pri_gate'] = DUT_X1_IPV4
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        rc &= Rinterfacev4api.add_interface(**Rv4)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc & rc1 & rc2, True, 'Add VPN Policy Failed.')   

    def test_02_check_traffic(self):
        time.sleep(10)
        rc = check_traffic.ping_traffic(PC2_eth1)
        Assertion.assert_equal(rc, True, "ERR: check ping failed")

    def test_03_disconnect_x2(self):
        rc = Rinterfacev4api.del_interface(**Rv2)
        Assertion.assert_equal(rc, True, "ERR:disconnect x2 and check ping failed")

    def test_04_check_traffic(self):
        time.sleep(15)
        rc = check_traffic.ping_traffic(PC2_eth1)
        Assertion.assert_equal(rc, True, "ERR:add x4 vlan and check ping failed")

    def test_05_restore_env(self):
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        rc &= Rinterfacev4api.del_interface(**Rv4)
        rc &= Rinterfacev4api.add_interface(**Rv2)
        Assertion.assert_equal(rc, True, "ERR:restore env failed")


# class Test_VPN_bound_to_VLAN_interface_TP2464_03(Test):
#     uuid = "1516906"
#     description = show_testcase_info(TESTPLAN, '1516906', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '1516906')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

#     def test_01_add_vpn_policy(self):
#         ref1 = copy.deepcopy(Lvpn)
#         ref2 = copy.deepcopy(Rvpn)
#         ref1['pri_gate'] = Remote_X2_IPV4
#         ref1['sec_gate'] = Remote_X4_IPV4
#         ref2['pri_gate'] = DUT_X2_IPV4
#         rc = Rvpn_obj.del_all_vpn_policies()
#         rc &= Lvpn_obj.del_all_vpn_policies()
#         logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
#         rc1 = Lvpn_obj.add_vpn_policy(**ref1)
#         logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
#         rc2 = Rvpn_obj.add_vpn_policy(**ref2)
#         Assertion.assert_equal(rc & rc1 & rc2, True, 'Add VPN Policy Failed.')   

#     def test_02_check_traffic(self):
#         rc = check_traffic.ping_traffic(PC2_eth1)
#         Assertion.assert_equal(rc, True, "ERR: check ping failed")

#     def test_03_disconnect_x2(self):
#         ref = Rinterfacev4api.get_vlan_interface_status(name='X2',vlan_id=str(rx2_tag))
#         ref['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['ip'] = '12.12.88.201'
#         rc = Rinterfacev4api.edit_interface(interface_name='X2', vlan_id=rx2_tag,**ref)
#         time.sleep(10)
#         rc2 = check_traffic.ping_traffic(PC2_eth1)
#         Assertion.assert_equal(rc&(not rc2), True, "ERR:disconnect x2 and check ping failed")

#     def test_04_add_vlan_x4_check_traffic(self):
#         rc= Rinterfacev4api.add_interface(**Rv4)
#         time.sleep(15)
#         rc &= check_traffic.ping_traffic(PC2_eth1)
#         Assertion.assert_equal(rc, True, "ERR:add x4 vlan and check ping failed")

#     def test_05_restore_env(self):
#         rc = Rvpn_obj.del_all_vpn_policies()
#         rc &= Lvpn_obj.del_all_vpn_policies()
#         rc &= Rinterfacev4api.del_interface(**Rv4)
#         Assertion.assert_equal(rc, True, "ERR:restore env failed")


class Test_VPN_bound_to_VLAN_interface_TP2464_03(Test):
    uuid = "SOSAIOT-TC-54683"
    description = show_testcase_info(TESTPLAN, '1516908', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516908')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['pri_gate'] = Remote_X2_IPV4
        ref1['local_net_type'] = 'any'
        ref2['pri_gate'] = DUT_X1_IPV4
        ref2['remote_net_type'] =  'any'
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc & rc1 & rc2, True, 'Add VPN Policy Failed.')   

    @repeat_method(3)
    def test_02_check_traffic_and_pkg(self):
        LpacketObj.clear_packets()
        LpacketObj.start_capture()
        rc = check_traffic.ping_traffic('yahoo.com')
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
        res2 = Rvpn_obj.get_active_vpn_tunnels()
        if '0.0.0.0 - 255.255.255.255' in str(res1[0]['localNet']) and '0.0.0.0 - 255.255.255.255'  in str(res2[0]['remoteNet']):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check active vpn tunnel  failed")
        

class Test_VPN_bound_to_VLAN_interface_TP2464_04(Test):
    uuid = "SOSAIOT-TC-54680"
    description = show_testcase_info(TESTPLAN, '1516905', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516905')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_config_interface(self):
        rc = Rinterfacev4api.config_interface(**Rx3)
        Assertion.assert_equal(rc, True, "ERR: Config Interface  failed")   

    def test_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['pri_gate'] = Remote_X1_IPV4
        ref1['sec_gate'] = Remote_X2_IPV4
        ref2['pri_gate'] = DUT_X1_IPV4
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc & rc1 & rc2, True, 'Add VPN Policy Failed.')   

    def test_02_check_traffic(self):
        rc = check_traffic.ping_traffic(PC2_eth1)
        Assertion.assert_equal(rc, True, "ERR: check ping failed")

    def test_03_disconnect_x1(self):
        ref = copy.deepcopy(Rx1)
        ref['ip']= '12.12.33.201'
        rc=Rinterfacev4api.config_interface(**ref)
        # rc = Rinterfacev4api.disable_interface(name='X1')
        time.sleep(10)
        rc2 = check_traffic.ping_traffic(PC2_eth1)
        Assertion.assert_equal(rc&(not rc2), True, "ERR:disconnect x1 and check ping failed")

    # def test_04__check_traffic(self):
    #     time.sleep(15)
    #     rc = check_traffic.ping_traffic(PC2_eth1)
    #     Assertion.assert_equal(rc, True, "ERR:check ping failed")





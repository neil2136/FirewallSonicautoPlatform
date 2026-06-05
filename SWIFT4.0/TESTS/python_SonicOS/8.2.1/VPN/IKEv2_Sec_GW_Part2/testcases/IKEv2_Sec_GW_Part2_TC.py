from definition.settings import *
from bin import check_traffic
from bin import conf_pri_gw


class TestIKEv2_Sec_GW_1513006(Test):
    uuid = "SOSAIOT-TC-54425"
    description = show_testcase_info(TESTPLAN, '1513006', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1513006')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['keep_alive'] = True
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_disable_rm_x2_cable(self):
        rc = conf_pri_gw.disable_rm_x2_port()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_03_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_04_test_log(self):
        time.sleep(10)        
        reg1 = 'VPN Policy: vpn1; Falied 5 retries'
        reg2 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
        reg_list = [reg1, reg2]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_05_recover_rm_x2_cable(self):
        LogObj.clear_log()
        rc = conf_pri_gw.enable_rm_x2_port()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_06_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_07_test_log_after_recover_rm_x2_port(self):
        time.sleep(10)        
        reg1 = r'11.11.11.200\s+500\s+12.12.1.201\s+500\s+udp\s+vpn1'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_08_sleep_for_expired(self):
        LogObj.clear_log()
        time.sleep(150)
        Assertion.assert_equal(True, True, "ERR: Test log failed")

    def test_09_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    # @repeat_method(6)
    # def test_10_test_log_after_vpn_expired(self):
    #     time.sleep(10)
    #     reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.2.201'
    #     reg_list = [reg1]
    #     rc = check_traffic.check_test_log(reg_list)
    #     Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_11_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_1513007(Test):
    uuid = "SOSAIOT-TC-54426"
    description = show_testcase_info(TESTPLAN, '1513007', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1513007')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        RLogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['keep_alive'] = True
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    @repeat_method(6)
    def test_02_test_log(self):
        time.sleep(10)
        reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.2.201'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_03_disable_rm_x2_cable(self):
        rc = conf_pri_gw.disable_rm_x2_port()
        time.sleep(20)        
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_04_test_log(self):
        time.sleep(10)        
        reg1 = 'VPN Policy: vpn1; Falied 5 retries'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(6)
    def test_05_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_06_test_log_for_remote(self):
        time.sleep(10)        
        reg1 = r'Tunnel Up. policy 2\(vpn2\).*Reason: IKEv2 IPSec Negotiation Done'
        reg_list = [reg1]
        rc = check_traffic.check_test_log_from_remote(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_07_sleep_for_120s(self):
        LogObj.clear_log()
        RLogObj.clear_log()
        time.sleep(120)        
        Assertion.assert_equal(True, True, "ERR: Test log failed")

    @repeat_method(6)
    def test_08_test_log_for_remote_after_vpn_expired(self):
        time.sleep(10)        
        reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_09_recover_rm_x2_cable(self):
        rc = conf_pri_gw.enable_rm_x2_port()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_10_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_11_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_1513008(Test):
    uuid = "SOSAIOT-TC-54427"
    description = show_testcase_info(TESTPLAN, '1513008', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1513008')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_rm_x2_cable(self):
        rc = conf_pri_gw.disable_rm_x2_port()
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['sec_gate'] = Parameter.REMOTEX3
        ref1['keep_alive'] = True
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_03_ping_from_local_to_remote(self):
        rc = check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_04_test_log(self):
        time.sleep(10)
        reg1 = 'VPN Policy: vpn1; Falied 5 retries'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_05_recover_rm_x2_cable(self):
        LogObj.clear_log()
        rc = conf_pri_gw.enable_rm_x2_port()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_06_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_07_test_log_after_recover_rm_x2_port(self):
        time.sleep(10)
        reg1 = r'11.11.11.200\s+500\s+12.12.2.201\s+500\s+udp\s+vpn1'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_08_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_1513013(Test):
    uuid = "SOSAIOT-TC-54432"
    description = show_testcase_info(TESTPLAN, '1513013', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1513013')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref2['pri_gate'] = '0.0.0.0'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_disable_rm_x2_cable(self):
        rc = conf_pri_gw.disable_rm_x2_port()
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_03_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_04_test_log(self):
        time.sleep(10)
        reg1 = 'VPN Policy: vpn1; Falied 5 retries'
        reg2 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
        reg_list = [reg1,reg2]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_05_recover_rm_x2_cable(self):
        rc = conf_pri_gw.enable_rm_x2_port()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")
    
    def test_06_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_1513014(Test):
    uuid = "SOSAIOT-TC-54433"
    description = show_testcase_info(TESTPLAN, '1513013', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1513013')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_rm_x2_cable(self):
        rc = conf_pri_gw.disable_rm_x2_port()
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['keep_alive'] = True
        ref2['pri_gate'] = '0.0.0.0'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    @repeat_method(6)
    def test_03_test_log(self):
        time.sleep(10)
        reg1 = 'VPN Policy: vpn1; Falied 5 retries'
        reg2 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
        reg_list = [reg1,reg2]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_04_recover_rm_x2_cable(self):
        rc = conf_pri_gw.enable_rm_x2_port()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_05_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_06_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_1513015(Test):
    uuid = "SOSAIOT-TC-54434"
    description = show_testcase_info(TESTPLAN, '1513015', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1513015')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['pri_gate'] = ''
        ref1['sec_gate'] = '1.1.1.1'
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        resp = Lvpn_obj.show_s2svpnpolicy()
        # Assertion.assert_equal(rc, False, 'Add VPN Policy Failed.')
        Assertion.assert_not_regular(str(resp), "vpn1", 'Add VPN Policy Failed.')


class TestIKEv2_Sec_GW_1513021(Test):
    uuid = "SOSAIOT-TC-54440"
    description = show_testcase_info(TESTPLAN, '1513021', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1513021')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        RLogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['preempt_interval'] = '120'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    @repeat_method(6)
    def test_02_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_03_test_log(self):
        time.sleep(10)
        reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.2.201'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_04_disable_rm_x2_cable(self):
        rc = conf_pri_gw.disable_rm_x2_port()
        time.sleep(20)        
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_05_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_06_test_log(self):
        time.sleep(10)        
        reg1 = 'VPN Policy: vpn1; Falied 5 retries'
        reg2 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
        reg_list = [reg1,reg2]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(6)
    def test_07_test_log_for_remote(self):
        time.sleep(10)        
        reg1 = r'Tunnel Up. policy 2\(vpn2\).*Reason: IKEv2 IPSec Negotiation Done'
        reg_list = [reg1]
        rc = check_traffic.check_test_log_from_remote(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_08_recover_rm_x2_cable(self):
        rc = conf_pri_gw.enable_rm_x2_port()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_09_test_log(self):
        time.sleep(10)        
        reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_sleep_for_120s(self):
        LogObj.clear_log()
        RLogObj.clear_log()
        time.sleep(120)        
        Assertion.assert_equal(True, True, "ERR: Test log failed")

    def test_11_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    # @repeat_method(6)
    # def test_12_test_log_for_remote_after_vpn_expired(self):
    #     time.sleep(10)        
    #     reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.2.201'
    #     reg_list = [reg1]
    #     rc = check_traffic.check_test_log(reg_list)
    #     Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_13_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_Sec_GW_1513022(Test):
    uuid = "SOSAIOT-TC-54441"
    description = show_testcase_info(TESTPLAN, '1513022', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1513022')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        RLogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['preempt_secondary_gateway'] = False
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    @repeat_method(6)
    def test_02_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_03_test_log(self):
        time.sleep(10)
        reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.2.201'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_04_disable_rm_x2_cable(self):
        rc = conf_pri_gw.disable_rm_x2_port()
        time.sleep(20)        
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_05_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_06_test_log(self):
        time.sleep(10)        
        reg1 = 'VPN Policy: vpn1; Falied 5 retries'
        reg2 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
        reg_list = [reg1,reg2]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(6)
    def test_07_test_log_for_remote(self):
        time.sleep(10)        
        reg1 = r'Tunnel Up. policy 2\(vpn2\).*Reason: IKEv2 IPSec Negotiation Done'
        reg_list = [reg1]
        rc = check_traffic.check_test_log_from_remote(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_08_recover_rm_x2_cable(self):
        rc = conf_pri_gw.enable_rm_x2_port()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(6)
    def test_09_test_log(self):
        time.sleep(10)        
        reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
        reg_list = [reg1]
        rc = check_traffic.check_test_log(reg_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_sleep_for_120s(self):
        LogObj.clear_log()
        RLogObj.clear_log()
        time.sleep(120)        
        Assertion.assert_equal(True, True, "ERR: Test log failed")

    def test_11_ping_from_local_to_remote(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    # @repeat_method(6)
    # def test_12_test_log_for_remote_after_vpn_expired(self):
    #     time.sleep(10)        
    #     reg1 = r'Tunnel Up. policy 2\(vpn1\).*GW 12.12.1.201'
    #     reg_list = [reg1]
    #     rc = check_traffic.check_test_log(reg_list)
    #     Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_13_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

from definition.settings import *
from definition import check_traffic


class Test_VPN_ESP_Fragmentation_01(Test):
    uuid = "SOSAIOT-TC-54693"
    description = show_testcase_info(TESTPLAN, '1509714', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1509714')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_and_check_Fragment(self):
        rc = Lvpn_adv.config_vpnadvanced(frag_packets=False)
        res = Lvpn_adv.show_vpnadvanced()
        if res['vpn']['frag_packets']['enable'] == False:
            rc &= True
            logger.info('check disable frag_packets')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: disable Fragmented Packet Handling failed")

    def test_02_enable_and_check_Fragment(self):
        rc = Lvpn_adv.config_vpnadvanced(frag_packets=True)
        res = Lvpn_adv.show_vpnadvanced()
        if res['vpn']['frag_packets']['enable'] == True:
            rc &= True
            logger.info('check enable frag_packets')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: enable Fragmented Packet Handling failed")


class Test_VPN_ESP_Fragmentation_02(Test):
    uuid = "SOSAIOT-TC-54699"
    description = show_testcase_info(TESTPLAN, '1532968', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1532968')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_esp(self):
        rc = Rdiag_obj.config_raw_api(stream = "ipsecFragmentAfterEsp=on")
        Assertion.assert_equal(rc, True, "ERR:  enable Fragment VPN packets after applying ESP on diag page failed")
    
    def test_02_send_multiple_length_ping(self):
        rc = check_traffic.ping_traffic(PC2,PC1_eth0,1200)
        rc &= check_traffic.ping_traffic(PC2,PC1_eth0,2800)
        rc &= check_traffic.ping_traffic(PC2,PC1_eth0,2000)
        Assertion.assert_equal(rc, True, "ERR: check ping failed")

    def test_03_restore_env(self):
        rc = Rdiag_obj.config_raw_api(stream = "ipsecFragmentAfterEsp=")
        Assertion.assert_equal(rc, True, "ERR: restore env failed")


class Test_VPN_ESP_Fragmentation_03(Test):
    uuid = "SOSAIOT-TC-54700"
    description = show_testcase_info(TESTPLAN, '1768471', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1768471')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_traffic(self):
        rc = check_traffic.ping_traffic(PC2,PC1_eth0,2800)
        Assertion.assert_equal(rc, True, "ERR: check ping failed")

    def test_02_check_traffic_reverse(self):
        rc = check_traffic.ping_traffic(PC1,PC2_eth0,2800)
        Assertion.assert_equal(rc, True, "ERR: check ping failed")


class Test_VPN_ESP_Fragmentation_04(Test):
    uuid = "SOSAIOT-TC-54701"
    description = show_testcase_info(TESTPLAN, '2023789', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2023789')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_cert)
        ref2 = copy.deepcopy(Rvpn_cert)
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        rc &= Rvpn_obj.add_vpn_policy(**ref2)

    def test_02_check_traffic(self):
        rc = check_traffic.ping_traffic(PC1,PC2_eth0,2800)
        Assertion.assert_equal(rc, True, "ERR: check ping failed")

## uuid = "1509712" need 15700 or 14700



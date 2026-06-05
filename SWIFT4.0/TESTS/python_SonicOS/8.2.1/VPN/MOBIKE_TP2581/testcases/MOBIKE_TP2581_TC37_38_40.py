from definition.settings import *


class TestMOBIKE_TP2581_TC37(Test):
    uuid = "SOSAIOT-TC-54221"
    description = show_testcase_info(TESTPLAN, '1714237', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1714237')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_addObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**rm_range)
        Assertion.assert_equal(rc, True, 'Add AO for DUT Failed.')
    
    def test_02_add_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Add first VPN Policy Failed.')

    def test_03_check_tsr(self):
        PC1_eth1 = OpenS.get_node_interface_ip('PC1', 'eth0')
        tsr_content = tsr_obj.export_tsr(PC1_eth1, 'scp', 'root', 'password')
        rc = False
        try:
            tsr_content = os.popen('cat /root/tsr.wri').read()
            start = 'IKEv2 Settings'
            end = 'IPSec Tunnel Stats'
            vpn_resp = re.search(start + '(.*)' + end, tsr_content, re.I|re.S|re.M).group()
            vpn_list = vpn_resp.split('Policy IPSec Tunnel Stats')
            for vpn_policy in vpn_list:
                if re.search('VPN Policy Name\s+: "vpn1"; enabled', vpn_policy, re.I|re.S|re.M) \
                    and re.search('Use IKEv2 IP Pool     : on', vpn_policy, re.I|re.S|re.M) \
                    and re.search('IP Pool name: remote_range', vpn_policy, re.I|re.S|re.M) \
                    and re.search('Allocated IP Address:', vpn_policy, re.I|re.S|re.M):
                    rc = True
                    logger.info("get ikev2 ip pool policy related configure")
                    break
                else:
                    logger.info("get ikev2 ip pool policy related configure failed")
                    pprint.pprint(vpn_policy)
        except Exception as e: 
            logger.error(repr(e))
        Assertion.assert_equal(rc, True, "ERR: check ikev2 ip pool policy failed.")

    def test_04_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc,True,'Remove VPN Policy Failed.')

    def test_05_delete_addObj(self):
        logger.info('-'*10+'delete ao'+'-'*10)
        rc = LAddrOBJ.del_ao_by_name(rm_range['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete AO Failed.')


class TestMOBIKE_TP2581_TC38(Test):
    uuid = "SOSAIOT-TC-54222"
    description = show_testcase_info(TESTPLAN, '1714238', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1714238')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_addObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**rm_range)
        Assertion.assert_equal(rc, True, 'Add AO for DUT Failed.')
    
    def test_02_add_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Add first VPN Policy Failed.')

    def test_03_export_preference(self):
        rc = setting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export the settings...")

    def test_04_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_05_import_Perference(self):
        rc = setting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to import the settings...")

    def test_06_show_vpn_policy(self):
        resp = Lvpn_obj.show_s2svpnpolicy()
        if re.search('vpn1', str(resp), re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "Error: show vpn policy failed.")

    def test_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_08_delete_addObj(self):
        logger.info('-'*10+'delete ao'+'-'*10)
        rc = LAddrOBJ.del_ao_by_name(rm_range['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete AO Failed.')


class TestMOBIKE_TP2581_TC40(Test):
    uuid = "SOSAIOT-TC-54224"
    description = show_testcase_info(TESTPLAN, '1714241', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1714241')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_addObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**rm_range)
        Assertion.assert_equal(rc, True, 'Add AO for DUT Failed.')
    
    def test_02_add_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Add first VPN Policy Failed.')

    def test_03_reboot_fw(self):
        rc = LRestartObj.restart_now()
        Assertion.assert_equal(rc, True, "ERR: restart fw failed")

    def test_04_show_vpn_policy(self):
        resp = Lvpn_obj.show_s2svpnpolicy()
        if re.search('vpn1', str(resp), re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "Error: show vpn policy failed.")

    def test_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn_1)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_06_delete_addObj(self):
        logger.info('-'*10+'delete ao'+'-'*10)
        rc = LAddrOBJ.del_ao_by_name(rm_range['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete AO Failed.')

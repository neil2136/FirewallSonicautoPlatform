from definition.settings import *
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')



class TC_01_For_Sonicpoint_Administrator_Sensitive_Keys_Excluded(Test):
    uuid = "SOSAIOT-TC-74985"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508955')
    
    def test_01_update_access_point(self):
        resp = accesspoint.config_sonicpoint_profile('SonicWave', **sonicwave)
        Assertion.assert_equal(resp, True, "ERR: Config sonicwave access point failed.")

    def test_02_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": False,
                "user_name": False,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_03_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_SONICPOINT')
        matches = re.findall(r"SonicPoint Admin Name:\s+testuser2", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: username is displayed.")
        matches = re.findall(r"Password:\s+testuser2", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: password is displayed.")


class TC_02_For_Sonicpoint_Administrator_Sensitive_Keys_Included(Test):
    uuid = "SOSAIOT-TC-74986"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508956')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": True,
                "user_name": True,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_SONICPOINT')
        matches = re.findall(r"SonicPoint Admin Name:\s+testuser2", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: username is not displayed.")
        matches = re.findall(r"Password:\s+testuser2", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: password is not displayed.")


class TC_03_L3_SSLVPN_UserName_Sensitive_Keys_Excluded(Test):
    uuid = "SOSAIOT-TC-74987"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508957')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": False,
                "user_name": False,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_SONICPOINT')
        match = re.search(r"SSLVPN Server:\s+1.1.1.1", tsr_content)
        Assertion.assert_equal(match.group(0), 'SSLVPN Server:  1.1.1.1', "ERR: SSLVPN Server is not displayed.")
        matches = re.findall(r"User Name:\s+sslvpntest", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: username is displayed.")
        matches = re.findall(r"Password:\s+sslvpntest", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: password is displayed.")


class TC_04_L3_SSLVPN_UserName_Included_And_Sensitive_Keys_Excluded(Test):
    uuid = "SOSAIOT-TC-74988"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508958')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": False,
                "user_name": True,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_SONICPOINT')
        match = re.search(r"SSLVPN Server:\s+1.1.1.1", tsr_content)
        Assertion.assert_equal(match.group(0), 'SSLVPN Server:  1.1.1.1', "ERR: SSLVPN Server is not displayed.")
        matches = re.findall(r"User Name:\s+sslvpntest", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: username is not displayed.")
        matches = re.findall(r"Password:\s+sslvpntest", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: password is displayed.")


class TC_05_L3_SSLVPN_UserName_Excluded_And_Sensitive_Keys_Included(Test):
    uuid = "SOSAIOT-TC-74989"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508959')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": True,
                "user_name": False,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_SONICPOINT')
        match = re.search(r"SSLVPN Server:\s+1.1.1.1", tsr_content)
        Assertion.assert_equal(match.group(0), 'SSLVPN Server:  1.1.1.1', "ERR: SSLVPN Server is not displayed.")
        matches = re.findall(r"User Name:\s+sslvpntest", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: username is displayed.")
        matches = re.findall(r"Password:\s+sslvpntest", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: password is not displayed.")


class TC_06_L3_SSLVPN_UserName_Sensitive_Keys_Included(Test):
    uuid = "SOSAIOT-TC-74990"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508960')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": True,
                "user_name": True,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_SONICPOINT')
        match = re.search(r"SSLVPN Server:\s+1.1.1.1", tsr_content)
        Assertion.assert_equal(match.group(0), 'SSLVPN Server:  1.1.1.1', "ERR: SSLVPN Server is not displayed.")
        matches = re.findall(r"User Name:\s+sslvpntest", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: username is not displayed.")
        matches = re.findall(r"Password:\s+sslvpntest", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: password is not displayed.")


class TC_07_L2TP_Server_UserName_Sensitive_Keys_Excluded(Test):
    uuid = "SOSAIOT-TC-75005"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508975')
    
    def test_01_L2TP_X1_Interface(self):
        x1 = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'l2tp',
            'l2tp_server': '2.2.2.2',
            'l2tp_user': 'testuser2',
            'l2tp_passwd': 'testuser2'
        }
        rc = interface.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to l2tp failed.")

    def test_02_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": False,
                "user_name": False,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_03_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_INTERFACES')
        match = re.search(r"L2TP Server IP Address\s+:\s+2.2.2.2", tsr_content)
        Assertion.assert_not_equal(match, None, "ERR: L2TP Server IP Address is not displayed.")
        matches = re.findall(r"User Name\s+:\s+testuser2", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: username is displayed.")
        matches = re.findall(r"Password\s+:\s+<Password exists>", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: password is displayed.")


class TC_08_L2TP_Server_UserName_Included_And_Sensitive_Keys_Excluded(Test):
    uuid = "SOSAIOT-TC-75006"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508976')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": False,
                "user_name": True,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_INTERFACES')
        match = re.search(r"L2TP Server IP Address\s+:\s+2.2.2.2", tsr_content)
        Assertion.assert_not_equal(match, None, "ERR: L2TP Server IP Address is not displayed.")
        matches = re.findall(r"User Name\s+:\s+testuser2", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: username is not displayed.")
        matches = re.findall(r"Password\s+:\s+<Password exists>", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: password is displayed.")


class TC_09_L2TP_Server_UserName_Sensitive_Keys_Included(Test):
    uuid = "SOSAIOT-TC-75007"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508977')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": True,
                "user_name": True,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_INTERFACES')
        match = re.search(r"L2TP Server IP Address\s+:\s+2.2.2.2", tsr_content)
        Assertion.assert_not_equal(match, None, "ERR: L2TP Server IP Address is not displayed.")
        matches = re.findall(r"User Name\s+:\s+testuser2", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: username is not displayed.")
        matches = re.findall(r"Password\s+:\s+<Password exists>", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: password is not displayed.")


class TC_10_PPTP_Server_UserName_Sensitive_Keys_Excluded(Test):
    uuid = "SOSAIOT-TC-75008" 

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508978')
    
    def test_01_PPTP_X2_Interface(self):
        x1 = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_server': '3.3.3.3',
            'pptp_user': 'testuser3',
            'pptp_passwd': 'testuser3'
        }
        rc = interface.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to pptp failed.")

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": False,
                "user_name": False,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_INTERFACES')
        match = re.search(r"PPTP Server IP Address\s+:\s+3.3.3.3", tsr_content)
        Assertion.assert_not_equal(match, None, "ERR:PPTP Server IP Address is not displayed.")
        matches = re.findall(r"User Name\s+:\s+testuser3", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: username is displayed.")
        matches = re.findall(r"Password\s+:\s+<Password exists>", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: password is displayed.")


class TC_11_PPTP_Server_UserName_Included_And_Sensitive_Keys_Excluded(Test):
    uuid = "SOSAIOT-TC-75009"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508979')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": False,
                "user_name": True,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_INTERFACES')
        match = re.search(r"PPTP Server IP Address\s+:\s+3.3.3.3", tsr_content)
        Assertion.assert_not_equal(match, None, "ERR: PPTP Server IP Address is not displayed.")
        matches = re.findall(r"User Name\s+:\s+testuser3", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: username is not displayed.")
        matches = re.findall(r"Password\s+:\s+<Password exists>", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: password is displayed.")


class TC_12_PPTP_SSLVPN_UserName_Excluded_And_Sensitive_Keys_Included(Test):
    uuid = "SOSAIOT-TC-75010"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508980')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": True,
                "user_name": False,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_INTERFACES')
        match = re.search(r"PPTP Server IP Address\s+:\s+3.3.3.3", tsr_content)
        Assertion.assert_not_equal(match, None, "ERR: PPTP Server IP Address is not displayed.")
        matches = re.findall(r"User Name\s+:\s+testuser3", tsr_content)
        Assertion.assert_equal(matches, [], "ERR: username is displayed.")
        matches = re.findall(r"Password\s+:\s+<Password exists>", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: password is not displayed.")

    
class TC_13_PPTP_Server_UserName_Sensitive_Keys_Included(Test):
    uuid = "SOSAIOT-TC-75011"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508981')

    def test_01_disable_sensitive_keys(self):
        tsr_options = {
                "sensitive_keys": True,
                "user_name": True,
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_check_tsr(self):
        tsr_content = diagnostic.get_tsr_part2('Blade_1_INTERFACES')
        match = re.search(r"PPTP Server IP Address\s+:\s+3.3.3.3", tsr_content)
        Assertion.assert_not_equal(match, None, "ERR: PPTP Server IP Address is not displayed.")
        matches = re.findall(r"User Name\s+:\s+testuser3", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: username is not displayed.")
        matches = re.findall(r"Password\s+:\s+<Password exists>", tsr_content)
        Assertion.assert_not_equal(matches, [], "ERR: password is not displayed.")


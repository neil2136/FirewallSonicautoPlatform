from definition.fw_ui import *


# On SAML profile for Management, only https service related SAML profiles will be shown
class Test_TC01(Test):
    uuid = "SOSAIOT-TC-77310"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp(self):
        idp_add = {
            'name': "idp",
            "authentication_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            "group_name_attribute": "department",
            "logout_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            'server_id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/",
            'trusted_certificate': "Microsoft Azure Federated SSO Certificate (673F596265895E9643B1FD8B785D1EA4)",
            'user_name_attribute': "displayname"
        }
        rc = saml_api.add_saml_identify_provider(**idp_add)
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")

    def test_02_add_https_service_sp(self):
        sp = {
            "domain_name": "shanghaiqa.com",
            'name': "sp_https",
            'service': {'https': True},
            'type': "domain"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add saml sp https service failed!!")

    def test_03_add_sslvpn_service_sp(self):
        sp = {
            "domain_name": "shanghaiqa.com",
            'name': "sp_sslvpn",
            'service': {'sslvpn': True},
            'type': "domain"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add saml sp sslvpn service failed!!")

    def test_04_add_profile_https(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp",
            'management': True,
            'name': "profile_https",
            'service_provider': "sp_https",
            'single_sign_off': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile https failed!!")

    def test_05_add_profile_sslvpn(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp",
            'management': False,
            'name': "profile_sslvpn",
            'service_provider': "sp_sslvpn",
            'single_sign_off': True,
            'sslvpn': True,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile sslvpn failed!!")

    def test_06_check_only_https_profile_shown(self):
        goto_saml_profile_tab_on_administration_page()
        logger.info('> check smal_sslvpn not on Administration/Management page')
        rc1 = fw_page_ui.does_element_exist_now(*locate_profile_https)
        logger.info(f'check Profile https exist result: {rc1}')
        rc2 = fw_page_ui.does_element_exist_now(*locate_profile_sslvpn)
        logger.info(f'check Profile sslvpn exist result: {rc2}')
        fw_page_ui.quit()
        rc = rc1 and (not rc2)
        Assertion.assert_equal(rc, True, 'ERR: check only https saml profile failed!!')


# SAML Profiles for management can be disabled/enabled
class Test_TC02(Test):
    uuid = "SOSAIOT-TC-77311"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_disable_profile_for_management(self):
        rc = disable_profile_for_management(profile='profile_https')
        Assertion.assert_equal(rc, True, "ERR: disable_profile_for_management failed!!")

    @repeat_method(3)
    def test_02_enable_profile_for_https_management(self):
        rc = enable_profile_for_management(profile='profile_https')
        Assertion.assert_equal(rc, True, "ERR: enable_profile_for_management failed!!")


# The details of SAML Profiles can be expanded
class Test_TC03(Test):
    uuid = "SOSAIOT-TC-77312"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_details_profile_expanded(self):
        goto_saml_profile_tab_on_administration_page()
        logger.info('> Expand profile on Administration/Management page')
        fw_page_ui.click_element(*locate_profile_expand)
        logger.info('> check SP configure')
        rc1 = fw_page_ui.does_element_exist_now('xpath', '//*[text()="SP CONFIGURATION"]')
        logger.info(f'> check SP configure result: {rc1}')
        rc2 = fw_page_ui.does_element_exist_now('xpath', '//*[text()="IDP CONFIGURATION"]')
        logger.info('> check IDP configure')
        logger.info(f'> check IDP configure result: {rc2}')

        fw_page_ui.quit()
        Assertion.assert_equal(rc1 & rc2, True, 'ERR: check_details_profile_expanded failed!!')


# "go to create more profiles" button can work
class Test_TC04(Test):
    uuid = "SOSAIOT-TC-77313"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_button_work(self):
        goto_saml_profile_tab_on_administration_page()
        logger.info('>click high link go to create more profile')
        fw_page_ui.click_element('xpath', '//*[text()="go to create more profiles"]')
        logger.info('>click high link go to create more profile DONE')
        logger.info('check current url')
        time.sleep(3)
        cur_url = fw_page_ui.get_current_browser_url()
        logger.info(f'current url is {cur_url}')
        rc1 = 'users-settings' in cur_url
        rc2 = fw_page_ui.does_element_exist_now('xpath', '//*[text()="SAML Profile"]')
        fw_page_ui.quit()
        Assertion.assert_equal(rc1 & rc2, True, 'ERR: check_button_work failed!!')


# "Single Sign on" button will show or disappear on firewall management login page when the management SAML Profile is enabled or disabled
class Test_TC05(Test):
    uuid = "SOSAIOT-TC-77314"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sp_X0_https(self):
        sp = {
            'address_object': "X0 IP",
            'name': "sp_x0_https",
            'service': {'https': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add_sp_X0_https service failed!!")

    def test_02_add_profile_X0_https(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp",
            'management': True,
            'name': "profile_x0_https",
            'service_provider': "sp_x0_https",
            'single_sign_off': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile X0 https service failed!!")

    @repeat_method(3)
    def test_03_check_single_sign_button_on_login_page(self):
        fw_page_ui.get_browser()
        fw_page_ui.go_to_url("https://192.168.168.168")
        logger.info('check Single Sign On button exist')
        rc = fw_page_ui.does_element_exist_now('xpath', '//*[text()="Single Sign On"]')
        logger.info(f'check Single Sign On button exist result: {rc}')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_single_sign_button_on_login_page failed!!')

    @repeat_method(3)
    def test_04_disable_profile_for_management(self):
        rc = disable_profile_for_management("profile_x0_https")
        Assertion.assert_equal(rc, True, "ERR: disable_profile_for_management failed!!")

    @repeat_method(3)
    def test_05_check_single_sign_button_disapper_on_login_page(self):
        fw_page_ui.get_browser()
        fw_page_ui.go_to_url("https://192.168.168.168")
        logger.info('check Single Sign On button exist')
        rc = fw_page_ui.does_element_exist_now('xpath', '//*[text()="Single Sign On"]')
        logger.info(f'check Single Sign On button exist result: {rc}')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, False, 'ERR: check_single_sign_button_disapper_on_login_page failed!!')

    @repeat_method(3)
    def test_06_enable_profile_for_management(self):
        rc = enable_profile_for_management("profile_x0_https")
        Assertion.assert_equal(rc, True, "ERR: enable_profile_for_management failed!!")


# Enable SAML Profiles for management on WAN, the other zone will not be shown "Single Sign on" button
class Test_TC06(Test):
    uuid = "SOSAIOT-TC-77315"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sp_X2_https(self):
        sp = {
            'address_object': "X2 IP",
            'name': "sp_x2_https",
            'service': {'https': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add_sp_X0_https service failed!!")

    def test_02_add_profile_X2_https(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp",
            'management': True,
            'name': "profile_x2_https",
            'service_provider': "sp_x2_https",
            'single_sign_off': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile X2 https service failed!!")

    @repeat_method(3)
    def test_03_check_single_button_on_login_page_when_access_FW_via_other_zone(self):
        script_path = suite_path + 'definition/script.py 0'
        cmd = f'python3 {script_path}'
        pc3_login.send_command(cmd)
        out = pc3_login.send_command('echo $?')
        print(f'rc: {out.strip()}')
        Assertion.assert_equal(out.strip(), '0',
                               'ERR: check single sign button will not be shown when access firewall via other zone failed!!')


# On login page, clicking on the "Single Sign on" option should initiate the SAML login flow and redirect the user to the IDP login page
class Test_TC07(Test):
    uuid = "SOSAIOT-TC-77316"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_01_check_Single_Sign_on_button_work(self):
        script_path = suite_path + 'definition/script.py'
        cmd = f'python3 {script_path} 1'
        pc3_login.send_command(cmd)
        out = pc3_login.send_command('echo $?')
        print(f'rc: {out.strip()}')
        Assertion.assert_equal(out.strip(), '0', 'ERR: check Single Sign on Button work failed!!')

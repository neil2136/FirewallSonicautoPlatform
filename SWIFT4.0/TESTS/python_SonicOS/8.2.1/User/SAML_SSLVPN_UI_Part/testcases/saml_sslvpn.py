from definition.fw_ui import *


# SAML authentication type can be selected for SSLVPN server Authentication Type
class Test_TC01(Test):
    uuid = "SOSAIOT-TC-77441"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_save_sslvpn_server_auth_as_SAML(self):
        opt = {
            'auth_type': "saml",
            "session_timeout": 10
        }
        rc = sslvpn_api.edit_server_setting(**opt)
        out = sslvpn_api.get_server_base_setting()
        logger.info(json.dumps(out))
        rc &= '"auth_type": "saml"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: save_sslvpn_server_auth_as_SAML failed!!')


# On SAML profiles for SSLVPN, only SSL VPN related SAML profiles will be shown
class Test_TC02(Test):
    uuid = "SOSAIOT-TC-77442"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, self.uuid)

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
            "address_object": "X0 IP",
            'name': "sp_sslvpn",
            'service': {'sslvpn': True},
            'type': "ip"
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
        init_test_page()
        logger.info('> click Profile button of SAML Profile Done')
        rc1 = fw_page_ui.does_element_exist_now(*locate_profile_https)
        logger.info(f'check Profile https exist result: {rc1}')
        rc2 = fw_page_ui.does_element_exist_now(*locate_profile_sslvpn)
        logger.info(f'check Profile sslvpn exist result: {rc2}')
        fw_page_ui.quit()
        rc = (not rc1) and rc2
        Assertion.assert_equal(rc, True, 'ERR: check only https saml profile failed!!')


# The details of SAML Profiles can be expanded
class Test_TC03(Test):
    uuid = "SOSAIOT-TC-77443"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_check_details_profile_expanded(self):
        init_test_page()

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


# SSLVPN SAML Profiles can be enabled/disabled
class Test_TC04(Test):
    uuid = "SOSAIOT-TC-77444"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_disable_profile_for_management(self):
        rc = disable_profile_for_management(profile='profile_sslvpn')
        Assertion.assert_equal(rc, True, "ERR: disable_profile_for_management failed!!")

    def test_02_enable_profile_for_https_management(self):
        rc = enable_profile_for_management(profile='profile_sslvpn')
        Assertion.assert_equal(rc, True, "ERR: enable_profile_for_management failed!!")


# "go to create more profiles" button can work
class Test_TC05(Test):
    uuid = "SOSAIOT-TC-77445"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_check_button_work(self):
        init_test_page()
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


# When the Auth type on SSLVPN server settings is set to "SAML", the virtual office login portal should show login button via SAML.
class Test_TC06(Test):
    uuid = "SOSAIOT-TC-77446"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, self.uuid)

    def test_01_enable_sslvpn_management_on_LAN(self):
        opt = {
            'LAN_enable': True
        }
        rc = sslvpn_api.edit_server_access_setting(**opt)
        Assertion.assert_equal(rc, True, 'ERR: enable_sslvpn_management_on_LAN failed!!')

    def test_02_test_sslvpn_login(self):
        fw_page_ui.get_chrome_with_head(headless=True)
        fw_page_ui.go_to_url("https://192.168.168.168:4433")
        logger.info('check Single Sign On button exist')
        rc = fw_page_ui.does_element_exist_now('xpath', '//div[contains(@class, "sw-login__saml-text")]')
        logger.info(f'check Single Sign On button exist result: {rc}')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_single_sign_button_on_login_page failed!!')


# On SSLVPN login portal page, clicking on the "LOG IN" option should initiate the SAML login flow and redirect the user to the IDP login page
class Test_TC07(Test):
    uuid = "SOSAIOT-TC-77448"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, self.uuid)

    @repeat_method(5, sleep=10)
    def test_01_check_login_button_login_page(self):
        fw_page_ui.get_chrome_with_head(headless=True)
        fw_page_ui.go_to_url("https://192.168.168.168:4433")
        logger.info('-> Click Login button')
        fw_page_ui.click_element('class', 'sw-login__trigger')
        logger.info('- Click Login Button SUCCESS')
        all_windows = fw_page_ui.get_browser_all_handles()
        time.sleep(3)
        fw_page_ui.switch_window()
        time.sleep(3)
        cur_url = fw_page_ui.get_current_browser_url()
        logger.info(f'current url is {cur_url}')
        for i in range(5):
            rc = 'https://login.microsoftonline.com' in cur_url
            if rc:
                break
            else:
                time.sleep(10)
                fw_page_ui.refresh_browser()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_login_button_login_page failed!!')

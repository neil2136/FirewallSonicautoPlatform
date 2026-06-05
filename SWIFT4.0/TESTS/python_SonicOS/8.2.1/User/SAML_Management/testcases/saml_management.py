from definition.fw_ui import *


# Users with SonicWALL Administrators privilege authenticate via SAML and manage FW
class Test_Saml_Management_TC01(Test):
    uuid = "SOSAIOT-TC-77317"
    description = show_testcase_info(TESTPLAN, 'tc01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_local_user_with_SonicWALL_Administrators_privilege(self):
        opt = {
            'action': "add",
            'username': "cyuan",
            # 'userpassword': "password",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["SonicWALL Administrators", "Trusted Users", "Everyone"]
        }
        rc = local_user_api.local_user(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add_local_user_with_SonicWALL_Administrators_privilege failed!!')

    @repeat_method(5, sleep=10)
    def test_02_check_saml_user_manage_fw_success(self):
        log_mon_api.clear_log()
        rc = manage_firewall_via_saml_user()
        Assertion.assert_equal(rc, True, "ERR: check_user_manage_fw_success Failed!!")


# The MGMT user information post authentication by IDP should be reflected under Firewall>Device>Users>Status section
class Test_Saml_Management_TC02(Test):
    uuid = "SOSAIOT-TC-77341"
    description = show_testcase_info(TESTPLAN, 'tc02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_the_saml_user_info_in_user_status(self):
        rc = False
        fw_page_ui.switchToDefaultWindow()
        url = 'https://shanghaiqa.com/sonicui/7/m/mgmt/users/users-status'
        for i in range(5):
            fw_page_ui.go_to_url(url)
            logger.info(f'->check if the saml User in the user status page...')
            fw_page_ui.wait_for_page_data_to_be_rendered()
            time.sleep(10)
            rc = fw_page_ui.does_element_exist('xpath', '//*[text()="cyuan"]')
            logger.info(f'->check the saml User in the user status page result: {rc}')
            if rc:
                break
            else:
                logger.info(f'check user status failed at {i+1} time, refresh page!')
                fw_page_ui.refresh_browser()
        Assertion.assert_equal(rc, True, 'ERR: check_the_saml_user_info_in_user_status failed!!')


# Click the Manage button again after several minutes and check firewall won't end current management session
class Test_Saml_Management_TC03(Test):
    uuid = "SOSAIOT-TC-77367"
    description = show_testcase_info(TESTPLAN, 'tc03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_firewall_wont_end_current_management_session(self):
        fw_page_ui.switchToNewWindow()
        rc_remain = False
        logger.info('-> Check the default Manage time...')
        rc_default = get_session_time() <= 60
        logger.info(f'-> Check the default time result: {rc_default}')
        logger.info('-> Wait 2 mins to Manage the firewall again...')
        time.sleep(120)
        for i in range(3):
            fw_page_ui.click_element('xpath', '//*[text()="Manage"]')
            time.sleep(3)
            remain_time = get_session_time()
            rc_remain = remain_time <= 57
            if rc_remain:
                break
        Assertion.assert_equal(rc_remain & rc_default, True,
                               "ERR: check_firewall_wont_end_current_management_session Failed!!")


# Verify the SAML user session time should be same and can be updated successfully as configured on IDP.
class Test_Saml_Management_TC04(Test):
    uuid = "SOSAIOT-TC-77368"
    description = show_testcase_info(TESTPLAN, 'tc04', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_user_session_time(self):
        rc = False
        logger.info('-> Logout and Login Again to check the Manage time...')
        logger.info('-> Click Logout...')
        logout_rc = logout_saml_auth()
        logger.info(f'logout result: {logout_rc}')
        if logout_rc:
            logger.info('Login Again to check the session time...')
            logger.info(f'current url is: {fw_page_ui.get_current_browser_url()}')
            time.sleep(3)
            # fw_page_ui.click_element('xpath', '//button[contains(text(), "Log Back In")]')
            fw_page_ui.click_element('xpath', '//button[@type="button"]')
            
            logger.info('Log Back In DONE...')
            time.sleep(3)
            logger.info('Single Sign On Again...')
            login_domain_type_Single_sign_on()
            logger.info('check the update time....')
            fw_page_ui.switchToNewWindow()
            cur_url = fw_page_ui.get_current_browser_url()
            time.sleep(10)

            logger.info('-> Check the Manage Page Load Success after Re-Login...')
            if fw_page_ui.does_element_exist('xpath', '//*[text()="Manage"]'):
                logger.info("-> The Manage Page Re-Load Successfully!")
                rc = get_session_time() <= 60
                logger.info(f'check the update time result: {rc}')
            else:
                logger.error('-> The Manage Page Load Failed!!')
        else:
            logger.error('-> Logout Failed!!')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True,
                               "ERR: check user session default time and update time Failed!!")


# Enable/disable Single Logout, testing SAML Management
class Test_Saml_Management_TC05(Test):
    uuid = "SOSAIOT-TC-77325"
    description = show_testcase_info(TESTPLAN, 'tc05', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_username_password_not_need_to_enter_again_disable_single_logout(self):
        logger.info("-> This case is Including TC04...")
        Assertion.assert_equal(True, True,
                               'ERR: check_username_password_not_need_to_enter_again_disable_single_logout failed!!')

    def test_02_enable_single_logout_for_profile_x0(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_azure",
            'service_provider': "sp_azure",
            'single_logout': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.edit_saml_profile_by_name("profile_azure", **saml_profile)
        Assertion.assert_equal(rc, True, "ERR: disable single logout for profile_x0 failed!!")

    @repeat_method(5, sleep=10)
    def test_03_check_username_password_need_to_enter_again_enable_single_logout(self):
        rc = False
        manage_rc = manage_firewall_via_saml_user()
        if manage_rc:
            logger.info('-> Logout and Login Again ...')
            logger.info('-> Click Logout...')
            logout_rc = logout_saml_auth()
            if logout_rc:
                time.sleep(3)
                # fw_page_ui.click_element('xpath', '//button[contains(text(), "Log Back In")]')
                fw_page_ui.click_element('xpath', '//button[@type="button"]')
                
                logger.info('-> Log Back In DONE...')
                time.sleep(3)
                logger.info('-> Single Sign On Again...')
                login_domain_type_Single_sign_on()
                fw_page_ui.switchToNewWindow()
                cur_url = fw_page_ui.get_current_browser_url()
                logger.info(f'-> Current URL is: {cur_url}')
                time.sleep(10)
                if 'https://login' in cur_url:
                    logger.info('Need Re-Login...')
                    for j in range(3):
                        if fw_page_ui.does_element_exist('xpath', '(//*[contains(text(), "cyuan@lu")])[2]'):
                            logger.info('-> The User Info Need Re-Fill in... Success Case...')
                            fw_page_ui.click_element('xpath', '(//*[contains(text(), "cyuan@lu")])[2]')
                            time.sleep(3)
                            logger.info('-> Fill in Password Again...')
                            fw_page_ui.set_text_field('xpath', '//input[@type="password"]', Parameter.PASSWD)
                            time.sleep(10)
                            logger.info('-> fill in password Done! submit it')
                            fw_page_ui.click_element('xpath', '//input[@type="submit"]')
                            time.sleep(1)
                            logger.info('-> Submit it Done!')
                            if fw_page_ui.does_element_exist('xpath', '//*[text()="Stay signed in?"]'):
                                logger.info('-> Stay signed in exist, not select it...')
                                fw_page_ui.click_element('xpath', '//input[@id="idBtn_Back"]')
                                logger.info('-> Stay signed in exist, not select it Done...')
                            rc = True
                            break
                        elif fw_page_ui.does_element_exist('xpath', '//input[@type="email"]'):
                            logger.info('-> User Login Page Load SUCCESS... Need to fill in User Info Again...')
                            user_login_again_rc = user_login_part()
                            if user_login_again_rc:
                                logger.info('->User Login Again PASS...')
                                rc = manage_part()
                                break
                        elif fw_page_ui.does_element_exist('xpath', '//*[text()="Manage"]'):
                            logger.error(
                                '-> The Manage Page Re-Load Success， So Not Need Re-login... Fail This Case...')
                            rc = False
                            break
                        else:
                            refresh_saml_login_page(j, max=20)
                elif 'https://shanghaiqa.com/sonicui/7/session-status/' in cur_url:
                    logger.info('-> It is still in Manage Page... So Not Need Re-Login... Fail This Case')
                elif 'https://shanghaiqa.com/getSamlAuth.html?' in cur_url:
                    logger.info('-> Need Refresh browser...')
                    for i in range(6):
                        refresh_saml_login_page(i)
                        url_after_referesh = fw_page_ui.get_current_browser_url()
                        if 'login.microsoftonline.com' in url_after_referesh:
                            logger.info(f'-> Refresh SUCCESS')
                            if fw_page_ui.does_element_exist('xpath', '(//*[contains(text(), "cyuan@lu")])[2]'):
                                fw_page_ui.click_element('xpath', '(//*[contains(text(), "cyuan@lu")])[2]')
                                time.sleep(3)
                                logger.info('-> Fill in Password Again...')
                                fw_page_ui.set_text_field('xpath', '//input[@type="password"]', Parameter.PASSWD)
                                time.sleep(1)
                                logger.info('-> fill in password Done! submit it')
                                fw_page_ui.click_element('xpath', '//input[@type="submit"]')
                                time.sleep(1)
                                logger.info('-> Submit it Done!')
                                rc = True
                            break
                    else:
                        logger.error(f'-> The Login Page Reload FAILED!! Stop the TEST... Fail This Case')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True,
                               'ERR: check_username_password_not_need_to_enter_again_disable_single_logout failed!!')


# Firewall should maintain an event log with user/group details
class Test_Saml_Management_TC06(Test):
    uuid = "SOSAIOT-TC-77343"
    description = show_testcase_info(TESTPLAN, 'tc06', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_saml_user_login_log(self):
        logs = log_mon_api.export_log_txt()
        rc = "User account ' 'cyuan' ' authenticated by SAML" in logs
        Assertion.assert_equal(rc, True, 'ERR: check_saml_user_login_log failed!!')


# Login MGMT with “HTTPS Login” disabled on the interface
class Test_Saml_Management_TC07(Test):
    uuid = "SOSAIOT-TC-77365"
    description = show_testcase_info(TESTPLAN, 'tc07', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc07')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_https_login_x0(self):
        x0_static = {
            'if': 'X0',
            'mode': 'static',
            'ip': Parameter.FIREWALL,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False
        }
        rc = if_v4_api.config_interface(**x0_static)
        Assertion.assert_equal(rc, True, 'ERR: disable_user_https_management_for_x0 failed')

    @repeat_method(5, sleep=10)
    def test_02_check_user_login_not_allow(self):
        rc = False
        https_access_SP_domain()
        login_domain_type_Single_sign_on()
        for i in range(6):
            user_login_page = fw_page_ui.does_element_exist('xpath', '//input[@type="email"]')
            if user_login_page:
                user_login_part()
                time.sleep(3)
                logger.info('check if Login Failed exist on GUI...')
                rc = fw_page_ui.does_element_exist('xpath', '//*[contains(text(),"Login Failed")]')
                logger.info(f'-> Check the Login Failed result: {rc}')
                break
            else:
                refresh_saml_login_page(i)
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_user_login_not_allow failed!!')

    def test_03_enable_x0_https_user_login_back(self):
        x0_static = {
            'if': 'X0',
            'mode': 'static',
            'ip': Parameter.FIREWALL,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True
        }
        rc = if_v4_api.config_interface(**x0_static)
        Assertion.assert_equal(rc, True, 'ERR: enable_x0_https_user_login_back failed')


# SAML authenticated user inactivity session timeout
class Test_Saml_Management_TC08(Test):
    uuid = "SOSAIOT-TC-77342"
    description = show_testcase_info(TESTPLAN, 'tc08', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5, sleep=10)
    def test_02_check_user_inactivity_session_timeout(self):
        rc = False
        manage_rc = manage_firewall_via_saml_user()
        if manage_rc:
            fw_page_ui.switchToNewWindow()
            logger.info('-> Wait the Session Timeout...')
            time.sleep(180)
            for j in range(10):
                logger.info(f'check the session timed out for the {j + 1} time')
                session_out = fw_page_ui.does_element_exist('xpath',
                                                                '//div[contains(text(), "Your session is timed out")]')
                if session_out:
                    logger.info('Find Current session is timed out...')
                    rc = True
                    break
                else:
                    time.sleep(30)
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: test_02_check_user_inactivity_session_timeout failed!!')


# Testing simultaneously login via SAML, with different users and privileges
class Test_Saml_Management_TC09(Test):
    uuid = "SOSAIOT-TC-77338"
    description = show_testcase_info(TESTPLAN, 'tc09', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc09')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_user_to_limited_privilege(self):
        opt = {
            'action': "edit",
            'username': "cyuan",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["Trusted Users", "Everyone", "Limited Administrators"]
        }
        rc = local_user_api.edit_local_user_by_name("cyuan", **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit_user_to_limited_privilege failed!!')

    @repeat_method(5, sleep=10)
    def test_02_check_limited_user_login(self):
        rc = False
        manage_rc = manage_firewall_via_saml_user()
        if manage_rc:
            time.sleep(20)
            cur_url = fw_page_ui.get_current_browser_url()
            logger.info(f'-> Current URL is: {cur_url}')
            logger.info('-> Switch to The Firewall Page...')
            logger.info(f'->check the manage page if it is in limited page...if the "Object" in the page...')
            rc = not fw_page_ui.does_element_exist_now('xpath','//span[contains(@class, "sw-top-nav-item") and contains(text(), "Object")]')
            logger.info(f'check the "Object" in Manage firewall page result: {rc}')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_limited_user_login failed!!')

    def test_03_edit_user_to_Read_only_privilege(self):
        opt = {
            'action': "edit",
            'username': "cyuan",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["Trusted Users", "Everyone", "SonicWALL Read-Only Admins"]
        }
        rc = local_user_api.edit_local_user_by_name("cyuan", **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit_user_to_limited_privilege failed!!')

    @repeat_method(5, sleep=10)
    def test_04_check_read_only_user_login(self):
        rc = False
        manage_rc = manage_firewall_via_saml_user()
        if manage_rc:
            logger.info(
                f'->Check Whether the manage page is in Read-Only mode...')
            time.sleep(20)
            cur_url = fw_page_ui.get_current_browser_url()
            logger.info(f'-> Current URL is: {cur_url}')
            logger.info('-> Switch to The Firewall Page...')
            fw_page_ui.switchToDefaultWindow()
            fw_page_ui.wait_for_page_data_to_be_rendered()
            rc = fw_page_ui.does_element_exist_now('xpath', '//*[contains(text(), "Read-Only")]')
            logger.info(f'check the "Read-Only" in Manage firewall page result: {rc}')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_limited_user_login failed!!')

    def test_05_edit_user_back_to_admin_privilege(self):
        opt = {
            'action': "edit",
            'username': "cyuan",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["Trusted Users", "Everyone", "SonicWALL Administrators"]
        }
        rc = local_user_api.edit_local_user_by_name("cyuan", **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit_user_to_limited_privilege failed!!')


# Enable SAML Profiles for management, users can authenticate via SAML and have management access to the firewall from LAN
class Test_Saml_Management_TC10(Test):
    uuid = "SOSAIOT-TC-77322"
    description = show_testcase_info(TESTPLAN, 'tc10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_user_manage_from_LAN(self):
        Assertion.assert_equal(True, True, 'ERR: user manage firewall from LAN failed!!')


# Restart FW,SAML function should still work
class Test_Saml_Management_TC11(Test):
    uuid = "SOSAIOT-TC-77354"
    description = show_testcase_info(TESTPLAN, 'tc11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_restart_FW(self):
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: reboot fw failed!')

    @repeat_method(5, sleep=10)
    def test_02_check_funtion_after_restart(self):
        rc = manage_firewall_via_saml_user()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check function after resart failed!!')


# Prefs export/import, SAML function should still work
class Test_Saml_Management_TC12(Test):
    uuid = "SOSAIOT-TC-77355"
    description = show_testcase_info(TESTPLAN, 'tc12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_exp_file(self):
        rc = setting_api.export_setting_exp('/tmp/cyuan.exp')
        Assertion.assert_equal(rc, True, "ERR: export exp file failed")

    def test_02_restore_fw(self):
        res = setting_api.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_03_config_x1_and_register_fw(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': "12.12.1.1",
            'dns1': Parameter.X1_DNS1,
            # 'dns2': Parameter.X1_DNS_2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True
        }
        rc = if_v4_api.config_interface(**x1_static)
        logger.info(f'config x1 result: {rc}')
        for i in range(10):
            time.sleep(10)
            rc = license_cli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed')

    def test_04_import_idp_ca(self):
        rc = False
        cert_file = suite_path + '/definition/file/sonicauto.cer'
        pc1_login.send_command(f'\cp {cert_file} /tmp')
        res = subprocess.run(['ls', '/tmp'], capture_output=True, text=True)
        print(res.stdout)
        if 'sonicauto.cer' in res.stdout:
            logger.info('cp cert file to PC1 success!!')
            rc = ca_api.import_ca_cert(file='/tmp/sonicauto.cer')
        else:
            logger.error('cp cert file to PC1 failed!!')
        Assertion.assert_equal(rc, True, "ERR: import ca file failed!!")

    def test_05_import_exp(self):
        rc = setting_api.import_setting_exp(filepath='/tmp/cyuan.exp')
        Assertion.assert_equal(rc, True, "ERR: import settings failed!!")

    @repeat_method(5, sleep=10)
    def test_06_check_settings_after_restore(self):
        rc = manage_firewall_via_saml_user()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check user manage firewall after restore Failed!!')


# CLI support for HTTPS management via SAML
class Test_Saml_Management_TC13(Test):
    uuid = "SOSAIOT-TC-77356"
    description = show_testcase_info(TESTPLAN, 'tc13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_saml_profile_via_CLI(self):
        opt = {
            'management': False
        }
        rc = saml_cli.edit_saml_profile_by_name(pro_name='profile_azure', **opt)
        Assertion.assert_equal(rc, True, 'ERR: disable saml profile via CLI failed!!')

    def test_02_enable_saml_profile_via_CLI(self):
        opt = {
            'management': True
        }
        rc = saml_cli.edit_saml_profile_by_name(pro_name='profile_azure', **opt)
        Assertion.assert_equal(rc, True, 'ERR: disable saml profile via CLI failed!!')


# Allow user to set saml debug level via CLI
class Test_Saml_Management_TC14(Test):
    uuid = "SOSAIOT-TC-77357"
    description = show_testcase_info(TESTPLAN, 'tc14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_saml_debug_via_CLI(self):
        cmds = ['configure', 'dbg', 'general-settings', 'log-to console', 'exit', 'auth', 'saml 2', 'commit']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: set saml debug via CLI failed!!')


# Different browsers testing
class Test_Saml_Management_TC15(Test):
    uuid = "SOSAIOT-TC-77353"
    description = show_testcase_info(TESTPLAN, 'tc15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5, sleep=10)
    def test_01_check_user_manage_fw_success_using_firefox(self):
        rc = manage_firewall_via_saml_user(browser_type='firefox')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, "ERR: check_user_manage_fw_success Failed!!")


# IP/Domain type for SAML SP, testing SAML https Management
class Test_Saml_Management_TC16(Test):
    uuid = "SOSAIOT-TC-77351"
    description = show_testcase_info(TESTPLAN, 'tc16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_domain_type_for_saml_https_management(self):
        Assertion.assert_equal(True, True, 'ERR: check_domain_type_for_saml_https_management failed!')


# Enable SAML Profiles for management, users can authenticate via SAML and have management access to the firewall from WAN
class Test_Saml_Management_TC17(Test):
    uuid = "SOSAIOT-TC-77321"
    description = show_testcase_info(TESTPLAN, 'tc17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3, sleep=5)
    def test_01_add_sp_for_X1(self):
        sp = {
            "domain_name": "shanghaiqa.com",
            'name': "sp_X1",
            'service': {'https': True},
            'type': "domain"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add saml sp https service for X1 failed!!")

    @repeat_method(3, sleep=5)
    def test_02_add_profile(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_X1",
            'service_provider': "sp_X1",
            'single_sign_off': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile https failed!!")

    @repeat_method(5, sleep=10)
    def test_03_check_user_manage_fw_success(self):
        script_path = suite_path + 'definition/scripts.py'
        out = pc2_login.send_command(f'python3 {script_path}')
        logger.info(f'out: {out}')
        Assertion.assert_regular(out, 'Manage Firewall SUCCESS', "ERR: check user manage firewall via X1 Failed!!")


# Enable SAML Profiles for management, users can authenticate via SAML and have management access to the firewall from DMZ
class Test_Saml_Management_TC18(Test):
    uuid = "SOSAIOT-TC-77323"
    description = show_testcase_info(TESTPLAN, 'tc18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3, sleep=5)
    def test_01_add_sp_for_X2(self):
        sp = {
            "domain_name": "shanghaiqa.com",
            'name': "sp_X2",
            'service': {'https': True},
            'type': "domain"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add saml sp https service for X1 failed!!")

    @repeat_method(3, sleep=5)
    def test_02_add_profile(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_X2",
            'service_provider': "sp_X2",
            'single_sign_off': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile https failed!!")

    @repeat_method(5, sleep=10)
    def test_03_check_user_manage_fw_success(self):
        script_path = suite_path + 'definition/scripts.py'
        out = pc3_login.send_command(f'python3 {script_path}')
        logger.info(f'out: {out}')
        Assertion.assert_regular(out, 'Manage Firewall SUCCESS',
                                 "ERR: check user manage firewall via DMZ zone Failed!!")


# Enable SAML Profiles for management, users can authenticate via SAML and have management access to the firewall from custom zone
class Test_Saml_Management_TC19(Test):
    uuid = "SOSAIOT-TC-77324"
    description = show_testcase_info(TESTPLAN, 'tc19', description=True)['title']
    jira = 'Gen7-55539'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3, sleep=5)
    def test_01_add_custome_zone(self):
        zone_obj_json = {
            "zones": [
                {
                    "name": "custom_zone",
                    "security_type": "Trusted",
                    "ssl_control": False,
                }
            ]
        }
        rc = zone_obj.add_zone_object(**zone_obj_json)
        Assertion.assert_equal(rc, True, "ERR: Add Zone object Failed.")

    @repeat_method(3, sleep=5)
    def test_02_update_x2_to_Custom_Zone(self):
        x2_static = {
            'if': 'X2',
            'zone': "custom_zone",
            'mode': 'static',
            'ip': '13.13.1.168',
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_http': True,
            'user_https': True,
        }
        rc = if_v4_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, 'ERR: config x2 to custom zone failed.')

    @repeat_method(5, sleep=10)
    def test_03_check_user_manage_fw_success_on_custom_zone(self):
        script_path = suite_path + 'definition/scripts.py'
        out = pc3_login.send_command(f'python3 {script_path}')
        logger.info(f'out: {out}')
        Assertion.assert_regular(out, 'Manage Firewall SUCCESS',
                                 "ERR: check user manage firewall via DMZ zone Failed!!")


# Enable SAML Profiles for management, authenticate Admins from local via the regular 'log in' option
class Test_Saml_Management_TC20(Test):
    uuid = "SOSAIOT-TC-77333"
    description = show_testcase_info(TESTPLAN, 'tc20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_login_option(self):
        login_firewall()
        fw_page_ui.quit()
        Assertion.assert_equal(True, True, 'ERR: verify_login_option failed!!')


# Disable SAML Profiles for management, authenticate via the regular 'log in' option
class Test_Saml_Management_TC21(Test):
    uuid = "SOSAIOT-TC-77334"
    description = show_testcase_info(TESTPLAN, 'tc21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_Saml_Management(self):
        opt = {
            'management': False
        }
        rc = saml_cli.edit_saml_profile_by_name(pro_name='profile_azure', **opt)
        Assertion.assert_equal(rc, True, 'ERR: disable saml profile via CLI failed!!')

    def test_02_verify_regular_login_option(self):
        login_firewall()
        fw_page_ui.quit()
        Assertion.assert_equal(True, True, 'ERR: verify_login_option failed!!')

    def test_03_enable_saml_management_back(self):
        opt = {
            'management': True
        }
        rc = saml_cli.edit_saml_profile_by_name(pro_name='profile_azure', **opt)
        Assertion.assert_equal(rc, True, 'ERR: enable_saml_management_back failed!!')


# Users without SonicWALL Administrators privilege authenticate via SAML
class Test_Saml_Management_TC22(Test):
    uuid = "SOSAIOT-TC-77319"
    description = show_testcase_info(TESTPLAN, 'tc22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3, sleep=10)
    def test_01_edit_local_user_without_admin_privilege(self):
        opt = {
            'action': "edit",
            'username': "cyuan",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["Trusted Users", "Everyone"]
        }
        rc = local_user_api.edit_local_user_by_name("cyuan", **opt)
        Assertion.assert_equal(rc, True, 'ERR: add_local_user_without_SonicWALL_Administrators_privilege failed!!')

    @repeat_method(5, sleep=10)
    def test_02_check_user_no_privilege_authentication(self):
        rc = False
        https_access_SP_domain()
        login_domain_type_Single_sign_on()
        for i in range(6):
            user_login_page = fw_page_ui.does_element_exist('xpath', '//input[@type="email"]')
            if user_login_page:
                user_login_part()
                time.sleep(3)
                rc = fw_page_ui.does_element_exist('xpath', '//*[contains(text(),"Login Failed")]')
                logger.info(f'-> Check the Login Failed exists result: {rc}')
                break
            else:
                refresh_saml_login_page(i)
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_user_no_privilege_authentication')

    @repeat_method(3, sleep=10)
    def test_03_add_privilege_for_user_back(self):
        opt = {
            'action': "edit",
            'username': "cyuan",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["Trusted Users", "Everyone", "SonicWALL Administrators"]
        }
        rc = local_user_api.edit_local_user_by_name("cyuan", **opt)
        Assertion.assert_equal(rc, True, 'ERR: add_local_user_without_SonicWALL_Administrators_privilege failed!!')


# Verify SAML auth to X1 can succeed when WLB is enabled and X2 has higher priority than X1
class Test_Saml_Management_TC24(Test):
    uuid = "SOSAIOT-TC-77366"
    description = show_testcase_info(TESTPLAN, 'tc24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_single_logout(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_azure",
            'service_provider': "sp_azure",
            'single_logout': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.edit_saml_profile_by_name("profile_azure", **saml_profile)
        Assertion.assert_equal(rc, True, "ERR: enable single logout for profile_x0 failed!!")

    @repeat_method(3, sleep=30)
    def test_02_set_X2_as_WAN(self):
        out = pc1_login.send_command('ping -c 5 192.168.168.168')
        logger.info(f'ping FIREWALL result: \n{out}')
        x2_static = {
            'if': 'X2',
            'zone': "WAN",
            'mode': 'static',
            'ip': '13.13.1.168',
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = if_v4_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, 'ERR: config x2 to WAN failed')

    def test_03_config_WLB(self):
        opt = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X2",
                                "rank": 1,
                                "probe_type": "physical"
                            },
                            {
                                "name": "X1",
                                "rank": 2,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = wlb_api.config_failover_groups_by_multi(**opt)
        Assertion.assert_equal(rc, True, 'ERR: config WLB failed!!')

    @repeat_method(5, sleep=10)
    def test_04_check_user_manage_fw_success(self):
        rc = manage_firewall_via_saml_user()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, "ERR: check_user_manage_fw_success Failed!!")


# Keep SAML user login/logout, see if there’s any memory leak
class Test_Saml_Management_TC25(Test):
    uuid = "SOSAIOT-TC-77347"
    description = show_testcase_info(TESTPLAN, 'tc25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5, sleep=60)
    def test_01_disable_single_logout(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_azure",
            'service_provider': "sp_azure",
            'single_logout': False,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.edit_saml_profile_by_name("profile_azure", **saml_profile)
        Assertion.assert_equal(rc, True, "ERR: disable single logout for profile_x0 failed!!")

    @repeat_method(5, sleep=10)
    def test_02_keep_user_login_logout(self):
        login_rc = False
        logout_rc = False
        https_access_SP_domain()
        login_domain_type_Single_sign_on()
        for i in range(6):
            user_login = fw_page_ui.does_element_exist('xpath', '//input[@type="email"]')
            if user_login:
                user_login_rc = user_login_part()
                if user_login_rc:
                    manage_rc = manage_part()
                    if manage_rc:
                        logger.info('-> Do SAML User Login/Logout Test, 50 times...')
                        for j in range(10):
                            logger.info(f'-> Do Login/Logout TEST for the {j + 1} time...')
                            logout_rc = logout_saml_auth()
                            logger.info(f'-> Logout Result in the {j + 1} TEST time is: {logout_rc}')
                            login_rc = saml_user_relogin()
                            logger.info(f'-> Login Result in the {j + 1} TEST time is: {login_rc}')
                            if not (logout_rc and login_rc):
                                logger.error(
                                    f'-> SAML User Logout/Re-login Failed in {j + 1} TEST time...Stop the test')
                                break
                        else:
                            logger.info('-> SAML User Logout/Login 50 time SUCCEED...')
                    break
            else:
                refresh_saml_login_page(i)
        time.sleep(10)
        fw_page_ui.quit()
        Assertion.assert_equal(login_rc & logout_rc, True, 'ERR: Test keep_user_login_logout Failed!!')


# Mixed testing of multiple interfaces and same IDP with domain type
class Test_Saml_Management_TC26(Test):
    uuid = "SOSAIOT-TC-77339"
    description = show_testcase_info(TESTPLAN, 'tc26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_multi_interface_with_same_IDP(self):
        Assertion.assert_equal(True, True, 'ERR: check_multi_interface_with_same_IDP failed!!')


# Verify the Max entries of the SAML Profiles For Management
class Test_Saml_Management_TC27(Test):
    uuid = "SOSAIOT-TC-77350"
    description = show_testcase_info(TESTPLAN, 'tc27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp(self):
        idp = {
            'name': "",
            "authentication_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            "group_name_attribute": "test",
            "logout_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            'server_id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/",
            'trusted_certificate': "Microsoft Azure Federated SSO Certificate (673F596265895E9643B1FD8B785D1EA4)",
            'user_name_attribute': "test"
        }
        for i in range(4, 17):
            idp.update({"name": f"idp_{i}"})
            rc = saml_api.add_saml_identify_provider(**idp)
            if not rc:
                logger.error(f'add the {idp_add["name"]} failed!!')
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")

    def test_02_add_16_profiles(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_17",
            'service_provider': "sp_azure",
            'single_sign_off': True,
            'single_logout': False,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        for i in range(4, 17):
            saml_profile.update({'identity_provider': f"idp_{i}", 'name': f"profile_{i}"})
            rc = saml_api.add_saml_profile(**saml_profile)
            if not rc:
                logger.error(f'add the profile_{i} failed!!')
        Assertion.assert_equal(rc, True, "ERR: add saml profile https failed!!")

    def test_03_add_17th_profile(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_17",
            'service_provider': "sp_azure",
            'single_sign_off': True,
            'single_logout': False,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc, err_msg = saml_api.add_saml_profile(**saml_profile, msg=True)
        logger.info(json.dumps(err_msg))
        rc &= 'SAML Authentication Profile Name: Number of SAML SP reaches the limitation' in json.dumps(err_msg)
        Assertion.assert_equal(rc, False, "ERR: add saml profile https failed!!")


# Non-443 port as HTTPS Port, testing SAML https Management
class Test_Saml_Management_TC23(Test):
    uuid = "SOSAIOT-TC-77349"
    description = show_testcase_info(TESTPLAN, 'tc23', description=True)['title']
    jira = 'Gen7-55539'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_management_https_port(self):
        opt = {
            'https_port': 444
        }
        rc = admin_api.conf_admin(**opt)
        Assertion.assert_equal(rc, True, 'ERR: update_management_https_port to 444 failed!!')

    @repeat_method(10, sleep=10)
    def test_02_test_saml_https_management_port444(self):
        rc = False
        fw_page_ui.get_chrome_with_head(headless=True)
        fw_page_ui.go_to_url('https://shanghaiqa.com:444')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        login_domain_type_Single_sign_on()
        for i in range(6):
            user_login = fw_page_ui.does_element_exist('xpath', '//input[@type="email"]')
            if user_login:
                rc = user_login_part()
                break
            else:
                refresh_saml_login_page(i)
        time.sleep(10)
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: test_saml_https_management port444 failed!!!')

    def test_03_update_management_https_port_back(self):
        cmds = ['configure', 'administration', 'https-port 443', 'commit', 'end', 'exit']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: update_management_https_port_back to 443 via CLI failed!!')


# IDP send response with missing required attributes
class Test_Saml_Management_TC28(Test):
    uuid = "SOSAIOT-TC-77362"
    description = show_testcase_info(TESTPLAN, 'tc28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_00_01_disable_management_for_all_saml_profiles(self):
        opt = {
                "management": False
        }
        profiles = saml_api.get_saml_profiles()
        for profile in profiles["user"]['saml']["profile"]:
            rc = saml_api.edit_saml_profile_by_name(profile_name=profile.get("name"), **opt)
            if not rc:
                logger.error(f'ERR: disable management for {profile["name"]} failed!!')
        Assertion.assert_equal(rc, True, f'ERR: disable management for {profile["name"]} failed!!')

    @repeat_method(5, sleep=60)
    def test_01_delete_exists_profiles(self):
        rc = saml_api.delete_all_saml_profiles()
        Assertion.assert_equal(rc, True, 'ERR: delete ALL saml profiles failed!!')

    def test_02_delete_exists_idp(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all saml idp failed!!')

    def test_03_add_idp_not_exist_in_IDP_server(self):
        idp_add = {
            'name': "idp_azure",
            "authentication_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            "group_name_attribute": "department",
            "logout_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            'server_id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/",
            'trusted_certificate': "Microsoft Azure Federated SSO Certificate (673F596265895E9643B1FD8B785D1EA4)",
            'user_name_attribute': "test"
        }
        rc = saml_api.add_saml_identify_provider(**idp_add)
        Assertion.assert_equal(rc, True, "ERR: add_idp_not_exist_in_IDP_server failed!!")

    def test_04_add_profile(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_azure",
            'service_provider': "sp_azure",
            'single_sign_off': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile https failed!!")

    @repeat_method(10, sleep=10)
    def test_05_check_user_cannot_login(self):
        rc = False
        https_access_SP_domain()
        login_domain_type_Single_sign_on()
        for i in range(6):
            user_login_page = fw_page_ui.does_element_exist('xpath', '//input[@type="email"]')
            if user_login_page:
                user_login_part()
                logger.info('-> Check "Login Failed" exists...')
                rc = fw_page_ui.does_element_exist('xpath', '//*[contains(text(),"Login Failed")]')
                break
            else:
                refresh_saml_login_page(i)
        time.sleep(10)
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check SAML User cannot Login Failed!!')

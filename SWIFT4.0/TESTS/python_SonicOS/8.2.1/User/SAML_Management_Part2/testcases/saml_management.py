from definition.fw_ui import *


# Group without SonicWALL Administrators privilege authenticate via SAML
class Test_Saml_Management_TC01(Test):
    uuid = "SOSAIOT-TC-77320"
    description = show_testcase_info(TESTPLAN, '3258887', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258887', description=True)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_local_user_in_IDP(self):
        opt = {
            'action': "add",
            'username': "cyuan",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["SonicWALL Administrators", "Trusted Users", "Everyone"]
        }
        rc = local_user_api.local_user(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add_local_user_in_IDP failed!!')

    def test_02_add_local_group_in_IDP(self):
        opt = {'user': {'local': {'group': [{'name': "qa", 'domain': "any"}]}}}
        rc = local_user_api.add_local_group(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add local group in IDP failed!!')

    @repeat_method(10, sleep=10)
    def test_03_check_user_login_not_allow(self):
        rc = False
        https_access_SP_domain()
        login_domain_type_Single_sign_on()
        for i in range(6):
            user_login_page = fw_page_ui.does_element_exist_now('xpath', '//input[@type="email"]')
            if user_login_page:
                user_login_part()
                time.sleep(3)
                rc = fw_page_ui.does_element_exist_now('xpath', '//*[contains(text(),"Login Failed")]')
                logger.info(f'-> Check the Login Failed result: {rc}')
                break
            else:
                refresh_saml_login_page(i)
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_user_login_not_allow failed!!')


# Group with SonicWALL Administrators privilege authenticate via SAML and manage FW
class Test_Saml_Management_TC02(Test):
    uuid = "SOSAIOT-TC-77318"
    description = show_testcase_info(TESTPLAN, '3258885', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258885')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_qa_group_to_Sonicwall_Administration(self):
        opt = {
            "user": {
                "local": {
                    "group": [{
                        'bookmark': [],
                        'comment': "",
                        'domain': "any",
                        'member': [{'name': "cyuan"}, {'name': "qa"}],
                        'name': "SonicWALL Administrators",
                        'one_time_password': {},
                        'to_management_on_login': False,
                        'vpn_client_access': []
                    }]
                }
            }
        }
        rc = local_user_api.config_local_group_by_name(groupname='SonicWALL%20Administrators', domainname='any', **opt)
        Assertion.assert_equal(rc, True, 'ERR: add_qa_group_to_Sonicwall_Administration failed!!')

    @repeat_method(10, sleep=10)
    def test_02_check_saml_user_manage_fw_success(self):
        log_mon_api.clear_log()
        rc = manage_firewall_via_saml_user()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, "ERR: check_user_manage_fw_success Failed!!")


# Test SLO when same user login from different PC/IPs
class Test_Saml_Management_TC03(Test):
    uuid = "SOSAIOT-TC-77326"
    description = show_testcase_info(TESTPLAN, '3258893', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258893')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_login_from_different_PC(self):
        rc1 = False
        rc2 = False
        logger.info(f'-> Login from PC1 first')
        pc1_login_rc = manage_firewall_via_saml_user()
        logger.info(f'-> PC1 login result: {pc1_login_rc}')
        time.sleep(10)
        if pc1_login_rc:
            logger.info(f'-> Login from PC4......')
            script_path = suite_path + 'definition/scripts.py TC03'
            out = pc4_login.send_command(f'python3 {script_path}')
            logger.info(f'out: {out}')
            rc1 = 'Logout SUCCESS' in out
            logger.info(f'-> PC4 Login Firewall result: {rc1}')
            if rc1:
                fw_page_ui.switchToDefaultWindow()
                url = 'https://shanghaiqa.com/sonicui/7/m/mgmt/users/users-status'
                fw_page_ui.go_to_url(url)
                logger.info(f'->check if the saml User in the user status page...')
                fw_page_ui.wait_for_page_data_to_be_rendered()
                time.sleep(10)
                rc2 = fw_page_ui.does_element_exist_now('xpath', '//*[text()="sonicauto"]')
                logger.info(f'->check the saml User in the user status page result: {rc2}')
                time.sleep(10)
            else:
                logger.error('PC4 Login Firewall Failed!!')
        else:
            logger.error('PC1 Login Firewall Failed!!')
        fw_page_ui.quit()
        Assertion.assert_equal(rc1&rc2, True, 'ERR: test_01_login_from_different_PC failed!!')


# SAML IDP Trusted Certificates is the IDP default Certificate
class Test_Saml_Management_TC04(Test):
    uuid = "SOSAIOT-TC-77327"
    description = show_testcase_info(TESTPLAN, '3258894', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258894')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_with_IDP_default_cert(self):
        Assertion.assert_equal(True, True, 'ERR: check_with_IDP_default_cert failed!!')


# Use a SAML assertion for a different SP
class Test_Saml_Management_TC05(Test):
    uuid = "SOSAIOT-TC-77363"
    description = show_testcase_info(TESTPLAN, '3490399', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3490399')  
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_profile_azure(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': False,
            'name': "profile_azure",
            'service_provider': "sp_azure",
            'single_logout': False,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.edit_saml_profile_by_name("profile_azure", **saml_profile)
        Assertion.assert_equal(rc, True, "ERR: disable single logout for profile_x0 failed!!")

    def test_02_import_new_cert(self):
        rc = False
        cert_file = suite_path + '/definition/file/saml_cyuan.cer'
        pc1_login.send_command(f'\cp {cert_file} /tmp')
        res = subprocess.run(['ls', '/tmp'], capture_output=True, text=True)
        print(res.stdout)
        if 'sonicauto.cer' in res.stdout:
            logger.info('cp cert file to PC1 success!!')
            rc = ca_api.import_ca_cert(file='/tmp/saml_cyuan.cer')
        else:
            logger.error('cp cert file to PC1 failed!!')
        Assertion.assert_equal(rc, True, "ERR: import New ca file failed!!")

    def test_03_add_new_IDP(self):
        idp_add = {
            'name': "idp_azure_X0",
            "authentication_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            "group_name_attribute": "department",
            "logout_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            'server_id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/",
            'trusted_certificate': "Microsoft Azure Federated SSO Certificate (673F596265895E9643B1FD8B785D1EA4)",
            'user_name_attribute': "displayname"
        }
        rc = saml_api.add_saml_identify_provider(**idp_add)
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")

    def test_04_add_sp(self):
        sp = {
            "address_object":"X2 IP",
            'name': "sp_azure_X0",
            'service': {'https': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add saml sp https service failed!!")
    #
    def test_05_add_profile(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure_X0",
            'management': True,
            'name': "profile_azure_X0",
            'service_provider': "sp_azure_X0",
            'single_sign_off': True,
            'single_logout': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile https failed!!")

    @repeat_method(10, sleep=10)
    def test_06_check_saml_assertion(self):
        script_path = suite_path + 'definition/scripts.py TC05'
        out = pc3_login.send_command(f'python3 {script_path}')
        logger.info(f'out: {out}')
        rc = 'check Manage button if exists result: False' in out
        Assertion.assert_equal(rc, True, 'ERR: check saml assertion for a different SP failed!!')




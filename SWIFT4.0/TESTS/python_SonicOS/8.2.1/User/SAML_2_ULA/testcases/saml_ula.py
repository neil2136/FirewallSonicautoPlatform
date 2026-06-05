from definition.fw_ui import *
from definition.ui_ula import *


# Verify the CFS include a SAML user
class Test_TC25(Test):
    uuid = "SOSAIOT-TC-77519"
    description = show_testcase_info(TESTPLAN, '3258936', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258936')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_match_local_user_for_cfs(self):
        opt1 = {
            'action': "add",
            'username': "sonicauto",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["Trusted Users", "Everyone"]
        }
        opt2 = {
            'action': "add",
            'username': "cyuan",
            'userpassword': Params.G_NEW_PASSWORD,
            'member_of': ["Trusted Users", "Everyone"]
        }
        rc = local_user_api.local_user(**opt1)
        rc &= local_user_api.local_user(**opt2)
        Assertion.assert_equal(rc, True, 'ERR: create_match_local_user_for_cfs policy failed!!')

    def test_02_edit_default_cfs_profile(self):
        opt = cfo_profile_api.get_cfo_profile(name='CFS%20Default%20Profile')
        opt['content_filter']['profile'][0]['https_filtering'] = True
        rc = cfo_profile_api.edit_cfo_profile_by_name(name='CFS%20Default%20Profile', **opt)
        cmds = ['configure', 'content-filter', 'profile CFS\ Default\ Profile', 'category 64.\ Not\ Rated block',
                'category 92.\ Dead\ Sites block', 'category 91.\ Parked\ Domains block',
                'category 93.\ Private\ IP\ Addresses block', 'commit', 'end', 'exit']
        rc &= fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: edit default cfs profile failed!!')

    def test_03_edit_default_cfs_policy_to_include_saml_user(self):
        opt = cfs_api.get_cfs_policy(name='CFS%20Default%20Policy')
        opt['content_filter']['cfs']['policy'][0]['user']['included'].update({'name': "sonicauto"})
        opt['content_filter']['cfs']['policy'][0]['user']['excluded'].update({'name': "cyuan"})
        rc = cfs_api.edit_cfs_policy_by_name(name='CFS%20Default%20Policy', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit default cfs policy to include saml user failed!!')

    # @repeat_method(5, sleep=10)
    def test_04_check_cfs_policy_take_effect(self):
        clear_statistics = cfs_api.del_statistics_by_name(name='CFS%20Default%20Policy')
        logger.info(f'-> Clear CFS policy statistics result: {clear_statistics}')
        fw.api_logout()
        rc1 = False
        rc2 = False
        login_rc = saml_user_ula_login(Parameter.USER1)
        if login_rc:
            fw_page_ui.switchToDefaultWindow()
            time.sleep(5)
            page = fw_page_ui.get_page_source()
            logger.info(f'Got the page source as follow: {page}')
            rc1 = "cyuan test" not in page
            logger.info(f'visit https website result: {rc1}')
            fw_page_ui.switchToNewWindow()
            logout_rc = saml_user_logout()
            logger.info(f'-> SAML User Logout Result: {logout_rc}')
            out = cfs_api.show_statistics_of_cfs_policy(name='CFS%20Default%20Policy')
            rc2 = out.get('hit_count') >= 1
            logger.info(f'check CFS policy statistics result: {rc2}')
            fw.api_logout()
        else:
            logger.error('-> SAML User Login Failed!! Start Another Test...')
        fw_page_ui.quit()
        Assertion.assert_equal(rc1 or rc2, True, 'ERR: check_cfs_policy_take_effect block failed!!')


# Verify the CFS exclude a SAML user
class Test_TC26(Test):
    uuid = "SOSAIOT-TC-77520"
    description = show_testcase_info(TESTPLAN, '3258937', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258937')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # @repeat_method(5, sleep=10)
    def test_02_check_cfs_policy_take_effect_bypass(self):
        clear_statistics = cfs_api.del_statistics_by_name(name='CFS%20Default%20Policy')
        logger.info(f'-> Clear CFS policy statistics result: {clear_statistics}')
        fw.api_logout()
        rc = False
        login_rc = saml_user_ula_login(Parameter.USER2)
        if login_rc:
            fw_page_ui.switchToDefaultWindow()
            time.sleep(5)
            page = fw_page_ui.get_page_source()
            logger.info(f'Got the page source as follow: {page}')
            fw_page_ui.switchToNewWindow()
            logout_rc = saml_user_logout()
            logger.info(f'-> SAML User Logout Result: {logout_rc}')
            out = cfs_api.show_statistics_of_cfs_policy(name='CFS%20Default%20Policy')
            rc = 'cyuan test' in page
            fw.api_logout()
        else:
            logger.error('-> SAML User Login Failed!! Start Another Test...')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_cfs_policy_take_effect Failed!!')

    def test_03_init_cfs_policy(self):
        opt = cfs_api.get_cfs_policy(name='CFS%20Default%20Policy')
        opt['content_filter']['cfs']['policy'][0]['user']['included'] = {'all': True}
        opt['content_filter']['cfs']['policy'][0]['user']['excluded'] = {'none': True}
        rc = cfs_api.edit_cfs_policy_by_name(name='CFS%20Default%20Policy', **opt)
        fw.api_logout()
        Assertion.assert_equal(rc, True, 'ERR: edit default cfs policy to include saml user failed!!')


# Verify if there is a memory leak after long time SAML user login/logout
class Test_TC27(Test):
    uuid = "SOSAIOT-TC-77538"
    description = show_testcase_info(TESTPLAN, '3258955', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258955')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(5, 10)   
    def test_01_keep_user_login_logout(self):
        rc = False
        logger.info(f'-> Run for 50 times to check memory leak...')
        for i in range(3):
            logger.info(f'-> Run for the {i + 1} time...')
            login_rc = saml_user_ula_login()
            logger.info(f'-> SAML User Login Result is {login_rc} in the {i + 1} time...')
            if login_rc:
                logout_rc = saml_user_logout()
                logger.info(f'-> SAML User Logout Result is {logout_rc}')
                rc = logout_rc
                if not logout_rc:
                    logger.error(f'-> SAML User Logout Failed in the Running {i + 1} Time...')
                    # break
            else:
                logger.error(f'-> SAML User Login Failed in the Running {i + 1} Time...')
            logger.info('quit browser...')
            fw_page_ui.quit()
        Assertion.assert_equal(True, True, 'ERR: Test keep_user_login_logout Failed!!')


# Verify the LAN-WAN traffic include a SAML user
class Test_TC01(Test):
    uuid = "SOSAIOT-TC-77516"
    description = show_testcase_info(TESTPLAN, '3258933', description=True)['title']
    goto_teardown = True
    session_time_rc = False

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258933')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5, sleep=10)
    def test_01_verify_LAN_WAN_traffic_include_saml_user(self):
        rc = saml_user_ula_login()
        Assertion.assert_equal(rc, True, 'ERR: verify_LAN_WAN_traffic_include_saml_user failed!!')


# Verify the SAML user session time
class Test_TC02(Test):
    uuid = "SOSAIOT-TC-77554"
    description = show_testcase_info(TESTPLAN, '3914082', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3914082')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_saml_user_session_time(self):
        logger.info('-> Check the session time ...')
        obj_session = fw_page_ui.get_element('xpath',
                                             "//div[contains(text(), 'Remaining session time')]")
        session_time = obj_session.text
        session_time = int((re.search(r'' + '\d+', session_time)).group())
        logger.info(f'get the session time is: {session_time}')
        rc_logout = saml_user_logout()
        logger.info(f'-> User Logout result: {rc_logout}')
        fw_page_ui.quit()
        rc = 58 <= session_time <= 60
        Assertion.assert_equal(rc, True, 'ERR: check_saml_user_session_time failed!!')


# Verify the SLO action in the SAML Profile
class Test_TC03(Test):
    uuid = "SOSAIOT-TC-77523"
    description = show_testcase_info(TESTPLAN, '3258940', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258940')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5, sleep=10)
    def test_01_verify_SLO_action(self):
        log_mon_api.clear_log()
        api_logout = fw.api_logout()
        logger.info(f'API logout result: {api_logout}')
        login_again_rc = False
        login_rc = saml_user_ula_login()
        time.sleep(30)
        logout_rc = saml_user_logout()
        fw_page_ui.quit()
        if login_rc & logout_rc:
            login_again_rc = saml_user_ula_login()
            time.sleep(30)
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(login_again_rc, True, 'ERR: verify SLO action Failed!!')


# Check the SAML user type/mode in the user-status table
# This case including in TC01
class Test_TC04(Test):
    uuid = "SOSAIOT-TC-77535"
    description = show_testcase_info(TESTPLAN, '3258952', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258952')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_saml_user_status(self):
        Assertion.assert_equal(True, True, 'ERR: check_saml_user_status failed!!')


# Verify the SMAL log 'ID:1765 User Authenticated by SAML
class Test_TC05(Test):
    uuid = "SOSAIOT-TC-77541"
    description = show_testcase_info(TESTPLAN, '3318761', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3318761')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_user_authentication_log(self):
        logs = log_mon_api.export_log_txt()
        logger.info(logs)
        rc = "Start SAML Authentication Process." in logs
        Assertion.assert_equal(rc, True, 'ERR: check user authentication log failed!!')


# Verify the SMAL log 'ID: 1773 SAML Authentication Start
class Test_TC06(Test):
    uuid = "SOSAIOT-TC-77543"
    description = show_testcase_info(TESTPLAN, '3318771', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3318771')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_saml_authentication_start_log(self):
        logs = log_mon_api.export_log_txt()
        logger.info(logs)
        rc = "User account ' 'sonicauto' ' authenticated by SAML" in logs
        Assertion.assert_equal(rc, True, 'ERR: check saml_authentication_start_log failed!!')


# Verify the SMAL log 'ID: 1774 SAML Assertion Received
class Test_TC07(Test):
    uuid = "SOSAIOT-TC-77544"
    description = show_testcase_info(TESTPLAN, '3318772', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3318772')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_saml_assertion_received_log(self):
        logs = log_mon_api.export_log_txt()
        logger.info(logs)
        rc = "SAML Assertion received from  192.168.168.169" in logs
        Assertion.assert_equal(rc, True, 'ERR: check saml_assertion_received log failed!!')


# Verify the SMAL log 'ID: 1775 SAML Single Lougout request Received
class Test_TC08(Test):
    uuid = "SOSAIOT-TC-77545"
    description = show_testcase_info(TESTPLAN, '3318773', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3318773')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_saml_logout_request_received_log(self):
        logs = log_mon_api.export_log_txt()
        logger.info(logs)
        rc = "SAML Single Logout request Received from SAML Logout request received from 192.168.168.169" in logs
        Assertion.assert_equal(rc, True, 'ERR: check saml_logout_request_received log failed!!')


# Verify the LAN-WAN traffic include a SAML user after FW reboot
class Test_TC09(Test):
    uuid = "SOSAIOT-TC-77536"
    description = show_testcase_info(TESTPLAN, '3258953', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258953')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reboot_firewall(self):
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: reboot fw failed!')

    @repeat_method(5, sleep=10)
    def test_02_check_fun_after_restart(self):
        rc = saml_user_ula_login()
        if rc:
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check saml ULA after reboot failed!!')


# restore
class Test_TC10(Test):
    uuid = "SOSAIOT-TC-77537"
    description = show_testcase_info(TESTPLAN, '3258954', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258954')
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
            'dns1': Parameter.X1_DNS_1,
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
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed')

    def test_04_import_idp_ca(self):
        rc = False
        cert_file = suite_path + '/definition/file/saml_cyuan.cer'
        pc1_login.send_command(f'\cp {cert_file} /tmp')
        res = subprocess.run(['ls', '/tmp'], capture_output=True, text=True)
        print(res.stdout)
        if 'saml_cyuan.cer' in res.stdout:
            logger.info('cp cert file to PC1 success!!')
            rc = ca_api.import_ca_cert(file='/tmp/saml_cyuan.cer')
        else:
            logger.error('cp cert file to PC1 failed!!')
        Assertion.assert_equal(rc, True, "ERR: import ca file failed!!")

    def test_05_import_exp(self):
        rc = setting_api.import_setting_exp(filepath='/tmp/cyuan.exp')
        Assertion.assert_equal(rc, True, "ERR: import settings failed!!")

    @repeat_method(5, sleep=10)
    def test_06_check_settings_after_restore(self):
        rc = saml_user_ula_login()
        if rc:
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check user manage firewall after restore Failed!!')


# Verify the LAN-WAN traffic exclude a SAML user
class Test_TC11(Test):
    uuid = "SOSAIOT-TC-77517"
    description = show_testcase_info(TESTPLAN, '3258934', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258934')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_acl_exclude_user(self):
        rc1 = acl.delete_accessrule_by_name(name='redirect_saml')
        logger.info(f'-> Delete added redirect saml ACL result: {rc1}')
        opt = {"access_rules": [{
            'ipv4': {
                "name": "redirect_saml",
                "from": "any",
                "to": "WAN",
                'saml_authentication': True,
                'saml_profile': "profile_azure_X0",
                "service": {
                    "name": "HTTPS"
                },
                'users': {'included': {'all': True}, 'excluded': {'name': "cyuan"}},
                "priority": {'manual': {'value': 30}}
            }}]
        }
        rc2 = acl.add_accessrule(**opt)
        fw.api_logout()
        Assertion.assert_equal(rc2, True, 'ERR: edit redirect acl to exclude user failed!!')

    @repeat_method(5, sleep=10)
    def test_03_verify_LAN_WAN_traffic_exclude_saml_user(self):
        rc = True
        login_rc = saml_user_ula_login(user='cyuan@lusunshine1314163.onmicrosoft.com')
        time.sleep(2)
        if login_rc:
            fw_page_ui.switchToDefaultWindow()
            time.sleep(3)
            rc = fw_page_ui.does_page_have_text('cyuan test')
            time.sleep(3)
        fw_page_ui.quit()
        Assertion.assert_equal(rc, False, 'ERR: verify_LAN_WAN_traffic_exclude_saml_user failed!!')


# Check the SSLVPN service profile should not listed into the LAN-WAN Access Rule SAML profile
class Test_TC12(Test):
    uuid = "SOSAIOT-TC-77549"
    description = show_testcase_info(TESTPLAN, '3392671', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3392671')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sslvpn_service_sp(self):
        sp = {
            "domain_name": "shanghaiqa.com",
            'name': "sp_sslvpn",
            'service': {'sslvpn': True},
            'type': "domain"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add_sslvpn_service_sp failed!!")

    def test_02_add_sslvpn_service_profile(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure_X0",
            'management': False,
            'name': "profile_sslvpn",
            'service_provider': "sp_sslvpn",
            'single_sign_off': True,
            'single_logout': True,
            'sslvpn': True,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add_sslvpn_service_profile failed!!")

    def test_03_check_sslvpn_profile_not_list_in_saml_acl(self):
        saml_acl = acl.get_access_rule_by_name('redirect_saml')
        logger.info(saml_acl)
        uuid = saml_acl['ipv4']['uuid']
        logger.info(f'-> uuid is: {uuid}')
        init_test_page()
        fw_page_ui.click_element('xpath', "//span[contains(text(), 'Default & Custom')]/../following-sibling::div")
        logger.info('-> Click Default & Custom from acces rule...')
        time.sleep(2)
        fw_page_ui.click_element('xpath', "//span[text()= 'Custom Rules']")
        logger.info('-> Select Custom Rules Done...')
        time.sleep(2)
        fw_page_ui.click_element('xpath', f'//input[@name="check_{uuid}"]/following-sibling::div')
        logger.info('-> Select The Redirect Saml acl rule Done...')
        time.sleep(2)
        fw_page_ui.click_element('xpath', '//span[text()="Edit"]')
        logger.info('-> Click Edit Button Done...')
        time.sleep(2)
        fw_page_ui.click_element('xpath', '//span[text()="User & TCP/UDP"]')
        logger.info('-> Select User & TCP/UDP tab Done...')
        fw_page_ui.click_element('xpath',
                                 '//input[@name="saml-profile"]/following-sibling::div[contains(@class, "sw-select__icon")]')
        rc = fw_page_ui.does_page_have_text('sp_sslvpn')
        logger.info(f'-> Check sslvpn profile result: {rc}')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, False, 'ERR: check_sslvpn_profile_not_list_in_saml_acl failed!!')


# Verify the LAN-WAN Access rule include SAML user info was saved in the TSR
class Test_TC13(Test):
    uuid = "SOSAIOT-TC-77518"
    description = show_testcase_info(TESTPLAN, '3258935', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258935')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_saml_info_in_tsr(self):
        rc = False
        diag_api.download_tsr('/tmp/techSupport')
        tsr_info = pc1_login.send_command('cat /tmp/techSupport')
        acl_tsr_info = re.search(r'Firewall : Access Rules_START(.*)#Firewall : Security Policy Table_END', tsr_info,
                                 re.DOTALL).group(1)
        # logger.info(f'-> Got ACL trs Info as follow: \n{acl_tsr_info}')
        acl_list = acl_tsr_info.split('\n\n')
        for acl in acl_list:
            if bool(re.search(r'SAML Authentication:\s+Enabled', acl,
                              re.M)) and 'SAML Profile: profile_azure_X0' in acl:
                logger.info(f'-> find the matched ACL: \n{acl}')
                rc = True
                break
        else:
            logger.info('Not Find the matched ACL')
        Assertion.assert_equal(rc, True, 'ERR: check_saml_info_in_tsr Failed!!')


# Verify changing of SAML Profile name should not be affected the in ULA Policy
class Test_TC14(Test):
    uuid = "SOSAIOT-TC-77552"
    description = show_testcase_info(TESTPLAN, '3765189', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3765189')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_saml_acl(self):
        rc = acl.delete_accessrule_by_name(name='redirect_saml')
        Assertion.assert_equal(rc, True, 'ERR: Delete added redirect saml ACL failed!!')

    def test_02_add_saml_acl(self):
        opt = {"access_rules": [{
            'ipv4': {
                "name": "redirect_saml",
                "from": "any",
                "to": "WAN",
                'saml_authentication': True,
                'saml_profile': "profile_azure_X0",
                "service": {
                    "name": "HTTPS"
                },
                'users': {'included': {'group': "Everyone"}, 'excluded': {'none': True}},
                "priority": {'manual': {'value': 30}}
            }}]
        }
        rc = acl.add_accessrule(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add saml acl failed!!')

    def test_03_verify_inuse_profile_cannot_change_name(self):
        opt = {
            'name': "profile_azure_test",
        }
        rc, err_msg = saml_api.edit_saml_profile_by_name("profile_azure_X0", msg=True, **opt)
        logger.info(json.dumps(err_msg))
        Assertion.assert_equal(rc, False, 'ERR: verify_inuse_profile_cannot_change_name failed!!')


# Verify in-used SAML Profile should be not allowed to change its service type
class Test_TC15(Test):
    uuid = "SOSAIOT-TC-77551"
    description = show_testcase_info(TESTPLAN, '3765188', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3765188')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_profile_can_not_modify_to_sslvpn_sp(self):
        saml_profile = {
            'service_provider': "sp_sslvpn",
            'sslvpn': True,
        }
        rc, err_msg = saml_api.edit_saml_profile_by_name("profile_azure_X0", msg=True, **saml_profile)
        logger.info(json.dumps(err_msg))
        Assertion.assert_equal(rc, False, 'ERR: verify_profile_can_not_modify_to_sslvpn_sp failed!!')


# Verify the SAML user activity when the user auth type is LDAP
class Test_TC16(Test):
    uuid = "SOSAIOT-TC-77521"
    description = show_testcase_info(TESTPLAN, '3258938', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258938')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_user_auth_to_LDAP(self):
        opt = {
            'auth_method': 'ldap'
        }
        rc = user_setting_api.user_method_authentication(**opt)
        api_logout = fw.api_logout()
        logger.info(f'API logout result: {api_logout}')
        Assertion.assert_equal(rc, True, 'ERR: update_user_auth_to_LDAP failed!!')

    @repeat_method(5, sleep=10)
    def test_03_verify_saml_user_authentication(self):
        rc = saml_user_ula_login()
        if rc:
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: verify saml_user_authentication failed!!')


# Check the CPU usage when initiate background traffic which hits an ACL with SAML enabled but did not complete the login
class Test_TC17(Test):
    uuid = "SOSAIOT-TC-77521"
    description = show_testcase_info(TESTPLAN, '3258942', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258942')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def refresh_page(self):
        for i in range(100):
            logger.info(f'-> Refresh the login page for the {i + 1} time...')
            time.sleep(2)
            fw_page_ui.refresh_browser()

    def test_01_check_cpu_usage_when_keep_saml_user_login_page_fresh(self):
        auth_page = False
        fw_page_ui.get_chrome_with_head(headless=True)
        fw_page_ui.go_to_url('https://12.12.1.169')
        time.sleep(1)
        # Check for user login page (email input field)
        fw_page_ui.switchToNewWindow()
        user_login_load = safe_element_check('xpath', '//input[@type="email"]')
        logger.info(f'-> Check User Login Page Load Result: {user_login_load}')
        
        if user_login_load:
            # refresh user login page for 100 times
            self.refresh_page() 
        else:
            fw_page_ui.switchToDefaultWindow()
            # Check for authentication required page
            auth_page = safe_element_check('xpath', '//*[contains(text(), "Authentication Required")]')
            logger.info(f'-> Check The Authentication Required Page Load Result: {auth_page}')
        
        if auth_page:
            logger.info('-> Click "Click here to log in"...')
            fw_page_ui.click_element('xpath', '//a[contains(text(), "Click here to log in")]')
            fw_page_ui.switchToNewWindow()
            time.sleep(5)
            self.refresh_page()
            
        fw_page_ui.quit()
        logger.info('-> Check the CPU usage...')
        _, out = fw_cli.do_cli_commands(['diag show cpu'], tag=1)
        pattern = r'CPU Utilization History for Last Minute \(60 seconds ago --> now\):(.*)CPU Utilization History for Last Hour'
        cpu_usage_info = re.search(pattern, out, re.DOTALL).group(1).strip()
        logger.info(cpu_usage_info)
        usage_list = cpu_usage_info.split(',')
        for usage in usage_list:
            if int(usage) > 90:
                rc = False
                logger.info('-> Got CPU usage is High at last 60 sec...')
                break
        else:
            rc = True
        Assertion.assert_equal(rc, True, 'ERR: test_01_check_cpu_usage_when_keep_saml_user_login_page_fresh failed!!')


# Verify the ULA case with SAML user when the Guest User is enabled on the client
class Test_TC18(Test):
    uuid = "SOSAIOT-TC-77532"
    description = show_testcase_info(TESTPLAN, '3258949', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258949')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_guest_service_on_LAN(self):
        opt = zone_api.show_zone_object(name='LAN')
        opt['zones'][0]['guest_services']['enable'] = True
        rc = zone_api.edit_zone_object(name='LAN', **opt)
        Assertion.assert_equal(rc, True, 'ERR: enable guest service on LAN zone Failed!!')

    @repeat_method(5, sleep=10)
    def test_02_check_saml_ula_after_enable_guest_service_LAN(self):
        fw_page_ui.get_chrome_with_head(headless=True)
        fw_page_ui.go_to_url('https://12.12.1.169')
        time.sleep(1)
        logger.info(f'-> Check if The Authentication Required Page Loads Successfully!!')
        cur_url = fw_page_ui.get_current_browser_url()
        logger.info(f'-> Got current URL is : {cur_url}')
        rc = 'https://192.168.168.168/sonicui/7/login/' in cur_url
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_saml_ula_after_enable_guest_service_LAN Failed!!')

    def test_03_disable_guest_service_on_LAN(self):
        opt = zone_api.show_zone_object(name='LAN')
        opt['zones'][0]['guest_services']['enable'] = False
        rc = zone_api.edit_zone_object(name='LAN', **opt)
        fw.api_logout()
        Assertion.assert_equal(rc, True, 'ERR: disable guest service on LAN zone Failed!!')


# Verify the SLO activity from different clients if one client logout
class Test_TC19(Test):
    uuid = "SOSAIOT-TC-77539"
    description = show_testcase_info(TESTPLAN, '3258956', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258956')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # @repeat_method(10, sleep=10)
    def test_01_verify_SLO_from_different_client_if_one_client_logout(self):
        rc = False
        login_pc1 = saml_user_ula_login()
        logger.info(f'-> PC1 Login result: {login_pc1}')
        script_path = suite_path + '/definition/script.py'
        if login_pc1:
            out = pc3_login.send_command(f'python3 {script_path}')
            login_pc3 = 'saml user login from PC3 SUCCESS' in out
            logger.info(f'-> PC3 Login result: {login_pc3}')
            time.sleep(10)
            if login_pc3:
                logger.info('-> Go back to check current session....')
                page_source = fw_page_ui.get_page_source()
                logger.info(page_source)
                rc = "you are now logged into the device" in page_source
            else:
                logger.error('-> PC3 login Failed!!')
        else:
            logger.error('-> PC1 login Failed!! Try Another Test...')
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: verify SLO_from_different_client_if_one_client_logout failed!!')


# Verify the ULA case with SAML user if the Local user is a domain user
class Test_TC20(Test):
    uuid = "SOSAIOT-TC-77539"
    description = show_testcase_info(TESTPLAN, '3258948', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258948')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_local_user_as_domain_user(self):
        opt = {
            'action': "add",
            'username': "sonicauto",
            'userpassword': Parameter.PWD,
            'domain': 'lusunshine1314163.onmicrosoft.com',
            'member_of': ["Trusted Users", "Everyone"]
        }
        rc = local_user_api.local_user(**opt)
        fw.api_logout()
        Assertion.assert_equal(rc, True, 'ERR: add_local_user_as_domain_user failed!!')

    @repeat_method(5, sleep=10)
    def test_02_saml_user_login(self):
        rc = saml_user_ula_login()
        if rc:
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: saml user login failed when Local user is a domain user!!')


# Verify the SAML user override the option 'Redirect non-admin users from HTTPS to HTTP on completion of login'
class Test_TC21(Test):
    uuid = "SOSAIOT-TC-77534"
    description = show_testcase_info(TESTPLAN, '3258951', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258951')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_test_option(self):
        opt = user_setting_api.show_user_setting()
        opt['user']['auth']['http_redirect_after_login'] = True
        rc = user_setting_api.user_settings_base(**opt)
        fw.api_logout()
        Assertion.assert_equal(rc, True,
                               'ERR: enable the option "Redirect non-admin users from HTTPS to HTTP on completion of login" failed!!')

    @repeat_method(5, sleep=10)
    def test_02_verify_saml_user_override_the_option(self):
        rc = saml_user_ula_login()
        if rc:
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: verify_saml_user_override_the_option failed!!')


# Verify the SAML user override the option 'On redirecting unauthenticated users, redirect to an external login page'
class Test_TC22(Test):
    uuid = "SOSAIOT-TC-77533"
    description = show_testcase_info(TESTPLAN, '3258950', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258950')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_tested_option(self):
        opt = user_setting_api.show_user_setting()
        opt['user']['auth']['redirect_external_page'] = 'https://baidu.com'
        rc = user_setting_api.user_settings_base(**opt)
        fw.api_logout()
        Assertion.assert_equal(rc, True,
                               'ERR: enable the option "On redirecting unauthenticated users, redirect to an external login page" failed!!')

    @repeat_method(5, sleep=10)
    def test_02_verify_saml_user_override_the_option(self):
        rc = saml_user_ula_login()
        if rc:
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: verify_saml_user_override_the_option failed!!')


# Verify the LAN-WAN traffic include a SAML user for group mapping with SAML user-group identification
class Test_TC23(Test):
    uuid = "SOSAIOT-TC-77548"
    description = show_testcase_info(TESTPLAN, '3392670', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3392670')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_local_group_in_IDP(self):
        opt = {'user': {'local': {'group': [{'name': "qa", 'domain': "any"}]}}}
        rc = local_user_api.add_local_group(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add local group in IDP failed!!')

    def test_02_add_qa_group_to_Everyone(self):
        opt = {
            "user": {
                "local": {
                    "group": [{
                        'bookmark': [],
                        'comment': "",
                        'domain': "any",
                        'member': [{'name': "cyuan"}, {'name': "qa"}],
                        'name': "Everyone",
                        'one_time_password': {},
                        'to_management_on_login': False,
                        'vpn_client_access': []
                    }]
                }
            }
        }
        rc = local_user_api.config_local_group_by_name(groupname='Everyone', domainname='any', **opt)
        api_logout = fw.api_logout()
        logger.info(f'-> API Logout Result: {api_logout}')
        Assertion.assert_equal(rc, True, 'ERR: add_qa_group_to_Sonicwall_Administration failed!!')

    @repeat_method(5, sleep=10)
    def test_03_check_saml_user_login(self):
        rc = saml_user_ula_login()
        if rc:
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_saml_user_login failed!!')


# Verify the SAML user activity with custom HTTPS port
class Test_TC24(Test):
    uuid = "SOSAIOT-TC-77524"
    description = show_testcase_info(TESTPLAN, '3258941', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3258941')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_management_https_port(self):
        opt = {
            'https_port': 444
        }
        rc = admin_api.conf_admin(**opt)
        api_logout = fw.api_logout()
        logger.info(f'-> API Logout Result: {api_logout}')
        Assertion.assert_equal(rc, True, 'ERR: update_management_https_port to 444 failed!!')

    @repeat_method(5, sleep=10)
    def test_02_check_saml_user_login(self):
        rc = saml_user_ula_login()
        if rc:
            saml_user_logout()
        fw_page_ui.quit()
        Assertion.assert_equal(rc, True, 'ERR: check_saml_user_login failed!!')

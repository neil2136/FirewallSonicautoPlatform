from settings import *
import re


class TestErrorLdapServer_TC3937374(Test):
    uuid = "SOSAIOT-TC-48505"
    description = "GEN7-51992:The firmware will not crash when try to test not added ldap server via command test 10.8.141.175 type ldap-search basic test use user login-name"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3937374')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_test_error_ldap_server_via_cli(self):
        cmds = [
            'configure',
            'user ldap',
            'test 12.3.4.100 type ldap-search basic ldap1 use user login-name',
            'end',
            'exit']
        output, msg = fw_cli.do_cli_commands(cmds, tag=1)
        logger.info(f'output after test error ldap server via cli: {output}')
        Assertion.assert_regular(msg, 'Error', "ERR: Test error ldap server via cli failed")

    @repeat_method(5)
    def test_02_check_fw_no_crash(self):
        logger.info("Wait for 30s to check the firewall is still alive after test error ldap server via cli")   
        time.sleep(30)
        output = os.popen(f'ping {Parameter.FIREWALL} -c 30').read()
        Assertion.assert_regular(output, '30 received', "ERR: Firewall is down after test error ldap server via cli")


# smoke case 1-9, full case 10-59
class Test_01_user_method_list(Test):
    uuid = "SOSAIOT-TC-48456"
    description = show_testcase_info(TESTPLAN,
                                     "1", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_list_user_method(self):
        result = usersstatuscli.list_user_methods()
        logger.info('list user method result: {}'.format(result))
        flag = True if 'authentication' and 'ldap' and 'local' and 'radius' and 'sso' in result else False
        Assertion.assert_equal(flag, True, "ERR: list user methods failed")


class Test_10_configure_login_uniqueness(Test):
    uuid = "SOSAIOT-TC-48473"
    description = show_testcase_info(TESTPLAN,
                                     "10", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_login_uniqueness(self):
        authen_setting_dict['login-uniqueness'] = True
        rc = userssettingscli.authen_setting(**authen_setting_dict)
        Assertion.assert_equal(rc, True, "ERR: modify login uniqueness failed")

    def test_02_check_result_in_CLI(self):
        auth_type = 'base'
        result = userssettingscli.show_authen_setting(auth_type)
        flag = True if 'no login-uniqueness' not in result else False
        Assertion.assert_equal(flag, True, "ERR: Check login-uniqueness in CLI failed")


class Test_11_user_method_configure(Test):
    uuid = "SOSAIOT-TC-48457"
    description = show_testcase_info(TESTPLAN,
                                     "11", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_user_method(self):
        auth_methods = ['ldap', 'ldap-local', 'radius', 'radius-local', 'local']
        auth_type = 'methods'
        res = True
        for authmethod in auth_methods:
            authen_setting_dict['auth-method'] = authmethod
            rc = userssettingscli.authen_setting(**authen_setting_dict)
            logger.info('config auth methods to {} result：{}'.format(authmethod, rc))
            res &= rc

            checkresult = userssettingscli.show_authen_setting(auth_type)
            flag = True if 'auth-method ' + authen_setting_dict['auth-method'] in checkresult else False
            logger.info('show auth method {} result: {}'.format(authmethod, flag))
            res &= flag
            time.sleep(5)
        Assertion.assert_equal(res, True, "ERR: modify user methods failed")


class Test_12_configure_auth_bypass(Test):
    uuid = "SOSAIOT-TC-48474"
    description = show_testcase_info(TESTPLAN,
                                     "12", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_auth_bypass(self):
        rc = userssettingscli.auth_bypass(**add_auth_bypass_dict)
        Assertion.assert_equal(rc, True, "ERR: add rule-auth-bypass-http-urls failed")

    def test_02_check_result_in_CLI(self):
        flag = False
        auth_type = 'rule-auth-bypass-http-url'

        result = userssettingscli.show_authen_setting(auth_type)
        if add_auth_bypass_dict[auth_type] in result:
            flag = True
            userssettingscli.auth_bypass(**del_auth_bypass_dict)

        Assertion.assert_equal(flag, True, "ERR: check add rule-auth-bypass-http-urls in CLI failed")


class Test_13_show_auth_user_status(Test):
    uuid = "SOSAIOT-TC-48475"
    description = show_testcase_info(TESTPLAN,
                                     "13", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_show_auth_user_status(self):
        authen_setting_dict['show-user-status-window'] = True

        rc = userssettingscli.authen_setting(**authen_setting_dict)
        Assertion.assert_equal(rc, True, "ERR: modify show_auth_user_status failed")

    def test_02_check_result_in_CLI(self):
        auth_type = 'base'
        result = userssettingscli.show_authen_setting(auth_type)
        flag = True if 'no show-user-status-window' not in result else False

        authen_setting_dict['initcmds'] = []
        Assertion.assert_equal(flag, True, "ERR: check show-user-status-window in CLI failed")


class Test_14_configure_status_window_heartbeat(Test):
    uuid = "SOSAIOT-TC-48476"
    description = show_testcase_info(TESTPLAN,
                                     "14", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_status_window_hearbeat(self):
        user_sessions_dict = {'show-user-status-window': '60', 'disconnected-user-detect': '99'}

        rc = userssettingscli.user_sessions(**user_sessions_dict)
        Assertion.assert_equal(rc, True, "ERR: modify status_window_hearbeat failed")

    def test_02_check_result_in_CLI(self):
        auth_type = 'base'
        result = userssettingscli.show_authen_setting(auth_type)
        flag = True if 'status-window-heartbeat period 60' and 'status-window-heartbeat timeout 99' in result else False
        Assertion.assert_equal(flag, True, "ERR: check result in CLI failed")


class Test_15_configure_web_login_session_limit(Test):
    uuid = "SOSAIOT-TC-48477"
    description = show_testcase_info(TESTPLAN,
                                     "15", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_web_login_session_limit(self):
        user_sessions_dict = {'web-login-session-limit': '123'}
        rc = userssettingscli.user_sessions(**user_sessions_dict)
        Assertion.assert_equal(rc, True, "ERR: modify web_login_session_limit failed")

    def test_02_check_result_in_CLI(self):
        auth_type = 'base'
        result = userssettingscli.show_authen_setting(auth_type)
        flag = True if 'web-login-session-limit 123' in result else False
        Assertion.assert_equal(flag, True, "ERR: check result in CLI failed")


class Test_16_configure_ldap_allow_references(Test):
    uuid = "SOSAIOT-TC-48478"
    description = show_testcase_info(TESTPLAN,
                                     "16", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_ldap_allow_references(self):
        rc = userldapcli.ldap_settings(**ldap_allow_references_dict)
        Assertion.assert_equal(rc, True, "ERR: modify ldap_allow_references failed")

    def test_02_check_result_in_CLI(self):
        auth_type = 'base'
        result = userldapcli.show_ldap_setting(auth_type)
        flag = True if 'no allow-references user-authentication' not in result else False
        Assertion.assert_equal(flag, True, "ERR: check result in CLI failed")


class Test_17_configure_ldap_allow_referrals(Test):
    uuid = "SOSAIOT-TC-48479"
    description = show_testcase_info(TESTPLAN,
                                     "17", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_ldap_allow_referrals(self):
        rc = userldapcli.ldap_settings(**ldap_setting_dict)
        Assertion.assert_equal(rc, True, "ERR: modify ldap allow referrals failed")

    def test_02_check_result_in_CLI(self):
        auth_type = 'base'
        result = userldapcli.show_ldap_setting(auth_type)
        flag = True if 'no allow-referrals' not in result else False
        Assertion.assert_equal(flag, True, "ERR: enable allow-referrals failed")


class Test_combined_tc_10_11_12_13_15_16_17(Test):
    uuid = 'NonTC'

    def test_01_combined_tc_10_11_12_13_15_16_17(self):
        auth_type = 'base'
        rc = userauthcli.auth_cli3(**combined_auth_dict)
        result = userssettingscli.show_authen_setting(auth_type)
        #check acceptable-use-policy
        flag = True if 'window-size 480 350' and 'content 22356' in result else False
        check_auth_dict['acceptable-use-policy'] = flag
        #check aup-on-zones
        check_auth_dict['aup-on-zones'] = True if 'aup-on-zones trusted' and 'aup-on-zones wan' and 'aup-on-zones public' in result else False
        #check auth-page-timeout
        check_auth_dict['auth-page-timeout'] = True if 'auth-page-timeout 10' in result else False
        #check case-sensitive-names
        check_auth_dict['case-sensitive-names'] = True if 'no case-sensitive-names' not in result else False
        #check disconnected-user-detect
        check_auth_dict['disconnected-user-detect'] = True if 'no disconnected-user-detect' not in result else False
        #check http-redirect-after-login
        check_auth_dict['http-redirect-after-login'] = True if 'no http-redirect-after-login' not in result else False
        #check inactivity-timeout
        check_auth_dict['inactivity-timeout'] = True if 'inactivity-timeout 40' in result else False

        combined_auth_dict['initcmds'] = []
        Assertion.assert_equal(rc, True, "ERR: Combined command failed")


class Test_2_configure_auth_acceptable_use_policy(Test):
    uuid = "SOSAIOT-TC-48459"
    description = show_testcase_info(TESTPLAN,
                                     "2", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_auth_acceptable_use_policy(self):
        Assertion.assert_equal(check_auth_dict['acceptable-use-policy'], True, "ERR: modify acceptable-use-policy failed")


class Test_3_configure_auth_aup_on_zones(Test):
    uuid = "SOSAIOT-TC-48485"
    description = show_testcase_info(TESTPLAN,
                                     "3", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_auth_aup_on_zones(self):
        Assertion.assert_equal(check_auth_dict['aup-on-zones'], True, "ERR: modify auth_aup_on_zones failed")


class Test_4_configure_auth_page_timeout(Test):
    uuid = "SOSAIOT-TC-48491"
    description = show_testcase_info(TESTPLAN,
                                     "4", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_auth_page_timeout(self):
        Assertion.assert_equal(check_auth_dict['auth-page-timeout'], True, "ERR: modify auth-page-timeout failed")


class Test_5_configure_auth_case_sensitive_names(Test):
    uuid = "SOSAIOT-TC-48496"
    description = show_testcase_info(TESTPLAN,
                                     "5", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_auth_case_sensitive_names(self):
        Assertion.assert_equal(
            check_auth_dict['case-sensitive-names'], True, "ERR: modify case-sensitive-names failed")


class Test_6_list_auth_cli(Test):
    uuid = "SOSAIOT-TC-48471"
    description = show_testcase_info(TESTPLAN,
                                     "6", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_list_auth_cli(self):
        result = userssettingscli.list_authen_cli()
        flag = True if 'api-json' and 'format' and 'ftp' and 'history' and 'idle-timeout' and 'interactive-prompts' and 'pager' in result else False
        Assertion.assert_equal(flag, True, "ERR: list user methods failed")


class Test_7_auth_disconnected_user_detect(Test):
    uuid = "SOSAIOT-TC-48502"
    description = show_testcase_info(TESTPLAN,
                                     "7", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_auth_disconnected_user_detect(self):
        Assertion.assert_equal(
            check_auth_dict['disconnected-user-detect'], True, "ERR: modify disconnected-user-detect failed")


class Test_8_auth_http_redirect_after_login(Test):
    uuid = "SOSAIOT-TC-48503"
    description = show_testcase_info(TESTPLAN,
                                     "8", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_auth_http_redirect_after_login(self):
        Assertion.assert_equal(check_auth_dict['http-redirect-after-login'], True, "ERR: modify http-redirect-after-login failed")


class Test_9_auth_inactivity_timeout(Test):
    uuid = "SOSAIOT-TC-48504"
    description = show_testcase_info(TESTPLAN,
                                     "9", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_auth_inactivity_timeout(self):
        Assertion.assert_equal(check_auth_dict['inactivity-timeout'], True,
                               "ERR: modify inactivity-timeout failed")


class Test_Combined_tc_18_19_20_22_23_24_25_26_27(Test):
    uuid = 'NonTC'

    def test_01_combined_tc_18_19_20_22_23_24_25_26_27(self):
        
        rc = userauthcli.ldap_cli3(**combined_ldap_dict)
        baseresult = userldapcli.show_ldap_setting('base')
        serverresult = userldapcli.show_ldap_setting('servers')
        #check default-user-group
        flag = True if 'default-user-group \"Trusted Users\"' in baseresult else False
        
        check_ldap_dict['default-user-group'] = flag
        #check directory primary-domain
        check_ldap_dict['primary-domain'] = True if 'primary-domain autodirectory.com' in serverresult else False
        # check local-tls-certificate
        check_ldap_dict['local-tls-certificate'] = True if 'no local-tls-certificate' not in baseresult else False
        # check local-users-only
        check_ldap_dict['local-users-only'] = True if 'no local-users-only' not in baseresult else False
        # check operation-timeout
        check_ldap_dict['operation-timeout'] = True if 'timeout operation 19' in serverresult else False
        # check relay
        check_ldap_dict['relay'] = True if 'no enable' not in baseresult else False
        # check schema
        check_ldap_dict['schema'] = True if 'schema samba-smb' in serverresult else False
        # check server member
        check_ldap_dict['server-member'] = True if 'server 12.3.4.5' in serverresult else False

        combined_auth_dict['initcmds'] = []
        Assertion.assert_equal(rc, True, "ERR: Combined command failed")


class Test_18_ldap_default_user_group(Test):
    uuid = "SOSAIOT-TC-48480"
    description = show_testcase_info(TESTPLAN,
                                     "18", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_default_user_group(self):
        Assertion.assert_equal(check_ldap_dict['default-user-group'], True, "ERR: modify default-user-group failed")


class Test_19_ldap_directory(Test):
    uuid = "SOSAIOT-TC-48458"
    description = show_testcase_info(TESTPLAN,
                                     "19", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_ldap_directory(self):
        Assertion.assert_equal(check_ldap_dict['primary-domain'], True,
                               "ERR: modify ldap_directory primary-domain failed")


class Test_20_ldap_local_tls_certificate(Test):
    uuid = "SOSAIOT-TC-48481"
    description = show_testcase_info(TESTPLAN,
                                     "20", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_local_tls_certificate(self):
        Assertion.assert_equal(check_ldap_dict['local-tls-certificate'], True,
                               "ERR: modify local-tls-certificate failed")


class Test_22_ldap_local_user_only(Test):
    uuid = "SOSAIOT-TC-48460"
    description = show_testcase_info(TESTPLAN,
                                     "22", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_ldap_local_user_only(self):
        Assertion.assert_equal(check_ldap_dict['local-users-only'], True,
                               "ERR: modify local-users-only failed")


class Test_23_ldap_operation_timeout(Test):
    uuid = "SOSAIOT-TC-48461"
    description = show_testcase_info(TESTPLAN,
                                     "23", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_ldap_operation_timeout(self):
        Assertion.assert_equal(check_ldap_dict['operation-timeout'], True,
                               "ERR: modify operation-timeout failed")


class Test_24_ldap_relay(Test):
    uuid = "SOSAIOT-TC-48462"
    description = show_testcase_info(TESTPLAN,
                                     "24", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_ldap_relay(self):
        Assertion.assert_equal(check_ldap_dict['relay'], True,
                               "ERR: modify ldap relay failed")


class Test_25_ldap_schema(Test):
    uuid = "SOSAIOT-TC-48482"
    description = show_testcase_info(TESTPLAN,
                                     "25", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_ldap_schema(self):
        Assertion.assert_equal(check_ldap_dict['schema'], True,
                               "ERR: modify ldap schema failed")


class Test_26_ldap_server_member(Test):
    uuid = "SOSAIOT-TC-48463"
    description = show_testcase_info(TESTPLAN,
                                     "26", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_ldap_server_member(self):
        Assertion.assert_equal(check_ldap_dict['server-member'], True,
                               "ERR: add ldap server member failed")


class Test_Combine_tc_28_29_30_31(Test):
    uuid = 'NonTC'

    def test_01_combined_tc_28_29_30_31(self):
        
        rc = userauthcli.local_cli3(**combined_local_dict)
        logger.info(rc)
        baseresult = userlocalcli.show_local_setting('base')
        groupresult = userlocalcli.show_local_setting('group name Limited\ Administrators')
        userresult = userlocalcli.show_local_setting('users')
        #check apply-password-constraints
        flag = True if 'no apply-password-constraints' not in baseresult else False
        
        check_local_dict['apply-password-constraints'] = flag
        #check group member
        check_local_dict['groupmember'] = True if 'member '+local_user_dict['user'] in groupresult else False
        # check prune-on-expiry
        check_local_dict['prune-on-expiry'] = True if 'no prune-on-expiry' not in baseresult else False
        # check user added
        check_local_dict['user-added'] = True if 'user '+local_user_dict['user'] in userresult else False

        combined_auth_dict['initcmds'] = []
        Assertion.assert_equal(rc, True, "ERR: Combined command failed")


class Test_28_local_apply_password_constraints(Test):
    uuid = "SOSAIOT-TC-48483"
    description = show_testcase_info(TESTPLAN,
                                     "28", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_apply_password_constraints(self):
        Assertion.assert_equal(check_local_dict['apply-password-constraints'], True, "ERR: modify apply-password-constraints failed")


class Test_29_local_group_member(Test):
    uuid = "SOSAIOT-TC-48484"
    description = show_testcase_info(TESTPLAN,
                                     "29", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_local_group_member(self):
        Assertion.assert_equal(check_local_dict['groupmember'], True,
                               "ERR: add local group member failed")


class Test_30_local_prune_on_expiry(Test):
    uuid = "SOSAIOT-TC-48486"
    description = show_testcase_info(TESTPLAN,
                                     "30", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_local_prune_on_expiry(self):
        Assertion.assert_equal(check_local_dict['prune-on-expiry'], True,
                               "ERR: modify prune-on-expiry failed")


class Test_31_local_user_add(Test):
    uuid = "SOSAIOT-TC-48464"
    description = show_testcase_info(TESTPLAN,
                                     "31", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_local_user_add(self):
        Assertion.assert_equal(check_local_dict['user-added'], True,
                               "ERR: add local user failed")


class Test_Combine_tc_32_34_35_36_38_39(Test):
    uuid = 'NonTC'
    

    def test_01_combined_tc_32_34_35_36_38_39(self):
        
        rc = userauthcli.radius_cli3(**combined_radius_dict)
        baseresult = userradiuscli.show_radius_setting('base')
        serverresult = userradiuscli.show_radius_setting('servers')

        # check default-user-group
        flag = True if 'default-user-group \"Guest Services\"' in baseresult else False
        
        check_radius_dict['default-user-group'] = flag
        # check local-users-only
        check_radius_dict['local-users-only'] = True if 'no local-users-only' not in baseresult else False
        # check retries
        check_radius_dict['retries'] = True if 'retries '+combined_radius_dict['retries'] in baseresult else False
        # check add server host
        check_radius_dict['server-host'] = True if 'server '+combined_radius_dict['serverhost'] in serverresult else False
        # check timeout
        check_radius_dict['timeout'] = True if 'timeout '+combined_radius_dict['timeout'] in baseresult else False
        # check user-group-mechanism
        check_radius_dict['user-group-mechanism'] = True if 'radius-attribute '+combined_radius_dict['user-group-mechanism'] in baseresult else False

        combined_auth_dict['initcmds'] = []
        Assertion.assert_equal(rc, True, "ERR: Combined command failed")


class Test_32_radius_default_user_group(Test):
    uuid = "SOSAIOT-TC-48487"
    description = show_testcase_info(TESTPLAN,
                                     "32", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_radius_default_user_group(self):
        Assertion.assert_equal(check_radius_dict['default-user-group'], True, "ERR: modify default-user-group failed")


class Test_34_radius_local_user_only(Test):
    uuid = "SOSAIOT-TC-48465"
    description = show_testcase_info(TESTPLAN,
                                     "34", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_radius_local_user_only(self):
        Assertion.assert_equal(check_radius_dict['local-users-only'], True,
                               "ERR: modify radius local-users-only failed")


class Test_35_radius_retries(Test):
    uuid = "SOSAIOT-TC-48488"
    description = show_testcase_info(TESTPLAN,
                                     "35", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_radius_retries(self):
        Assertion.assert_equal(check_radius_dict['retries'], True,
                               "ERR: modify radius retries failed")


class Test_36_radius_server_host(Test):
    uuid = "SOSAIOT-TC-48466"
    description = show_testcase_info(TESTPLAN,
                                     "36", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_radius_server_host(self):
        Assertion.assert_equal(check_radius_dict['server-host'], True,
                               "ERR: add a radius server host failed")


class Test_38_radius_timeout(Test):
    uuid = "SOSAIOT-TC-48489"
    description = show_testcase_info(TESTPLAN,
                                     "38", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_radius_timeout(self):
        Assertion.assert_equal(check_radius_dict['timeout'], True,
                               "ERR: modify radius timeout failed")


class Test_39_radius_user_group_mechanism(Test):
    uuid = "SOSAIOT-TC-48490"
    description = show_testcase_info(TESTPLAN,
                                     "39", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_radius_user_group_mechanism(self):
        Assertion.assert_equal(check_radius_dict['user-group-mechanism'], True,
                               "ERR: modify radius user-group-mechanism failed")


class Test_Combined_TC_40_43_44_46_47_48_49_54_56_57_58(Test):
    uuid = 'NonTC'
    jira = 'GEN7-33892'

    def test_01_combined_tc_40_43_44_46_47_48_49_54_56_57_58(self):
        
        rc = userauthcli.sso_cli3(**combined_sso_dict)

        showsso = userssocli.show_sso_setting('sso')
        windowsresult = userssocli.show_sso_setting('windows-service-user-names')

        # check agent host
        flag = True if 'agent ' + combined_sso_dict['agent'] in showsso else False
        
        check_sso_dict['agent'] = flag
        # check enforce-on-zone
        check_sso_dict['enforce-on-zone'] = True if 'no enforce-on-zone ' + combined_sso_dict[
            'enforce-on-zone'] not in showsso else False
        # check hold-time-after-failure 10
        check_sso_dict['hold-time'] = True if 'hold-time ' + combined_sso_dict['hold-time'] in showsso else False
        # check local-users-only
        check_sso_dict['local-users-only'] = True if 'no local-users-only' not in showsso else False
        # check method sso-agent
        check_sso_dict['method'] = True if 'no method sso-agent' not in showsso else False
        # check non-domain-limited-access
        check_sso_dict['non-domain-limited-access'] = True if 'no non-domain-limited-access' not in showsso else False
        # check poll-rate
        check_sso_dict['poll-rate'] = True if 'poll rate 10' in showsso else False
        # check security-services-bypass-dns
        check_sso_dict['security-services-bypass-dns'] = True if re.search(r'DNS(.*)full-bypass', showsso,
                                                                           re.S | re.M) else False
        # check terminal-services-agent
        check_sso_dict['terminal-services-agent'] = True if 'terminal-services-agent ' + combined_sso_dict[
            'terminal-services-agent'] in showsso else False
        # check tsa-services-bypass
        check_sso_dict['tsa-services-bypass'] = True if 'no tsa-services-bypass' not in showsso else False
        # check user-group-mechanism ldap
        check_sso_dict['user-group-mechanism'] = True if 'user-group-mechanism ldap' in showsso else False
        # check windows-service-user-name someservice
        check_sso_dict['windows-service-user-name'] = True if combined_sso_dict[
                                                                  'windows-service-user-name'] in windowsresult else False

        combined_auth_dict['initcmds'] = []
        Assertion.assert_equal(rc, True, "ERR: Combined command failed")


class Test_40_sso_agent_host(Test):
    uuid = "SOSAIOT-TC-48467"
    description = show_testcase_info(TESTPLAN,
                                     "40", description=True)['title']
    jira = 'GEN7-33892'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '40')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_sso_agent_host(self):
        Assertion.assert_equal(check_sso_dict['agent'], True, "ERR: add agent host failed")


class Test_41_sso_list_cli(Test):
    uuid = "SOSAIOT-TC-48468"
    description = show_testcase_info(TESTPLAN,
                                     "41", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_sso_list_cli(self):
        result = userssocli.list_sso_cli()
        flag = True if 'api-json' and 'format' and 'ftp' and 'history' and 'idle-timeout' and 'interactive-prompts' and 'pager' in result else False
        Assertion.assert_equal(flag, True, "ERR: list user methods failed")


class Test_43_sso_enforce_on_zone(Test):
    uuid = "SOSAIOT-TC-48492"
    description = show_testcase_info(TESTPLAN,
                                     "43", description=True)['title']
    jira = 'GEN7-33892'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_enforce_on_zone(self):
        Assertion.assert_equal(check_sso_dict['enforce-on-zone'], True,
                               "ERR: modify sso enforce-on-zone failed")


class Test_44_sso_hold_time_after_failure(Test):
    uuid = "SOSAIOT-TC-48493"
    description = show_testcase_info(TESTPLAN,
                                     "44", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_hold_time_after_failure(self):
        Assertion.assert_equal(check_sso_dict['hold-time'], True,
                               "ERR: modify sso hold-time after-failure failed")


class Test_46_sso_local_users_only(Test):
    uuid = "SOSAIOT-TC-48472"
    description = show_testcase_info(TESTPLAN,
                                     "46", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_local_users_only(self):
        Assertion.assert_equal(check_sso_dict['local-users-only'], True,
                               "ERR: modify sso local-users-only failed")


class Test_47_sso_method_sso_agent(Test):
    uuid = "SOSAIOT-TC-48469"
    description = show_testcase_info(TESTPLAN,
                                     "47", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '47')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_method_sso_agent(self):
        Assertion.assert_equal(check_sso_dict['method'], True,
                               "ERR: modify sso method sso-agent failed")


class Test_48_sso_non_domain_limited_access(Test):
    uuid = "SOSAIOT-TC-48494"
    description = show_testcase_info(TESTPLAN,
                                     "48", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '48')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_non_domain_limited_access(self):
        Assertion.assert_equal(check_sso_dict['non-domain-limited-access'], True,
                               "ERR: modify sso non-domain-limited-access failed")


class Test_49_sso_poll_rate(Test):
    uuid = "SOSAIOT-TC-48495"
    description = show_testcase_info(TESTPLAN,
                                     "49", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '49')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_poll_rate(self):
        Assertion.assert_equal(check_sso_dict['poll-rate'], True,
                               "ERR: modify sso poll-rate failed")


class Test_52_sso_security_services_bypass_dns(Test):
    uuid = "SOSAIOT-TC-48497"
    description = show_testcase_info(TESTPLAN,
                                     "52", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '52')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_security_services_bypass_dns(self):
        Assertion.assert_equal(check_sso_dict['security-services-bypass-dns'], True,
                               "ERR: modify sso security-services-bypass-dns failed")


class Test_54_sso_terminal_services_agent(Test):
    uuid = "SOSAIOT-TC-48498"
    description = show_testcase_info(TESTPLAN,
                                     "54", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '54')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_terminal_services_agent(self):
        Assertion.assert_equal(check_sso_dict['terminal-services-agent'], True,
                               "ERR: modify sso terminal-services-agent failed")


class Test_56_sso_tsa_services_bypass(Test):
    uuid = "SOSAIOT-TC-48499"
    description = show_testcase_info(TESTPLAN,
                                     "56", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_terminal_services_agent(self):
        Assertion.assert_equal(check_sso_dict['tsa-services-bypass'], True,
                               "ERR: modify sso tsa-services-bypass failed")


class Test_57_sso_user_group_mechanism(Test):
    uuid = "SOSAIOT-TC-48500"
    description = show_testcase_info(TESTPLAN,
                                     "57", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '57')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_user_group_mechanism(self):
        Assertion.assert_equal(check_sso_dict['user-group-mechanism'], True,
                               "ERR: modify sso user-group-mechanism failed")


class Test_58_sso_windows_service_user_name(Test):
    uuid = "SOSAIOT-TC-48501"
    description = show_testcase_info(TESTPLAN,
                                     "58", description=True)['title']
    jira = 'GEN7-33892'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '58')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_sso_windows_service_user_name(self):
        Assertion.assert_equal(check_sso_dict['windows-service-user-name'], True,
                               "ERR: modify sso windows-service-user-name failed")


class Test_59_check_local_users_groups(Test):
    uuid = "SOSAIOT-TC-48470"
    description = show_testcase_info(TESTPLAN,
                                     "59", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '59')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_local_users_groups(self):
        rc1 = userlocalcli.add_local_user(**add_user1_dict)
        rc2 = userlocalcli.add_local_user(**add_user2_dict)
        rc3 = userlocalcli.add_local_group(**add_group1_dict)
        rc = True if rc1 and rc2 and rc3 else False

        usercheck = userlocalcli.show_local_setting('user name '+add_user1_dict['user'])
        groupcheck = userlocalcli.show_local_setting('group name '+add_group1_dict['group'])

        if rc1:
            userlocalcli.delete_local_user(**del_user1_dict)
        if rc2:
            userlocalcli.delete_local_user(**del_user2_dict)
        if rc3:
            userlocalcli.delete_local_group(**del_group1_dict)

        checkgp = True if 'member-of '+add_group1_dict['group'] in usercheck else False
        checkuser = True if 'member '+add_user1_dict['user'] in groupcheck and add_user2_dict['user'] not in groupcheck else False
        result = True if checkgp and checkuser and rc else False
        Assertion.assert_equal(result, True, "ERR: check local users and local groups in CLI failed")

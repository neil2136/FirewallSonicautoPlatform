from definition.settings import *
from definition.ui_user import FWPage

class sslvpn_config(Test):
    uuid = 'NonTC'

    def test_01_install_nx_Linux(self):
        cpy_build = cp_nx.cpbuildnx_linux_local()
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux()
        logger.info(inst)

    def test_02_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")

    def test_03_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_04_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,
        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")

    def test_05_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "sslvpntest",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = user_local.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")

    def test_06_edit_user(self):
        edit_local_user_domain = {
            'action': 'edit',
            'oldusername': 'sslvpntest',
            'domain': 'os-autosnwl.com',
            'username': 'sslvpntest',
            'userpassword': 'password',
            'one_time_password': 'otp',
            'email_address': 'test1@smtpstest.com',
            # 'vpn_client_access': ['LAN Subnets'],
            "member_of": ['SSLVPN Services']
        }

        rc = user_local.local_user(**edit_local_user_domain)
        get_resp = user_local.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_07_add_mail_server(self):
        mail_server_dict = {
            "mail_server": PC1_ETH1_IP,
            "mail_from": 'ujjwal@smtpstest.com',
        }
        log_auto_config = logautomationapi.cfg_mail_server(**mail_server_dict)
        logger.info(f'mail_server_config:{log_auto_config}')

        log_auto_test = logautomationapi.mail_server_test()
        logger.info(f'mail_server_test:{log_auto_test}')

    def test_08_sslserver_settings_with_port_enabled(self):
        ssl_vpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': False,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
        server_settings = sslvpnserver.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(server_settings, True, "Err: failed to config server settings")

    def test_09_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_10_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test11_edit_radius_user_mechanism(self):
        edit_radius_server_json = {
            "user": {
                "radius": {
                    "timeout": 5,
                    "retries": 3,
                    "periodic_check_server": True,
                    "mschapv2_mode": False,
                    "local_users_only": False,
                    "user_group_mechanism": {
                        "ldap": True
                    }
                }
            }
        }
        radius_user = user_radius.edit_user_radius_settings(**edit_radius_server_json)
        logger.info("Radius user edited is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user edit failed")

class MFA_OTP_MAIL_1(Test):
    uuid = "SOSAIOT-TC-77304"

    description= show_testcase_info(TESTPLAN, '2424387', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2424387')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_http_server_on_PC2(self):
        http_server_config = [
            'ip r add 192.168.168.0/24 via 14.1.1.168',
            'service httpd start',
            'systemctl status httpd'
        ]
        output = PC2_login.send_commands(http_server_config)
        logger.info(output)

    def test_02_Radius_user_settings(self):
        user_authen = {
            "auth_method": "Radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    def test_04_enable_server_access(self):
        enable = {
            'LAN_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_05_login_via_radius_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168:4433", "sslvpntest", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

class MFA_OTP_MAIL_2(Test):
    uuid = "SOSAIOT-TC-77285"

    description= show_testcase_info(TESTPLAN, '1514466', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514466')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168", "test1", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_05_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

class MFA_OTP_MAIL_3(Test):
    uuid = "SOSAIOT-TC-77288"

    description= show_testcase_info(TESTPLAN, '1514469', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514469')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'Guest Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 10,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168", "test1", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_05_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

class MFA_OTP_MAIL_4(Test):
    uuid = "SOSAIOT-TC-77286"

    description= show_testcase_info(TESTPLAN, '1514467', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514467')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'Limited Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 10,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168", "test1", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_05_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

class MFA_OTP_MAIL_5(Test):
    uuid = "SOSAIOT-TC-77287"

    description= show_testcase_info(TESTPLAN, '1514468', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514468')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Read-Only Admins'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 10,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168", "test1", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_05_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

class MFA_OTP_MAIL_6(Test):
    uuid = "SOSAIOT-TC-77300"

    description= show_testcase_info(TESTPLAN, '1514482', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514482')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'force_password_change': True,
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 40,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168", "test1", "password", fpwd=True)
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_05_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

class MFA_OTP_MAIL_7(Test):
    uuid = "SOSAIOT-TC-77299"

    description= show_testcase_info(TESTPLAN, '1514481', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514481')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'force_password_change': True,
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'Limited Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168", "test1", "password", fpwd=True)
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_05_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

class MFA_OTP_MAIL_8(Test):
    uuid = "SOSAIOT-TC-77301"

    description= show_testcase_info(TESTPLAN, '1514483', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514483')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'force_password_change': True,
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Read-Only Admins'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 10,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168", "test1", "password", fpwd=True)
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_05_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

class MFA_OTP_MAIL_9(Test):
    uuid = "SOSAIOT-TC-77302"

    description= show_testcase_info(TESTPLAN, '1514484', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514484')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'force_password_change': True,
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'Guest Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168", "test1", "password", fpwd=True)
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_05_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

class MFA_OTP_MAIL_10(Test):
    uuid = "SOSAIOT-TC-77289"

    description= show_testcase_info(TESTPLAN, '1514470', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514470')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:LOCALs method is not selected successfully")

    def test_02_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestlocal',
            'userpassword': 'password',
            'force_password_change': True,
            'email_address': 'test1@smtpstest.com',
            'one_time_password': 'otp',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = user_local.local_user(**user_json)
        resp1 = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: sslvpntestlocal not created')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_04_enable_server_access(self):
        enable = {
            'LAN_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_05_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168:4433", "sslvpntestlocal", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_06_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('sslvpntestlocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: user not deleted')

class MFA_OTP_MAIL_11(Test):
    uuid = "SOSAIOT-TC-89781"

    description= show_testcase_info(TESTPLAN, '1514485', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514485')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:LOCALs method is not selected successfully")

    def test_02_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestlocal',
            'userpassword': 'password',
            'force_password_change': True,
            'email_address': 'test1@smtpstest.com',
            'one_time_password': 'otp',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = user_local.local_user(**user_json)
        resp1 = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: sslvpntestlocal not created')

    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_04_enable_server_access(self):
        enable = {
            'LAN_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_05_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168:4433", "sslvpntestlocal", "password", fpwd=True)
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_06_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('sslvpntestlocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: user not deleted')

class MFA_OTP_MAIL_12(Test):
    uuid = "SOSAIOT-TC-77291"

    description= show_testcase_info(TESTPLAN, '1514472', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514472')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "Radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_03_enable_server_access(self):
        enable = {
            'LAN_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_04_login_via_radius_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168:4433", "sslvpntest", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

class MFA_OTP_MAIL_13(Test):
    uuid = "SOSAIOT-TC-77290"

    description= show_testcase_info(TESTPLAN, '1514471', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514471')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_03_enable_server_access(self):
        enable = {
            'LAN_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_04_login_via_ldap_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168:4433", "sslvpntest", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

class MFA_OTP_MAIL_14(Test):
    uuid = "SOSAIOT-TC-77292"

    description= show_testcase_info(TESTPLAN, '1514473', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514473')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:LOCALs method is not selected successfully")

    def test_02_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestlocal',
            'userpassword': 'password',
            'email_address': 'test1@smtpstest.com',
            'one_time_password': 'otp',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = user_local.local_user(**user_json)
        resp1 = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: sslvpntestlocal not created')
    
    @repeat_method(5)
    def test_03_verify_NX_login_via_otp(self):
        connect_nxlinux_remote_with_otp_via_mail(user='sslvpntestlocal', pswd='password',
                                                 netexurl='192.168.168.168:4433',
                                                 domain='LocalDomain', openstack_PC='-PC1')

        flag = False
        save_path = '/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path, "r")
        data_read_text = data.read()
        if "Login successful" in data_read_text:
            flag = True
        Assertion.assert_equal(flag, True, 'err: User sslvpntestlocal is not present')

    def test_04_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('sslvpntestlocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: user not deleted')

class MFA_OTP_MAIL_15(Test):
    uuid = "SOSAIOT-TC-77294"

    description= show_testcase_info(TESTPLAN, '1514475', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514475')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_03_verify_NX_login_via_otp(self):

        connect_nxlinux_remote_with_otp_via_mail(user='sslvpntest', pswd='password', netexurl='192.168.168.168:4433',
                                                 domain='LocalDomain', openstack_PC='-PC1')

        save_path = '/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path, "r")
        data_read_text = data.read()
        if "Login successful" in data_read_text:
            m = True
            Assertion.assert_equal(m, True, 'err: User is not present')
        else:
            m = True
            Assertion.assert_equal(m, False, 'err: User is not present')

class MFA_OTP_MAIL_16(Test):
    uuid = "SOSAIOT-TC-77293"

    description= show_testcase_info(TESTPLAN, '1514474', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514474')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_03_verify_NX_login_via_otp(self):

        connect_nxlinux_remote_with_otp_via_mail(user='sslvpntest', pswd='password', netexurl='192.168.168.168:4433',
                                                 domain='LocalDomain', openstack_PC='-PC1')

        save_path = '/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path, "r")
        data_read_text = data.read()
        if "Login successful" in data_read_text:
            m = True
            Assertion.assert_equal(m, True, 'err: User is not present')
        else:
            m = True
            Assertion.assert_equal(m, False, 'err: User is not present')

class MFA_OTP_MAIL_17(Test):
    uuid = "SOSAIOT-TC-89783"

    description= show_testcase_info(TESTPLAN, '1514487', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514487')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"', "ERR:LOCALs method is not selected successfully")

    def test_02_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestlocal',
            'userpassword': 'password',
            'force_password_change': True,
            'email_address': 'test1@smtpstest.com',
            'one_time_password': 'otp',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = user_local.local_user(**user_json)
        resp1 = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: sslvpntestlocal not created')
    
    @repeat_method(5)
    def test_03_verify_NX_login_via_otp(self):

        connect_nxlinux_remote_with_otp_via_mail_forced_pwd(user='sslvpntestlocal', pswd='password',
                                                            netexurl='192.168.168.168:4433',
                                                            domain='LocalDomain', openstack_PC='-PC1', fpwd=True)
        flag = False
        save_path = '/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path, "r")
        data_read_text = data.read()
        if "Your password was changed successfully" in data_read_text:
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: Unable to change password')
        logger.info("Password got changed successfully")

        connect_nxlinux_remote_with_otp_via_mail(user='sslvpntestlocal', pswd='S0nic@uto', netexurl='192.168.168.168:4433', domain='LocalDomain', openstack_PC='-PC1')

        flag = False
        save_path = '/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path, "r")
        data_read_text = data.read()
        if "Login successful" in data_read_text:
            flag = True
        Assertion.assert_equal(flag, True, 'err: User sslvpntestlocal is not present')

    def test_04_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('sslvpntestlocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: user not deleted')

class MFA_OTP_MAIL_18(Test):
    uuid = "SOSAIOT-TC-77303"

    description= show_testcase_info(TESTPLAN, '1514488', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514488')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")
    def test_02_edit_user(self):
        edit_local_user_domain = {
                'action': 'edit',
                'oldusername': 'sslvpntest',
                'domain': 'os-autosnwl.com',
                'username': 'sslvpntest',
                'userpassword': 'password',
                'force_password_change': True,
                'one_time_password': 'otp',
                'email_address': 'test1@smtpstest.com',
                # 'vpn_client_access': ['LAN Subnets'],
                "member_of": ['SSLVPN Services']
        }

        rc = user_local.local_user(**edit_local_user_domain)
        get_resp = user_local.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")
    def test_03_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")
    
    @repeat_method(5)
    def test_04_verify_NX_login_via_otp(self):
        connect_nxlinux_remote_with_otp_via_mail(user='sslvpntest', pswd='password', netexurl='192.168.168.168:4433',
                                                 domain='LocalDomain', openstack_PC='-PC1')
        flag = False
        save_path = '/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path, "r")
        data_read_text = data.read()
        if "Login successful" in data_read_text:
            flag = True
        Assertion.assert_equal(flag, True, 'err: User is not present')

class MFA_OTP_MAIL_19(Test):
    uuid = "SOSAIOT-TC-89782"

    description= show_testcase_info(TESTPLAN, '1514486', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514486')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_02_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_03_enable_server_access(self):
        enable = {
            'LAN_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_04_login_via_ldap_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168:4433", "sslvpntest", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

def retrieve_otp_from_mail():
    try:
        received_mail = pop3_client.get_email(PC1_ETH1_IP, 'test1', 'password')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)
        logger.info("OTP is present in the mail")
        login_otp = str(received_mail).split("\n")[-1]
        logger.info('OTP is {}'.format(login_otp))
        return login_otp
    except Exception as err:
        logger.error(err)

class MFA_OTP_MAIL_20(Test):
    uuid = "SOSAIOT-TC-77282"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514462')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_X2_Zone_to_DMZ(self):
        logger.info("Set x2 zone to DMZ... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to DMZ failed")

    def test_02_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_03_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'password',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_04_edit_lan_dmz_access_rule(self):
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='DMZ')
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                acl_dict = copy.deepcopy(default_acl_dict)
                acl_dict.update({"users": {
                    "included": {"group": "Everyone"},
                    "excluded": {"none": True}
                }})
                res = accessrule_api.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                Assertion.assert_equal(res, True, "ERR: cannot added access rule")

    def test_05_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
            # ret = ret.decode() #converting byte to string
            # Assertion.assert_equal('+OK' in ret, True, "ERR: clear test1 inbox failed")
            
        except Exception as err:
            logger.err(err)
            Assertion.assert_equal(False, True, "ERR: Exception occurred while clearing inbox")

        Assertion.assert_equal(True, True, "ERR: clear user inbox failed")
    
    @repeat_method(5)
    def test_06_login_via_local_user(self):
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url = "https://14.1.1.168"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Multi_factor_auth_otp_mail/definition/ui_user.py ' + '-url ' + url + ' -user test1 -pwd password'
        out = PC2_login.send_command(cmd)
        logger.info(f"login with user\n{out}")
        time.sleep(10)

        http_server_config = [
            'ip r add 14.1.1.0/24 via 192.168.168.168',
            'service httpd start',
            'systemctl status httpd'
        ]
        output = static_client.send_commands(http_server_config)
        logger.info(output)

        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_07_delete_localUser(self):
        logger.info('Delete the user ')
        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

    def test_08_Modify_X2_Zone_to_LAN(self):
        logger.info("Set x2 zone to LAN... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to LAN failed")

    def test_09_Delete_Access_Rule(self):
        res = accessrule_api.reset_accessrule_default_setting()
        Assertion.assert_equal(res, True, 'reset access rules failed')

class MFA_OTP_MAIL_21(Test):
    uuid = "SOSAIOT-TC-77283"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514463')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_http_server_on_LAN_PC(self):
        HTTP_CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/User/Multi_factor_auth_otp_mail/config/httpserver'
        certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
        configPath = os.environ["PYTHON_SONICOS_HOME"] + '/DPI-SSL/Server_DPISSL_HTTPS/cert/httpd/'
        cmd_list = [
            'mkdir /var/www/https/',
            'chmod 777 /var/www/https/',
            '\cp -rf {}/* /var/www/https/'.format(HTTP_CONFS_PATH),
            'rm -f /etc/httpd/conf.d/ssl.conf',
            '\cp -fr {}/ssl.conf /etc/httpd/conf.d/'.format(configPath + "conf.d"),
            '\cp -fr {}/httpd.conf /etc/httpd/conf/'.format(configPath + "conf"),
            'grep /www/https /etc/httpd/conf.d/ssl.conf',
            'install {}/* /etc/pki/tls/certs/'.format(certPath),
            'install {}/* /etc/pki/tls/private/'.format(certPath),
            'systemctl start httpd',
            'systemctl status httpd'
        ]
        res = static_client.send_commands(cmd_list)
        flag = True if re.search(r'active \(running\)', res, re.S | re.I) else False
        Assertion.assert_equal(flag, True, "ERR: setup for lanpc failed")

    def test_02_Modify_X2_Zone_to_DMZ(self):
        logger.info("Set x2 zone to DMZ... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to DMZ failed")

    def test_03_Radius_user_settings(self):
        user_authen = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_04_edit_lan_dmz_access_rule(self):
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='DMZ')
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                acl_dict = copy.deepcopy(default_acl_dict)
                acl_dict.update({"users": {
                    "included": {"group": "Everyone"},
                    "excluded": {"none": True}
                }})
                res = accessrule_api.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                Assertion.assert_equal(res, True, "ERR: cannot added access rule")

    def test_05_edit_dmz_lan_access_rule(self):
        getres = accessrule_api.get_accessrule_via_zones(srczone='DMZ', dstzone='LAN')
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                acl_dict = copy.deepcopy(default_acl_dict)
                acl_dict.update({"users": {
                    "included": {"group": "Everyone"},
                    "excluded": {"none": True}
                }})
                res = accessrule_api.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                Assertion.assert_equal(res, True, "ERR: cannot added access rule")

    def test_06_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_07_enable_server_access(self):
        enable = {
            'DMZ_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'DMZ_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_08_login_via_ldap_user(self):
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url = "https://14.1.1.168:4433"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Multi_factor_auth_otp_mail/definition/ui_user.py ' + '-url ' + url + ' -user sslvpntest -pwd password'
        out = PC2_login.send_command(cmd)
        logger.info(f"login with user\n{out}")
        time.sleep(10)

        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")
    
    def test_09_Modify_X2_Zone_to_LAN(self):
        logger.info("Set x2 zone to LAN... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to LAN failed")

    def test_10_Delete_Access_Rule(self):
        res = accessrule_api.reset_accessrule_default_setting()
        Assertion.assert_equal(res, True, 'reset access rules failed')

class MFA_OTP_MAIL_22(Test):
    uuid = "SOSAIOT-TC-77284"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514464')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_X2_Zone_to_DMZ(self):
        logger.info("Set x2 zone to DMZ... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to DMZ failed")

    def test_02_Radius_user_settings(self):
        user_authen = {
            "auth_method": "Radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_03_edit_lan_dmz_access_rule(self):
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='DMZ')
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                acl_dict = copy.deepcopy(default_acl_dict)
                acl_dict.update({"users": {
                    "included": {"group": "Everyone"},
                    "excluded": {"none": True}
                }})
                res = accessrule_api.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                Assertion.assert_equal(res, True, "ERR: cannot added access rule")

    def test_04_edit_dmz_lan_access_rule(self):
        getres = accessrule_api.get_accessrule_via_zones(srczone='DMZ', dstzone='LAN')
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                acl_dict = copy.deepcopy(default_acl_dict)
                acl_dict.update({"users": {
                    "included": {"group": "Everyone"},
                    "excluded": {"none": True}
                }})
                res = accessrule_api.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                Assertion.assert_equal(res, True, "ERR: cannot added access rule")

    def test_05_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_06_enable_server_access(self):
        enable = {
            'DMZ_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'DMZ_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_07_login_via_radius_user(self):
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url = "https://14.1.1.168:4433"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Multi_factor_auth_otp_mail/definition/ui_user.py ' + '-url ' + url + ' -user sslvpntest -pwd password'
        out = PC2_login.send_command(cmd)
        logger.info(f"login with user\n{out}")
        time.sleep(10)

    def test_08_Modify_X2_Zone_to_LAN(self):
        logger.info("Set x2 zone to LAN... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to LAN failed")

    def test_09_Delete_Access_Rule(self):
        res = accessrule_api.reset_accessrule_default_setting()
        Assertion.assert_equal(res, True, 'reset access rules failed')

class MFA_OTP_MAIL_23(Test):
    uuid = "SOSAIOT-TC-89780"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514479')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_X2_Zone_to_DMZ(self):
        logger.info("Set x2 zone to DMZ... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to DMZ failed")

    def test_02_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        res = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:LOCALs method is not selected successfully")

    def test_03_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestlocal',
            'userpassword': 'password',
            'force_password_change': True,
            'email_address': 'test1@smtpstest.com',
            'one_time_password': 'otp',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = user_local.local_user(**user_json)
        resp1 = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: sslvpntestlocal not created')

    def test_04_edit_lan_dmz_access_rule(self):
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='DMZ')
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                acl_dict = copy.deepcopy(default_acl_dict)
                acl_dict.update({"users": {
                    "included": {"group": "Everyone"},
                    "excluded": {"none": True}
                }})
                res = accessrule_api.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                Assertion.assert_equal(res, True, "ERR: cannot added access rule")

    def test_05_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
            # ret = ret.decode() #converting byte to string
            # logger.info(ret)
            # Assertion.assert_equal('+OK' in ret, True, "ERR: clear test1 inbox failed")
            
        except Exception as err:
            logger.err(err)
            Assertion.assert_equal(False, True, "ERR: Exception occurred while clearing inbox")

        Assertion.assert_equal(True, True, "ERR: test1 inbox failed")

    def test_06_enable_server_access(self):
        enable = {
            'DMZ_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'DMZ_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_07_login_via_local_user(self):
        getres = accessrule_api.get_accessrule_via_zones(srczone='DMZ', dstzone='LAN')
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                acl_dict = copy.deepcopy(default_acl_dict)
                acl_dict.update({"users": {
                    "included": {"group": "Everyone"},
                    "excluded": {"none": True}
                }})
                res = accessrule_api.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                Assertion.assert_equal(res, True, "ERR: cannot added access rule")
    
    @repeat_method(5)
    def test_08_login_via_radius_user(self):   
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url = "https://14.1.1.168:4433"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Multi_factor_auth_otp_mail/definition/ui_user.py ' + '-url ' + url + ' -user sslvpntestlocal -pwd password -fpwd True'
        out = PC2_login.send_command(cmd)
        logger.info(f"login with user\n{out}")
        time.sleep(10)

    def test_09_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('sslvpntestlocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestlocal"', 'err: user not deleted')

    def test_10_Modify_X2_Zone_to_LAN(self):
        logger.info("Set x2 zone to LAN... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to LAN failed")

    def test_11_Delete_Access_Rule(self):
        res = accessrule_api.reset_accessrule_default_setting()
        Assertion.assert_equal(res, True, 'reset access rules failed')

class MFA_OTP_MAIL_24(Test):
    uuid = "SOSAIOT-TC-77298"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514480')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_X2_Zone_to_DMZ(self):
        logger.info("Set x2 zone to DMZ... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to DMZ failed")

    def test_02_Radius_user_settings(self):
        user_authen = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        logger.info("The Radius auth selected is  {}".format(Radius_auth))
        Assertion.assert_equal(Radius_auth, True, "ERR: Radius method is not selected successfully")

    def test_03_edit_lan_dmz_access_rule(self):
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='DMZ')
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                acl_dict = copy.deepcopy(default_acl_dict)
                acl_dict.update({"users": {
                    "included": {"group": "Everyone"},
                    "excluded": {"none": True}
                }})
                res = accessrule_api.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                Assertion.assert_equal(res, True, "ERR: cannot added access rule")

    def test_04_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_05_edit_user(self):
        edit_local_user_domain = {
                'action': 'edit',
                'oldusername': 'sslvpntest',
                'domain': 'os-autosnwl.com',
                'username': 'sslvpntest',
                'userpassword': 'password',
                'force_password_change': True,
                'one_time_password': 'otp',
                'email_address': 'test1@smtpstest.com',
                # 'vpn_client_access': ['LAN Subnets'],
                "member_of": ['SSLVPN Services']
        }

        rc = user_local.local_user(**edit_local_user_domain)
        get_resp = user_local.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': False
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    @repeat_method(5)
    def test_07_login_via_ldap_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        fw_ui = FWPage("https://192.168.168.168:4433", "sslvpntest", "password")
        out = fw_ui.login_ui()
        logger.info(f"login with user\n{out}")
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Testcase failed")

    def test_08_Modify_X2_Zone_to_LAN(self):
        logger.info("Set x2 zone to LAN... ")
        x2_if_change = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_if_change)
        Assertion.assert_equal(rc, True, "ERR: Set X2 zone to LAN failed")

    def test_09_Delete_Access_Rule(self):
        res = accessrule_api.reset_accessrule_default_setting()
        Assertion.assert_equal(res, True, 'reset access rules failed')

def connect_nxlinux_remote_with_otp_via_mail(user, pswd, netexurl, domain, openstack_PC):
    try:
        s = pxssh.pxssh()
        hostname = Params.testbed + openstack_PC
        logger.info(hostname)
        username = "root"
        password = "password"
        pc_login = s.login(hostname, username, password)
        print("Successfully login to:" + hostname)
        s.prompt()  # match the prompt
        logger.info(s.before)  # print everything before the prompt.
        s.sendline('killall netExtender')
        s.prompt()
        logger.info(s.before)
        s.sendline('netExtender')
        s.prompt()
        s.before
        print("SSLVPN SERVER:" + netexurl)
        s.sendline(netexurl)
        s.prompt()
        logger.info(s.before)
        logger.info("User Authentication")
        print("User:" + user)
        s.sendline(user)
        s.prompt()
        logger.info(s.before)
        logger.info("Password:")
        s.sendline(pswd)
        s.prompt()
        logger.info(s.before)
        print("Domain:" + domain)
        s.sendline("LocalDomain")
        s.sendline('Yes')
        s.prompt()
        logger.info(s.before)
        time.sleep(5)
        login_otp = retrieve_otp_from_mail()
        print("One Time Password", login_otp)
        s.sendline(login_otp)
        s.prompt()
        print(s.before)
        result = s.before
        print(result)
        save_path = '/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        f = open(file_path, "wb")
        m = f.write(result)
        f.close()


    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)


def connect_nxlinux_remote_with_otp_via_mail_forced_pwd(user, pswd, netexurl, domain, openstack_PC, fpwd=False):
    try:
        s = pxssh.pxssh()
        hostname = Params.testbed + openstack_PC
        logger.info(hostname)
        username = "root"
        password = "password"
        pc_login = s.login(hostname, username, password)
        print("Successfully login to:" + hostname)
        s.prompt()  # match the prompt
        logger.info(s.before)  # print everything before the prompt.
        s.sendline('killall netExtender')
        s.prompt()
        logger.info(s.before)
        s.sendline('netExtender')
        s.prompt()
        s.before
        print("SSLVPN SERVER:" + netexurl)
        s.sendline(netexurl)
        s.prompt()
        logger.info(s.before)
        logger.info("User Authentication")
        print("User:" + user)
        s.sendline(user)
        s.prompt()
        logger.info(s.before)
        logger.info("Password:")
        s.sendline(pswd)
        s.prompt()
        logger.info(s.before)
        print("Domain:" + domain)
        s.sendline("LocalDomain")
        s.sendline('Yes')
        s.prompt()
        logger.info(s.before)
        time.sleep(5)
        if fpwd:
            s.sendline('y')
            s.prompt()
            logger.info(s.before)
            print("Current password")
            s.sendline('password')
            s.prompt()
            logger.info(s.before)
            print("Enter new password")
            s.sendline('S0nic@uto')
            s.prompt()
            logger.info(s.before)
            print("Re-enter new password")
            s.sendline('S0nic@uto')
            s.prompt()
            logger.info(s.before)
        # login_otp = retrieve_otp_from_mail()
        # print("One Time Password",login_otp)
        # s.sendline(login_otp)
        # s.prompt()
        print(s.before)
        result = s.before
        print(result)
        save_path = '/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        f = open(file_path, "wb")
        m = f.write(result)
        f.close()


    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)
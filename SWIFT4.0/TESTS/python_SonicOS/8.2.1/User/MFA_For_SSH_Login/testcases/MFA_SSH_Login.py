import json
import time
import pexpect
import poplib
import argparse

from definition.settings import *

class sslvpn_config(Test):
    uuid = 'NonTC'

    def test_01_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()

        Assertion.assert_regular(
            json.dumps(resp),
            '"auth_method": "local"',
            "ERR: LOCAL method is not selected successfully"
        )

    def test_02_add_mail_server(self):
        mail_server_dict = {
            "mail_server": '172.17.1.5',
            "mail_from": 'test1@smtpstest.com',
        }
        log_auto_config = logautomationapi.cfg_mail_server(**mail_server_dict)
        logger.info(f'mail_server_config:{log_auto_config}')

        log_auto_test = logautomationapi.mail_server_test()
        logger.info(f'mail_server_test:{log_auto_test}')

class MFA_SSH_Login_1(Test):
    uuid = "SOSAIOT-TC-75557"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75557', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75557')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    @repeat_method(5)
    def test_03_clear_test1_inbox(self):
        try:
            pop3_client.delete_email('172.17.1.5', 'test1', 'password')
        except Exception as err:
            logger.error(str(err))

        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    @repeat_method(5)
    def test_04_login_via_local_user(self):
        output = enable_cli_login(
            X1_IP,
            'test1',
            'S0nic@uto'
        )
        Assertion.assert_regular(output, "test1@", "ERR: CLI login failed")

    def test_05_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_2(Test):
    uuid = "SOSAIOT-TC-75559"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75559', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75559')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'Limited Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    @repeat_method(5)
    def test_03_clear_test1_inbox(self):
        try:
            pop3_client.delete_email('172.17.1.5', 'test1', 'password')
        except Exception as err:
            logger.error(str(err))

        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    @repeat_method(5)
    def test_04_login_via_local_user(self):
        output = enable_cli_login(
            X1_IP,
            'test1',
            'S0nic@uto'
        )
        Assertion.assert_regular(output, "test1@", "ERR: CLI login failed")

    def test_05_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )


class MFA_SSH_Login_3(Test):
    uuid = "SOSAIOT-TC-75561"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75561', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75561')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'Guest Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    @repeat_method(5)
    def test_03_clear_test1_inbox(self):
        try:
            pop3_client.delete_email('172.17.1.5', 'test1', 'password')
        except Exception as err:
            logger.error(str(err))

        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    @repeat_method(5)
    def test_04_login_via_local_user(self):
        output = enable_cli_login(
            X1_IP,
            'test1',
            'S0nic@uto'
        )
        Assertion.assert_regular(output, "test1@", "ERR: CLI login failed")

    def test_05_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_4(Test):
    uuid = "SOSAIOT-TC-75563"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75563', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75563')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Read-Only Admins'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    @repeat_method(5)
    def test_03_clear_test1_inbox(self):
        try:
            pop3_client.delete_email('172.17.1.5', 'test1', 'password')
        except Exception as err:
            logger.error(str(err))

        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    @repeat_method(5)
    def test_04_login_via_local_user(self):
        output = enable_cli_login(
            X1_IP,
            'test1',
            'S0nic@uto'
        )
        Assertion.assert_regular(output, "test1@", "ERR: CLI login failed")

    def test_05_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_5(Test):
    uuid = "SOSAIOT-TC-75556"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75556', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75556')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'totp',
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    @repeat_method(5)
    def test_03_login_via_local_user(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )

        logger.info(f"actual output is: {output}")
        logger.info(f"expected output is: test1@")

        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "test1@", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_04_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_6(Test):
    uuid = "SOSAIOT-TC-75558"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75558', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75558')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'totp',
            'member_of': ['Trusted Users', 'Limited Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    # @repeat_method(5)
    def test_03_login_via_local_user(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )

        logger.info(f"actual output is: {output}")
        logger.info(f"expected output is: test1@")

        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "test1@", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_04_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_7(Test):
    uuid = "SOSAIOT-TC-75560"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75560', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75560')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'totp',
            'member_of': ['Trusted Users', 'Guest Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    # @repeat_method(5)
    def test_03_login_via_local_user(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )

        logger.info(f"actual output is: {output}")
        logger.info(f"expected output is: test1@")

        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "test1@", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_04_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_8(Test):
    uuid = "SOSAIOT-TC-75562"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75562', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75562')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'totp',
            'member_of': ['Trusted Users', 'SonicWALL Read-Only Admins'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    # @repeat_method(5)
    def test_03_login_via_local_user(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )

        logger.info(f"actual output is: {output}")
        logger.info(f"expected output is: test1@")

        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "test1@", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_04_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_9(Test):
    uuid = "SOSAIOT-TC-75565"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75565', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75565')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'totp',
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    # @repeat_method(5)
    def test_03_login_via_local_user(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )

        logger.info(f"actual output is: {output}")
        logger.info(f"expected output is: emergency scratch code")

        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "emergency scratch code", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_04_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_10(Test):
    uuid = "SOSAIOT-TC-75566"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75566', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75566')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': 'totp',
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )

    # @repeat_method(5)
    def test_03_login_via_local_user(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )
        local_user.unbind_totp_key_with_name(name="test1")
        logger.info("Unbinding done")
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )
        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "emergency scratch code", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_04_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_11(Test):
    uuid = "SOSAIOT-TC-75571"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75571', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75571')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': "totp",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )
    
    def test_03_edit_local_user(self):
        edit_localuser = {
            "action": "edit",
            "username": "test1",
            "userpassword": "S0nic@uto",
            "one_time_password": "",
            'member_of': ['Trusted Users', 'SonicWALL Administrators']
        }
        response = local_user.local_user(**edit_localuser)
        logger.info(response)
        resp = local_user.show_local_user_by_name("test1")
        Assertion.assert_regular(json.dumps(resp),'"name": "test1"','ERR: Failed to create a user')

    # @repeat_method(5)
    def test_04_login_via_local_user(self):
        success, output = ssh_login(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )
        if output is None:
            raise AssertionError("ERR: SSH login failed — output is None")
        
        Assertion.assert_regular(output, "test1@", "ERR: SSH login failed")
        logger.info("SSH login assertion passed successfully")

    def test_05_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_12(Test):
    uuid = "SOSAIOT-TC-75572"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75572', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75572')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': "totp",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )
    
    def test_03_edit_local_user(self):
        edit_localuser = {
            "action": "edit",
            "username": "test1",
            "userpassword": "S0nic@uto",
            "one_time_password": "otp",
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Administrators']
        }
        response = local_user.local_user(**edit_localuser)
        logger.info(response)
        resp = local_user.show_local_user_by_name("test1")
        Assertion.assert_regular(json.dumps(resp),'"name": "test1"','ERR: Failed to create a user')

    @repeat_method(5)
    def test_04_clear_test1_inbox(self):
        try:
            pop3_client.delete_email('172.17.1.5', 'test1', 'password')
        except Exception as err:
            logger.error(str(err))

        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    @repeat_method(5)
    def test_05_login_via_local_user(self):
        output = enable_cli_login(
            X1_IP,
            'test1',
            'S0nic@uto'
        )
        Assertion.assert_regular(output, "test1@", "ERR: CLI login failed")

    def test_06_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_13(Test):
    uuid = "SOSAIOT-TC-75570"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75570', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75570')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': "otp",
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )
    
    def test_03_edit_local_user(self):
        edit_localuser = {
            "action": "edit",
            "username": "test1",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            'member_of': ['Trusted Users', 'SonicWALL Administrators']
        }
        response = local_user.local_user(**edit_localuser)
        logger.info(response)
        resp = local_user.show_local_user_by_name("test1")
        Assertion.assert_regular(json.dumps(resp),'"name": "test1"','ERR: Failed to create a user')

    # @repeat_method(5)
    def test_04_login_via_local_user(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )
        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "emergency scratch code", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_05_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_14(Test):
    uuid = "SOSAIOT-TC-75569"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75569', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75569')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'one_time_password': "",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }

        local_user.local_user(**user_json)
        time.sleep(5)

        resp = local_user.show_local_users()
        Assertion.assert_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: Failed to create local user'
        )
    
    def test_03_edit_local_user(self):
        edit_localuser = {
            "action": "edit",
            "username": "test1",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            'member_of': ['Trusted Users', 'SonicWALL Administrators']
        }
        response = local_user.local_user(**edit_localuser)
        logger.info(response)
        resp = local_user.show_local_user_by_name("test1")
        Assertion.assert_regular(json.dumps(resp),'"name": "test1"','ERR: Failed to create a user')

    # @repeat_method(5)
    def test_04_login_via_local_user(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="test1",
            password_fw="S0nic@uto"
        )
        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "emergency scratch code", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_05_delete_local_user(self):
        logger.info('Delete the user')

        local_user.delete_local_user_no_domain('test1')
        time.sleep(5)

        resp = local_user.show_local_users()

        Assertion.assert_not_regular(
            json.dumps(resp),
            '"name": "test1"',
            'ERR: User not deleted'
        )

class MFA_SSH_Login_15(Test):
    uuid = "SOSAIOT-TC-75564"
    description= show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75564', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-75564')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_admin(self):
        edit_admin_user = {
            "administration":{
                "admin":{
                    "name": "admin",
                    "one_time_password":{
                       "totp":True 
                    }
                }
            }
        }
        response = admin_user.edit_admin(**edit_admin_user)
        logger.info(response)
        resp = admin_user.show_admin_setting()
        Assertion.assert_regular(json.dumps(resp),'"totp"','ERR: Failed to create a user')
    # @repeat_method(5)
    def test_03_login_via_admin(self):
        success, output = ssh_totp_first_time(
            ip="192.168.168.168",
            username_fw="admin",
            password_fw="S0nic@uto"
        )
        if output is None:
            raise AssertionError("ERR: SSH TOTP login failed — output is None")
        
        Assertion.assert_regular(output, "admin", "ERR: SSH TOTP login failed")
        logger.info("SSH TOTP login assertion passed successfully")

    def test_04_reset_admin(self):
        edit_admin_user = {
            "administration":{
                "admin":{
                    "name": "admin",
                    "one_time_password":{}
                }
            }
        }
        admin_user.unbind_totp_key()
        response = admin_user.edit_admin(**edit_admin_user)
        logger.info(response)
        resp = admin_user.show_admin_setting()
        Assertion.assert_equal(resp['administration']['admin']['one_time_password'],{},'ERR: Failed to create a user')


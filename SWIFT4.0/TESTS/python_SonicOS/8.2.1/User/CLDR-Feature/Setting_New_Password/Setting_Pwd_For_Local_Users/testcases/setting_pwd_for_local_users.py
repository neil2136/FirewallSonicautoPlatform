import sys
import os
import json
import re
import paramiko


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_Local_Users/')

from definition.settings import *
from definition.conf_fw import *

class config_ldap_NonTC(Test):
    uuid = 'NonTC'
    def test_01_Enable_Credential_Auditor(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"credential_auditor": {"enable": True,', "failed to enable toggle button")

    def test_02_disable_password_restrictions(self):
        obj_json = {
            "administration": {
                "password": {
                    "aging": {},
                    "last_changed": {},
                    "uniqueness": {},
                    "enforce_character_difference": False,
                    "minimum_length": 8,
                    "complexity": {},
                }
            }
        }
        response = admin_setting.conf_admin_update(**obj_json)
        Assertion.assert_equal(response, True, "ERR: edit user setting failed")
        resp = admin_setting.show_admin_setting()
        Assertion.assert_regular(json.dumps(resp), '"complexity": {},', "ERR: Failed to edit password constraints")

# FOR LDAP USER
class TC01_setting_pwd_for_local_users(Test):
    uuid = "SOSAIOT-TC-77743"
    description = show_testcase_info(Parameter.TESTPLAN, '4113382"', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113382"')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_local_user_update": True,
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_local_user_update": true,', "failed to enable toggle button")

    def test_02_add_localuser(self):
        time.sleep(60)
        add_localuser = {
            "action": "add",
            "username": "test124",
            "userpassword": "sonicwall",
            "member_of": ["Trusted Users", "SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
        }
        success, response = user.local_user(msg=True, **add_localuser)
        logger.info(response)
        error_msg = response["status"]["info"][0]["message"].lower()
        expected_part1 = "password is one that is known to have possibly"
        expected_part2 = "please choose another"
        flag = (success is False and expected_part1 in error_msg and expected_part2 in error_msg)
        Assertion.assert_equal(flag, True, f"ERR: Expected compromised password error not returned. Got: {error_msg}")

class TC02_setting_pwd_for_local_users(Test):
    uuid = "SOSAIOT-TC-77742"
    description = show_testcase_info(Parameter.TESTPLAN, '4113381', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113381')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_local_user_update": False,
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_local_user_update": false,', "failed to disable toggle button")

    def test_02_add_localuser(self):
        time.sleep(60)
        add_localuser = {
            "action": "add",
            "username": "test444",
            "userpassword": "sonicwall",
            "member_of": ["Trusted Users", "SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
        }
        resp = user.local_user(msg=True, **add_localuser)
        success = resp[1]['status']['success']
        message = resp[1]['status']['info'][0]['message']
        Assertion.assert_equal(message, "Success.", "ERR: Expected Output not displayed")

class TC03_setting_pwd_for_local_users(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77741"
    description = show_testcase_info(Parameter.TESTPLAN, '4113380', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113380')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','block-local-user-update','enable',
                        'commit', 'exit']
            rc = fw_cli.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: block-local-user-update toggle not enabled")

    def test_02_Updating_Pwd_CLI(self):
        time.sleep(60)
        username = "sum"
        commands = ['con', 'user local', f'user {username}', 'password sonicwall', 'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        # Normalize CLI output aggressively
        output = " ".join(rc[1].lower().split())
        logger.info(f"CLI OUTPUT: {output}")
        expected_phrases = [f"error: creating {username.lower()}", "password is one that is known to have possibly been compromised", "please choose another"]
        flag = all(phrase in output for phrase in expected_phrases)
        Assertion.assert_equal(flag, True, "ERR: Compromised password error message not displayed via CLI")

class TC04_setting_pwd_for_local_users(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77740"
    description = show_testcase_info(Parameter.TESTPLAN, '4113379', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113379')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','no block-local-user-update',
                        'commit', 'exit']
            rc = fw_cli.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: block-local-user-update toggle not enabled")

    def test_02_Updating_Pwd_CLI(self):
        time.sleep(60)
        username = "sum1"
        commands = ['con', 'user local', f'user {username}', 'password sonicwall', 'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        output = " ".join(rc[1].lower().split())
        logger.info(f"CLI OUTPUT: {output}")

        warning_msg = "password that has been set is one that is known to have possibly been compromised"
        success_msg = "changes made"
        error_msg = f"error: creating {username.lower()}"
        flag = (warning_msg in output and success_msg in output and error_msg not in output)
        Assertion.assert_equal(flag, True, "ERR: User creation with compromised password warning not displayed correctly")









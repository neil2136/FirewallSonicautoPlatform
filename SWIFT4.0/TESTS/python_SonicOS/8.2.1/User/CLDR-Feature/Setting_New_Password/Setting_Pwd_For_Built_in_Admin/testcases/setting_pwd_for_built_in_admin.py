import sys
import os
import json
import re
import paramiko
import time

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_Built_in_Admin/')

from definition.settings import *
from definition.conf_fw import *
from pexpect import pxssh

class NonTC_Revert_Old_Pwd(Test):
    def change_admin_password(old_pwd, new_pwd):
        try:
            hostname = static_pc
            username = "root"
            password = "password"
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, username=username, password=password)
            shell = client.invoke_shell()
            time.sleep(2)
            shell.recv(65535)
            # SSH into firewall
            shell.send("ssh admin@192.168.168.168\n")
            time.sleep(2)
            output = shell.recv(65535).decode("utf-8").lower()
            logger.info(output)
            if "are you sure you want to continue connecting" in output:
                shell.send("yes\n")
                time.sleep(2)
                shell.recv(65535)
            # Send password
            shell.send(old_pwd + "\n")
            time.sleep(2)
            # Enter config
            shell.send("configure\n")
            time.sleep(2)
            output = shell.recv(65535).decode("utf-8").lower()
            logger.info(output)
            # Handle preempt prompt
            if "do you wish to preempt" in output:
                shell.send("yes\n")
                time.sleep(2)
                shell.recv(65535)
            # Administration mode
            shell.send("administration\n")
            time.sleep(2)
            # Change password
            shell.send(
                f"admin password old-password {old_pwd} "
                f"new-password {new_pwd} confirm-password {new_pwd}\n")
            time.sleep(3)
            # Commit changes
            shell.send("commit\n")
            time.sleep(5)
            shell.send("exit\n")
            time.sleep(2)
            output = shell.recv(65535).decode("utf-8").lower()
            logger.info(output)
            client.close()
            # Validate success
            if "changes made" in output or "password" in output:
                return True
            return False
        except Exception as e:
            logger.error("Failed to change admin password")
            logger.error(str(e))
            return False

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
class TC01_setting_pwd_for_built_in_admin(Test):
    uuid = "SOSAIOT-TC-77761"
    description = show_testcase_info(Parameter.TESTPLAN, '4113633', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113633')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_admin_update": True,
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_admin_update": true,', "failed to enable toggle button")

    def test_02_compromised_pwd_check(self):
        time.sleep(30)
        json_obj = {
            "old_pwd": "S0nic@uto",
            "new_pwd": "sonicwall"
        }
        resp = admin_setting.change_password(msg = True, **json_obj)
        success = resp[1]['status']['success']
        message = resp[1]['status']['info'][0]['message']
        expected_msg = "The password is one that is known to have possibly been compromised, please choose another"
        Assertion.assert_equal(
            message,
            expected_msg,
            f"ERR: Expected compromised password message, got: {resp}"
        )

class TC02_setting_pwd_for_built_in_admin(Test):
    uuid = "SOSAIOT-TC-77760"
    description = show_testcase_info(Parameter.TESTPLAN, '4113632', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113632')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_admin_update": False,
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_admin_update": false,', "failed to disable toggle button")

    def test_02_compromised_pwd_check(self):
        time.sleep(30)
        json_obj = {
            "old_pwd": "S0nic@uto",
            "new_pwd": "sonicwall"
        }
        resp = admin_setting.change_password(msg=True, **json_obj)
        success = resp[1]['status']['success']
        message = resp[1]['status']['info'][0]['message']
        expected_msg = "The password that has been set is one that is known to have possibly been compromised"
        Assertion.assert_equal(
            message,
            expected_msg,
            f"ERR: Expected compromised password message not displayed, got: {resp}")

    def test_03_Revert_Pwd(self):
        result = NonTC_Revert_Old_Pwd.change_admin_password("sonicwall", G_PASSWORD_NEW)
        Assertion.assert_equal(result, True, "ERR: Failed to revert admin password via CLI")

class TC03_setting_pwd_for_built_in_admin(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77759"
    description = show_testcase_info(Parameter.TESTPLAN, '4113631', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113631')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','block-admin-update','enable',
                        'commit', 'exit']
            rc = fw_cli.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: block-admin-update toggle not enabled")

    def test_02_Updating_Pwd_CLI(self):
        time.sleep(30)
        flag = False
        logger.info('Enable user login with external auth toggle button')
        commands = ['con', 'administration', 'admin password old-password S0nic@uto new-password sonicwall confirm-password sonicwall',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        output = rc[1].lower()
        # Substrings to match
        msg1 = "password is one that is known to have possibly been compromised"
        msg2 = "please choose another"

        if msg1 in output and msg2 in output:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Expected Output not displayed")

class TC04_setting_pwd_for_built_in_admin(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77758"
    description = show_testcase_info(Parameter.TESTPLAN, '4113630', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113630')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        flag = False

        commands = ['con', 'user authentication', 'credential-auditor', 'enable', 'no block-admin-update',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: block-admin-update toggle not disabled")

    def test_02_Updating_Pwd_CLI(self):
        time.sleep(30)
        flag = False
        commands = [
            'con', 'administration',
            'admin password old-password S0nic@uto new-password sonicwall confirm-password sonicwall',
            'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        output = rc[1].lower()
        output = output.replace("\r", "").replace("\n", " ")
        warn_part1 = "password that has been set is one that is known to have possibly"
        warn_part2 = "been compromised"
        if warn_part1 in output and warn_part2 in output:
            flag = True
        Assertion.assert_equal(
            flag,
            True,
            "ERR: Expected compromised password warning not displayed")

    def test_03_Revert_Pwd(self):
        result = NonTC_Revert_Old_Pwd.change_admin_password("sonicwall", G_PASSWORD_NEW)
        Assertion.assert_equal(result, True, "ERR: Failed to revert admin password via CLI")


























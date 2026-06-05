import sys
import os
import json
import re
import paramiko


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_LDAP_Bind/')

from definition.settings import *
from definition.conf_fw import *

class config_ldap_NonTC(Test):
    uuid = 'NonTC'

    def test_01_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'test',
                'bind_password': 'password',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }
            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

    def test_02_Enable_Credential_Auditor(self):
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

    def test_03_disable_password_restrictions(self):
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
class TC01_setting_pwd_for_ldap_bind(Test):
    uuid = "SOSAIOT-TC-77769"
    description = show_testcase_info(Parameter.TESTPLAN, '4113553', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113553')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_ldap_bind_update": True,
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_ldap_bind_update": true,', "failed to enable toggle button")

    def test_02_config_ldapuser(self):
        time.sleep(30)
        json_obj = {
            'role': 'primary',
            'host': '192.168.168.85',
            'bind': 'distinguished_name',
            'distinguished_name': 'test',
            'bind_password': 'password',
            'referred_bind_with_account': 'other-servers'}
        resp = ldap.edit_ldap_server(msg=True,**json_obj)
        message = resp[1]['status']['info'][0]['message']
        expected_msg = "LDAP server bind  password: The password is one that is known to have possibly been compromised, please choose another"
        Assertion.assert_equal(
            message,
            expected_msg,
            f"ERR: Expected compromised password message not displayed, got: {resp}")


class TC02_setting_pwd_for_ldap_bind(Test):
    uuid = "SOSAIOT-TC-77768"
    description = show_testcase_info(Parameter.TESTPLAN, '4113552', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113552')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_ldap_bind_update": False,
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_ldap_bind_update": false,', "failed to disable toggle button")

    def test_02_config_ldapuser(self):
        time.sleep(30)
        json_obj = {
            'role': 'primary',
            'host': '192.168.168.85',
            'bind': 'distinguished_name',
            'distinguished_name': 'test',
            'bind_password': 'password',
            'referred_bind_with_account': 'other-servers'
        }
        res= ldap.edit_ldap_server(msg=True, **json_obj)
        message = res[1]['status']['info'][0]['message']
        Assertion.assert_equal(message, "Success.", "ERR: Expected Output not displayed")
        print(message)

class TC03_setting_pwd_for_ldap_bind(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77767"
    description = show_testcase_info(Parameter.TESTPLAN, '4113551', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14113551')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','block-ldap-bind-update','enable',
                        'commit', 'exit']
            rc = fw_cli.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: block-ldap-bind-update toggle not enabled")

    def test_02_Updating_Pwd_CLI(self):
        time.sleep(30)
        flag = False

        commands = ['con', 'user ldap', 'server 192.168.168.85', 'bind-password password', 'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        output = rc[1].lower()
        # Substrings to match (MUST be lowercase)
        msg1 = "ldap server bind password: the password is one that is known to have"
        msg2 = "possibly been compromised, please choose another"
        if msg1 in output and msg2 in output:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Expected Output not displayed")

class TC04_setting_pwd_for_ldap_bind(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77766"
    description = show_testcase_info(Parameter.TESTPLAN, '4113550', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113550')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        flag = False

        commands = ['con', 'user authentication', 'credential-auditor', 'enable', 'no block-ldap-bind-update',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: block_ldap_bind_update toggle not disabled")

    def test_02_Updating_Pwd_CLI(self):
        time.sleep(30)
        flag = False
        commands = ['con', 'user ldap', 'server 192.168.168.85',
                    'bind-password password', 'commit', 'exit']

        rc = fw_cli.do_cli_commands(commands, tag=1)
        output = rc[1].lower()

        msg1 = "warning: the password that has been set is one that is known to have"
        msg2 = "been compromised"

        if msg1 in output and msg2 in output:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Expected warning output not displayed")









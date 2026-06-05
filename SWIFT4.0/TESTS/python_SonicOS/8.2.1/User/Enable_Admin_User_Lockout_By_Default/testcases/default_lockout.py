from definition.settings import *

def ssh_connection_fw(falilure=False):
    
    cmd = f"ssh admin@{Parameter.FIREWALL}"
    
    if falilure:
        ssh = pexpect.spawn(cmd)
        # Respond to prompts
        for i in range(3):
            idx = ssh.expect([r"Password:\s?$", pexpect.TIMEOUT])
            if idx == 0:
                ssh.sendline("Wrongpassword")
                logger.info("Entered Wrong Password")
            else:
                logger.info("Unexpected output from cli.")
                ssh.close()
                return False
        
        ssh.close()  
        return True
    else:
        ssh = pexpect.spawn(cmd)
        # with correct password
        idx = ssh.expect([r"Password:\s?$", pexpect.TIMEOUT])
        if idx == 0:
            logger.info(Params.G_NEW_PASSWORD)
            ssh.sendline(Params.G_NEW_PASSWORD)
            logger.info("Entered Correct Password")
        else:
            logger.info("Unexpected output from cli.")
            ssh.close()
            return False
        
        result = ssh.expect([r"Password:\s?$", r"admin@\w+", pexpect.TIMEOUT])
        if result == 0:
            logger.info("Access denied")
            return False
        elif result == 1:
            logger.info("Logged In.")
            ssh.close()
            return True
        else:
            logger.info("Unexpected output from cli.")
            return False

    
class TC01_Lockout_Enabled_By_Default(Test):
    uuid = "SOSAIOT-TC-77559"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928628')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_lockout_settings(self):
        res  = admin_api.show_admin_setting()
        actual_json = res["administration"]["user_lockout"]
        logger.info(f"Lockout settings:\n{actual_json}")
        expected_json = {'enable': True, 'failures_rate': 3, 'failures_duration': 1, 'lockout_duration': 5}
        Assertion.assert_equal(actual_json, expected_json, "ERR: Lockout settings are different after restore default boot.")


class TC02_Disable_Lockout_Warning(Test):
    uuid = "SOSAIOT-TC-77560"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928629')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_warning(self):
        res = ui_login.disable_lockout_warning()
        Assertion.assert_equal(res, True, "ERR: Warning not displayed.")


class TC03_Warning_When_Lockout_disabled(Test):
    uuid = "SOSAIOT-TC-77562"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928631')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_disable_admin_lockout(self):
        admin_json["administration"]["user_lockout"]["enable"] = False
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Disable admin/user lockout failed.")
    
    def test_02_verify_warning(self):
        res = ui_login.lockout_warning_when_login()
        Assertion.assert_equal(res, True, "ERR: Warning not displayed.")
    
    def test_03_enable_lockout(self):
        admin_json["administration"]["user_lockout"]["enable"] = True
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable admin/user lockout failed.")


class TC04_User_lockout_funtionality(Test):
    uuid = "SOSAIOT-TC-77563"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928632')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_user_lockout_when_enabled(self):
        res = ui_login.multiple_attempts_with_wrong_password(timeout=350)
        Assertion.assert_equal(res, True, f"ERR: Failed to make user locked out.")

    def test_02_disable_admin_lockout(self):
        admin_json["administration"]["user_lockout"]["enable"] = False
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Disable admin/user lockout failed.")
    
    def test_03_user_lockout_when_disabled(self):
        res = ui_login.multiple_attempts_with_wrong_password(timeout=0)
        Assertion.assert_equal(res, True, f"ERR: Failed to check user locked out when lockout is disabled.")
    
    def test_04_enable_lockout(self):
        admin_json["administration"]["user_lockout"]["enable"] = True
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable admin/user lockout failed.")


class TC05_Max_Login_Attempts_Using_CLI(Test):
    uuid = "SOSAIOT-TC-77566"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928635')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_max_attempts(self):
        result = ssh_connection_fw(falilure=True)
        Assertion.assert_equal(result, True, "ERR: Failed to lockout admin using CLI.")
        logger.info("Waiting till Lockout period expires!")
        time.sleep(300)
    
    @repeat_method(3)
    def test_02_login_using_cli(self):
        result = ssh_connection_fw()
        Assertion.assert_equal(result, True, "ERR: Failed to login after lockout period expired.")


class TC06_other_Admin_Users_Lockout(Test):
    uuid = "SOSAIOT-TC-77564"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928633')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_credential_auditor_disable_api(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": False,  
                        "block_user_login_with_external_auth": False
                    }
                }
            }
        }
        resp = user_setting.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": false,', "failed to disable toggle button")

    def test_02_enable_multiple_admin(self):
        admin_json = {
            "administration": {
              "multiple_admin": True
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable Multiple Admin failed.")
    
    @parameterized.expand([
        ("Admin1", "Password@1", "Guest Administrators"),
        ("Admin2", "Password@2", "Audit Administrators"),
        ("Admin3", "Password@3", "System Administrators"),
        ("Admin4", "Password@4", "Limited Administrators"),
        ("Admin5", "Password@5", "SonicWALL Administrators"),
        ("Admin6", "Password@6", "SonicWALL Read-Only Admins"),
        ("Admin7", "Password@7", "Cryptographic Administrators")
    ])
    def test_03_local_user(self, usr, psw, member):
        user_json = {
            'action': 'add',
            'username': usr,
            'userpassword': psw,
            'member_of': [member],
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), f'"name": "{usr}"', f"ERR: failed to add {member} user.")
    
    @parameterized.expand([
        ("Admin1", "Password@1", "Guest Administrators"),
        ("Admin2", "Password@2", "Audit Administrators"),
        ("Admin3", "Password@3", "System Administrators"),
        ("Admin4", "Password@4", "Limited Administrators"),
        ("Admin5", "Password@5", "SonicWALL Administrators"),
        ("Admin6", "Password@6", "SonicWALL Read-Only Admins"),
        ("Admin7", "Password@7", "Cryptographic Administrators")
    ])
    def test_04_admin_user_lockout(self, usr, psw, member):
        logger.info(f"\n------- {member} admin Lockout -------")
        res = ui_login.multiple_attempts_with_wrong_password(user=usr, password=psw, timeout=350)
        Assertion.assert_equal(res, True, f"ERR: Failed to make user locked out.")
        
        # disable lockout
        admin_json["administration"]["user_lockout"]["enable"] = False
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Disable admin/user lockout failed.")
       
        res2 = ui_login.multiple_attempts_with_wrong_password(user=usr, password=psw, timeout=0)
        Assertion.assert_equal(res2, True, f"ERR: Failed to check user locked out when lockout disabled.")
        
        # enable lockout
        admin_json["administration"]["user_lockout"]["enable"] = True
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable admin/user lockout failed.")


class TC07_Import_Configuration_File(Test):
    uuid = "SOSAIOT-TC-77561"
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928630')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_admin_lockout(self):
        json_input = copy.deepcopy(admin_json)
        json_input["administration"]["user_lockout"]["enable"] = True
        json_input["administration"]["user_lockout"]["failures_rate"] = 2
        json_input["administration"]["user_lockout"]["failures_duration"] = 2
        resp = admin_api.edit_admin(**json_input)
        Assertion.assert_equal(resp, True, "ERR: Edit lockout settings failed.")

    def test_02_export_config_file(self):
        resp = settings_obj.export_setting_exp()
        Assertion.assert_equal(resp, True, "ERR: Failed to export config file")
    
    def test_03_edit_lockout_settings(self):
        admin_json["administration"]["user_lockout"]["enable"] = True
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Edit lockout settings failed.")

    def test_04_import_config_file(self):
        resp = settings_obj.import_setting_exp('/tmp/test.exp')
        logger.info(f"**** \n{resp}")
        Assertion.assert_equal(resp, True, "ERR: Failed to import config file")
    
    def test_05_verify_lockout_settings(self):
        res  = admin_api.show_admin_setting()
        actual_json = res["administration"]["user_lockout"]
        logger.info(f"Lockout settings:\n{actual_json}")
        expected_json = {'enable': True, 'failures_rate': 2, 'failures_duration': 2, 'lockout_duration': 5}
        Assertion.assert_equal(actual_json, expected_json, "ERR: Lockout settings are different after import config file.")

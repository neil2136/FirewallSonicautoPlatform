from definition.settings import *

    
class TC_01_Enforce_Psw_Complexity_By_Default(Test):
    uuid = "SOSAIOT-TC-77572"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928645')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_password_settings(self):
        res  = admin_api.show_admin_setting()
        actual_json = res["administration"]["password"]["complexity"]
        logger.info(f"Lockout settings:\n{actual_json}")
        expected_json = {'type': 'alpha-and-numeric-and-symbols', 'upper_case': 1, 'lower_case': 1, 'digital': 1, 'symbolic': 1}
        Assertion.assert_equal(actual_json, expected_json, "ERR: Lockout settings are different after restore default boot.")


class TC_02_Import_Configuration_File(Test):
    uuid = "SOSAIOT-TC-77573"
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928646')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_config_file(self):
        resp = settings_obj.export_setting_exp()
        Assertion.assert_equal(resp, True, "ERR: Failed to export config file")
    
    def test_02_edit_password_settings(self):
        res  = admin_api.show_admin_setting()
        res["administration"]["password"]["complexity"]={}
        resp = fw_api.api_put("api/sonicos/administration/global",False, data=res)
        Assertion.assert_equal(resp, True, "ERR: Edit password settings failed.")

    def test_03_import_config_file(self):
        resp = settings_obj.import_setting_exp('/tmp/test.exp')
        logger.info(f"**** \n{resp}")
        Assertion.assert_equal(resp, True, "ERR: Failed to import config file")
    
    def test_04_verify_password_settings(self):
        res  = admin_api.show_admin_setting()
        actual_json = res["administration"]["password"]["complexity"]
        logger.info(f"Lockout settings:\n{actual_json}")
        expected_json = {'type': 'alpha-and-numeric-and-symbols', 'upper_case': 1, 'lower_case': 1, 'digital': 1, 'symbolic': 1}
        Assertion.assert_equal(actual_json, expected_json, "ERR: password settings are different after import config file.")


class TC_03_All_Admin_Users_Creation(Test):
    uuid = "SOSAIOT-TC-77577"
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928650')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_enable_multiple_admin(self):
        admin_json = {
            "administration": {
              "multiple_admin": True
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable Multiple Admin failed.")

    @parameterized.expand([
        ("local", "S0nic@uto@1", "Everyone"),
        ("Admin1", "S0nic@uto@2", "Guest Administrators"),
        ("Admin2", "S0nic@uto@3", "Audit Administrators"),
        ("Admin3", "S0nic@uto@4", "System Administrators"),
        ("Admin4", "S0nic@uto@5", "Limited Administrators"),
        ("Admin5", "S0nic@uto@6", "SonicWALL Administrators"),
        ("Admin6", "S0nic@uto@7", "SonicWALL Read-Only Admins"),
        ("Admin7", "S0nic@uto@8", "Cryptographic Administrators")
    ])
    def test_02_create_user(self, usr, psw, member):
        user_json = {
            'action': 'add',
            'username': usr,
            'userpassword': psw,
            'member_of': [member],
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), f'"name": "{usr}"', f"ERR: failed to add {usr} user.")


class TC_04_All_Users_login(Test):
    uuid = "SOSAIOT-TC-77578"
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3928651')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_edit_lan_wan_ipv4_rule(self):
        rule = access_rules_ipv4.get_ipv4_access_rule_given_from_to(srczone='LAN', destzone='WAN')
        del rule['access_rules'][0]['ipv4']['users']['included']
        rule['access_rules'][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        res = fw_api.api_put(f'api/sonicos/access-rules/ipv4/uuid/{uuid}', data=rule)
        Assertion.assert_equal(res, True, "ERR: edit access rule failed.")
    
    @parameterized.expand([
        ("local", "S0nic@uto@1", "Everyone"),
        ("Admin1", "S0nic@uto@2", "Guest Administrators"),
        ("Admin2", "S0nic@uto@3", "Audit Administrators"),
        ("Admin3", "S0nic@uto@4", "System Administrators"),
        ("Admin4", "S0nic@uto@5", "Limited Administrators"),
        ("Admin5", "S0nic@uto@6", "SonicWALL Administrators"),
        ("Admin6", "S0nic@uto@7", "SonicWALL Read-Only Admins"),
        ("Admin7", "S0nic@uto@8", "Cryptographic Administrators")
    ])
    def test_02_all_users_login(self, usr, psw, member):
        res = ui_login.login(usr, psw, member)
        Assertion.assert_equal(res, True, f"ERR: Failed to login using {member} user")
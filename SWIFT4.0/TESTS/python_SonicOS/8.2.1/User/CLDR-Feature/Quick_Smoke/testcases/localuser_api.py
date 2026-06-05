import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Quick_Smoke')

from definition.settings import *



class TC01_disable_CLDR(Test):
    uuid = 'SOSAIOT-TC-77930'

    def test_Enable_Credential_Auditor(self):

        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": False,
                    }}
        }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        print(res)
        Assertion.assert_not_regular(json.dumps(res), '{"period": 30, "unit": "days"}',
                                 "failed to enable toggle button")
        logger.info(" disabling the option “Enable Credential Auditor”")

    def test_Users_AdminPrivelage(self):
        add_localuser = {
            "action": "add",
            "username": "testlocal_admin",
            "userpassword": "Password",
            "member_of": ["SonicWALL Administrators"],
        }

        response = local_user.local_user(**add_localuser)
        response_get = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testlocal_admin"',
                                 'err: Failed to create adminuser')


class TC02_enable_CLDR(Test):
    uuid = 'SOSAIOT-TC-77932'

    def test_Enable_Credential_Auditor(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
    "enable": True,
    "check_period": {
      "period": 30,
      "unit": "days"
    },
    "block_local_user_update": True,
    "block_admin_update": True,
    "block_ldap_bind_update": True,
    "block_user_login_with_external_auth": True,
    "periodic_detect_local_user_restriction": {},
    "periodic_detect_admin_restriction": {},
    "periodic_detect_ldap_bind": {
      "warn_only": True
    }
  }
            }
        }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
    def test_Users_AdminPrivelage(self):
        add_localuser = {
            "action": "add",
            "username": "testlocal_admin_enabled",
            "userpassword": "Password",
            "member_of": ["SonicWALL Administrators"],
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_regular(json.dumps(response), "false",  'err: Credential Error didnt raise')



import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/CLDR_Local_User_Password')

from definition.settings import *


# No restriction cases
class NonTC_1(Test):
    uuid = 'NonTC'

    def test_Enable_Credential_Auditor(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": False,
                    },
                    "block_local_user_update": False,
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"credential_auditor": {"enable": False,',
                                 "failed to enable toggle button")

class TC001_LocalUsers_Admin(Test):

    uuid ="SOSAIOT-TC-77742"

    def test_Users_AdminPrivelage(self):
        add_localuser = {
            "action": "add",
            "username": "testlocal_admin",
            "userpassword": "test@Passw0rd",
            "member_of": ["SonicWALL Administrators"],
        }

        response = local_user.local_user(**add_localuser)
        response_get = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testlocal_admin"', 'err: Failed to create adminuser')
        logger.info("When CLDR disabled Local user as Admin added")


class TC002_LocalUsers_SSLVPN(Test):
    uuid = "SOSAIOT-TC-77748"

    def test_03_add_user_sslvpn_portal(self):
        add_localuser = {
            'action': 'add',
            'username': 'testlocal_portal',
            'userpassword': 'test@Passw0rd',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services']
        }
        resp = local_user.local_user(**add_localuser)
        resp1 = local_user.show_local_user_by_name('testlocal_portal')
        Assertion.assert_regular(json.dumps(resp1), '"name": "testlocal_portal"',
                                 'err: sslvpntest not added to SSLVPN Services')
        logger.info("When CLDR disabled Local user for sslvpn portal")



class TC003_LocalUsers_NX(Test):
    uuid = "SOSAIOT-TC-77750"

    def test_03_add_user_sslvpn_NX(self):
        add_localuser = {
            'action': 'add',
            'username': 'testlocal_NX',
            'userpassword': 'test@Passw0rd',
            'member_of': ['Trusted Users',  'SSLVPN Services']
        }
        resp = local_user.local_user(**add_localuser)
        resp1 = local_user.show_local_user_by_name('testlocal_NX')
        Assertion.assert_regular(json.dumps(resp1), '"name": "testlocal_NX"',
                                 'err: sslvpntest not added to SSLVPN Services')
        logger.info("When CLDR disabled Local user for NX")


# With restriction cases
class NonTC_2(Test):
    uuid = 'NonTC'

    def test_Enable_Credential_Auditor(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
    "enable": True,
    "check_period": {
      "period": 1,
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
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"credential_auditor": {"enable": True,',
                                 "failed to enable toggle button")

class TC004_LocalUsers_Admin_enabled(Test):

    uuid ="SOSAIOT-TC-77743"

    def test_Users_AdminPrivelage(self):
        add_localuser = {
            "action": "add",
            "username": "testlocal_admin_enabled",
            "userpassword": "Password",
            "member_of": ["SonicWALL Administrators"],
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_regular(json.dumps(response), "false",  'err: Credential Error didnt raise')
class TC005_LocalUsers_SSLVPN_enabled(Test):
    uuid = "SOSAIOT-TC-77749"

    def test_03_add_user_sslvpn_portal(self):
        add_localuser = {
            'action': 'add',
            'username': 'testlocal_portal_enabled',
            'userpassword': 'Password',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services']
        }
        resp = local_user.local_user(**add_localuser)
        Assertion.assert_regular(json.dumps(resp),"false",  'err: Credential Error didnt raise')
        logger.info("Compromised password didnt accept.")


class TC006_LocalUsers_NX_enabled(Test):
    uuid = "SOSAIOT-TC-77751"

    def test_03_add_user_sslvpn_NX(self):
        add_localuser = {
            'action': 'add',
            'username': 'testlocal_NX_enabled',
            'userpassword': 'Password',
            'member_of': ['Trusted Users',  'SSLVPN Services']
        }
        resp = local_user.local_user(**add_localuser)
        Assertion.assert_regular(json.dumps(resp), "false",  'err: Credential Error didnt raise')
        logger.info("Compromised password didnt accept.")


class TC007_LocalUser_Admin_CL(Test):
    uuid = "SOSAIOT-TC-77741"

    def test_01_check_local_users_groups(self):
        add_user1_dict = {'user': 'user1', 'password': 'user@Passw0rd'}
        rc1 = userlocalcli.add_local_user(**add_user1_dict)

        resp1 = local_user.show_local_user_by_name('user1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "user1"','err: Credential Error didnt raise')
        logger.info("Compromised password didnt accept.")


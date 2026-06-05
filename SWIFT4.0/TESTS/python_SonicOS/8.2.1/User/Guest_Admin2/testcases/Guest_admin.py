import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin2')
from definition.settings import *
from lib.ui_group import *



#TC01 Test "Apply  password constraints  for all local users" on guest admin
class Guest_admin_001(Test):
    uuid = "SOSAIOT-TC-76113"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test_user1',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'Everyone', 'Guest Administrators']
        }
        post_resp = guest_admin.local_user(**user_json)
        get_resp = guest_admin.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user1"', 'err: user_test1 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: user_test1 not created')

    def test_02_add_password_constraints(self):
        password_constraints = {
            "administration": {
            "password": {
                "minimum_length": 5,
                "complexity": {
                    "type": "alpha-and-numeric",
                    "upper_case": 0,
                    "lower_case": 1,
                    "digital": 1
                },
                "constraints_apply_to": {
                    "builtin_admin": False,
                    "full_admins": False,
                    "limited_admins": False,
                    "guest_admins": True
                }
            }
            }
        }

        put_resp = user_settings.edit_admin(**password_constraints)
        Assertion.assert_equal(put_resp, True, "ERR: Failed to update password constraints")



    def test_03_verify_password_constraints(self):
        ui_resp = ui_obj.verify_password_constraints("test_user1", "password")
        Assertion.assert_equal(ui_resp, True, "ERR: Failed to verify password constraints")

    def test_04_delete_local_user(self):
        rc1 = guest_admin.delete_local_user_no_domain('test_user1')
        Assertion.assert_equal(rc1, True, "ERR: deleting user failed")

    def test_05_update_default_settings(self):
        password_constraints = {
                    "administration": {
                    "password": {
                        "minimum_length": 8,
                        "constraints_apply_to": {
                            "builtin_admin": True,
                            "full_admins": True,
                            "limited_admins": True,
                            "guest_admins": True
                        }
                    }
                    }
                }


        resp = ui_obj.change_password_constraints_to_default()
        Assertion.assert_equal(resp, True, "ERR: Failed to update password constraints to None")
        put_resp = user_settings.edit_admin(**password_constraints)
        Assertion.assert_equal(put_resp, True, "ERR: Failed to update password constraints")


#TC02 Update password in the login popup window after login as a guest admin
class Guest_admin_002(Test):
    uuid = "SOSAIOT-TC-76114"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test_user1',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'Everyone', 'Guest Administrators']
        }
        post_resp = guest_admin.local_user(**user_json)
        get_resp = guest_admin.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user1"', 'err: user_test1 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: user_test1 not created')

    def test_02_add_password_constraints(self):
        password_constraints = {
            "administration": {
            "password": {
                "minimum_length": 5,
                "complexity": {
                    "type": "alpha-and-numeric",
                    "upper_case": 0,
                    "lower_case": 1,
                    "digital": 1
                },
                "constraints_apply_to": {
                    "builtin_admin": False,
                    "full_admins": False,
                    "limited_admins": False,
                    "guest_admins": True
                }
            }
            }
        }

        put_resp = user_settings.edit_admin(**password_constraints)
        Assertion.assert_equal(put_resp, True, "ERR: Failed to update password constraints")

    def test_03_verify_password_change(self):
        ui_resp = ui_obj.verify_password_change("test_user1", "password", "s0nicauto")
        Assertion.assert_equal(ui_resp, True, "ERR: Failed to change password")

    def test_04_delete_local_user(self):
        rc1 = guest_admin.delete_local_user_no_domain('test_user1')
        Assertion.assert_equal(rc1, True, "ERR: deleting user failed")

    def test_05_update_default_settings(self):
        password_constraints = {
            "administration": {
                "password": {
                    "minimum_length": 8,
                    "constraints_apply_to": {
                        "builtin_admin": True,
                        "full_admins": True,
                        "limited_admins": True,
                        "guest_admins": True
                    }
                }
            }
        }

        resp = ui_obj.change_password_constraints_to_default()
        Assertion.assert_equal(resp, True, "ERR: Failed to update password constraints to None")
        put_resp = user_settings.edit_admin(**password_constraints)
        Assertion.assert_equal(put_resp, True, "ERR: Failed to update password constraints")

#TC03 Preempt:verify that guest admin is unable to preempt Full Admin
class Guest_admin_003(Test):
    uuid = "SOSAIOT-TC-76115"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test_user1',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'Everyone', 'Guest Administrators']
        }
        post_resp = guest_admin.local_user(**user_json)
        get_resp = guest_admin.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user1"', 'err: user_test1 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: user_test1 not created')

    def test_02_admin_login(self):
        ui_resp = ui_obj.login_ui("https://192.168.168.168", "admin", "sonicauto")
        Assertion.assert_equal(ui_resp, True, "ERR: Failed to login admin")

    def test_03_guest_admin_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(30)
        url = "https://13.0.0.10"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin2/lib/ui_guest_login.py ' + \
              '-url ' + url + ' -user test_user1 -pwd password -method login_guest_admin_non_config'
        out = static_client.send_command(cmd)
        time.sleep(30)
        logger.info(out)
        Assertion.assert_regular(out, 'True', "ERR: Guest admin login failed")

    def test_04_delete_guest_admin(self):
        time.sleep(10)
        rc1 = guest_admin.delete_local_user_no_domain('test_user1')
        Assertion.assert_equal(rc1, True, "ERR: deleting user failed")


#TC04 Preempt:try to preempt between two guest admin users
class Guest_admin_004(Test):
    uuid = "SOSAIOT-TC-76116"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_guest_admin1(self):
        user_json = {
            'action': 'add',
            'username': 'test_user1',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'Everyone', 'Guest Administrators']
        }
        post_resp = guest_admin.local_user(**user_json)
        # get_resp = guest_admin.show_local_users()



        user_json1 = {
            'action': 'add',
            'username': 'test_user2',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'Everyone', 'Guest Administrators']
        }
        post_resp = guest_admin.local_user(**user_json1)
        time.sleep(15)
        get_resp = guest_admin.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user1"', 'err: user_test1 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: user_test1 not created')

        Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user2"', 'err: user_test2 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: user_test1 not created')


    def test_02_guest_admin1_login(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, "192.168.168.168", 'test_user1', 'password')
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")

    def test_03_guest_admin2_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(30)
        url = "https://13.0.0.10"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin2/lib/ui_guest_login.py ' + \
              '-url ' + url + ' -user test_user2 -pwd password -method login_admin_config'
        out = static_client.send_command(cmd)
        time.sleep(30)
        logger.info("login with user\n" + out)
        Assertion.assert_regular(out, 'True', "ERR: Guest admin login failed")

    def test_04_delete_guest_admin(self):
        time.sleep(10)
        rc1 = guest_admin.delete_local_user_no_domain('test_user1')
        Assertion.assert_equal(rc1, True, "ERR: deleting user failed")

        rc2 = guest_admin.delete_local_user_no_domain('test_user2')
        Assertion.assert_equal(rc2, True, "ERR: deleting user failed")


#TC05 Preempt:try to preempt between guest admin user and limitted admin user
class Guest_admin_005(Test):
    uuid = "SOSAIOT-TC-76117"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_guest_admin(self):
        user_json = {
            'action': 'add',
            'username': 'test_user1',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'Everyone', 'Guest Administrators']
        }
        post_resp = guest_admin.local_user(**user_json)
        get_resp = guest_admin.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user1"', 'err: user_test1 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: user_test1 not created')

    def test_02_create_limited_admin(self):
        user_json = {
            'action': 'add',
            'username': 'test_user2',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'Everyone', 'Limited Administrators']
        }
        post_resp = guest_admin.local_user(**user_json)
        get_resp = guest_admin.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user2"', 'err: user_test1 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Limited Administrators"', 'err: user_test1 not created')

    def test_03_guest_admin_login(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, "192.168.168.168", 'test_user1', 'password')
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")

    def test_04_limited_admin_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(30)
        url = "https://13.0.0.10"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin2/lib/ui_guest_login.py ' + \
              '-url ' + url + ' -user test_user1 -pwd password -method login_admin_config'
        out = static_client.send_command(cmd)
        time.sleep(30)
        logger.info("login with user\n" + out)
        Assertion.assert_regular(out, 'True', "ERR: Guest admin login failed")

    def test_05_delete_users(self):
        time.sleep(10)
        rc1 = guest_admin.delete_local_user_no_domain('test_user1')
        Assertion.assert_equal(rc1, True, "ERR: deleting user failed")

        rc2 = guest_admin.delete_local_user_no_domain('test_user2')
        Assertion.assert_equal(rc2, True, "ERR: deleting user failed")

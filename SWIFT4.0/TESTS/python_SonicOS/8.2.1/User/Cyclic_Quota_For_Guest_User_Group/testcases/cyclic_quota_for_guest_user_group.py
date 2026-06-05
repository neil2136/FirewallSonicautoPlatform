import sys
import os
import json
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Cyclic_Quota_For_Guest_User_Group')
from definition.settings import *

class NonTC_GuestUsers(Test):
    uuid = "NonTC"

    def test_enable_guest_user(self):
        commands = ["configure", "zone LAN", "guest-services", "enable", "commit", "exit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: can't edit in cli quota")

class TC001_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75300"
    description = show_testcase_info(TESTPLAN, '1519617', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519617')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_guest_user(self):
        add_guestuser_profile = {
            'action': 'add',
            'profilename': 'test_cycle',
            'generate': True,
            'generatename': True,
            'generatepassword': False,
            'activate_on_login': True,
            'enable_account': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 1,
            'acco_lifetype': 'hours'
        }
        response = guest_user.user_guest_profile(**add_guestuser_profile)
        logger.info(response)
        response_get = guest_user.show_user_guest_profile()
        Assertion.assert_regular(json.dumps(response_get), '"name": "test_cycle"',
                                 'err: Failed to create guest users profile')
        commands = ["configure", "user guest", "profile test_cycle", "quota-cycle day", "commit", "exit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: can't edit in cli quota")
    def test_02_delete_user(self):
        response = guest_user.del_user_guest_profile(profilename= "test_cycle")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest profile")

class TC002_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75301"
    description = show_testcase_info(TESTPLAN, '1519618', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519618')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_show_testcase_info(self):
        pass
    def test_01_cli_verify_guest_user(self):
        commands = ["configure", "user guest", "user test_guest", "quota-cycle day", "commit", "exit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: can't edit in cli quota")
    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_guest")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC003_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75307"
    description = show_testcase_info(TESTPLAN, '1519626', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519626')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_limit_guest_user(self):
        add_guestuser_profile = {
            'action': 'add',
            'profilename': 'test_cycle',
            'generate': True,
            'generatename': True,
            'generatepassword': False,
            'activate_on_login': True,
            'enable_account': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 1,
            'acco_lifetype': 'hours',
            'limit': True,
            'limit_receive': -1,
            'limit_transmit': 50
        }
        response = guest_user.user_guest_profile(**add_guestuser_profile)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: it is allowing invalid limit_receive arguments")

class TC004_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75308"
    description = show_testcase_info(TESTPLAN, '1519627', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519627')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_limit_guest_user(self):
        add_guestuser_profile = {
            'action': 'add',
            'profilename': 'test_cycle',
            'generate': True,
            'generatename': True,
            'generatepassword': False,
            'activate_on_login': True,
            'enable_account': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 1,
            'acco_lifetype': 'hours',
            'limit': True,
            'limit_receive': 50,
            'limit_transmit': -50
        }
        response = guest_user.user_guest_profile(**add_guestuser_profile)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: it is allowing invalid limit_transmit arguments")

class TC005_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75309"
    description = show_testcase_info(TESTPLAN, '1519628', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519628')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_limit_guest_user(self):
        add_guestuser_profile = {
            'action': 'add',
            'profilename': 'test_cycle',
            'generate': True,
            'generatename': True,
            'generatepassword': False,
            'activate_on_login': True,
            'enable_account': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 1,
            'acco_lifetype': 'hours',
            'limit': True,
            'limit_receive': 50,
            'limit_transmit': -50,
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": -22,
        }
        response = guest_user.user_guest_profile(**add_guestuser_profile)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: it is allowing invalid sessionlifetime arguments")

class TC006_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75313"
    description = show_testcase_info(TESTPLAN, '1519632', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519632')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_limit_guest_user(self):
        guest_user_1 = {
            'action': 'add',
            'accountname': 'testguest1',
            'password': 'S0nic@uto',
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days',
            'prune_on_expiry': True,
            'comment': 'Newadd',
            'quota_cycle': 'day',
            'session_lifetime': True,
            'sess_lifetime': 30,
            'sess_lifetype': 'minutes'
        }
        rc = guest_user.user_guest_account(**guest_user_1)
        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search('Quota Cycle Type :Per Day', doc) else False
            Assertion.assert_equal(flag, True, "ERR: can't find testguest1 config in tsr")
            os.remove('/tmp/techSupport')

    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="testguest1")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC007_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75314"
    description = show_testcase_info(TESTPLAN, '1519633', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519633')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_limit_guest_user(self):

        add_guestuser_account = {
    "user": {
        "guest": {
            "user": [
                {
                    "name": "testguestlimit",
                    "comment": "Auto-Generated",
                    "password": "S0nic@uto",
                    "enable": True,
                    "login_uniqueness": True,
                    "prune_on_expiry": True,
                    "activate_on_login": False,
                    "account_lifetime": {
                        "days": 7
                    },
                    "idle_timeout": {
                        "minutes": 10
                    },
                    "quota_cycle": {},
                    "session_lifetime": {
                        "hours": 1
                    },
                    "limit": {
                        "receive": 50,
                        "transmit": 50
                    }
                }
            ]
        }
    }
}
        response = guest_user.configure_user_guest_account_json(**add_guestuser_account)
        logger.info(response)
        response_get = guest_user.show_user_guest_account()
        res=guest_user.export_guest_account()
        res_list=res.split("\n")
        for i in res_list:
            if "testguestlimit" in i:
                guest_detail=i
        Assertion.assert_regular(str(guest_detail), '"50 MB"', 'err: traffic bandwidth is not in MB ')
    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="testguestlimit")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC008_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75310"
    description = show_testcase_info(TESTPLAN, '1519629', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519629')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_guest_user_quota(self):
        guest_user_1 = {
            'action': 'add',
            'accountname': 'test_04',
            'password': 'S0nic@uto',
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days',
            'prune_on_expiry': True,
            'comment': 'Newadd',
            'quota_cycle': 'day',
            'session_lifetime': True,
            'sess_lifetime': 2,
            'sess_lifetype': 'minutes',
            'idle_timeout' : True,
            'idle_type' : 'minutes',
            'idle_time' : 2
        }
        rc = guest_user.user_guest_account(**guest_user_1)
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Guest_usr1 = users.UserLoginApi(headers, ip, 'test_04', 'S0nic@uto')
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        time.sleep(180)
        log = log_obj.clear_log()
        time.sleep(10)
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
        time.sleep(30)
        log = log_obj.show_log()
        expected_msg="'message': 'User Session Quota Expired'"
        flag=False
        if expected_msg in str(log):
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")
    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_04")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC009_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75302"
    description = show_testcase_info(TESTPLAN, '1519620', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519620')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_guest_user_quota(self):
        guest_user_1 = {
            'action': 'add',
            'accountname': 'test_03',
            'password': 'S0nic@uto',
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days',
            'prune_on_expiry': True,
            'comment': 'Newadd',
            'quota_cycle': 'day',
            'session_lifetime': True,
            'sess_lifetime': 2,
            'sess_lifetype': 'minutes',
            'idle_timeout' : True,
            'idle_type' : 'minutes',
            'idle_time' : 2
        }
        rc = guest_user.user_guest_account(**guest_user_1)
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Guest_usr1 = users.UserLoginApi(headers, ip, 'test_03', 'S0nic@uto')
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        time.sleep(180)
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")

    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_03")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

# TestCase commented because time modification is not supported
#
# class TC010_GuestUsers(Test):
#     uuid = "SOSAIOT-TC-75305"
#     description = show_testcase_info(TESTPLAN, '1519623', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '1519623')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_guest_user_quota(self):
#         guest_user_1 = {
#             'action': 'add',
#             'accountname': 'test_04',
#             'password': 'S0nic@uto',
#             'activate_on_login': True,
#             'enable_guest_service_privilege': True,
#             'login_uniqueness': False,
#             'account_lifetime': False,
#             'acco_lifetime': 2,
#             'acco_lifetype': 'days',
#             'prune_on_expiry': True,
#             'comment': 'Newadd',
#             'quota_cycle': 'day',
#             'session_lifetime': True,
#             'sess_lifetime': 2,
#             'sess_lifetype': 'minutes',
#             'idle_timeout': True,
#             'idle_type': 'minutes',
#             'idle_time': 2
#         }
#         res = time_obj.show_time()
#         date = res['time']['date']
#         time_json = {
#             "time": {
#                 "use_ntp": False,
#                 "time": "23:54:00",
#                 "date": date,
#                 "time_zone": "pacific-time",
#                 "daylight_savings": True,
#                 "universal": False,
#                 "international_format": False,
#                 "only_custom_ntp": False,
#                 "ntp_update_interval": 60
#             }
#         }
#         rc = time_obj.set_time(**time_json)
#         Assertion.assert_equal(rc, True, "ERR: set time failed")
#         rc = guest_user.user_guest_account(**guest_user_1)
#         headers = OrderedDict([('Accept', 'application/json'),
#                                ('Content-Type', 'application/json'),
#                                ('Accept-Encoding', 'application/json'),
#                                ('charset', 'UTF-8')])
#         Guest_usr1 = users.UserLoginApi(headers, ip, 'test_04', 'S0nic@uto')
#         time.sleep(60)
#         is_auth, bearer_token = Guest_usr1.guest_user_login()
#         Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
#         time.sleep(180)
#         is_auth, bearer_token = Guest_usr1.guest_user_login()
#         Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
#         time.sleep(180)
#         res = time_obj.show_time()
#         is_auth, bearer_token = Guest_usr1.guest_user_login()
#         Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
#     def test_02_delete_user(self):
#         response = guest_user.del_user_guest_account(accountname="test_04")
#         Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC011_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75303"
    description = show_testcase_info(TESTPLAN, '1519621', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519621')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_guest_user_quota(self):
        guest_user_1 = {
            'action': 'add',
            'accountname': 'test_03',
            'password': 'S0nic@uto',
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days',
            'prune_on_expiry': True,
            'comment': 'Newadd',
            'session_lifetime': True,
            'sess_lifetime': 20,
            'sess_lifetype': 'minutes',
            'idle_timeout' : True,
            'idle_type' : 'minutes',
            'idle_time' : 15,
            "limit": True,
            "limit_transmit": 2,
            "limit_receive": 2
        }
        rc = guest_user.user_guest_account(**guest_user_1)
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Guest_usr1 = users.UserLoginApi(headers, ip, 'test_03', 'S0nic@uto')
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(180)
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with guest user ")

    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_03")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC012_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75304"
    description = show_testcase_info(TESTPLAN, '1519622', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519622')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_guest_user_quota(self):
        guest_user_1 = {
            'action': 'add',
            'accountname': 'test_03',
            'password': 'S0nic@uto',
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days',
            'prune_on_expiry': True,
            'comment': 'Newadd',
            'session_lifetime': True,
            'sess_lifetime': 20,
            'sess_lifetype': 'minutes',
            'idle_timeout' : True,
            'idle_type' : 'minutes',
            'idle_time' : 15,
            "limit": True,
            "limit_transmit": 1,
            "limit_receive": 2
        }
        rc = guest_user.user_guest_account(**guest_user_1)
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Guest_usr1 = users.UserLoginApi(headers, ip, 'test_03', 'S0nic@uto')
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(180)
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with guest user ")

    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_03")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC013_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75306"
    description = show_testcase_info(TESTPLAN, '1519624', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519624')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_guest_user_quota(self):
        res = time_obj.show_time()
        date = res['time']['date']
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "23:55:00",
                "date": date,
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_obj.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set time failed")

        guest_user_1 = {
            'action': 'add',
            'accountname': 'test_03',
            'password': 'S0nic@uto',
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days',
            'prune_on_expiry': True,
            'comment': 'Newadd',
            'session_lifetime': True,
            'sess_lifetime': 20,
            'sess_lifetype': 'minutes',
            'idle_timeout' : True,
            'idle_type' : 'minutes',
            'idle_time' : 15,
            "limit": True,
            "limit_transmit": 1,
            "limit_receive": 2,
            'quota_cycle': 'day'

        }
        rc = guest_user.user_guest_account(**guest_user_1)
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Guest_usr1 = users.UserLoginApi(headers, ip, 'test_03', 'S0nic@uto')
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(180)
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with guest user ")
        time.sleep(180)
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")

    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_03")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC014_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75311"
    description = show_testcase_info(TESTPLAN, '1519630', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519630')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_guest_user_quota(self):
        guest_user_1 = {
            'action': 'add',
            'accountname': 'test_04',
            'password': 'S0nic@uto',
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days',
            'prune_on_expiry': True,
            'comment': 'Newadd',
            'session_lifetime': True,
            'sess_lifetime': 20,
            'sess_lifetype': 'minutes',
            'idle_timeout': True,
            'idle_type': 'minutes',
            'idle_time': 15,
            "limit": True,
            "limit_transmit": 1,
            "limit_receive": 2,
            'quota_cycle': 'day'

        }
        rc = guest_user.user_guest_account(**guest_user_1)
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Guest_usr1 = users.UserLoginApi(headers, ip, 'test_04', 'S0nic@uto')
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        time.sleep(10)
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(20)
        log = log_obj.clear_log()
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
        time.sleep(30)
        log = log_obj.show_log()
        expected_msg="'message': 'User Traffic Quota Exceeded'"
        flag=False
        if expected_msg in str(log):
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")
    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_04")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")

class TC015_GuestUsers(Test):
    uuid = "SOSAIOT-TC-75312"
    description = show_testcase_info(TESTPLAN, '1519631', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519631')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_guest_user_quota(self):
        guest_user_1 = {
            'action': 'add',
            'accountname': 'test_04',
            'password': 'S0nic@uto',
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days',
            'prune_on_expiry': True,
            'comment': 'Newadd',
            'session_lifetime': True,
            'sess_lifetime': 20,
            'sess_lifetype': 'minutes',
            'idle_timeout': True,
            'idle_type': 'minutes',
            'idle_time': 15,
            "limit": True,
            "limit_transmit": 2,
            "limit_receive": 1,
            'quota_cycle': 'day'

        }
        rc = guest_user.user_guest_account(**guest_user_1)
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Guest_usr1 = users.UserLoginApi(headers, ip, 'test_04', 'S0nic@uto')
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        time.sleep(10)
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(20)
        log = log_obj.clear_log()
        is_auth, bearer_token = Guest_usr1.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
        time.sleep(30)
        log = log_obj.show_log()
        expected_msg="'message': 'User Traffic Quota Exceeded'"
        flag=False
        if expected_msg in str(log):
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")
    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_04")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")
import sys
import os
import json
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Cyclic_Quota_For_Local_User')
from definition.settings import *


class TC001_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75325"
    description = show_testcase_info(TESTPLAN, '1507033', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507033')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test_cycle",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"]
          }

        response = local_user.local_user(**add_localuser)
        logger.info(response)
        response_get = local_user.show_local_users()
        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search('Quota Type: Non Cyclic', doc) else False
            Assertion.assert_equal(flag, True, "ERR: can't find test1 connfig in tsr")
            os.remove('/tmp/techSupport')

    def test_02_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('test_cycle')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test_cycle"', 'err: user not deleted')


class TC002_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75316"
    description = show_testcase_info(TESTPLAN, '1507023', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507023')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_cli_verify_local_user(self):
        add_localuser = {
            "action": "add",
            "username": "test_cycle",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users", "SonicWALL Administrators"],
            "account_lifetime": True,
            "quota_cycle": "day",
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True

        }

        response = local_user.local_user(**add_localuser)
        logger.info(response)
        commands = ["configure","user local","user test_cycle","quota-cycle day","limit receive 400","limit transmit 233","session-lifetime hours 10","commit", "exit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: can't edit in cli quota")
        res=local_user.show_local_user_by_name(name="test_cycle")
        Assertion.assert_regular(json.dumps(res), '"name": "test_cycle"', 'err: test_cycle not added to custom quota')

    def test_02_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('test_cycle')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test_cycle"', 'err: user not deleted')

class TC003_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75324"
    description = show_testcase_info(TESTPLAN, '1507032', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507032')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_restart_check_user(self):
        add_localuser = {
            "action": "add",
            "username": "test_cycle",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users", "SonicWALL Administrators"],
            "account_lifetime": True,
            "quota_cycle": "day",
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True

        }

        response = local_user.local_user(**add_localuser)
        logger.info(response)
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, "ERR: restart firewall failed")
        res = local_user.show_local_user_by_name(name="test_cycle")
        Assertion.assert_regular(json.dumps(res), '"name": "test_cycle"', 'err: test_cycle not added to custom quota')

    def test_02_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('test_cycle')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test_cycle"', 'err: user not deleted')


class TC004_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75337"
    description = show_testcase_info(TESTPLAN, '1546587', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1546587')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_import_check_user(self):
        add_localuser = {
            "action": "add",
            "username": "test_cycle",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users", "SonicWALL Administrators"],
            "account_lifetime": True,
            "quota_cycle": "day",
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True

        }

        response = local_user.local_user(**add_localuser)
        logger.info(response)
        rc = fw_boot.export_setting_exp(filepath='/tmp/testlog1.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export the settings...")
        rc1 = fw_boot.import_setting_exp(filepath='/tmp/testlog1.exp')
        Assertion.assert_equal(rc1, True, "Error: Failed to import the settings...")
        res = local_user.show_local_user_by_name(name="test_cycle")
        Assertion.assert_regular(json.dumps(res), '"name": "test_cycle"', 'err: test_cycle not added to custom quota')

    def test_02_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('test_cycle')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test_cycle"', 'err: user not deleted')


class TC005_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75327"
    description = show_testcase_info(TESTPLAN, '1546577', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1546577')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_login_check_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "testcycledemo",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone","Trusted Users", "SonicWALL Administrators"],
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 2,
            "prune_on_expiry": True

        }
        res=local_user.delete_local_user_no_domain(username="testcycledemo")
        response = local_user.local_user(**add_localuser)
        logger.info(response)
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Guest_usr1 = users.UserLoginApi(headers,ip, 'testcycledemo', 'S0nic@uto')
        is_auth, bearer_token = Guest_usr1.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")
        time.sleep(180)
        is_auth, bearer_token = Guest_usr1.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with local user ")

    def test_02_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('testcycledemo')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "testcycledemo"', 'err: user not deleted')


class TC006_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75333"
    description = show_testcase_info(TESTPLAN, '1546583', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1546583')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_maximum_account_lifetime(self):
        add_localuser = {
            "action": "add",
            "username": "test_cycle1",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "account_lifetime": True,
            "quota_cycle": "day",
            "lifetype": "days",
            "accountlifetime": 30,
            "session_lifetime": True,
            "sessionlifetimetype": "days",
            "sessionlifetime": 32,
            "prune_on_expiry": True

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, False, "Error: User quota is created with The session lifetime greater than the account lifetime")

    def test_02_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('test_cycle1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test_cycle1"', 'err: user not deleted')


class TC007_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75318"
    description = show_testcase_info(TESTPLAN, '1507025', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507025')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        res = time_obj.show_time()
        date = res['time']['date']
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "23:54:00",
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
        add_localuser = {
            "action": "add",
            "username": "test_cycle",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_cycle', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        time.sleep(180)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
        time.sleep(180)
        res = time_obj.show_time()
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")

    def test_02_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_cycle")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")


class TC008_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75321"
    description = show_testcase_info(TESTPLAN, '1507028', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507028')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        res = time_obj.show_time()
        date = res['time']['date']
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "23:54:00",
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
        add_localuser = {
            "action": "add",
            "username": "test_cycle",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_cycle', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        time.sleep(180)
        log = log_obj.clear_log()
        time.sleep(10)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
        time.sleep(30)
        log = log_obj.show_log()
        expected_msg = "'message': 'User Session Quota Expired'"
        flag = False
        if expected_msg in str(log):
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")

    def test_02_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_cycle")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")



class TC009_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75326"
    description = show_testcase_info(TESTPLAN, '1507034', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507034')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        res = time_obj.show_time()
        date = res['time']['date']
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "23:54:00",
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
        add_localuser = {
            "action": "add",
            "username": "test_cycle",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_cycle', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        time.sleep(180)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
        time.sleep(180)
        res = time_obj.show_time()
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")

    def test_02_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_cycle")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")


class TC010_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75317"
    description = show_testcase_info(TESTPLAN, '1507024', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507024')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_cycle_3",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit" :True,
            "receivelimit" : 2,
            "transmit" : 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_cycle_3', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with guest user ")

    def test_02_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_cycle_3")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")


class TC011_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75319"
    description = show_testcase_info(TESTPLAN, '1507026', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507026')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        res = time_obj.show_time()
        date = res['time']['date']
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "23:54:00",
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
        add_localuser = {
            "action": "add",
            "username": "test_cycle_4",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 2,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_cycle_4', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(180)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with guest user ")
        time.sleep(180)
        res = time_obj.show_time()
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")

    def test_02_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_cycle_4")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")


class TC012_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75320"
    description = show_testcase_info(TESTPLAN, '1507027', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507027')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        res = time_obj.show_time()
        date = res['time']['date']
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "23:54:00",
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
        add_localuser = {
            "action": "add",
            "username": "test_cycle_4",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 2,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_cycle_4', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(180)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with guest user ")
        time.sleep(180)
        res = time_obj.show_time()
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")

    def test_02_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_cycle_4")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")


class TC013_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75322"
    description = show_testcase_info(TESTPLAN, '1507029', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507029')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_cycle_4",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 2,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_cycle_4', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(180)
        log = log_obj.clear_log()
        time.sleep(10)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
        time.sleep(30)
        log = log_obj.show_log()
        expected_msg = "'message': 'User Traffic Quota Exceeded'"
        flag = False
        if expected_msg in str(log):
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")

    def test_02_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_cycle_4")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")


class TC014_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75323"
    description = show_testcase_info(TESTPLAN, '1507030', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507030')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_cycle_4",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 1,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_cycle_4', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with guest user ")
        result = local_host.send_command(f'hping3 --icmp -i u1000 -c 62500 -t 30 12.12.1.169')
        time.sleep(180)
        log = log_obj.clear_log()
        time.sleep(10)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with guest user ")
        time.sleep(30)
        log = log_obj.show_log()
        expected_msg = "'message': 'User Traffic Quota Exceeded'"
        flag = False
        if expected_msg in str(log):
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")

    def test_02_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_cycle_4")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest user")
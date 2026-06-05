import sys
import os
import json
import re
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Localuser_Quota')
from definition.initial_parameter import *
class Local_UserConfig(Test):
    uuid = 'NonTC'

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 10,
            "prune_on_expiry": False
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

class TC01_verify_Quota_configuration_for_localusers(Test):
    uuid = "SOSAIOT-TC-75315"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_verify_Quota_configuration_for_localusers(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': 'day',
            'session_lifetime': True,
            'sessionlifetimetype': 'days',
            'sessionlifetime': 1,
            'userquotalimit': True,
            'receivelimit': 2,
            'transmit': 0

        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"quota_cycle": {"day": True}', 'err: Failed to configure  quota for local user')
        Assertion.assert_regular(json.dumps(resp1), '"limit": {"receive": 2, "transmit": 0}', 'err: Failed to configure quota for local user')


class TC08_verify_Quota_setting_of_sessionLifetime(Test):
    uuid = "SOSAIOT-TC-75327"
    description = show_testcase_info(Parameter.TESTPLAN, '08', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_Quota_setting_of_sessionLifetime(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'days',
            'sessionlifetime': 1,



        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"session_lifetime": {"days": 1}', 'err: Failed to configure  session lifetime for local user')
        Assertion.assert_regular(json.dumps(resp1), '"quota_cycle": {}', 'err: Failed to configure quota for local user')



class TC20_verify_maximum_value_receive_limit(Test):
    uuid = "SOSAIOT-TC-75328"
    description = show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_maximum_value_receive_limit(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'days',
            'sessionlifetime': 1,
            'userquotalimit': True,
            'receivelimit': 0,
            'transmit': 0


        }

        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"limit": {"receive": 0, "transmit": 0}',
                                 'err: Failed to configure maximum value for transmit limit for local user')

class TC21_verify_minimum_value_receive_limit(Test):
    uuid = "SOSAIOT-TC-75329"
    description = show_testcase_info(Parameter.TESTPLAN, '21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_minimum_value_of_receive_limit(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'days',
            'sessionlifetime': 1,
            'userquotalimit': True,
            'receivelimit': 1,
            'transmit': 0


        }

        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"limit": {"receive": 1, "transmit": 0}','err: Failed to configure minimum value for receive limit for local user')



class TC22_verify_maximum_value_transmit_limit(Test):
    uuid = "SOSAIOT-TC-75330"
    description = show_testcase_info(Parameter.TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_maximum_value_transmit_limit(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'days',
            'sessionlifetime': 1,
            'userquotalimit': True,
            'receivelimit': 1,
            'transmit': 0


        }

        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"limit": {"receive": 1, "transmit": 0}',
                                 'err: Failed to configure maximum value for transmit limit for local user')


class TC23_verify_minimum_value_transmit_limit(Test):
    uuid = "SOSAIOT-TC-75331"
    description = show_testcase_info(Parameter.TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_minimum_value_of_transmit_limit(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'days',
            'sessionlifetime': 1,
            'userquotalimit': True,
            'receivelimit': 1,
            'transmit': 1


        }

        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"limit": {"receive": 1, "transmit": 1}',
                                 'err: Failed to configure minimum value for receive limit for local user')

class TC24_verify_minimum_value_for_sessionLifetime(Test):
    uuid = "SOSAIOT-TC-75332"
    description = show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_minimum_value_for_sessionLifetime(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'minutes',
            'userquotalimit': True,
            'sessionlifetime': 1,
            'receivelimit': 1,
            'transmit': 1


        }

        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"session_lifetime": {"minutes": 1}',
                                 'err: Failed to configure minimum value for session lifetime for local user')



class TC25_verify_maximum_value_Sessionlifetime(Test):
    uuid = '1086758'
    description = show_testcase_info(Parameter.TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_maximum_value_Sessionlifetime(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'days',
            'sessionlifetime': 9999,



        }

        resp = local_user.local_user(**user_json, msg=True)

        Assertion.assert_regular(resp[1]['status']['info'][0]['message'], "The session lifetime can not be greater than"
                                                                          "                                   the account lifetime.", "err: failed to throw error")




class TC26_verify_invalid_value_for_receiveLimit(Test):
    uuid = "SOSAIOT-TC-75334"
    description = show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_invalid_value_for_receiveLimit(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'minutes',
            'userquotalimit': True,
            'sessionlifetime': 1,
            'receivelimit': "a",
            'transmit': 1


        }

        resp = local_user.local_user(**user_json, msg=True)

        Assertion.assert_regular(resp[1]['status']['info'][0]['message'], 'Schema validation error: property \'receive\' expected: \'NUMBER\', found: \'"STRING..."\'\n', "err: failed to throw error")


class TC27_verify_invalid_value_for_transmitLimit(Test):
    uuid = "SOSAIOT-TC-75335"
    description = show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_invalid_value_for_transmitLimit(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'minutes',
            'userquotalimit': True,
            'sessionlifetime': 1,
            'receivelimit': 1,
            'transmit': -1


        }

        resp = local_user.local_user(**user_json, msg=True)

        Assertion.assert_regular(resp[1]['status']['info'][0]['message'], "Schema validation error: property 'transmit': invalid format\n", "err: failed to throw error")




class TC28_verify_invalid_value_for_sessionLifetime(Test):
    uuid = "SOSAIOT-TC-75336"
    description = show_testcase_info(Parameter.TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_invalid_value_for_sessionLifetime(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW,
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 9,
            "prune_on_expiry": False,
            'quota_cycle': {},
            'session_lifetime': True,
            'sessionlifetimetype': 'minutes',
            'userquotalimit': True,
            'sessionlifetime': -1,
            'receivelimit': 1,
            'transmit': -1


        }

        resp = local_user.local_user(**user_json, msg=True)

        Assertion.assert_regular(resp[1]['status']['info'][0]['message'], "Schema validation error: property 'minutes': invalid format\n", "err: failed to throw error")



class TC37_Check_LocalUser_config_in_TSR(Test):
    uuid = "SOSAIOT-TC-75337"
    description = show_testcase_info(Parameter.TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_Check_LocalUser_config_in_TSR(self):
        resp1 = local_user.show_local_user_by_name('test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to show user test1')
        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search('Quota Type: Non Cyclic', doc) else False
            Assertion.assert_equal(flag, True, "ERR: can't find test1 connfig in tsr")
            os.remove('/tmp/techSupport')

class TC_delete_Localuser(Test):
    uuid = 'NonTC'

    def test_delete_localUser(self):
        stage_description = 'Delete the user with account lifetime configured'
        logger.info(stage_description)

        resp =local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()

        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')

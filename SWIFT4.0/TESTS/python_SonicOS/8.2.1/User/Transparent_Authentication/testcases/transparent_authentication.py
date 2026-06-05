from definition.settings import *


class TC_01_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75290"
    description = show_testcase_info(Parameter.TESTPLAN, '1825269', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825269')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def config_sso_retries_field(self, value=None):
        input_data = {
            'action': 'add',
            'host': Parameter.SSO_SERV,
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': value
        }
        response = user_sso.sso_agent(**input_data)
        return response

    def test_01_sso_retries_field(self):
        # retries =[1]
        retries = [1, 5, 10, 100]
        for i in retries:
            response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
            response = self.config_sso_retries_field(value=i)
            if i == 100:
                Assertion.assert_equal(response, False, "ERR: Retries field boundaries test Failed.")
            else:
                Assertion.assert_equal(response, True, "ERR: Retries field boundaries test Failed.")


class TC_02_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75289"
    description = show_testcase_info(Parameter.TESTPLAN, '1825268', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825268')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_ssouser(self):
        edit_timeout = {
            "user": {
                "sso": {
                    "hold_time": {
                        "after_failure": 1,
                        "after_no_user": 0
                    }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, False, "ERR: Updating the hold timeout value failed")


class TC_03_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75288"
    description = show_testcase_info(Parameter.TESTPLAN, '1825267', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825267')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user_sso_settings(self):
        user_sso_settings = {
            'user': {
                'sso': {
                    'user_group_mechanism': {
                        'local_only': True
                    },
                    'hold_time': {
                        'after_failure': 1,
                        'after_no_user': 1
                    },
                    'poll': {
                        'rate': {
                            'minutes': 0
                        },
                        'same_agent': False
                    }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**user_sso_settings)
        Assertion.assert_equal(response, False, "ERR: Unable to Enable User SSO Settings")


class TC_04_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75287"
    description = show_testcase_info(Parameter.TESTPLAN, '1825266', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825266')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_ssouser(self):
        edit_timeout = {
            "user": {
                "sso": {
                    "hold_time": {
                        "after_failure": 0,
                        "after_no_user": 1
                    }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, False, "ERR: Updating the hold timeout value failed")


class TC_05_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75286"
    description = show_testcase_info(Parameter.TESTPLAN, '1825263', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825263')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_ssouser(self):
        edit_timeout = {
            "user": {
                "sso": {
                    'poll': {
                        'rate': {
                            'minutes': "n"
                        }
                    }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, False, "ERR: Updating the hold timeout value failed")


class TC_06_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75285"
    description = show_testcase_info(Parameter.TESTPLAN, '1825262', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825262')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': Parameter.SSO_SERV,
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225ac',
            'retries': 3
        }
        response = user_sso.sso_agent(**input_data)
        response_1 = user_sso.test_sso_agent(ip=Parameter.SSO_SERV)
        expected_result = "SSO agent did not respond"
        Assertion.assert_regular(str(response_1), expected_result, "ERR: Check Shared Secret not match got passed")


class TC_07_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75284"
    description = show_testcase_info(Parameter.TESTPLAN, '1825261', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825261')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user_sso_settings(self):
        user_sso_settings = {
            'user': {
                'sso': {
                    'user_group_mechanism': {
                        "ldap": True
                    }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**user_sso_settings)
        Assertion.assert_equal(response, True, "ERR: Unable to Enable User SSO Settings")


class TC_08_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75283"
    description = show_testcase_info(Parameter.TESTPLAN, '1825260', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825260')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user_sso_settings(self):
        user_sso_settings = {
            'user': {
                'sso': {
                    "local_users_only": True
                }
            }
        }
        response = user_sso.config_sso_base_settings(**user_sso_settings)
        Assertion.assert_equal(response, True, "ERR: Unable to Enable User SSO Settings")


class TC_09_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75282"
    description = show_testcase_info(Parameter.TESTPLAN, '1825259', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825259')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': "",
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': 3
        }
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, False, "ERR: Empty input check got passed")


class TC_10_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75281"
    description = show_testcase_info(Parameter.TESTPLAN, '1825257', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825257')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_ssouser(self):
        edit_timeout = {
            "user": {
                "sso": {
                    "hold_time": {
                        "after_failure": "#",
                        "after_no_user": 1
                    }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, False, "ERR: Updating the hold timeout value failed")


class TC_11_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75280"
    description = show_testcase_info(Parameter.TESTPLAN, '1825256', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825256')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_ssouser(self):
        edit_timeout = {
            "user": {
                "sso": {
                    "hold_time": {
                        "after_failure": 0,
                        "after_no_user": "%"
                    }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, False, "ERR: Updating the hold timeout value failed")


class TC_12_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75279"
    description = show_testcase_info(Parameter.TESTPLAN, '1825254', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825254')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_ssouser(self):
        values = ["#", "%", "n"]
        for i in values:
            input_data = {
                'action': 'add',
                'host': Parameter.SSO_SERV,
                'port': 2258,
                'timeout': 5,
                'max_requests': i,
                'enable': True,
                'shared_key': '225abc',
                'retries': 3
            }
            response = user_sso.sso_agent(**input_data)
            Assertion.assert_equal(response, False, "ERR: Empty input check got passed")


class TC_13_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75278"
    description = show_testcase_info(Parameter.TESTPLAN, '1825253', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825253')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def config_sso_retries_field(self, value=None):
        input_data = {
            'action': 'add',
            'host': Parameter.SSO_SERV,
            'port': value,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': 3
        }
        response = user_sso.sso_agent(**input_data)
        return response

    def test_add_ssouser(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
        values = [1, 2, 3000, 65535, 65536]
        for i in values:
            response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=i)
            response = self.config_sso_retries_field(value=i)
            if i == 65536:
                Assertion.assert_equal(response, False, "ERR: port number boundary test with SSO agent failed.")
            else:
                Assertion.assert_equal(response, True, "ERR: port number boundary test with SSO agent failed.")


class TC_14_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75277"
    description = show_testcase_info(Parameter.TESTPLAN, '1825252', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825252')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': "@#$AA",
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': 3
        }
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, False, "ERR: Illegal character check for Host name got passed")


class TC_15_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-94686"
    description = show_testcase_info(Parameter.TESTPLAN, '1825251', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825251')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': "a" * 100 + "c" * 5,
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': 3
        }
        response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, False, "ERR: Illegal character check for Host name got passed")


class TC_16_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75276"
    description = show_testcase_info(Parameter.TESTPLAN, '1825249', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825249')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': Parameter.SSO_SERV,
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc' * 3,
            'retries': 3
        }
        response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, False, "ERR:  Shared Key field accepts more than 16 characters passed")


class TC_17_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75275"
    description = show_testcase_info(Parameter.TESTPLAN, '1825248', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825248')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        for i in ["#", "%", "n"]:
            input_data = {
                'action': 'add',
                'host': Parameter.SSO_SERV,
                'port': i,
                'timeout': 5,
                'max_requests': 3,
                'enable': True,
                'shared_key': '225abc',
                'retries': 3
            }
            response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
            response = user_sso.sso_agent(**input_data)
            Assertion.assert_equal(response, False, "ERR:  Incorrectly formatted data with Port number test passed")


class TC_18_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-94684"
    description = show_testcase_info(Parameter.TESTPLAN, '1825247', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825247')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': Parameter.SSO_SERV,
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': 3
        }
        response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, True, "ERR:  config SSO agent got Failed.")
        input_data = {
            'action': 'edit',
            'host': Parameter.SSO_SERV,
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225ab',
            'retries': 3
        }
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, False, "ERR:  config SSO agent got Passed with odd number of keys.")


class TC_19_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75274"
    description = show_testcase_info(Parameter.TESTPLAN, '1825246', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825246')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': Parameter.SSO_SERV,
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': 101
        }
        response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, False, "ERR:  config SSO agent got passed with more than MAX retries.")


class TC_20_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75273"
    description = show_testcase_info(Parameter.TESTPLAN, '1825244', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825244')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        for i in ["#", "%", "n"]:
            input_data = {
                'action': 'add',
                'host': Parameter.SSO_SERV,
                'port': 2258,
                'timeout': 5,
                'max_requests': 3,
                'enable': True,
                'shared_key': '225abc',
                'retries': i
            }
            response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
            response = user_sso.sso_agent(**input_data)
            Assertion.assert_equal(response, False, "ERR:Incorrectly formatted data in the Retries field got passed.")


class TC_21_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75272"
    description = show_testcase_info(Parameter.TESTPLAN, '1825242', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825242')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': Parameter.SSO_SERV,
            'port': 2258,
            'timeout': 301,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': 3
        }
        response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, False,
                               "ERR: Incorrectly Timeout (seconds) field boudaries test field got passed.")


class TC_22_transparent_authentication(Test):
    uuid = "SOSAIOT-TC-75271"
    description = show_testcase_info(Parameter.TESTPLAN, '1825241', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825241')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sso_retries_field(self):
        input_data = {
            'action': 'add',
            'host': "192.198.198",
            'port': 2258,
            'timeout': 3,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc',
            'retries': 3
        }
        response = user_sso.del_sso_agent(name=f'{Parameter.SSO_SERV}', port=2258)
        response = user_sso.sso_agent(**input_data)
        Assertion.assert_equal(response, False, "ERR: Invalid IP address check got passed.")

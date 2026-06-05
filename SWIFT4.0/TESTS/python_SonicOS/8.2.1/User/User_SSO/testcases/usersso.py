from definition.settings import *

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/User_SSO')


class TC01_PUT_SSO_User_Settings(Test):
    uuid = "SOSAIOT-TC-47837"
    description = show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_put_sso_user_settings(self):
        sso_user_settings = {
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
                            'minutes': 1
                        },
                        'same_agent': False
                    }
                }
            }
        }

        response = user_sso.config_sso_base_settings(**sso_user_settings)
        Assertion.assert_equal(response, True, "ERR: Unable to PUT User SSO Settings")


class TC02_POST_SSO_User_Agent(Test):
    uuid = "SOSAIOT-TC-47838"
    description = show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_sso_agent(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '1.1.1.1',
                 'port': 2220,
                 'timeout': 10,
                 'retries': 3,
                 'max_requests': 32,
                 'enable': True,
                 'shared_key':'12345678'
        }

        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to POST User SSO Agent")


class TC03_PUT_SSO_User_Agent(Test):
    uuid = "SOSAIOT-TC-47839"
    description = show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_put_sso_agent(self):
        put_sso_agent = {
            "user": {
                "sso": {
                    "agent": [
                        {
                            'host': '1.1.1.2',
                            'port': 2220,
                            'timeout': 10,
                            'retries': 3,
                            'max_requests': 32,
                            'enable': True,
                            'shared_key': '12345678'
                        }
                    ]
                }
            }    
        }
        response = user_sso.edit_sso_agent_name_port(name="1.1.1.1", port="2220", **put_sso_agent)
        Assertion.assert_equal(response, True, "ERR: Unable to PUT User SSO Agent")

    
class TC04_POST_SSO_User_Terminal_Service_Agent(Test):
    uuid = "SOSAIOT-TC-47840"
    description = show_testcase_info(Parameter.TESTPLAN, '4', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_sso_terminal_service_agent(self):    
        post_tsa_dict = {
            'action': 'add',
            'host': '1.1.1.1',
            'port': 2260,
            'enable': True,
            'shared_key': '12345678'
        }
        response = user_sso.terminal_services_agent(**post_tsa_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to POST User SSO Terminal Service Agent")

    
class TC05_PUT_SSO_User_Terminal_Service_Agent(Test):
    uuid = "SOSAIOT-TC-47841"
    description = show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_put_sso_terminal_service_agent(self):    
        put_tsa_dict = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            'action': 'edit',
                            'host': '1.1.1.1',
                            'port': 2259,
                            'enable': True,
                            'shared_key': '12345678'
                        }
                    ]
                }
            }    
        }
        response = user_sso.edit_terminal_services_agent_name_port(name="1.1.1.1", port="2260", **put_tsa_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to PUT User SSO Terminal Service Agent")


class TC06_POST_SSO_User_Radius_Accounting_Client(Test):
    uuid = "SOSAIOT-TC-47842"
    description = show_testcase_info(Parameter.TESTPLAN, '6', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_sso_radius_accounting_client(self):    
        post_radius_client_dict = {
            'action': 'add',
            'host': "1.1.1.1",
            'secret': '12345678',  
        }
        response = user_sso.sso_radius_accounting_client(**post_radius_client_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to POST User SSO Radius Accounting Client")


class TC07_PUT_SSO_User_Radius_Accounting_Client(Test):
    uuid = "SOSAIOT-TC-47843"
    description = show_testcase_info(Parameter.TESTPLAN, '7', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_put_sso_radius_accounting_client(self):    
        put_radius_client_dict = {
            "user": {
                "sso": {
                    "radius_accounting_client": [
                        {
                            'action': 'edit',
                            'host': "1.1.1.2",
                            'secret': '12345678', 
                        }
                    ]
                }
            }    
        }
        response = user_sso.edit_radius_accounting_client(name="1.1.1.1", **put_radius_client_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to PUT User SSO Radius Accounting Client")


class TC08_PUT_Non_Existing_SSO_User_Agent(Test):
    uuid = "SOSAIOT-TC-47844"
    description = show_testcase_info(Parameter.TESTPLAN, '8', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_put_non_existing_sso_agent(self):
        put_sso_agent = {
            "user": {
                "sso": {
                    "agent": [
                        {
                            'host': '1.1.1.1',
                            'port': 2221,
                            'timeout': 10,
                            'max_requests': 32,
                            'enable': True,
                            'shared_key':'12345678'
                        }
                    ]
                }
            }    
        }
        response = user_sso.edit_sso_agent(name="2.2.2.2", **put_sso_agent)
        Assertion.assert_equal(response, False, "ERR: Able to PUT Non Existing User SSO Agent")
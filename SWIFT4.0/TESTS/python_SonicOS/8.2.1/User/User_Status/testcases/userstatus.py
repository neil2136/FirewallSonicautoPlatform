from definition.settings import *

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/User_Status')


class TC01_GET_User_Management(Test):
    uuid = "SOSAIOT-TC-47845"
    description = show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_get_user_management(self):
        response = user_status.show_user_management()
        Assertion.assert_regular(json.dumps(response), 'user', "ERR: Unable to GET User Management Settings")


class TC02_PUT_User_Management(Test):
    uuid = "SOSAIOT-TC-47846"
    description = show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")    

    def test_01_put_user_management(self):
        user_status_dict = {
            'inactive_users': False,
            'unauthenticated_users': True
        }
        response = user_status.user_management(**user_status_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to PUT User Management Settings")

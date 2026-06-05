from definition.settings import *
from definition.utils import user_member_check

class Test_01_Limited_Privilege_Added_6(Test):
    """
    Edit user. Add Limited Management Capabitilies privilege(covered by case 3, enhance it to Guest Services test)
    """
    uuid = "SOSAIOT-TC-75495"
    description = show_testcase_info(Parameter.TESTPLAN, "01", description=True)['title']

    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_01_add_guest_admin(self):
        adduser = userlocal.local_user(**add_guest_user)
        logger.info(adduser)
        output = userlocal.user_member_of(**add_guest_member)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Add user member failed.")

    def test_01_02_check_guestuser(self):
        output = userlocal.show_local_groups()
        logger.info(output)
        checkresult = user_member_check(output, guest_group_name, guest_user_name)
        Assertion.assert_equal(checkresult, True, "ERR: the guestuser is not in Guest Services Group.")


class Test_02_Limited_Administrator_Added_8(Test):
    """
    Add user to a group that has Limited Administrator privileges
    """
    uuid = "SOSAIOT-TC-75496"
    description = show_testcase_info(Parameter.TESTPLAN, "02", description=True)['title']

    def test_02_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_01_add_limit_account(self):
        adduser = userlocal.local_user(**add_limit_user)
        logger.info(adduser)
        output = userlocal.user_member_of(**add_limit_member)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Add limit user member failed.")

    def test_02_02_check_guestuser(self):
        output = userlocal.show_local_groups()
        logger.info(output)
        checkresult = user_member_check(output, limit_group_name, limit_user_name)
        Assertion.assert_equal(checkresult, True, "ERR: the limituser is not in Limited Administrators Group.")


class Test_03_Limited_management_Check_19(Test):
    """
    Verify user with the limited management right can manage the firmware(from LAN)
    """
    uuid = "SOSAIOT-TC-75493"
    description = show_testcase_info(Parameter.TESTPLAN, "03", description=True)['title']

    def test_03_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_03_01_add_limit_account(self):
        adduser = userlocal.local_user(**add_limit_admin)
        logger.info(adduser)
        output = userlocal.user_member_of(**add_limit_admin_member)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Add user member failed.")

    def test_03_02_config_X0_interface(self):
        output = interface.config_interface(**X0_static_opt)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Config X0 Interface failed")

    def test_03_03_limituser_login(self):
        output, bearer_token = limituserlogin.local_user_login()
        guest_user_config['bearer_token'] = bearer_token
        local_user_config['bearer_token'] = bearer_token
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: the Limit admin user login failed.")

    # def test_03_04_check_limituser_login(self):
    #     output = userstatus.show_users_status()
    #     logger.info(output)
    #     # userfilter = re.findall('readonlyuser|Read-only', output)
    #     limituserlogin.local_user_login()
    #     logout = limituserlogin.admin_user_logout()
    #     logger.info(logout)
    #     Assertion.assert_regular(str(output), limit_admin_username, "ERR: the Limit user is not in local user status.")

    def test_03_04_check_guest_user_configurable(self):
        output = limituserlogin.add_guest_user_account(**guest_user_config)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Add guest user failed.")

    def test_03_05_check_local_user_configurable(self):
        output = limituserlogin.add_local_user_account(**local_user_config)
        logger.info(output)
        Assertion.assert_equal(output, False, "ERR: Add local user surceased. it is not expect !")


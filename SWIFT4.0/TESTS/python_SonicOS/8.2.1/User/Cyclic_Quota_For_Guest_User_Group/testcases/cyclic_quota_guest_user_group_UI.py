import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Cyclic_Quota_For_Guest_User_Group')


from definition.settings import *


#[GUI]verify quota cycle type setting can be configured in local users
class TC001_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75291"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519609')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        response = ui_obj.add_and_validate_cyclic_quota_local_user(name="test_ui")
        Assertion.assert_equal(response, True, "ERR: verifying Cyclic_quota failed")

    def test_02_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('test_ui')
        resp = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp), '"name": "test_ui"', 'err: user not deleted')

class TC002_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75292"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519610')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        response = ui_obj.add_and_validate_guest_services(name="test_ui")
        Assertion.assert_equal(response, True, "ERR: verifying add_and_validate_guest_services failed")
    def test_02_delete_user(self):
        response = guest_user.del_user_guest_profile(profilename= "test_ui")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest profile")

class TC003_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75293"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519610')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        response = ui_obj.add_and_validate_guest_account(name="test_ui")
        Assertion.assert_equal(response, True, "ERR: verifying add_and_validate_guest_services failed")
    def test_02_delete_user(self):
        response = guest_user.del_user_guest_account(accountname="test_ui")
        Assertion.assert_equal(response, True, "ERR: can't able to delete guest profile")

class TC004_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75294"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519610')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        response = ui_obj.validate_cyclic_quota_drop_down_guest_account()
        Assertion.assert_equal(response, True, "ERR: verifying add_and_validate_guest_services failed")

class TC005_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75295"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519613')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        response = ui_obj.wlan_zone_guest_services(enable=True)
        response &= ui_obj.validate_wlan_zone_guest_services(enable=True)
        Assertion.assert_equal(response, True, "ERR: verifying add_and_validate_guest_services failed")

class TC006_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75296"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519614')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        res =ui_obj.get_value()
        if "sw-toggle--off" in res:
            response = True
        else:
            response = ui_obj.wlan_zone_guest_services_on(enable=False)
        Assertion.assert_equal(response, True, "ERR: verifying add_and_validate_guest_services failed")

class TC007_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75297"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519615')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        res= ui_obj.get_text()
        Assertion.assert_equal(res, True, "ERR: show perday quota is failed")

    
class TC008_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75298"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519616')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        res= ui_obj.get_text(text ="Per Week")
        Assertion.assert_equal(res, True, "ERR: show per week quota is failed")

class TC009_Cyclic_quota(Test):
    uuid = "SOSAIOT-TC-75299"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3024002')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cyclic_quota(self):
        res= ui_obj.get_text(text ="Per Month")
        Assertion.assert_equal(res, True, "ERR: show per Month quota is failed")

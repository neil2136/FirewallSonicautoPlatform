from definition.settings import *
from definition.utils import *


class Test_CFS_User_TC198(Test):
    uuid = "SOSAIOT-TC-77582"

    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "uri_list": {
                "search_order": "allowed-first",
                "allowed": [{"name": CaseParms.URI_OBJ_NAME_1}],
            }
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(5)
    def test_02_verify_search_passed_via_lan(self):
        logger.info("Verify CFS policy on LAN client after sleeping 5s")
        time.sleep(5)
        res = chk_url_resp_cfs(PC2_login, "unblock", url=CaseParms.CFS_TEST_URL_1)
        Assertion.assert_equal(res, True, "ERR: verify web unblocked via cfs failed")

    def test_03_restore_cfs_profile(self):
        logger.info("Restore the CFS profile.")
        name = get_cfs_value_by_key(cfs_def_profile_dict, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_def_profile_dict)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")


class Test_CFS_User_TC199(Test):
    uuid = "SOSAIOT-TC-77583"

    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "uri_list": {
                "search_order": "forbidden-first",
                "allowed": [{"name": CaseParms.URI_OBJ_NAME_1}],
            }
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(5)
    def test_02_verify_search_passed_via_lan(self):
        Test_CFS_User_TC198().test_02_verify_search_passed_via_lan()

    def test_03_restore_cfs_profile(self):
        Test_CFS_User_TC198().test_03_restore_cfs_profile()


class Test_CFS_User_TC203(Test):
    uuid = "SOSAIOT-TC-77584"


    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "uri_list": {
                "allowed": [{"name": CaseParms.URI_OBJ_NAME_2}],
            }
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(5)
    def test_02_verify_search_passed_via_lan(self):
        logger.info("Verify CFS policy on LAN client after sleeping 5s")
        time.sleep(5)
        res = chk_url_resp_cfs(PC2_login, "unblock", url=CaseParms.CFS_TEST_URL_2)
        Assertion.assert_equal(res, True, "ERR: verify web unblocked via cfs failed")

    def test_03_restore_cfs_profile(self):
        Test_CFS_User_TC198().test_03_restore_cfs_profile()


class Test_CFS_User_TC204(Test):
    uuid = "SOSAIOT-TC-77585"

    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "uri_list": {
                "allowed": [{"name": CaseParms.URI_OBJ_NAME_3}],
            }
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(5)
    def test_02_verify_search_passed_via_lan(self):
        logger.info("Verify CFS policy on LAN client after sleeping 5s")
        time.sleep(5)
        res = chk_url_resp_cfs(PC2_login, "unblock", url=CaseParms.CFS_TEST_URL_3)
        Assertion.assert_equal(res, True, "ERR: verify web unblocked via cfs failed")

    def test_03_restore_cfs_profile(self):
        Test_CFS_User_TC198().test_03_restore_cfs_profile()


class Test_CFS_User_TC197(Test):
    uuid = "SOSAIOT-TC-77587"


    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "uri_list": {
                "forbidden_operation": "confirm",
                "forbidden": [{"name": CaseParms.URI_OBJ_NAME_1}],
            }
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        upd_cate_value = {"29. Search Engines and Portals": "confirm"}
        cfs_profile_cate_upd = upd_cfs_profile_cate(cfs_profile, **upd_cate_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile_cate_upd)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(5)
    def test_02_verify_search_blocked_via_lan(self):
        logger.info("waiting for 30s to valid cfs configure...")
        time.sleep(30)
        res = chk_url_resp_cfs(PC2_login, "confirm")
        Assertion.assert_equal(res, True, "ERR: verify web confirmed via cfs failed")

    def test_03_restore_cfs_profile(self):
        logger.info("Restore the CFS profile.")
        name = get_cfs_value_by_key(cfs_def_profile_dict, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_def_profile_dict)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    def test_04_restore_cfs_profile(self):
        Test_CFS_User_TC198().test_03_restore_cfs_profile()


class Test_CFS_User_TC200(Test):
    uuid = "SOSAIOT-TC-77605"


    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {"29. Search Engines and Portals": "allow"}
        cfs_profile_dict = upd_cfs_profile_cate(cfs_def_profile_dict, **upd_value)
        upd_value = {
            "uri_list": {
                "search_order": "allowed-first",
                "forbidden": [{"name": CaseParms.URI_OBJ_NAME_1}],
            },
        }
        cfs_profile = upd_cfs_payload(cfs_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(3)
    def test_02_verify_search_blocked_via_lan(self):
        logger.info("waiting for 30s to valid cfs configure...")
        time.sleep(30)
        res = chk_url_resp_cfs(PC2_login, "block")
        Assertion.assert_equal(res, True, "ERR: verify web blocked via cfs failed")


class Test_CFS_User_TC201(Test):
    uuid = "SOSAIOT-TC-77606"


    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "uri_list": {
                "search_order": "forbidden-first",
                "forbidden": [{"name": CaseParms.URI_OBJ_NAME_1}],
            },
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(3)
    def test_02_verify_search_blocked_via_lan(self):
        Test_CFS_User_TC200().test_02_verify_search_blocked_via_lan()


class Test_CFS_User_TC205(Test):
    uuid = "SOSAIOT-TC-77607"

    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "uri_list": {
                "forbidden": [{"name": CaseParms.URI_OBJ_NAME_3}],
            },
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(3)
    def test_02_verify_search_blocked_via_lan(self):
        logger.info("waiting for 20s to valid cfs configure...")
        time.sleep(20)
        res = chk_url_resp_cfs(PC2_login, "block", url=CaseParms.CFS_TEST_URL_3)
        Assertion.assert_equal(res, True, "ERR: verify web blocked via cfs failed")


class Test_CFS_Profile_TC145(Test):
    uuid = "SOSAIOT-TC-77608"


    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "youtube_restrict_mode": False,
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    @repeat_method(3)
    def test_02_verify_search_blocked_via_lan(self):
        Test_CFS_User_TC200().test_02_verify_search_blocked_via_lan()

    def test_03_restore_cfs_profile(self):
        Test_CFS_User_TC198().test_03_restore_cfs_profile()


class Test_CFS_Profile_TC149(Test):
    uuid = "SOSAIOT-TC-77609"


    def test_01_edit_cfs_profile(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "safe_search": False,
            "youtube_restrict_mode": False,
        }
        cfs_profile = upd_cfs_payload(cfs_def_profile_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_profile, "name")
        res = cfsprofileapi.edit_cfo_profile_by_name(name=name, **cfs_profile)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS profile.")

    def test_02_edit_cfs_action(self):
        logger.info("Edit the CFS profile.")
        upd_value = {
            "wipe_cookies": False,
            "flow_reporting": False,
        }
        cfs_action = upd_cfs_payload(cfs_def_action_dict, **upd_value)
        name = get_cfs_value_by_key(cfs_action, "name")
        res = cfsactionapi.edit_cfo_action_by_name(name=name, **cfs_action)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS action.")

    @repeat_method(3)
    def test_03_verify_search_blocked_via_lan(self):
        Test_CFS_User_TC200().test_02_verify_search_blocked_via_lan()

    def test_04_restore_cfs_action(self):
        logger.info("Restore the CFS action.")
        name = get_cfs_value_by_key(cfs_def_action_dict, "name")
        res = cfsactionapi.edit_cfo_action_by_name(name=name, **cfs_def_action_dict)
        Assertion.assert_equal(res, True, "ERR: Failed to set the CFS action.")

    def test_05_restore_cfs_profile(self):
        Test_CFS_User_TC198().test_03_restore_cfs_profile()


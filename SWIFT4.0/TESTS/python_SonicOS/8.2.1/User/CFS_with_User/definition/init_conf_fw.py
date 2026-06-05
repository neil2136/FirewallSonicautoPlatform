from definition.settings import *
from definition.utils import upd_cfs_profile_cate, gen_url_obj_payload, upd_cfs_payload


class TestConfigFW(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("Config X1 interface")
        res = interfacev4api.config_interface(**x1_wan_v4_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")

    def test_02_Config_X1_V6(self):
        logger.info("config X1 interface V6")
        rc = interfacev6api.config_interface_ipv6(**x1_wan_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv6 to static failed")

    def test_03_Config_X2(self):
        logger.info("Config X2 interface")
        res = interfacev4api.config_interface(**x2_lan_v4_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 to static failed")

    def test_04_Config_X2_V6(self):
        logger.info("config X2 interface V6")
        rc = interfacev6api.config_interface_ipv6(**x2_lan_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv6 to static failed")

    def test_05_Config_X3(self):
        logger.info("Config X3 interface")
        res = interfacev4api.config_interface(**x3_lan_v4_dict)
        Assertion.assert_equal(res, True, "ERR: Config X3 to static failed")

    def test_06_Config_X3_V6(self):
        logger.info("config X3 interface V6")
        rc = interfacev6api.config_interface_ipv6(**x3_lan_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 to static failed")

    @repeat_method(10)
    def test_07_register_fw(self):
        logger.info("Sleep 20s before registering firewall")
        time.sleep(20)
        res = licensecli.register("online")
        Assertion.assert_equal(res, True, "ERR: Register fw failed")

    def test_08_config_cfs_settings(self):
        logger.info("Enable CFS service")
        res = cfsapi.edit_cfs_settings(**cfs_service_dict)
        Assertion.assert_equal(res, True, "ERR: Config CFS settings failed")

    def test_09_edit_cfs_profile(self):
        logger.info("Edit CFS default profile")
        res = cfsprofileapi.edit_cfo_profile_by_name(
            name="CFS Default Profile", **cfs_def_profile_dict
        )
        Assertion.assert_equal(res, True, "ERR: Config CFS profile failed")

    def test_10_add_cus_cfs_profile(self):
        logger.info("Add CFS custom profile")
        cfs_profile_dict = copy.deepcopy(cfs_def_profile_dict)
        cfs_profile_dict["content_filter"]["profile"][0]["name"] = (
            CaseParms.CUS_CFS_PROFILE_NAME
        )
        upd_value = {"29. Search Engines and Portals": "allow"}
        cfs_profile_dict = upd_cfs_profile_cate(cfs_profile_dict, **upd_value)
        res = cfsprofileapi.add_cfo_profile(**cfs_profile_dict)
        Assertion.assert_equal(res, True, "ERR: Add CFS profile failed")

    def test_11_add_cus_cfs_action(self):
        logger.info("Add CFS custom action")
        upd_value = {"name": CaseParms.CUS_CFS_ACT_NAME}
        cfs_action = upd_cfs_payload(cfs_def_action_dict, **upd_value)
        res = cfsactionapi.add_cfo_action(**cfs_action)
        Assertion.assert_equal(res, True, "ERR: Add CFS action failed")

    def test_12_add_uri_list_object(self):
        logger.info("Add URI list object")
        upd_value_1 = {
            "name": CaseParms.URI_OBJ_NAME_1,
            "type": "uri",
            "uri": [{"uri": f"{CaseParms.CFS_TEST_URL_1}"}],
        }
        url_obj_payload_1 = gen_url_obj_payload(**upd_value_1)
        resp_1 = cfsobjectapi.add_cfo_object(**url_obj_payload_1)
        upd_value_2 = {
            "name": CaseParms.URI_OBJ_NAME_2,
            "type": "uri",
            "uri": [{"uri": f"{CaseParms.CFS_TEST_URL_2}"}],
        }
        url_obj_payload_2 = gen_url_obj_payload(**upd_value_2)
        resp_2 = cfsobjectapi.add_cfo_object(**url_obj_payload_2)
        upd_value_3 = {
            "name": CaseParms.URI_OBJ_NAME_3,
            "type": "uri",
            "uri": [{"uri": f"{CaseParms.CFS_TEST_URL_3}"}],
        }
        url_obj_payload_3 = gen_url_obj_payload(**upd_value_3)
        resp_3 = cfsobjectapi.add_cfo_object(**url_obj_payload_3)
        upd_value_4 = {
            "name": CaseParms.URI_OBJ_NAME_4,
            "type": "uri",
            "uri": [{"uri": f"{CaseParms.CFS_TEST_URL_4}"}],
        }
        url_obj_payload_4 = gen_url_obj_payload(**upd_value_4)
        resp_4 = cfsobjectapi.add_cfo_object(**url_obj_payload_4)
        upd_value_5 = {
            "name": CaseParms.URI_OBJ_NAME_5,
            "type": "uri",
            "uri": [{"uri": f"{CaseParms.CFS_TEST_URL_5}"}],
        }
        url_obj_payload_5 = gen_url_obj_payload(**upd_value_5)
        resp_5 = cfsobjectapi.add_cfo_object(**url_obj_payload_5)
        upd_value_6 = {
            "name": CaseParms.URI_OBJ_NAME_6,
            "type": "uri",
            "uri": [{"uri": f"{CaseParms.CFS_TEST_URL_6}"}],
        }
        url_obj_payload_6 = gen_url_obj_payload(**upd_value_6)
        resp_6 = cfsobjectapi.add_cfo_object(**url_obj_payload_6)
        res = [resp_1, resp_2, resp_3, resp_4, resp_5, resp_6]
        logger.info(f"Add URL objects results = {res}")
        Assertion.assert_equal(all(res), True, "ERR: Add URI list object failed")

    def test_13_add_ipv6_nat_policy(self):
        logger.info("Add NAT policy for IPv6")
        output = natpolicyapi.add_nat_policy(**ipv6_nat_dict)
        Assertion.assert_equal(output, True, "ERR: add ipv6 nat policy failed")

    def test_14_add_users(self):
        users = [
            local_user_1,
            local_user_2,
            guest_user,
        ]
        add_resp = [userlocalapi.local_user(**user) for user in users]
        logger.info(f"Add users response = {add_resp}")
        get_users = userlocalapi.show_local_users()
        chk_users = [user.get("username") in json.dumps(get_users) for user in users]
        logger.info(f"Check users response = {chk_users}")
        res = bool(chk_users) and all(chk_users)
        Assertion.assert_equal(res, True, "ERR: Add users failed.")

    def test_15_add_user_group(self):
        user_gps = [user_group_1, user_group_2]
        add_resp = [userlocalapi.add_local_group(**user_gp) for user_gp in user_gps]
        logger.info(f"Add user groups response = {add_resp}")
        get_groups = userlocalapi.show_local_groups()
        chk_gps = [
            gp_name in json.dumps(get_groups)
            for gp_name in [CaseParms.USER_GROUP_1, CaseParms.USER_GROUP_2]
        ]
        logger.info(f"Check user group response = {chk_gps}")
        res = bool(chk_gps) and all(chk_gps)
        Assertion.assert_equal(res, True, "ERR: Add user groups failed.")

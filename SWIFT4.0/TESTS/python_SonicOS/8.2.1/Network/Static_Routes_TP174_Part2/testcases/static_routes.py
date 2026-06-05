from definition.settings import *
from definition.utils import *


class TestStaticRoutes_TC5(Test):
    uuid = "SOSAIOT-TC-58751"
    description = show_testcase_info(TESTPLAN, '5', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: Show Testcase Info failed")

    def test_01_edit_access_rule(self):
        output = access_rule_api.add_ipv4_access_rule(**dmz_to_lan_dict)
        Assertion.assert_equal(output, True, "ERR: Cannot Added Access Rule")

    def test_02_add_static_route(self):
        route_policy_dict["route_policies"][0]["ipv4"]["destination"]["name"] = Parameter.R_X3_NET
        route_policy_dict["route_policies"][0]["ipv4"]["gateway"]["name"] = Parameter.R_X2_IP
        rc = route_api.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(rc, True, "ERR: Add Static Route Failed")

    def test_03_verify_traffic(self):
        rc = False
        for i in range(5):
            out = PC3_HOST.send_command('ping {} -c 5'.format(PC2_ETH1_IP))
            logger.info(f'out is {out}')
            if '100% packet loss' not in out:
                rc = True
                break
            elif i == 4:
                logger.info('Ping failed')
        Assertion.assert_equal(rc, True, "ERR: Verify Traffic Failed")

    def test_04_delete_static_route(self):
        rc = route_api.del_route_policy_by_name(route_policy_dict["route_policies"][0]["ipv4"]["name"])
        Assertion.assert_equal(rc, True, "ERR: Del Static Route Failed")


class TestStaticRoutes_TC8(Test):
    uuid = "SOSAIOT-TC-58753"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: Show Testcase Info Failed")

    def test_01_config_x2_interface(self):
        logger.info("config X2 interface... ")
        rc = interface_api.config_interface(**dut_x2_wan_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 Interface Failed")

    def test_02_add_static_route(self):
        route_policy_dict["route_policies"][0]["ipv4"]["source"]["name"] = "X0 Subnet"
        route_policy_dict["route_policies"][0]["ipv4"]["destination"]["name"] = Parameter.R_X3_NET
        route_policy_dict["route_policies"][0]["ipv4"]["gateway"]["name"] = Parameter.R_X2_IP
        rc = route_api.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(rc, True, "ERR: Add Static Route Failed")

    def test_03_verify_traffic(self):
        rc = False
        for i in range(5):
            out = PC1_HOST.send_command('ping {} -c 5'.format(PC2_ETH1_IP))
            logger.info(f'out is {out}')
            if '100% packet loss' not in out:
                rc = True
                break
            elif i == 4:
                logger.info('Ping failed')
        Assertion.assert_equal(rc, True, "ERR: Verify Traffic Failed")

    def test_04_delete_static_route(self):
        rc = route_api.del_route_policy_by_name("to_remote_x3")
        Assertion.assert_equal(rc, True, "ERR: Del Static Route Failed")


class TestStaticRoutes_TC9(Test):
    uuid = "SOSAIOT-TC-58754"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: Show Testcase Info Failed")

    def test_01_add_static_route(self):
        _route_list_before_add = route_api.get_route_policy()
        CaseParams.route_list_before_add = move_priority_from_route(**_route_list_before_add)
        route_policy_dict["route_policies"][0]["ipv4"]["destination"]["name"] = Parameter.R_X3_NET
        route_policy_dict["route_policies"][0]["ipv4"]["gateway"]["name"] = Parameter.R_X2_IP
        _added_route_policy = copy.deepcopy(route_policy_dict)
        CaseParams.added_route_policy = move_priority_from_route(**_added_route_policy)
        rc = route_api.add_route_policy(**CaseParams.added_route_policy)
        Assertion.assert_equal(rc, True, "ERR: Add static Route Failed")

    def test_02_verify_route_added(self):
        logger.info('Get The Added Route Policy From FW And Compare It With Post Route Policy Content')
        verify_added_route = {}
        _route_list_after_add = route_api.get_route_policy()
        CaseParams.route_list_after_add = move_priority_from_route(**_route_list_after_add)
        try:
            for _route_policy in CaseParams.route_list_after_add['route_policies']:
                if _route_policy["ipv4"]["name"] == "to_remote_x3":
                    verify_added_route = copy.deepcopy(_route_policy["ipv4"])
            verify_added_route.pop("uuid")
        except Exception as e:
            logger.error(f"Exception happens: {e}")
        added_content = copy.deepcopy(CaseParams.added_route_policy["route_policies"][0]["ipv4"])
        Assertion.assert_equal(verify_added_route, added_content, "ERR: Add Static Route Failed")

    def test_03_all_routes_display_correct(self):
        logger.info('Get All Route Policy From FW And Compare It With The Content Added Before + Added Policies')
        expected_all_route = {}
        try:
            _fw_added_route_dis = route_api.get_route_policy_by_name("to_remote_x3")
            CaseParams.fw_added_route_dis = move_priority_from_route(**_fw_added_route_dis)
            logger.info(f'self.route_list_before_add["route_policies"]:{CaseParams.route_list_before_add["route_policies"]}')
            expected_all_route = {
                "route_policies":
                    CaseParams.route_list_before_add["route_policies"] + CaseParams.fw_added_route_dis[
                        "route_policies"]
            }
            logger.info(f"expected_all_route is {expected_all_route}")
        except Exception as e:
            logger.error(f"Exception happens: {e}")
        Assertion.assert_equal(expected_all_route, CaseParams.route_list_after_add,
                               "ERR: Add Static Route Failed")

    def test_04_edit_route_policy(self):
        route_policy_dict["route_policies"][0]["ipv4"]["service"] = {'group': 'ICMP'}
        _added_route_policy = copy.deepcopy(route_policy_dict)
        CaseParams.added_route_policy = move_priority_from_route(**_added_route_policy)
        rc = route_api.edit_route_policy("to_remote_x3", **CaseParams.added_route_policy)
        Assertion.assert_equal(rc, True, "ERR: Add Static Route Failed")

    def test_05_verify_route_edited(self):
        logger.info('Get The Edited Route Policy From FW And Compare It With Put Route Policy Content')
        verify_added_route = {}
        _route_list_after_edit = route_api.get_route_policy()
        try:
            added_content = {}
            CaseParams.route_list_after_edit = move_priority_from_route(**_route_list_after_edit)
            for _route_policy in self.route_list_after_edit['route_policies']:
                if _route_policy["ipv4"]["name"] == "to_remote_x3":
                    verify_added_route = copy.deepcopy(_route_policy["ipv4"])
            verify_added_route.pop("uuid")
            added_content = copy.deepcopy(CaseParams.added_route_policy["route_policies"][0]["ipv4"])
        except Exception as e:
            logger.error(f"Exception happens: {e}")
        Assertion.assert_equal(verify_added_route, added_content, "ERR: Add Static Route Failed")

    def test_06_all_routes_display_correct(self):
        logger.info('Get All Route Policy From FW And Compare It With '
                    'The Content Edited Before - Older Edited Policies + Newer Edited Policies')
        expected_all_route = {}
        _fw_added_route_dis = route_api.get_route_policy_by_name("to_remote_x3")
        CaseParams.fw_added_route_dis = move_priority_from_route(**_fw_added_route_dis)
        logger.info(f'self.route_list_before_add["route_policies"]:{CaseParams.route_list_before_add["route_policies"]}')
        for _route_policy in CaseParams.route_list_after_add["route_policies"]:
            if _route_policy["ipv4"]["name"] == "to_remote_x3":
                CaseParams.route_list_after_add["route_policies"].remove(_route_policy)
        try:
            expected_all_route = {
                "route_policies":
                    CaseParams.route_list_after_add["route_policies"] + CaseParams.fw_added_route_dis[
                        "route_policies"]
            }
            logger.info(f"expected_all_route is {expected_all_route}")
        except Exception as e:
            logger.error(f"Exception happens: {e}")
        Assertion.assert_equal(expected_all_route, CaseParams.route_list_after_edit,
                               "ERR: Add Static Route Failed")

    def test_07_delete_static_route(self):
        rc = route_api.del_route_policy_by_name("to_remote_x3")
        Assertion.assert_equal(rc, True, "ERR: Del Static Route Failed")

    def test_08_verify_route_deleted(self):
        logger.info('The Added Policies Is Not Founded In The Policies')
        rc = False
        _route_list_after_delete = route_api.get_route_policy()
        CaseParams.route_list_after_delete = move_priority_from_route(**_route_list_after_delete)
        for _route_policy in CaseParams.route_list_after_delete['route_policies']:
            if _route_policy["ipv4"]["name"] == "to_remote_x3":
                rc = True
                break
        Assertion.assert_equal(rc, False, "ERR: Add Static Route Failed")

    def test_09_all_routes_display_correct(self):
        logger.info('Get All Route Policy From FW And Compare It With The Content Added Before')
        Assertion.assert_equal(CaseParams.route_list_after_delete, CaseParams.route_list_before_add,
                               "ERR: Add Static Route Failed")

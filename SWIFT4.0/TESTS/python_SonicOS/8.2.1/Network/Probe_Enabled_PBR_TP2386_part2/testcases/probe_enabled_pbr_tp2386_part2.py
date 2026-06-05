import json
from definition.settings import *
from definition.utils import *


# Excepted: This case is to verify the format of the name field
class TestTC01_GUI_functionality_format_check_for_name_field(Test):
    uuid = "SOSAIOT-TC-58702"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_different_charactors_of_name(self):
        namelist = ['testPolicy', 'Test12', '!@$ 123456']
        reslist = []
        for name in namelist:
            logger.info(f'********************start to add nm policy with name {name}')
            nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
            nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = name
            logger.info(nm_dict)
            res = networkmonitorapi.add_network_monitor(**nm_dict)
            logger.info(f'res is :{res}')
            reslist.append(res)
        logger.info(f'reslist is:{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: add network monitor policy failed")

    def test_03_delete_all_nm_policies(self):
        res1 = networkmonitorapi.del_network_monitor('testPolicy', version=4)
        res2 = networkmonitorapi.del_network_monitor('Test12', version=4)
        res3 = networkmonitorapi.del_network_monitor('!@$ 123456', version=4)
        Assertion.assert_equal(res1 & res2 & res3, True, "ERR: delete network monitor policy failed")


# Excepted: This case is to verify that an object that is in use as the gateway or probe target can be edited.
class TestTC10_GUI_functionality_edit_an_object_that_is_used_by_nm_policy(Test):
    uuid = "SOSAIOT-TC-58703"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_probe_type_ping_explicit(self):
        nm_dict = copy.deepcopy(nm_ping_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'tc10_test'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True,
                               "ERR: add network monitor policy with probe type ping explicit failed")

    def test_03_edit_probe_target_host_ao_to_range_ao(self):
        edit_ao_dict = {
            "object_type": "range",
            "name": "pc2_eth1",
            "zone": "WAN",
            "value": "12.12.1.170,12.12.1.180"
        }
        res = addressobjectsapi.edit_addressobject_by_name('pc2_eth1', **edit_ao_dict)
        Assertion.assert_equal(res, True, "ERR: edit ao used by nm policy to range type failed")

    def test_04_edit_gateway_ao_host_to_another_value(self):
        edit_ao_dict = {
            "object_type": "host",
            "name": "x1_gw",
            "zone": "WAN",
            "value": "12.12.1.100"
        }
        res = addressobjectsapi.edit_addressobject_by_name('x1_gw', **edit_ao_dict)
        Assertion.assert_equal(res, True, "ERR: edit gateway host ao value used by nm policy failed")

    @repeat_method(3)
    def test_05_check_probe_target_and_gateway_value_for_nm_policy(self):
        time.sleep(30)
        output = networkmonitorapi.get_network_monitor_status_by_name('tc10_test')
        logger.info(f'output is:{output}')
        # 7.0.1
        # checklist = ['"start": "12.12.1.170"', '"end": "12.12.1.180"']
        # 7.1.1
        checklist = ['"start": "12.12.1.170"', '"end": "12.12.1.180"', '"gateway": "12.12.1.100"']
        checkres = [i in str(json.dumps(output)) for i in checklist]
        logger.info(f'option check result: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check_nm_policy failed.")

    def test_06_initial_probe_ao_and_gateway_ao(self):
        edit_ao_dict_1 = {
            "object_type": "host",
            "name": "pc2_eth1",
            "zone": "WAN",
            "value": "12.12.1.169"
        }
        edit_ao_dict_2 = {
            "object_type": "host",
            "name": "x1_gw",
            "zone": "WAN",
            "value": "12.12.1.1"
        }
        res1 = addressobjectsapi.edit_addressobject_by_name('pc2_eth1', **edit_ao_dict_1)
        res2 = addressobjectsapi.edit_addressobject_by_name('x1_gw', **edit_ao_dict_2)
        Assertion.assert_equal(res1 & res2, True, "ERR: initial probe ao and gateway ao failed.")

    def test_07_delete_nm_policy(self):
        res = networkmonitorapi.del_network_monitor('tc10_test', version=4)
        Assertion.assert_equal(res, True, "ERR: delete nm policy failed.")


# Excepted:  This case is to verify that firewall will report error when change the AO that is in use by a NM policy
# to a wrong type which is not accepted by the field.
class TestTC11_Negative_test_change_ao_used_by_nm_policy_to_a_wrong_type(Test):
    uuid = "SOSAIOT-TC-58704"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']
    error_msg = 'This address object change is not permitted by Network Monitor'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_probe_type_ping_explicit(self):
        nm_dict = copy.deepcopy(nm_ping_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'tc11_test'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True,
                               "ERR: add network monitor policy with probe type ping explicit failed")

    def test_03_edit_probe_targrt_host_ao_to_network_ao(self):
        edit_ao_dict = {
            "object_type": "network",
            "name": "pc2_eth1",
            "zone": "WAN",
            "value": "12.12.1.0,255.255.255.0"
        }
        (res, msg) = addressobjectsapi.edit_addressobject_by_name('pc2_eth1', msg=True, **edit_ao_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        Assertion.assert_regular(str(msg), self.error_msg, "ERR: edit ao used by nm policy to network type failed")

    def test_04_edit_gateway_ao_from_host_type_to_network_type(self):
        edit_ao_dict = {
            "object_type": "network",
            "name": "x1_gw",
            "zone": "WAN",
            "value": "12.12.1.0,255.255.255.0"
        }
        (res, msg) = addressobjectsapi.edit_addressobject_by_name('x1_gw', msg=True, **edit_ao_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        Assertion.assert_regular(str(msg), self.error_msg, "ERR: edit ao used by nm policy to network type failed")

    def test_05_delete_nm_policy(self):
        res = networkmonitorapi.del_network_monitor('tc11_test', version=4)
        Assertion.assert_equal(res, True, "ERR: delete nm policy failed.")


# Excepted: tcp port value out of boundary can not be accepted
class TestTC14_GUI_functionality_boundary_check_for_port_option(Test):
    uuid = "SOSAIOT-TC-58705"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_tcp_explicit_with_port_0(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'port_0'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"]["tcp"]["port"] = 0
        logger.info(f'nm_dict is {nm_dict}')
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), "property 'port' can't be empty value", "ERR:add nm policy with tcp "
                                                                                          "port 0 succeeded")

    def test_03_add_nm_policy_tcp_explicit_with_port_65536(self):
        error_msg = 'Value or string length(65536) out of bounds (min = 1, max = 65535)'
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'port_65536'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"]["tcp"]["port"] = 65536
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res}, msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        flag = True if error_msg in json.dumps(msg) else False
        Assertion.assert_equal(flag, True, "ERR:add nm policy with tcp port 65535 failed ")

    def test_04_add_nm_policy_tcp_explicit_with_port_65535(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'port_65535'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"]["tcp"]["port"] = 65535
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR:add nm policy with tcp port 65535 failed ")

    def test_05_add_nm_policy_tcp_explicit_with_port_80(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'port_80'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"]["tcp"]["port"] = 80
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR:add nm policy with tcp port 65535 failed ")

    def test_06_delete_nm_policies(self):
        res1 = networkmonitorapi.del_network_monitor('port_80', version=4)
        res2 = networkmonitorapi.del_network_monitor('port_65535', version=4)
        Assertion.assert_equal(res1 & res2, True, "ERR: delete network monitor policy failed")


# Excepted: For values other than integer, firewall will report error Data is incorrectly formatted.
class TestTC15_GUI_functionality_format_check_for_probe_parameters(Test):
    uuid = "SOSAIOT-TC-58706"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']
    error_msg = "Schema validation error: property 'port' expected: 'NUMBER', found"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_port_number_not_integer(self):
        error_msg = "Schema validation error: property 'port' expected: 'NUMBER', found"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"]["tcp"]["port"] = 'abc'
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with port not integer succeeded")

    def test_03_add_nm_policy_with_probe_interval_not_integer(self):
        error_msg = "Schema validation error: property 'interval' expected: 'NUMBER'"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = 'abc'
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with interval not integer succeeded")

    def test_04_add_nm_policy_with_reply_timeout_not_integer(self):
        error_msg = "Schema validation error: property 'reply_timeout' expected: 'NUMBER'"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["reply_timeout"] = 'abc'
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with reply timeout not integer "
                                                             "succeeded")

    def test_05_add_nm_policy_with_failure_threshold_not_integer(self):
        error_msg = "Schema validation error: property 'missed' expected: 'NUMBER'"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["missed"] = 'abc'
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with reply interval missed not integer "
                                                             "succeeded")

    def test_06_add_nm_policy_with_success_threshold_not_integer(self):
        error_msg = "Schema validation error: property 'successful' expected: 'NUMBER'"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["successful"] = 'abc'
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with successful not integer succeeded")


# Excepted:  GUI functionality-boundary check, probe interval out of boundary can not be accepted
class TestTC16_GUI_functionality_boundary_check_for_probe_interval(Test):
    uuid = "SOSAIOT-TC-58707"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_probe_interval_0(self):
        error_msg = "Schema validation error: property 'interval' can't be empty value"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_interval_0'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = 0
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with interval 0 succeeded")

    def test_03_add_nm_policy_with_probe_interval_9999(self):
        error_msg = "Value or string length(9999) out of bounds (min = 1, max = 3600)"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_interval_9999'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = 9999
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        flag = True if error_msg in json.dumps(msg) else False
        Assertion.assert_equal(flag, True, "ERR:add nm policy with interval 9999 succeeded")

    def test_04_add_nm_policy_with_probe_interval_60(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_interval_60'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = 60
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with interval 60 failed")

    def test_05_add_nm_policy_with_probe_interval_1(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_interval_1'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = 1
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with interval 1 failed")

    def test_06_add_nm_policy_with_probe_interval_3600(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_interval_3600'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = 3600
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with interval 3600 failed")

    def test_07_delete_nm_policies(self):
        res1 = networkmonitorapi.del_network_monitor('probe_interval_60', version=4)
        res2 = networkmonitorapi.del_network_monitor('probe_interval_1', version=4)
        res3 = networkmonitorapi.del_network_monitor('probe_interval_3600', version=4)
        logger.info(f'res1 is:{res1},res2 is:{res2},res3 is:{res3}')
        Assertion.assert_equal(res1 & res2 & res3, True, "ERR: delete network monitor policy failed")


# Excepted:  GUI functionality-boundary check, reply timeout out of boundary can not be accepted
class TestTC17_GUI_functionality_boundary_check_for_reply_timeout(Test):
    uuid = "SOSAIOT-TC-58708"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_reply_timeout_0(self):
        error_msg = "Schema validation error: property 'reply_timeout' can't be empty value"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'reply_timeout_0'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["reply_timeout"] = 0
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with reply timeout 0 succeeded")

    def test_03_add_nm_policy_with_reply_timeout_10(self):
        error_msg = "The probe interval must be greater than the reply timeout"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'reply_timeout_10'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["reply_timeout"] = 10
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with reply timeout 10 succeeded")

    def test_04_add_nm_policy_with_reply_timeout_3(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'reply_timeout_3'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["reply_timeout"] = 3
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with reply timeout 3 failed")

    def test_05_add_nm_policy_with_reply_timeout_1(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'reply_timeout_1'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["reply_timeout"] = 1
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with reply timeout 1 failed")

    def test_06_add_nm_policy_with_reply_timeout_60_and_probe_interval_100(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'reply_timeout_60'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = 100
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["reply_timeout"] = 60
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with reply timeout 60 and probe interval 100 failed")

    def test_07_add_nm_policy_with_reply_timeout_80_and_probe_interval_80(self):
        error_msg = "Value or string length(80) out of bounds (min = 1, max = 60)"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'reply_timeout_80'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = 100
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["reply_timeout"] = 80
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        flag = True if error_msg in json.dumps(msg) else False
        Assertion.assert_equal(flag, True, "ERR:add nm policy with reply timeout 80 and probe "
                                           "interval 100 succeeded")

    def test_08_delete_nm_policies(self):
        res1 = networkmonitorapi.del_network_monitor('reply_timeout_3', version=4)
        res2 = networkmonitorapi.del_network_monitor('reply_timeout_1', version=4)
        res3 = networkmonitorapi.del_network_monitor('reply_timeout_60', version=4)
        logger.info(f'res1 is:{res1},res2 is:{res2},res3 is:{res3}')
        Assertion.assert_equal(res1 & res2 & res3, True, "ERR: delete network monitor policy failed")


# Excepted:  GUI functionality-boundary check, failure threshold out of boundary can not be accepted
class TestTC18_GUI_functionality_boundary_check_for_failure_threshold(Test):
    uuid = "SOSAIOT-TC-58709"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_tcp_explicit_with_failure_threshold_0(self):
        error_msg = "Schema validation error: property 'missed' can't be empty value"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'failure_threshold_0'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["missed"] = 0
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with missed 0 succeeded")

    def test_03_add_nm_policy_tcp_explicit_with_failure_threshold_200(self):
        error_msg = "Value or string length(200) out of bounds (min = 1, max = 100)"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'failure_threshold_200'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["missed"] = 200
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        flag = True if error_msg in json.dumps(msg) else False
        Assertion.assert_equal(flag, True, "ERR:add nm policy with missed 200 succeeded")

    def test_04_add_nm_policy_tcp_explicit_with_failure_threshold_1(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'failure_threshold_1'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["missed"] = 1
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with missed 1 failed")

    def test_05_add_nm_policy_tcp_explicit_with_failure_threshold_100(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'failure_threshold_100'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["missed"] = 100
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with missed 1 failed")

    def test_06_delete_nm_policies(self):
        res1 = networkmonitorapi.del_network_monitor('failure_threshold_1', version=4)
        res2 = networkmonitorapi.del_network_monitor('failure_threshold_100', version=4)
        logger.info(f'res1 is:{res1},res2 is:{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: delete network monitor policy failed")


# Excepted:  GUI functionality-boundary check, success threshold out of boundary can not be accepted
class TestTC19_GUI_functionality_boundary_check_for_success_threshold(Test):
    uuid = "SOSAIOT-TC-58710"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_tcp_explicit_with_success_threshold_0(self):
        error_msg = "Schema validation error: property 'successful' can't be empty value"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'success_threshold_0'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["successful"] = 0
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with successful 0 succeeded")

    def test_03_add_nm_policy_tcp_explicit_with_success_threshold_200(self):
        error_msg = "Value or string length(200) out of bounds (min = 1, max = 100)"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'success_threshold_200'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["successful"] = 200
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        flag = True if error_msg in json.dumps(msg) else False
        Assertion.assert_equal(flag, True, "ERR:add nm policy with successful 200 succeeded")

    def test_04_add_nm_policy_tcp_explicit_with_success_threshold_1(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'success_threshold_1'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["successful"] = 1
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with successful 1 succeeded")

    def test_05_add_nm_policy_tcp_explicit_with_success_threshold_100(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'success_threshold_100'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["interval"]["successful"] = 100
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_equal(res, True, "ERR:add nm policy with successful 100 succeeded")

    def test_06_delete_nm_policies(self):
        res1 = networkmonitorapi.del_network_monitor('success_threshold_1', version=4)
        res2 = networkmonitorapi.del_network_monitor('success_threshold_100', version=4)
        logger.info(f'res1 is:{res1},res2 is:{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: delete network monitor policy failed")


# Excepted: GUI functionality - Empty Name is not allowed.
class TestTC02_GUI_functionality_empty_name_is_not_allowed(Test):
    uuid = "SOSAIOT-TC-58711"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_empty_name(self):
        error_msg = "Schema validation error: property 'name' can't be empty value"
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = ''
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        logger.info(f'json.dumps(msg) is:{json.dumps(msg)}')
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR:add nm policy with empty name succeeded")


# Excepted: GUI functionality - All must respond option can be checked/unchecked.
class TestTC20_GUI_functionality_all_must_respond_option_test(Test):
    uuid = "SOSAIOT-TC-58712"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_must_response_checked(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'test_all_hosts_must_response_option'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"]["name"] = "range_ao"
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["must_respond"] = True
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')

    def test_03_check_must_response_value_in_tsr(self):
        flag = False
        output = diagnosticapi.get_tsr_part2('Network : Network Monitor')
        logger.info(f'output is:{output}')
        nmlist = output.split('\n\n')
        for list in nmlist:
            logger.info(list)
            if "test_all_hosts_must_response_option" in list:
                flag = True if "allHostsMustRespond     : 1" in list else False
        Assertion.assert_equal(flag, True, "ERR: check must response option in tsr failed")

    def test_04_edit_nm_policy_with_must_response_unchecked(self):
        nm_dict = {
            "nm_name": "test_all_hosts_must_response_option",
            "probe_type": "ping_non_explicit",
            "probe_target": {"name": "range_ao"},
            "must_respond": False
        }
        res = networkmonitorapi.edit_network_monitor_ipv4(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: uncheck all hosts must response option for nm policy failed")

    def test_05_delete_nm_policies(self):
        res = networkmonitorapi.del_network_monitor('test_all_hosts_must_response_option', version=4)
        logger.info(f'res is:{res}')
        Assertion.assert_equal(res, True, "ERR: delete network monitor policy failed")


# Excepted: GUI functionality -comments can be displayed correctly
class TestTC21_GUI_functionality_comment_field(Test):
    uuid = "SOSAIOT-TC-58713"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_comment_and_check_comment(self):
        flag = False
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'test_comment'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["comment"] = 'test_comment'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        if res:
            output = networkmonitorapi.get_network_monitor(name="test_comment")
            logger.info(f'output is :{output}')
            flag = True if '"comment": "test_comment"' in json.dumps(output) else False
        else:
            logger.error('add nm policy with comment failed')
        Assertion.assert_equal(flag, True, "ERR: add nm policy with comment failed")

    def test_03_delete_nm_policy(self):
        res = networkmonitorapi.del_network_monitor('test_comment', version=4)
        logger.info(f'res is:{res}')
        Assertion.assert_equal(res, True, "ERR: delete network monitor policy failed")


# Excepted: Button functionality- Delete all NM policies.
class TestTC25_Button_functionality_delete_all_nm_policies(Test):
    uuid = "SOSAIOT-TC-58717"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_multiple_nm_policies(self):
        reslist = []
        nm_list = [{'nm_name': 'test_delete_1',
                    'probe_name': 'pc2_eth1'},
                   {'nm_name': 'test_delete_2',
                    'probe_name': 'pc2_eth2'},
                   {'nm_name': 'test_delete_3',
                    'probe_name': 'pc3_eth1'},
                   {'nm_name': 'test_delete_4',
                    'probe_name': 'range_ao'}]
        for nm in nm_list:
            nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
            nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = nm["nm_name"]
            nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"]["name"] = nm["probe_name"]
            res = networkmonitorapi.add_network_monitor(**nm_dict)
            reslist.append(res)
        logger.info(f'reslist is:{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: add multiple nm policies failed")

    def test_03_delete_all_nm_policies(self):
        reslist = []
        nm_name_list = ['test_delete_1', 'test_delete_2', 'test_delete_3', 'test_delete_4']
        for nm_name in nm_name_list:
            res = networkmonitorapi.del_network_monitor(nm_name, version=4)
            reslist.append(res)
        Assertion.assert_equal(all(reslist), True, "ERR: delete all nm policies failed")


# Excepted: Negative test - Delete a policy that is in use by a route.
class TestTC26_Negative_test_delete_nm_policy_used_by_route(Test):
    uuid = "SOSAIOT-TC-58718"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'nm_ping_non_explicit'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add nm policy failed")

    def test_03_add_route_policy_with_probe_selected(self):
        res = routepolicyapi.add_route_policy(**route_policy_with_probe_dict)
        Assertion.assert_equal(res, True, "ERR: add route policy with probe selected failed")

    def test_04_delete_nm_policy_used_by_route_policy(self):
        (res, msg) = networkmonitorapi.del_network_monitor('nm_ping_non_explicit', version=4, msg=True)
        logger.info(f'res is:{res},msg is:{msg}')
        flag = True if 'Object is in use by a Route Policy' in str(msg) and 'Probe entry cannot be deleted' in str(
            msg) else False
        Assertion.assert_equal(flag, True, "ERR: delete nm policy successfully")

    def test_05_delete_route_policy(self):
        res = routepolicyapi.del_route_policy_by_name('pbr_with_probe', version='v4')
        Assertion.assert_equal(res, True, "ERR: delete route policy failed")


# Excepted: Button functionality- Clear statistics.
class TestTC27_Button_functionality_clear_statistics(Test):
    uuid = "SOSAIOT-TC-58719"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    @repeat_method(3)
    def test_02_get_nm_policy_status(self):
        time.sleep(30)
        flag = False
        output1 = networkmonitorapi.get_network_monitor_status_by_name('nm_ping_non_explicit')
        logger.info(f'output1 is:{output1}')
        if output1["netMonProbeStatus"]:
            probestatus1 = output1["netMonProbeStatus"]["probeStatus"]
            resolvedprobetargets1 = output1["netMonProbeStatus"]["resolvedProbeTargets"]
            probessent1 = output1["netMonProbeStatus"]["probesSent"]
            responsesreceived1 = output1["netMonProbeStatus"]["responsesReceived"]
            targetarray1_ip = output1["netMonProbeStatus"]["targetArray"][0]["targets"]["ip"]
            targetarray1_status = output1["netMonProbeStatus"]['targetArray'][0]["targets"]["status"]
            logger.info(f'probestatus1 is :{probestatus1}')
            logger.info(f'resolvedprobetargets1 is :{resolvedprobetargets1}')
            logger.info(f'probessent1 is:{probessent1}')
            logger.info(f'responsesreceived1 is:{responsesreceived1}')
            logger.info(f'targetarray1_ip is:{targetarray1_ip}')
            logger.info(f'targetarray1_status is:{targetarray1_status}')
            if probestatus1 and resolvedprobetargets1 and probessent1 and responsesreceived1 and targetarray1_ip == '193.168.1.20' and targetarray1_status == 'UP':
                res = networkmonitorapi.clear_network_monitor_statistics()
                if res:
                    output2 = networkmonitorapi.get_network_monitor_status_by_name('nm_ping_non_explicit')
                    logger.info(f'output2 is:{output2}')
                    probestatus2 = output2["netMonProbeStatus"]["probeStatus"]
                    resolvedprobetargets2 = output1["netMonProbeStatus"]["resolvedProbeTargets"]
                    probessent2 = output2["netMonProbeStatus"]["probesSent"]
                    responsesreceived2 = output2["netMonProbeStatus"]["responsesReceived"]
                    logger.info(f'probestatus2 is :{probestatus2}')
                    logger.info(f'resolvedprobetargets2 is :{resolvedprobetargets2}')
                    logger.info(f'probessent2 is:{probessent2}')
                    logger.info(f'responsesreceived2 is:{responsesreceived2}')
                    if '0' in probestatus2 and resolvedprobetargets2 == 1 and probessent2 == 0 and responsesreceived2 == 0:
                        flag = True
                else:
                    logger.error('do clear statistics failed')
        Assertion.assert_equal(flag, True, "ERR: clear statistics failed")

    def test_03_delete_nm_policy(self):
        res = networkmonitorapi.del_network_monitor('nm_ping_non_explicit', version=4)
        Assertion.assert_equal(res, True, "ERR:delete nm policy failed")


# Excepted:This case is to verify each NM policy must be given a unique name.
class TestTC03_GUI_functionality_Policy_name_must_be_unique(Test):
    uuid = "SOSAIOT-TC-58720"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_first_nm_policy_with_name_test_name_unique(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'test_name_unique'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add nm policy failed")

    def test_03_add_second_nm_policy_with_name_test_name_unique(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'test_name_unique'
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        Assertion.assert_regular(str(msg), 'Already exists', "ERR: add nm policy with same name failed")

    def test_04_delete_nm_policies(self):
        res = networkmonitorapi.del_network_monitor('test_name_unique', version=4)
        logger.info(f'res is:{res}')
        Assertion.assert_equal(res, True, "ERR: delete network monitor policy failed")


# Excepted: This case is to verify max 32 characters can be entered in the Name field.
class TestTC04_GUI_functionality_max_length_of_the_name_field(Test):
    uuid = "SOSAIOT-TC-58728"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']
    nm_policy_name = '01234567890123456789012345678901234567890123456789012345789'
    nm_policy_name_32 = '0123456789012345678901'
    jira = "GEN7-47223"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_name_length_more_than_32_characters(self):
        flag = False
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = self.nm_policy_name
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        if res:
            output = networkmonitorapi.get_network_monitor_status_by_name(self.nm_policy_name)
            flag = True if not output else False
        Assertion.assert_equal(flag, True, "ERR: check nm policy with name length more then 32 failed")


# Excepted: This case is to verify Interface option should be disabled when select Ping or TCP probe.
class TestTC08_GUI_functionality_Gateway_and_interface_can_be_specified(Test):
    uuid = "SOSAIOT-TC-58744"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_probe_type_ping_explicit(self):
        nm_dict = copy.deepcopy(nm_ping_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'tc08_test'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy failed")

    def test_03_delete_network_monitot_policy(self):
        res = networkmonitorapi.del_network_monitor('tc08_test', version=4)
        Assertion.assert_equal(res, True, "ERR: delete network monitor policy failed")


# Excepted: This case is to verify object can not be deleted when its selected as the Gateway or probe target.
class TestTC09_GUI_functionality_Delete_an_object_used_by_nm_policy(Test):
    uuid = "SOSAIOT-TC-58745"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']
    error_msg = 'Object is in use by a Network Monitor policy'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_probe_type_ping_explicit(self):
        nm_dict = copy.deepcopy(nm_ping_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'tc09_test'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {"name": "pc2_eth1"}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["next_hop"] = {"name": "x1_gw"}
        logger.info(f'nm_dict is :{nm_dict}')
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy failed")

    def test_03_delete_probe_target(self):
        addressobj_del = {
            'ip_type': 'ipv4',
            'name': 'pc2_eth1',
        }
        (res, msg) = addressobjectsapi.del_addressobject(msg=True, **addressobj_del)
        logger.info(f'res is:{res},msg is:{msg}')
        Assertion.assert_regular(str(msg), self.error_msg, "ERR: delete ao used by nm policy failed")

    def test_04_delete_probe_target(self):
        addressobj_del = {
            'ip_type': 'ipv4',
            'name': 'x1_gw',
        }
        (res, msg) = addressobjectsapi.del_addressobject(msg=True, **addressobj_del)
        logger.info(f'res is:{res},msg is:{msg}')
        Assertion.assert_regular(str(msg), self.error_msg, "ERR: delete ao used by nm policy failed")

    def test_05_delete_network_monitot_policy(self):
        res = networkmonitorapi.del_network_monitor('tc09_test', version=4)
        Assertion.assert_equal(res, True, "ERR: delete network monitor policy failed")


# Excepted:This case is to verify delete or delete all button only take effects for custom policies.
class TestTC31_Auto_added_policies_can_not_be_deleted(Test):
    uuid = "SOSAIOT-TC-58722"
    description = show_testcase_info(TESTPLAN, '31', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_x0_range(self):
        x0_range_dict = {
            "object_type": "range",
            "name": "x0_range",
            "zone": "LAN",
            "value": "192.168.168.9,192.168.168.11"
        }
        res = addressobjectsapi.config_addressobject(**x0_range_dict)
        Assertion.assert_equal(res, True, "ERR: Failed to add x0 range ao")

    def test_03_add_nat_policy_with_probe(self):
        res = natpolicyapi.add_nat_policy(**add_nat_policy_with_probe_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR:add nat policy with probe failed")

    @repeat_method(2)
    def test_04_delete_auto_added_policy(self):
        time.sleep(30)
        error_msg_1 = "'NAT PROBE3' not a reasonable value"
        error_msg_2 = 'no network-monitor policy \\"NAT PROBE3\\"\' does not match'
        output = networkmonitorapi.get_network_monitor_status()
        logger.info(f'output is:{output}')
        (res, msg) = networkmonitorapi.del_network_monitor('NAT PROBE3', version=4, msg=True)
        logger.info(f'res is:{res},msg is :{msg}')
        flag = True if error_msg_1 in str(msg) or error_msg_2 in json.dumps(msg) else False
        Assertion.assert_equal(flag, True, "ERR:delete nat policy with probe successfully")


# Excepted:Auto-added policies can be edited through Advanced settings of NAT policy.
class TestTC32_Auto_added_nm_policies_can_be_edited_through_nat_policy(Test):
    uuid = "SOSAIOT-TC-58723"
    description = show_testcase_info(TESTPLAN, '32', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_auto_added_nm_policy_status(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name('NAT PROBE1')
        logger.info(f'output is:{output}')
        res = True if 'green' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check nm status failed")

    def test_03_edit_nat_policy_and_check_auto_added_nm_policy_changes(self):
        flag = False
        res = natpolicyapi.edit_nat_policy_by_name('nat_policy_with_probe', version='v4',
                                                   **edit_nat_policy_with_probe_dict)
        logger.info(f'res is :{res}')
        if res:
            nmstatus = networkmonitorapi.get_network_monitor_status_by_name('NAT PROBE2')
            logger.info(f'yellow is {nmstatus}')
            if nmstatus:
                if 'yellow' in str(nmstatus):
                    flag = True
            else:
                logger.info("didn't get auto added nm policy")
        else:
            logger.info('edit nat policy failed')
        Assertion.assert_equal(flag, True, "ERR: edit nat policy and check auto added nm policy failed")


# Excepted:This case is to verify NAT probe policies will be deleted if enable probing is disabled on advanced NAT
class TestTC33_Auto_added_nm_policies_can_be_deleted_through_nat_policy(Test):
    uuid = "SOSAIOT-TC-58724"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_edit_nat_policy_with_probe_disabled(self):
        nat_dict = copy.deepcopy(edit_nat_policy_with_probe_dict)
        nat_dict["nat_policies"][0]["ipv4"]["high_availability"] = {"probing": {}}
        logger.info(f'nat_dict is:{nat_dict}')
        res = natpolicyapi.edit_nat_policy_by_name('nat_policy_with_probe', version='v4', **nat_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: edit nat policy with probe disabled failed")

    def test_03_check_auto_added_nm_policy_if_auto_deleted(self):
        output = networkmonitorapi.get_network_monitor_status_by_name('NAT PROBE2')
        logger.info(f'output is :{output}')
        flag = True if not output else False
        Assertion.assert_equal(flag, True, "ERR: check auto added nm policy failed")


# Excepted: probe target of Host type works fine
class TestTC42_Probe_target_of_host_type(Test):
    uuid = "SOSAIOT-TC-58731"
    description = show_testcase_info(TESTPLAN, '42', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_monitot_policy_and_check_nm_up(self):
        nm_update = {
            "name": 'nm_probe_hostao'
        }
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"].update(nm_update)
        res = add_nm_and_check_nm_status(networkmonitorapi, **nm_dict)
        Assertion.assert_equal(res, True,
                               "ERR: add network monitor policy with probe hostao and check nm status failed")

    def test_03_disconnect_probe_target(self):
        res = PC2_Login.send_commands(['ifconfig eth2 down', 'ifconfig'])
        Assertion.assert_not_regular(res, PC2_ETH2_IP, "ERR: disconnect probe target failed")

    def test_04_check_nm_down(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name('nm_probe_hostao')
        res = True if 'red' in str(output) and 'DOWN' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check new network monitor status failed")

    def test_05_connect_probe_target(self):
        res = PC2_Login.send_commands(['ifconfig eth2 up', 'ifconfig'])
        time.sleep(5)
        Assertion.assert_regular(res, PC2_ETH2_IP, "ERR: connect probe target failed")

    def test_06_delete_nm_policy(self):
        res = networkmonitorapi.del_network_monitor('nm_probe_hostao', version=4)
        Assertion.assert_equal(res, True, "ERR:delete nm policy successfully")


# Excepted: probe target of Range type works fine
class TestTC43_probe_target_of_range_type(Test):
    uuid = "SOSAIOT-TC-58732"
    description = show_testcase_info(TESTPLAN, '43', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_monitor_policy(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {'name': 'range_ao'}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_rangeao'
        res = add_nm_and_check_nm_status(networkmonitorapi, **nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy with probe rangeao")

    def test_03_disconnect_engress_interface_x2(self):
        res = interfacev4api.disable_interface(name='X2')
        Assertion.assert_equal(res, True, "ERR: disable interface X2 failed")

    def test_04_check_nm_down(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name('probe_rangeao')
        res = True if 'red' in str(output) and 'DOWN' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check new network monitor status failed")

    def test_05_connect_engress_interface_x2(self):
        res = interfacev4api.enable_interface(name='X2')
        Assertion.assert_equal(res, True, "ERR: enable interface X2 failed")

    def test_06_delete_nm_policy(self):
        res = networkmonitorapi.del_network_monitor('probe_rangeao', version=4)
        Assertion.assert_equal(res, True, "ERR:delete nm policy successfully")


# Excepted: probe target of FQDN type works fine
class TestTC44_Probe_target_of_FQDN_type(Test):
    uuid = "SOSAIOT-TC-58733"
    description = show_testcase_info(TESTPLAN, '44', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_probe_target_with_fqdn_ao(self):
        probe_object_dict = {
            "object_type": "fqdn",
            "name": "fqdn_ao",
            "zone": "WAN",
            "value": "www.baidu.com"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe FQDN address object failed")

    def test_03_add_network_monitot_policy(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {'name': 'fqdn_ao'}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_fqdnao'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy with probe FQDN ao failed")

    @repeat_method(10)
    def test_04_check_nm_up(self):
        time.sleep(30)
        output = networkmonitorapi.get_network_monitor_status_by_name('probe_fqdnao')
        res = True if 'green' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")


# Excepted: This case is to verify Group object(host, range, or FQDN objects only) can be probed successfully.
class TestTC45_Probe_target_of_group_type(Test):
    uuid = "SOSAIOT-TC-58734"
    description = show_testcase_info(TESTPLAN, '45', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '45')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_monitot_policy(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {'group': 'lanprobgroup'}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_groupao'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy with probe group ao failed")

    @repeat_method(2)
    def test_03_check_nm_up(self):
        time.sleep(30)
        output = networkmonitorapi.get_network_monitor_status_by_name('probe_groupao')
        res = True if 'green' in str(output) and '2 Up' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")

    def test_04_disconnect_probe_target_pc3_eth1(self):
        res = PC3_Login.send_commands(['ifconfig eth1 down', 'ifconfig'])
        Assertion.assert_not_regular(res, PC3_ETH1_IP, "ERR: disconnect probe target failed")

    def test_05_check_nm_up_if_one_member_down(self):
        time.sleep(30)
        output = networkmonitorapi.get_network_monitor_status_by_name('probe_groupao')
        res = True if 'green' in str(output) and '1 Up' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")

    def test_06_connect_probe_target_pc3_eth1(self):
        res = PC3_Login.send_commands(['ifconfig eth1 up', 'ifconfig'])
        Assertion.assert_regular(res, PC3_ETH1_IP, "ERR: disconnect probe target failed")


# Excepted:  This case is to verify the function of All hosts must respond.
class TestTC47_Functional_test_for_option_all_hosts_must_respond(Test):
    uuid = "SOSAIOT-TC-58735"
    description = show_testcase_info(TESTPLAN, '47', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '47')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_must_response_checked(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'test_all_hosts_must_response_option'
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {'group': 'lanprobgroup'}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["must_respond"] = True
        (res, msg) = networkmonitorapi.add_network_monitor(msg=True, **nm_dict)
        logger.info(f'res is:{res},msg is:{msg}')

    @repeat_method(2)
    def test_03_check_nm_up(self):
        time.sleep(30)
        output = networkmonitorapi.get_network_monitor_status_by_name('test_all_hosts_must_response_option')
        res = True if 'green' in str(output) and '2 Up' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")

    def test_04_disconnect_probe_target_pc3_eth1(self):
        res = PC3_Login.send_commands(['ifconfig eth1 down', 'ifconfig'])
        Assertion.assert_not_regular(res, PC3_ETH1_IP, "ERR: disconnect probe target failed")

    def test_05_check_nm_up_if_one_member_down(self):
        time.sleep(30)
        output = networkmonitorapi.get_network_monitor_status_by_name('test_all_hosts_must_response_option')
        res = True if 'red' in str(output) and '1 Up' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")

    def test_06_connect_probe_target_pc3_eth1(self):
        res = PC3_Login.send_commands(['ifconfig eth1 up', 'ifconfig'])
        Assertion.assert_regular(res, PC3_ETH1_IP, "ERR: disconnect probe target failed")


# Excepted: The NM policy can be added successfully and selected as the probe policy of the route.
class TestTC57_Add_network_monitor_policy(Test):
    uuid = "SOSAIOT-TC-58738"
    description = show_testcase_info(TESTPLAN, '57', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '57')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_monitot_policy(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'nm_ping_non_explicit'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy failed")


# Excepted: This case is to verify the static route will be disabled when the probe policy is up
class TestTC58_Functional_test_for_option_disable_route_when_probe_succeeds(Test):
    uuid = "SOSAIOT-TC-58739"
    description = show_testcase_info(TESTPLAN, '58', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '58')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_route_policy_with_probe_selected(self):
        res = routepolicyapi.add_route_policy(**route_policy_with_probe_dict)
        logger.info(f'res is {res}')
        Assertion.assert_equal(res, True, "ERR: add route policy with probe and check its status failed")

    @repeat_method(3)
    def test_03_check_route_policy_status_if_down(self):
        time.sleep(30)
        output1 = networkmonitorapi.get_network_monitor_status_by_name('nm_ping_non_explicit')
        output2 = routepolicyapi.get_route_policy_status(name='pbr_with_probe')
        logger.info(f'output1 is:{output1},output2 is:{output2}')
        flag = True if 'green' in str(output1) and output2 == '0' else False
        Assertion.assert_equal(flag, True, "ERR: check route policy status failed")

    def test_04_disconnect_probe_target_pc2_eth2(self):
        res = PC2_Login.send_commands(['ifconfig eth2 down', 'ifconfig'])
        Assertion.assert_not_regular(res, PC2_ETH2_IP, "ERR: disconnect probe target failed")

    @repeat_method(3)
    def test_05_check_route_policy_status_if_up(self):
        time.sleep(30)
        output1 = networkmonitorapi.get_network_monitor_status_by_name('nm_ping_non_explicit')
        output2 = routepolicyapi.get_route_policy_status('pbr_with_probe')
        logger.info(f'output1 is:{output1},output2 is:{output2}')
        flag = True if 'red' in str(output1) and output2 == '1' else False
        Assertion.assert_equal(flag, True, "ERR: check route policy status failed")

    def test_06_connect_probe_target_pc2_eth2(self):
        res = PC2_Login.send_commands(['ifconfig eth2 up', 'ifconfig'])
        time.sleep(30)
        Assertion.assert_regular(res, PC2_ETH2_IP, "ERR: connect probe target failed")

    def test_07_delete_route_policy(self):
        res = routepolicyapi.del_route_policy_by_name('pbr_with_probe', version='v4')
        Assertion.assert_equal(res, True, "ERR: delete route policy failed")


# Excepted: This case is to verify the static route with an unknown status policy should be active
# when option Probe default state is up is selected.
class TestTC59_Functional_test_for_option_probe_default_state_is_up(Test):
    uuid = "SOSAIOT-TC-58740"
    description = show_testcase_info(TESTPLAN, '59', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '59')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_route_policy_with_probe_selected_and_check_status(self):
        update_dict = {
            "disable_when_probes_succeed": False,
            "default_probe_state_up": True,
        }
        route_dict = copy.deepcopy(route_policy_with_probe_dict)
        route_dict["route_policies"][0]["ipv4"].update(update_dict)
        logger.info(f'route_dict is:{route_dict}')
        res = routepolicyapi.add_route_policy(**route_dict)
        Assertion.assert_equal(res, True, "ERR: add route policy with probe and check its status failed")

    @repeat_method(3)
    def test_03_check_route_policy_status_if_up(self):
        output1 = networkmonitorapi.get_network_monitor_status_by_name('nm_ping_non_explicit')
        output2 = routepolicyapi.get_route_policy_status(name='pbr_with_probe')
        logger.info(f'output1 is:{output1},output2 is:{output2}')
        flag = True if 'green' in str(output1) and output2 == '1' else False
        Assertion.assert_equal(flag, True, "ERR: check route policy status failed")

    def test_04_edit_nm_policy_and_make_to_unknown_state(self):
        nm_dict = {
            "nm_name": "nm_ping_non_explicit",
            "probe_type": "ping_non_explicit",
            "probe_target": {"name": "x2_unreacheable_host"},
        }
        logger.info(f'nm_dict is:{nm_dict}')
        res = networkmonitorapi.edit_network_monitor_ipv4(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: edit nm policy failed")

    def test_05_check_route_policy_status_if_up_when_probe_default_state_is_up_option_selected(self):
        output1 = networkmonitorapi.get_network_monitor_status_by_name('nm_ping_non_explicit')
        output2 = routepolicyapi.get_route_policy_status('pbr_with_probe')
        logger.info(f'output1 is:{output1},output2 is:{output2}')
        flag = True if 'yellow' in str(output1) and output2 == '1' else False
        Assertion.assert_equal(flag, True, "ERR: check route policy status failed")

    def test_06_delete_route_policy(self):
        res = routepolicyapi.del_route_policy_by_name('pbr_with_probe', version='v4')
        Assertion.assert_equal(res, True, "ERR: delete route policy failed")


# Excepted: NM policies and pbr can be added and showed in cli
class TestTC72_Add_nm_policy_in_cli(Test):
    uuid = "SOSAIOT-TC-58743"
    description = show_testcase_info(TESTPLAN, '72', description=True)['title']
    nm_policy_name = 'nm_ipv4_added_by_cli'
    pbr_name = 'route_ipv4_added_by_cli'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '72')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_in_cli(self):
        nm_tcp_opt = {
            'name': self.nm_policy_name,
            'probe-target': 'name "pc2_eth1"',
            'outbound-interface': 'X1',
            'next-hop': 'name "X1 Default Gateway"',
            'probe-type': 'tcp explicit',  # tcp,tcp explicit,ping,ping explicit
            'port': '100',
            'intervel': 5,
            'reply-timeout': 2,
            'down-after': 6,
            'up-after': 7,
            'must-respond': True,
            'rst-as-miss': True,
        }
        res = networkmonitorcli.add_nm_policy(**nm_tcp_opt)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy in cli failed")

    def test_03_add_route_policy_with_probe_selected_in_cli(self):
        routepolicy = {
            'if': 'X1',
            'metric': 20,
            'source': 'any',  # any,group,host,name,network,range
            'destination': 'name "10.103.202.200"',
            'name': self.pbr_name,
            'probe': self.nm_policy_name,
        }
        res = routecli.add_route_policy(**routepolicy)
        Assertion.assert_equal(res, True, "ERR: add route policy in cli failed")

    def test_04_check_nm_policy_in_cli(self):
        output = networkmonitorcli.show_nm_policy(name='nm_ipv4_added_by_cli', version='ipv4')
        Assertion.assert_regular(output, self.nm_policy_name, "ERR: check nm policy added in cli failed")

    def test_05_check_route_policy_with_probe_selected_in_cli(self):
        output = routecli.show_route_policy_by_name(version='ipv4', name='route_ipv4_added_by_cli')
        Assertion.assert_regular(output, self.pbr_name, "ERR: check route policy in cli failed")

    def test_06_delete_network_monitot_policy_and_nm_policy(self):
        res1 = routepolicyapi.del_route_policy_by_name('route_ipv4_added_by_cli')
        res2 = networkmonitorapi.del_network_monitor('nm_ipv4_added_by_cli', version=4)
        Assertion.assert_equal(res1 & res2, True, "ERR: delete network monitor policy and nm policy failed")

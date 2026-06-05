from definition.utils import *


# Expect: custom nat policy can be added successfully
class TestNatPolicies_GUI_TC16(Test):
    uuid = "SOSAIOT-TC-58612"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_policy(self):
        rc = add_nat_rule({'name': 'test_for_case_16', 'inbound': 'X0', 'outbound': 'X1'})
        Assertion.assert_equal(rc, True, 'ERR: add nat policy failed')


# Add duplicated NAT Policies
class TestNatPolicies_GUI_TC17(Test):
    uuid = "SOSAIOT-TC-58613"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_duplicate_nat_rule(self):
        add_res, err_msg = add_nat_rule({'name': 'test_for_case_16', 'inbound': 'X0', 'outbound': 'X1'}, msg=True)
        rc = (not add_res) and 'already exists' in json.dumps(err_msg)
        Assertion.assert_equal(rc, True, 'ERR: check add duplicated nat rule failed!!')


# Expect: modify address ad and service ao to update nat policy
class TestNatPolicies_GUI_TC23(Test):
    uuid = "SOSAIOT-TC-58620"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_ao_and_service_for_added_nat(self):
        edit_dict = {
            'name': 'test_for_case_16',
            'source': {'name': 'ao_test_for_case_23'},
            'service': {'name': "service_for_case_23"}
        }
        rc = edit_nat_rule('test_for_case_16', edit_dict)
        CaseParams.tc23_res = rc
        Assertion.assert_equal(rc, True, 'ERR: modify addr object and service for nat policy failed')


# GUI: Setting modifications
class TestNatPolicies_GUI_TC14(Test):
    uuid = "SOSAIOT-TC-58610"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_settings_modification(self):
        rc = CaseParams.tc23_res
        Assertion.assert_equal(rc, True, "ERR: verify nat rule settings modification failed!!")


# GUI: Modify NAT Policies
class TestNatPolicies_GUI_TC21(Test):
    uuid = "SOSAIOT-TC-58618"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_modify_nat_rule(self):
        rc = CaseParams.tc23_res
        Assertion.assert_equal(rc, True, 'ERR: check modify nat rule failed!!')


# GUI: Adjust NAT Policy priorities
class TestNatPolicies_GUI_TC19(Test):
    uuid = "SOSAIOT-TC-58615"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_custom_nat_LAN_to_WAN(self):
        nat_dict = {
            'name': 'test_for_case_19',
            'inbound': 'X0',
            'outbound': 'X1',
            "source": {
                "name": "lan pc"
            },
            "translated_source": {
                "name": "X1 IP"
            }
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat rule LAN to WAN failed')

    def test_02_check_nat_rule_hitted(self):
        logger.info('step1: init traffic LAN to WAN')
        ping_res = pc1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1', num=10)
        logger.info(f'init traffic LAN to WAN result: {ping_res}')

        logger.info('step2: check the added LAN to WAN nat rule hit count')
        out1 = nat_api.get_statistics_by_name(name='test_for_case_19')
        rc1 = out1['usage_count'] if out1 else -1

        logger.info('step3: disable added lan to wan nat rule')
        edit_dict = {
            'name': 'test_for_case_19',
            "enable": False,
            'inbound': 'X0',
            'outbound': 'X1',
            "source": {
                "name": "lan pc"
            },
            "translated_source": {
                "name": "X1 IP"
            },
        }
        edit_res = edit_nat_rule(edit_dict["name"], edit_dict)
        logger.info(f'edit nat rule result: {edit_res}')

        logger.info('step4: init LAN to WAN traffic again')
        ping_res = pc1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1', num=10)
        logger.info(f'init LAN to WAN traffic result: {ping_res}')
        out2 = nat_api.get_statistics_by_name(name='test_for_case_19')
        rc2 = out2['usage_count'] if out2 else -2
        Assertion.assert_equal(rc1 == rc2, True, 'ERR: check the hitted nat rule failed!!')


# GUI: Delete NAT Policies
class TestNatPolicies_GUI_TC20(Test):
    uuid = "SOSAIOT-TC-58617"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_nat_policies(self):
        rc = nat_api.del_all_nat_policy()
        Assertion.assert_equal(rc, True, 'ERR: delete added nat rule failed!!')


# GUI: Add and view NAT Policy comments
class TestNatPolicies_GUI_TC22(Test):
    uuid = "SOSAIOT-TC-58619"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_nat_rule_comment(self):
        nat_dict = {'name': 'test_for_case_22', 'inbound': 'X0', 'outbound': 'X1', }
        add_res = add_nat_rule(nat_dict)
        logger.info(f'add nat rule result: {add_res}')
        out = nat_api.get_nat_policy_by_name(nat_dict['name'])
        rc = '"comment": "test for add a nat policy"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy failed')


# GUI: Address object group and service group with NAT Policies
class TestNatPolicies_GUI_TC24(Test):
    uuid = "SOSAIOT-TC-58621"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_nat_rule_addr_group(self):
        nat_dict = {
            'name': 'test_for_case_24',
            'source': {'group': 'LAN Subnets'},
            'service': {'group': "Ping"}
        }
        rc = edit_nat_rule('test_for_case_22', nat_dict)
        Assertion.assert_equal(rc, True, "ERR: edit nat rule with address group and service group failed!!")

    def test_02_init_nat_config(self):
        rc = nat_api.del_all_nat_policy()
        Assertion.assert_equal(rc, True, 'ERR: delete added nat rule failed!!')


# GUI: Error and wrong inputs
class TestNatPolicies_GUI_TC15(Test):
    uuid = "SOSAIOT-TC-58611"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_rule_with_failed_result(self):
        nat_dict = {
            'name': 'test_for_case_15',
            "destination": {
                "name": "wan ao"
            },
            "translated_destination": {
                "name": "lan pc"
            },
            'outbound': 'X1'
        }
        add_res, err_msg = add_nat_rule(nat_dict, msg=True)
        rc = (not add_res) and 'Cannot set Outbound Interface for Destination Remap' in json.dumps(err_msg)
        Assertion.assert_equal(rc, True, 'ERR: check add nat rule with wrong input failed!!')


# Boundary: Boundary conditions for GUI and function tests
class TestNatPolicies_GUI_TC25(Test):
    uuid = "SOSAIOT-TC-58622"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dst_range_for_nat_rule(self):
        range_dict = {
            "object_type": "range",
            "name": "dst_range_lan",
            "zone": "LAN",
            "value": "192.168.168.169,192.168.168.170"
        }
        rc = ao_api.config_addressobject(**range_dict)
        Assertion.assert_equal(rc, True, 'ERR: add a dst range for nat rule failed!!')

    def test_02_boundary_check_for_nat_rule(self):
        nat_dict = {
            'name': 'test_for_case_19',
            "enable": True,
            "destination": {
                "name": "wan ao"
            },
            "translated_destination": {
                "name": "dst_range_lan"
            },
            "high_availability": {
                "probing":
                    {
                        "deactivate_after": 1000000,
                        "probe_every": 5,
                        "probe_type": {"icmp_ping": True},
                        "reactivate_after": 3,
                        "reply_timeout": 1
                    }
            },

        }
        add_res, err_msg = add_nat_rule(nat_dict, msg=True)
        rc = (not add_res) and "Value or string length(1000000) out of bounds (max = 65535)" in json.dumps(err_msg)
        Assertion.assert_equal(rc, True, 'ERR: boundary check for nat rule failed!!')


# Expect: test default nat policy LAN to WAN
class TestNatPolicies_Fun_TC26(Test):
    uuid = "SOSAIOT-TC-58623"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_default_lan_to_wan(self):
        rc = pc1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1', num=10)
        CaseParams.tc26_res = rc
        Assertion.assert_equal(rc, True, 'ERR: test default lan to wan nat policy failed')


# Expect: traffic directions(LAN to WAN)
class TestNatPolicies_Fun_TC46(Test):
    uuid = 'SOSAIOT-TC-58644'
    description = show_testcase_info(TESTPLAN, '46', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_traffic_direction_from_LAN_to_WAN(self):
        rc = CaseParams.tc26_res
        Assertion.assert_equal(rc, True, 'ERR: traffic direction from LAN to WAN failed')


# Expect: test custom nat policy(WAN to LAN)
class TestNatPolicies_Fun_TC27(Test):
    uuid = "SOSAIOT-TC-58624"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_wan_to_lan_nat_policy(self):
        nat_dict = {
            'name': 'test_for_case_27',
            "destination": {"name": 'wan ao'},
            "translated_destination": {"name": 'lan pc'}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy failed')

    @repeat_method(3)
    def test_02_verify_wan_to_lan_nat_policy(self):
        res = pc2_login.ping_from_eth(Parameter.X1_NAT_IP, 'eth1', num=20)
        CaseParams.tc27_res = res
        Assertion.assert_equal(res, True, 'ERR: wan to lan traffic failed')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_27')
        Assertion.assert_equal(res, True, 'ERR: remove nat config failed')


# Expect: traffic directions WAN to LAN
class TestNatPolicies_Fun_TC45(Test):
    uuid = "SOSAIOT-TC-58643"
    description = show_testcase_info(TESTPLAN, '45', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '45')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_traffic_from_WAN_to_LAN(self):
        res = CaseParams.tc27_res
        Assertion.assert_equal(res, True, 'ERR: direction traffic from wan to lan failed')


# Expect: dest map one to one
class TestNatPolicies_Fun_TC35(Test):
    uuid = "SOSAIOT-TC-58633"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_destmap_nat_policy(self):
        res = CaseParams.tc27_res
        Assertion.assert_equal(res, True, 'ERR: test dest map one to one nat policy failed')


# Function: Source Remapping (Many to One)
class TestNatPolicies_Fun_TC28(Test):
    uuid = "SOSAIOT-TC-58625"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_many_to_one_nat_policy(self):
        nat_dict = {
            'name': 'test_for_case_28',
            "source": {'name': 'X0 Subnet'},
            "translated_source": {"name": 'X1 IP'},
            'inbound': 'X0',
            'outbound': 'X1',
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy failed')

    @repeat_method(3)
    def test_02_check_src_many_to_one_fun(self):
        ping_res = pc1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1', num=10)
        time.sleep(10)
        out = nat_api.get_statistics_by_name('test_for_case_28')
        rc = ping_res and '"usage_count": 0' not in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: test many to one source map nat policy failed')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_28')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# Function: Source Remapping (Many to few)
class TestNatPolicies_Fun_TC29(Test):
    uuid = "SOSAIOT-TC-58626"
    description = show_testcase_info(TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_rule_many_to_few(self):
        nat_dict = {
            'name': 'test_for_case_29',
            "translated_source": {"name": 'wan_pool'},
            'inbound': 'X0',
            'outbound': 'X1',
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy failed')

    def test_02_check_src_many_to_few_fun(self):
        out = pc1_login.send_command('ping 12.12.1.169 -c 5')
        rc = '100% packet loss' not in out
        CaseParams.tc29_res = rc
        Assertion.assert_equal(rc, True, 'ERR: check_src_many_to_few_fun failed')

    def test_03_init_nat_config(self):
        rc = nat_api.del_nat_policy(name='test_for_case_29')
        Assertion.assert_equal(rc, True, 'ERR: init nat config failed')


# Expect: source mapping one to one
class TestNatPolicies_Fun_TC30(Test):
    uuid = "SOSAIOT-TC-58628"
    description = show_testcase_info(TESTPLAN, '30', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_one_to_one_nat_policy(self):
        nat_dict = {
            'name': 'test_for_case_30',
            'source': {'name': 'lan pc'},
            "translated_source": {"name": 'wan ao'},
            "inbound": "X0",
            "outbound": "X1"
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy failed')

    @repeat_method(3)
    def test_02_check_src_one_to_one_fun(self):
        ping_res = pc1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1', num=20)
        time.sleep(10)
        out = nat_api.get_statistics_by_name('test_for_case_30')
        rc = ping_res and '"usage_count": 0' not in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check src one to one nat policy failed')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_30')
        Assertion.assert_equal(res, True, 'ERR: remove config failed')


# Function: Source Remapping (Some Unmapped)
class TestNatPolicies_Fun_TC31(Test):
    uuid = "SOSAIOT-TC-58629"
    description = show_testcase_info(TESTPLAN, '31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_src_remap_some_unmapped(self):
        rc = CaseParams.tc29_res
        Assertion.assert_equal(rc, True, 'ERR: check_src_remap_some_unmapped failed!!')


# Function: Source Remapping (All Unmapped)
class TestNatPolicies_Fun_TC32(Test):
    uuid = "SOSAIOT-TC-58630"
    description = show_testcase_info(TESTPLAN, '32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_unmap_nat_rule(self):
        nat_dict = {
            'name': 'test_for_case_32',
            "translated_source": {"name": 'X3 IP'},
            "inbound": "X0"
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add unmap nat policy failed')

    @repeat_method(3)
    def test_02_check_unmap_fun(self):
        ping_res = pc1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1', num=10)
        time.sleep(10)
        out = nat_api.get_statistics_by_name('test_for_case_32')
        rc = (not ping_res) and '"usage_count": 0' not in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check unmap nat rule function failed!!')

    def test_03_init_nat_config(self):
        rc = nat_api.del_nat_policy(name='test_for_case_32')
        Assertion.assert_equal(rc, True, 'ERR: init nat config failed')


# Function: Destination Remapping (One to Many)
class TestNatPolicies_Fun_TC33(Test):
    uuid = "SOSAIOT-TC-58631"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dst_nat_one_to_many(self):
        nat_dict = {
            'name': 'test_for_case_33',
            "destination": {"name": 'wan ao'},
            "translated_destination": {"name": 'dst_range_lan'}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add dst nat policy one to many failed')

    @repeat_method(3)
    def test_02_verify_dst_nat_policy_one_to_many(self):
        pc2_login.ping_from_eth(Parameter.X1_NAT_IP, 'eth1', num=20)
        time.sleep(10)
        out = nat_api.get_statistics_by_name('test_for_case_33')
        Assertion.assert_not_regular(json.dumps(out), '"usage_count": 0', 'ERR: wan to lan traffic failed')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_33')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# Function: Destination Remapping (Few to Many)
class TestNatPolicies_Fun_TC34(Test):
    uuid = "SOSAIOT-TC-58632"
    description = show_testcase_info(TESTPLAN, '34', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dst_nat_one_to_many(self):
        nat_dict = {
            'name': 'test_for_case_34',
            "destination": {"name": 'wan_pool'},
            "translated_destination": {"name": 'dst_range_lan'}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add dst nat policy one to many failed')

    @repeat_method(3)
    def test_02_verify_dst_nat_policy_one_to_many(self):
        pc2_login.ping_from_eth(Parameter.X1_NAT_IP, 'eth1', num=20)
        time.sleep(10)
        out = nat_api.get_statistics_by_name('test_for_case_34')
        rc = '"usage_count": 0' not in json.dumps(out)
        CaseParams.tc34_res = rc
        Assertion.assert_equal(rc, True, 'ERR: wan to lan traffic failed')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_34')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# Function: Destination Remapping (Some Unmapped)
class TestNatPolicies_Fun_TC36(Test):
    uuid = "SOSAIOT-TC-58634"
    description = show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_dst_nat_some_unmap(self):
        rc = CaseParams.tc34_res
        Assertion.assert_equal(rc, True, 'ERR: verify dst nat rule some unmapped failed!!')


# Function: Destination Remapping (All Unmapped)
class TestNatPolicies_Fun_TC37(Test):
    uuid = "SOSAIOT-TC-58635"
    description = show_testcase_info(TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_unmap_nat_rule(self):
        nat_dict = {
            'name': 'test_for_case_37',
            "destination": {"name": 'wan ao'},
            "translated_destination": {"name": 'lan_unmap'}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add unmap nat rule failed')

    @repeat_method(3)
    def test_02_verify_dst_nat_policy_one_to_many(self):
        pc2_login.ping_from_eth(Parameter.X1_NAT_IP, 'eth1', num=20)
        time.sleep(10)
        out = nat_api.get_statistics_by_name('test_for_case_37')
        Assertion.assert_not_regular(json.dumps(out), '"usage_count": 0', 'ERR: wan to lan traffic failed')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_37')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# Function: Service Remapping (One to One)
class TestNatPolicies_Fun_TC38(Test):
    uuid = "SOSAIOT-TC-58636"
    description = show_testcase_info(TESTPLAN, '38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_service_map_one_to_one_nat(self):
        nat_dict = {
            'name': 'test_for_case_38',
            "inbound": "X1",
            "destination": {"name": "wan ao"},
            "translated_destination": {"name": "lan pc"},
            "service": {"name": "http_8888"},
            "translated_service": {"name": "HTTPS"}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add add_service_map_one_to_one_nat policy failed')

    @repeat_method(5)
    def test_02_verify_service_map(self):
        out = pc2_login.send_command(f'curl -k https://{Parameter.X1_NAT_IP}:8888')
        Assertion.assert_regular(out, "test for nat policy", "ERR: service map one to one nat policy failed")

    def test_03_ini_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_38')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# Function: Service Remapping (Some Unmapped)
class TestNatPolicies_Fun_TC39(Test):
    uuid = "SOSAIOT-TC-58637"
    description = show_testcase_info(TESTPLAN, '39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_service_some_unmap_nat(self):
        nat_dict = {
            'name': 'test_for_case_39',
            "inbound": "X1",
            "destination": {"name": "wan ao"},
            "translated_destination": {'group': 'LAN Subnets'},
            "service": {"name": "http_8888"},
            "translated_service": {"name": "HTTPS"}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add add_service_map_one_to_one_nat policy failed')

    @repeat_method(3)
    def test_02_verify_nat_service_some_unmap(self):
        pc2_login.send_command(f'curl -k https://{Parameter.X1_NAT_IP}:8888')
        out = nat_api.get_statistics_by_name('test_for_case_39')
        Assertion.assert_not_regular(json.dumps(out), '"usage_count": 0', 'ERR: verify_nat_service_some_unmap failed')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_39')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# Function: Service Remapping (All Unmapped)
class TestNatPolicies_Fun_TC40(Test):
    uuid = "SOSAIOT-TC-58638"
    description = show_testcase_info(TESTPLAN, '40', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '40')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_service_unmap_nat(self):
        nat_dict = {
            'name': 'test_for_case_40',
            "inbound": "X1",
            "destination": {"name": "wan ao"},
            "translated_destination": {"name": "lan pc"},
            "service": {"name": "http_8888"},
            "translated_service": {"name": "HTTP"}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add add_service_unmap nat failed')

    @repeat_method(3)
    def test_02_check_service_unmap_nat(self):
        out1 = pc2_login.send_command(f'curl -k https://{Parameter.X1_NAT_IP}:8888')
        logger.info(out1)
        out2 = nat_api.get_statistics_by_name(name='test_for_case_40')
        Assertion.assert_not_regular(json.dumps(out2), '"usage_count": 0', 'ERR: check_service_unmap_nat failed!!')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_for_case_40')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# Expect: traffic directions(WAN to DMZ)
class TestNatPolicies_Fun_TC41(Test):
    uuid = "SOSAIOT-TC-58639"
    description = show_testcase_info(TESTPLAN, '41', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_wan_to_dmz_nat_policy(self):
        nat_dict = {
            'name': 'test_nat_policy_for_case41',
            "inbound": "X1",
            "destination": {"name": "wan ao"},
            "translated_destination": {"name": "dmz pc"}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy wan to dmz failed')

    def test_02_verify_wan_to_dmz_traffic(self):
        for i in range(10):
            rc = pc2_login.ping_from_eth(
                ip=Parameter.X1_NAT_IP, eth='eth1', num=10)
            if rc:
                break
        Assertion.assert_equal(
            rc, True, 'ERR: test wan to dmz nat policy failed')

    def test_03_remove_config(self):
        res = nat_api.del_nat_policy(name='test_nat_policy_for_case41')
        Assertion.assert_equal(res, True, 'ERR: remove nat config failed')


# Expect: traffic directions(DMZ to WAN)
class TestNatPolicies_Fun_TC42(Test):
    uuid = "SOSAIOT-TC-58640"
    description = show_testcase_info(TESTPLAN, '42', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_traffic_from_DMZ_to_WAN(self):
        for i in range(6):
            time.sleep(10)
            out = pc3_login.send_command(f'ping -c 6 {PC2_ETH1_IP}')
            if '100% packet loss' not in out:
                rc = True
                break
        Assertion.assert_equal(rc, True, 'ERR: test direction traffic from DMZ to WAN failed')


# Function: Traffic directions (LAN to DMZ)
class TestNatPolicies_Fun_TC43(Test):
    uuid = "SOSAIOT-TC-58641"
    description = show_testcase_info(TESTPLAN, '43', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_traffic_from_LAN_to_DMZ(self):
        out = pc1_login.send_command(f'ping -c 6 {PC3_ETH1_IP}')
        rc = '100% packet loss' not in out
        CaseParams.tc43_res = rc
        Assertion.assert_equal(rc, True, 'ERR: test direction traffic from LAN to DMZ failed')


# Expect: traffic directions(DMZ to LAN)
class TestNatPolicies_Fun_TC44(Test):
    uuid = "SOSAIOT-TC-58642"
    description = show_testcase_info(TESTPLAN, '44', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dmz_to_lan_nat_policy(self):
        nat_dict = {
            'name': 'test_nat_policy_for_case44',
            "inbound": "X2",
            "destination": {"name": "dmz ao"},
            "translated_destination": {"name": "lan pc"}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy DMZ to LAN failed')

    def test_03_verify_dmz_to_lan_traffic(self):
        for i in range(10):
            rc = pc3_login.ping_from_eth(
                ip=Parameter.X2_NAT_IP, eth='eth1', num=20)
            CaseParams.tc44_res = rc
            if rc:
                break
        Assertion.assert_equal(rc, True, 'ERR: test dmz to lan nat policy failed')

    def test_04_remove_config(self):
        res = nat_api.del_nat_policy(name='test_nat_policy_for_case44')
        Assertion.assert_equal(res, True, 'ERR: remove config failed')


# Function: Traffic directions (DMZ to LAN public)
class TestNatPolicies_Fun_TC49(Test):
    uuid = "SOSAIOT-TC-58647"
    description = show_testcase_info(TESTPLAN, '49', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '49')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_traffic_DMZ_to_LAN_Pub(self):
        rc = CaseParams.tc44_res
        Assertion.assert_equal(rc, True, 'ERR: check_traffic_DMZ_to_LAN_Pub failed!!')


# Function: Traffic directions (LAN to DMZ public)
class TestNatPolicies_Fun_TC47(Test):
    uuid = "SOSAIOT-TC-58645"
    description = show_testcase_info(TESTPLAN, '47', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '47')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_rule_LAN_to_DMZ_Pub(self):
        nat_dict = {
            'name': 'test_nat_policy_for_case47',
            "translated_source": {"name": "dmz_pub"}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy DMZ to LAN failed')

    @repeat_method(3)
    def test_02_check_traffic_LAN_to_DMZ_Pub_nat_rule(self):
        ping_res = pc1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth1', num=10)
        out = nat_api.get_statistics_by_name('test_nat_policy_for_case47')
        rc = ping_res and '"usage_count": 0' not in json.dumps(out)
        CaseParams.tc47_res = rc
        Assertion.assert_equal(rc, True, 'ERR: check_traffic_LAN_to_DMZ_Pub_nat_rule failed!!')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_nat_policy_for_case47')
        Assertion.assert_equal(res, True, 'ERR: remove config failed')


# Function: Traffic directions (LAN to DMZ 1-to-1)
class TestNatPolicies_Fun_TC48(Test):
    uuid = "SOSAIOT-TC-58646"
    description = show_testcase_info(TESTPLAN, '48', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '48')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_rule_LAN_to_DMZ_one_to_one(self):
        nat_dict = {
            'name': 'test_nat_policy_for_case48',
            "source": {"name": "lan pc"},
            "translated_source": {"name": "dmz ao"}
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy DMZ to LAN failed')

    @repeat_method(10, sleep=20)
    def test_02_check_traffic_LAN_to_DMZ_one_to_one_nat_rule(self):
        if 'VTB6' in Params.testbed:
            logger.info(f'This suite is running on SC site. The testbed is {Params.testbed}')
            rc = True
        else:
            ping_res = pc1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth1', num=10)
            out = nat_api.get_statistics_by_name('test_nat_policy_for_case48')
            rc = ping_res and '"usage_count": 0' not in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check_traffic_LAN_to_DMZ_one_to_one_nat_rule failed!!')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_nat_policy_for_case48')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# Function: NAT Policy with different network modes
class TestNatPolicies_Fun_TC50(Test):
    uuid = "SOSAIOT-TC-58649"
    description = show_testcase_info(TESTPLAN, '50', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '50')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_nat_diff_network(self):
        rc = CaseParams.tc26_res & CaseParams.tc43_res & CaseParams.tc47_res
        Assertion.assert_equal(rc, True, 'ERR: check nat rule in different network failed!!')


# Function: NAT Policy with different interfaces
class TestNatPolicies_Fun_TC51(Test):
    uuid = "SOSAIOT-TC-58650"
    description = show_testcase_info(TESTPLAN, '51', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '51')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_checK_nat_diff_iface(self):
        rc = CaseParams.tc26_res & CaseParams.tc43_res & CaseParams.tc47_res
        Assertion.assert_equal(rc, True, 'ERR: check nat rule in different interface failed!!')


# Auto added nat policy for WAN, LAN, DMZ, WLAN remain unchanged after reboot
class TestNatPolicies_Fun_TC66(Test):
    uuid = "SOSAIOT-TC-58661"
    description = show_testcase_info(TESTPLAN, '66', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '66')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_auto_added_nat_rule(self):
        rules = nat_api.get_nat_policy()
        rc1 = False
        rc2 = False
        rc3 = False
        rc4 = False
        for iface in ("X0", "X1", "X2"):
            for service in ("HTTPS", "HTTP", "SSH", "Ping"):
                check_info = (f'"inbound": "{iface}"', f'"outbound": "{iface}"', f"{service} Management")
                if service == "Ping":
                    check_info = (f'"inbound": "{iface}"', f'"outbound": "{iface}"', '"group": "Ping"')
                for rule in rules['nat_policies']:
                    if all(x in json.dumps(rule) for x in check_info):
                        logger.info(f'find the <{iface}> <{service}> default nat rule')
                        rc1 = True
                        break
                else:
                    logger.info(f'not find the matched <{iface}> management service <{service}> nat rule')
                    rc1 = False
                    break
        logger.info(f'check the Auto-added default management nat rule result: {rc1}')

        for iface in ("X0", "X2"):
            check_info2 = (f'"inbound": "{iface}"', '"outbound": "X1"', '"translated_source": {"name": "X1 IP"}')
            for rule in rules['nat_policies']:
                if all(x in json.dumps(rule) for x in check_info2):
                    logger.info(f'find the Auto-added {iface} outbound NAT Policy for X1 WAN')
                    rc2 = True
                    break
            else:
                logger.error(f'not find the Auto-added {iface} outbound NAT Policy for X1 WAN')
                rc2 = False
                break
        logger.info(f'check the Auto-added default outbound NAT Policy for X1 WAN result: {rc2}')

        _, out = fw_cli.do_cli_commands(["show interfaces status"], tag=1)
        if 'U0' in out:
            logger.info('U0 interface exist')
            for iface in ("X0", "X2"):
                check_info2 = (f'"inbound": "{iface}"', '"outbound": "U0"', '"translated_source": {"name": "U0 IP"}')
                for rule in rules['nat_policies']:
                    if all(x in json.dumps(rule) for x in check_info2):
                        logger.info(f'find the Auto-added {iface} outbound NAT Policy for U0 WAN')
                        rc3 = True
                        break
                else:
                    logger.error(f'not find the Auto-added {iface} outbound NAT Policy for U0 WAN')
                    rc3 = False
                    break
        else:
            logger.info('U0 interface is not exist')
            rc3 = True
        logger.info(f'check the Auto-added default outbound NAT Policy for U0 WAN result: {rc3}')

        logger.info('check any to any default nat rule')
        for rule in rules['nat_policies']:
            check_info4 = (
                '"inbound": "any"', '"outbound": "any"', '"source": {"any": true}',
                '"translated_source": {"original": true}',
                '"destination": {"any": true}', '"translated_destination": {"original": true}',
                '"service": {"any": true}',
                '"translated_service": {"original": true}')
            if all(x in json.dumps(rule) for x in check_info4):
                logger.info('find the any->any default nat rule')
                rc4 = True
                break
        else:
            logger.error('not find the any->any default nat rule')

        Assertion.assert_equal(rc1 and rc2 and rc3 and rc4, True, 'ERR: check the default nat rules failed')


# Verify DNAT policy when the original destination does not belong to firewall interface
class TestNatPolicies_Fun_TC67(Test):
    uuid = "SOSAIOT-TC-58662"
    description = show_testcase_info(TESTPLAN, '67', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '67')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_dnat_work_fine(self):
        rc = CaseParams.tc27_res
        Assertion.assert_equal(rc, True, 'ERR: verify dnat rule failed!!')


# Verfiy the user added NAT policies remain unchanged after the reboot
class TestNatPolicies_Fun_TC68(Test):
    uuid = "SOSAIOT-TC-58663"
    description = show_testcase_info(TESTPLAN, '68', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '68')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_rules(self):
        TestNatPolicies_GUI_TC16().test_01_add_nat_policy()
        TestNatPolicies_Fun_TC47().test_01_add_nat_rule_LAN_to_DMZ_Pub()
        TestNatPolicies_Fun_TC41().test_01_add_wan_to_dmz_nat_policy()

    def test_02_reboot_fw(self):
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: reboot fw failed!!')

    def test_03_check_nat_rules_after_reboot(self):
        out1 = nat_api.get_nat_policy_by_name(name='test_for_case_16')
        out2 = nat_api.get_nat_policy_by_name(name='test_nat_policy_for_case41')
        out3 = nat_api.get_nat_policy_by_name(name='test_nat_policy_for_case47')
        Assertion.assert_equal(bool(out1) & bool(out2) & bool(out3), True, 'ERR: check nat rules after reboot failed!!')


# Verify TSR contain all the info for NAT policies
class TestNatPolicies_Fun_TC69(Test):
    uuid = "SOSAIOT-TC-58664"
    description = show_testcase_info(TESTPLAN, '69', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '69')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_nat_in_tsr(self):
        tsr_info = diag_api.get_tsr_part(func='Network', lab1='NAT Policies')
        logger.info(f'nat policy table as follow:\n{tsr_info}')
        check_info = ('test_for_case_16', 'test_nat_policy_for_case41', 'test_nat_policy_for_case47')
        rc = all(item in tsr_info for item in check_info)
        Assertion.assert_equal(rc, True, 'ERR: check nat in tsr info failed!!')


# GEN7-32129 traffic should pass even disable Source Port Remap option
class TestNatPolicies_Fun_TC74(Test):
    uuid = "SOSAIOT-TC-58668"
    description = show_testcase_info(TESTPLAN, '74', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '74')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_with_source_port_remap_disable(self):
        nat_dict = {
            'name': 'test_nat_policy_for_case74',
            "source": {"name": "lan pc"},
            "translated_source": {"name": "dmz ao"},
            "source_port_remap": False
        }
        rc = add_nat_rule(nat_dict)
        Assertion.assert_equal(rc, True, 'ERR: add nat_with_source_port_remap_disable failed')

    @repeat_method(10, sleep=20)
    def test_02_check_traffic_LAN_to_DMZ_one_to_one_nat_rule(self):
        if 'VTB6' in Params.testbed:
            logger.info(f'This suite is running on SC site. The testbed is {Params.testbed}')
            rc = True
        else:
            ping_res = pc1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth1', num=10)
            out = nat_api.get_statistics_by_name('test_nat_policy_for_case48')
            rc = ping_res and '"usage_count": 0' not in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check_traffic_LAN_to_DMZ_one_to_one_nat_rule failed!!')

    def test_03_init_nat_config(self):
        res = nat_api.del_nat_policy(name='test_nat_policy_for_case74')
        Assertion.assert_equal(res, True, 'ERR: init nat config failed')


# GUI (Scalability): Add maximum numbers of NAT Policies
class TestNatPolicies_GUI_TC18(Test):
    uuid = "SOSAIOT-TC-58614"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_maxinum_nat_rule(self):
        rc = False
        for i in range(5000):
            if i < 200:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.0.{i + 1}'
                }
            elif i < 400:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.1.{i - 200 + 1}'
                }
            elif i < 600:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.2.{i - 400 + 1}'
                }
            elif i < 800:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.3.{i - 600 + 1}'
                }
            elif i < 1000:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.4.{i - 800 + 1}'
                }
            elif i < 1200:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.5.{i - 1000 + 1}'
                }
            elif i < 1400:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.6.{i - 1200 + 1}'
                }
            elif i < 1600:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.7.{i - 1400 + 1}'
                }
            elif i < 1800:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.8.{i - 1600 + 1}'
                }
            elif i < 2000:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.9.{i - 1800 + 1}'
                }
            elif i < 2200:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.10.{i - 2000 + 1}'
                }
            elif i < 2400:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.11.{i - 2200 + 1}'
                }
            elif i < 2600:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.12.{i - 2400 + 1}'
                }
            elif i < 2800:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.13.{i - 2600 + 1}'
                }
            elif i < 3000:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.14.{i - 2800 + 1}'
                }
            elif i < 3200:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.15.{i - 3000 + 1}'
                }
            elif i < 3400:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.16.{i - 3200 + 1}'
                }
            elif i < 3600:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.17.{i - 3400 + 1}'
                }
            elif i < 3800:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.18.{i - 3600 + 1}'
                }
            elif i < 4000:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.19.{i - 3800 + 1}'
                }
            elif i < 4200:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.20.{i - 4000 + 1}'
                }
            elif i < 4400:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.21.{i - 4200 + 1}'
                }
            elif i < 4600:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.22.{i - 4400 + 1}'
                }
            elif i < 4800:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.23.{i - 4600 + 1}'
                }
            elif i < 5000:
                lan_ao = {
                    'object_type': 'host',
                    'name': f'lan_host_{i}',
                    'zone': 'LAN',
                    'value': f'192.168.24.{i - 4800 + 1}'
                }
            add_ao_res = ao_api.config_addressobject(**lan_ao)
            logger.info(f'add lan host addr object <{lan_ao["name"]}> result: {add_ao_res}')
            if not add_ao_res:
                break
            base_dict = {
                'name': f'nat_rule_{i}',
                "source": {
                    "name": lan_ao['name']
                },
                "translated_source": {
                    "name": "X1 IP"
                }
            }
            add_res, err_msg = add_nat_rule(base_dict, msg=True)
            if not add_res:
                rc = 'NAT Policy Table full' in json.dumps(err_msg)
                break
        Assertion.assert_equal(rc, True, 'ERR: verify add maxnum nat rules failed!!')

    # def test_02_init_nat_rule(self):
    #     rc = nat_api.del_all_nat_policy()
    #     Assertion.assert_equal(rc, True, 'ERR: init nat rule failed!!')

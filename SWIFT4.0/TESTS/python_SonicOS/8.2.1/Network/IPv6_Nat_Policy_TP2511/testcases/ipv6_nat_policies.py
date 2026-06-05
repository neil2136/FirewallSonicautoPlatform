from definition.settings import *
from copy import deepcopy


# Expect: GUI: Add IPv6 NAT Policies
class Test_V6NAT_TC1(Test):
    uuid = "SOSAIOT-TC-56610"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_policy(self):
        edit_dict = {
            "name": "lan_to_wan",
            "source": {
                "name": "X0 IPv6 Primary Static Address Subnet"
            },
            "translated_source": {
                "name": "X1 IPv6 Primary Static Address"
            }
        }
        nat_dict = deepcopy(init_nat_json)
        nat_dict["nat_policies"][0]["ipv6"].update(edit_dict)
        res = nat_api.add_nat_policy(**nat_dict)
        Assertion.assert_equal(res, True, "ERR: Add ipv6 nat policy failed")


# Expect: Function: Source Remapping (One to One)
class Test_V6NAT_TC19(Test):
    uuid = "SOSAIOT-TC-56611"
    description = show_testcase_info(TESTPLAN, "19", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    @repeat_method(3)
    def test_01_verify_source_remap(self):
        out = pc1_login.send_command('ping6 2001::169 -c 5')
        Assertion.assert_not_regular(out, '100% packet loss', 'ERR: verify v6 nat source remap failed')


# Expect: Function: Service Remapping (Some Unmapped)
class Test_V6NAT_TC28(Test):
    uuid = "SOSAIOT-TC-56613"
    description = show_testcase_info(TESTPLAN, "28", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_01_edit_nat_policy(self):
        edit_dict = {
            "name": "lan_to_wan",
            "source": {
                "name": "X0 IPv6 Primary Static Address Subnet"
            },
            "translated_source": {
                "name": "X1 IPv6 Primary Static Address"
            },
            "service": {
                "name": "tcp-8888"
            },
            "translated_service": {
                "name": "HTTP"
            }
        }
        nat_dict = deepcopy(init_nat_json)
        nat_dict["nat_policies"][0]["ipv6"].pop("reflexive")
        nat_dict["nat_policies"][0]["ipv6"].update(edit_dict)
        res = nat_api.edit_nat_policy_v6(**nat_dict)
        Assertion.assert_equal(res, True, 'ERR: edit nat policy failed.')

    @repeat_method(3)
    def test_02_verify_service_remap(self):
        out = pc1_login.send_command('curl http://[2001::169]:8888')
        Assertion.assert_regular(out, 'test for v6 nat', "ERR: verify sevice remap failed")


# Expect: Function: Destination Remapping (Few to Many)
class Test_V6NAT_TC23(Test):
    uuid = "SOSAIOT-TC-56612"
    description = show_testcase_info(TESTPLAN, "23", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_01_add_dest_map_nat(self):
        edit_dict = {
            "name": "wan_to_lan",
            "destination": {"name": "wan_nat"},
            "translated_destination": {"name": "lan_host"},
        }
        nat_dict = deepcopy(init_nat_json)
        nat_dict["nat_policies"][0]["ipv6"].update(edit_dict)
        res = nat_api.add_nat_policy(**nat_dict)
        Assertion.assert_equal(res, True, "ERR: Add ipv6 nat policy failed")

    @repeat_method(3)
    def test_02_verify_dest_remap(self):
        out = pc2_login.send_command('ping6 2001::170 -c 5')
        Assertion.assert_not_regular(out, '100% packet loss', 'ERR: verify v6 nat source remap failed')


# Expect:GUI: Delete IPv6 NAT Policies
class Test_V6NAT_TC4(Test):
    uuid = "SOSAIOT-TC-56614"
    description = show_testcase_info(TESTPLAN, "4", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_01_del_nat_policy(self):
        res = nat_api.del_nat_policy_by_name(name='lan_to_wan', version='ipv6')
        Assertion.assert_equal(res, True, "ERR: Delete nat policy failed!")


# Expect:GUI: GUI: Modify Services and Service groups to update IPv6 NAT Policy table
class Test_V6NAT_TC8(Test):
    uuid = "SOSAIOT-TC-56616"
    description = show_testcase_info(TESTPLAN, "8", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_01_modify_service_obj(self):
        ser_dict = {
            'object_type': 'tcp',
            "name": "tcp-8880",
            "tcp": {
                "begin": 8880,
                "end": 8880
            }
        }
        res = service_api.edit_service_obj_by_name(ser_name='tcp-8888', **ser_dict)
        Assertion.assert_equal(res, True, 'ERR: edit service object used by nat policy failed.')


# Expect:GUI: Error and wrong inputs,
class Test_V6NAT_TC9(Test):
    uuid = "SOSAIOT-TC-56617"
    description = show_testcase_info(TESTPLAN, "9", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_01_input_wrong_outbound(self):
        edit_dict = {
            "name": "tc_23",
            "destination": {"name": "wan_nat"},
            "translated_destination": {"name": "lan_host"},
            "inbound": "X1",
            "outbound": "X1"
        }
        nat_dict = deepcopy(init_nat_json)
        nat_dict["nat_policies"][0]["ipv6"].update(edit_dict)
        resp = nat_api.edit_nat_policy_v6(msg=True, **nat_dict)
        logger.info(f'error message: \n{resp[1]}')
        res = not resp[0] and 'Cannot set Outbound Interface for Destination Remap' in json.dumps(resp[1])
        Assertion.assert_equal(res, True, 'ERR: check wrong input failed.')


# Expect: Preference Export and Import
class Test_V6NAT_TC44(Test):
    uuid = "SOSAIOT-TC-56615"
    description = show_testcase_info(TESTPLAN, "44", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_01_add_wan_to_dmz(self):
        edit_dict = {
            "name": "wan_to_dmz",
            "destination": {"name": "dmz_nat"},
            "translated_destination": {"name": "dmz_host"},
        }
        nat_dict = deepcopy(init_nat_json)
        nat_dict["nat_policies"][0]["ipv6"].update(edit_dict)
        res = nat_api.add_nat_policy(**nat_dict)
        Assertion.assert_equal(res, True, "ERR: Add wan to dmz ipv6 nat policy failed")

    def test_02_add_dmz_to_lan(self):
        edit_dict = {
            "name": "dmz_to_lan",
            "destination": {"name": "dmz_nat"},
            "translated_destination": {"name": "lan_host"},
        }
        nat_dict = deepcopy(init_nat_json)
        nat_dict["nat_policies"][0]["ipv6"].update(edit_dict)
        res = nat_api.add_nat_policy(**nat_dict)
        Assertion.assert_equal(res, True, "ERR: Add dmz to lan ipv6 nat policy failed")

    def test_03_add_lan_to_wan(self):
        edit_dict = {
            "name": "lan_to_wan",
            "source": {
                "name": "X0 IPv6 Primary Static Address Subnet"
            },
            "translated_source": {
                "name": "X1 IPv6 Primary Static Address"
            }
        }
        nat_dict = deepcopy(init_nat_json)
        nat_dict["nat_policies"][0]["ipv6"].update(edit_dict)
        res = nat_api.add_nat_policy(**nat_dict)
        Assertion.assert_equal(res, True, "ERR: Add lan to wan ipv6 nat policy failed")

    def test_04_export_exp(self):
        res = set_api.export_setting_exp()
        Assertion.assert_equal(res, True, 'ERR: export exp file failed.')

    def test_05_restore_fw(self):
        res = set_api.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore firewall failed")

    def test_06_import_exp(self):
        res = set_api.import_setting_exp('/tmp/test.exp')
        Assertion.assert_equal(res, True, 'ERR: import exp file failed')

    def test_07_check_settings(self):
        param = {
            'version': "ipv6",
            'entries': "all",
            'type': "custom"
        }
        resp = nat_cli.show_natpolicy(**param)
        check_list = ['wan_to_lan', 'dmz_to_lan', 'lan_to_wan', 'wan_to_dmz']
        res = all(x in resp for x in check_list)
        Assertion.assert_equal(res, True, 'ERR: check settings failed.')

    def test_08_register_fw(self):
        for i in range(5):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_09_check_fun(self):
        out1 = pc1_login.send_command('ping6 2001::169 -c 5')
        out2 = pc2_login.send_command('ping6 2001::170 -c 5')
        res = '100% packet loss' not in out1 and '100% packet loss' not in out2
        Assertion.assert_equal(res, True, 'ERR: check v6 nat function failed')

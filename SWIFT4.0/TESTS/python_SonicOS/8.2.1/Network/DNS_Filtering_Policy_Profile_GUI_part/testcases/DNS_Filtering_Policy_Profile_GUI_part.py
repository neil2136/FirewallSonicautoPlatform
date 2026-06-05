from definition.settings import *


# Expected: Verify the default Action of DNS Policy is Proxy in CLI.
class TestSettings_1521074(Test):
    uuid = "SOSAIOT-TC-51461"
    description = show_testcase_info(TESTPLAN, '1521074', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521074')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_default_action_in_cli(self):
        rc_add = dnsPolicy_cli.add_dns_policy(**{'name': CParam.Name})
        logger.info(f'Add dns policy...... {rc_add}')
        rc_show = dnsPolicy_cli.show_dns_policy(name=CParam.Name)
        rc = 'action proxy' in str(rc_show) if rc_show else False
        Assertion.assert_equal(rc, True, "ERR: check_default_action_in_cli failed!!")

    def test_02_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify add a DNS Policies with with Action 'Proxy'.
class TestSettings_1521075(Test):
    uuid = "SOSAIOT-TC-51462"
    description = show_testcase_info(TESTPLAN, '1521075', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521075')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy_proxy(self):
        rc = dnsRule_api.add_dns_rule(**dns_proxy_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_proxy failed!!")

    def test_02_delete_added_dns_policy(self):
        rc = dnsRule_api.del_dns_rule_by_name(name=CParam.Name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify add a DNS Policies with with Action 'Filter'.
class TestSettings_1521076(Test):
    uuid = "SOSAIOT-TC-51463"
    description = show_testcase_info(TESTPLAN, '1521076', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521076')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy_filter(self):
        rc = dnsRule_api.add_dns_rule(**dns_filter_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_filter failed!!")

    def test_02_delete_added_dns_policy(self):
        rc = dnsRule_api.del_dns_rule_by_name(name=CParam.Name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify a duplicate DNS Policy can not be added.
class TestSettings_1521078(Test):
    uuid = "SOSAIOT-TC-51464"
    description = show_testcase_info(TESTPLAN, '1521078', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521078')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy_filter(self):
        rc = dnsRule_api.add_dns_rule(**dns_filter_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_filter failed!!")

    def test_02_add_duplicate_policy_name(self):
        res = dnsRule_api.add_dns_rule(msg=True, **dns_proxy_dict)
        logger.info(res)
        rc = 'already exist' in json.dumps(res[1]).lower() if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: add_duplicate_policy_name should fail!!")

    def test_03_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify the Max count of Policy entries is correct.
class TestBoundary_1521079(Test):
    uuid = "SOSAIOT-TC-51465"
    description = show_testcase_info(TESTPLAN, '1521079', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521079')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_get_max_count(self):
        diag_api.download_tsr()
        tsr_content = os.popen('cat /tmp/techSupport').read()
        start = '=======Misc : Product======='
        end = '=======Misc : DHCP Network Discovery Info======='
        pattern1 = start + '\n(.*)\n' + end
        match1 = re.search(r'' + pattern1 + '', tsr_content, re.I | re.S | re.M)
        if not match1:
            logger.error('Get Max Matrix TSR failed!!')
        else:
            match1 = match1.group(1)
            logger.info(match1)
            pat = 'max DNS Policies'
            match2 = re.search(r'' + pat + r':\s+?(\d+)', str(match1), re.I | re.S | re.M)
            logger.info(match2)
            value = int(match2.group(1)) if match2 and match2.group(1).isdigit() else 0
            CParam.Max_count = value
        Assertion.assert_equal(bool(CParam.Max_count), True, "ERR: get_max_count failed!!")

    def test_02_add_max_count_policies(self):
        rc = False
        policy = copy.deepcopy(dns_filter_dict)
        for count in range(CParam.Max_count):
            policy["dns_policies"][0]["name"] = f'{CParam.Name}_{count}'
            rc = dnsRule_api.add_dns_rule(**policy)
            if not rc:
                logger.error(f'Add dns policy {count} failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: add_max_count_policies failed!!")

    def test_03_add_one_more_policy_failed(self):
        res = dnsRule_api.add_dns_rule(msg=True, **dns_filter_dict)
        rc = 'DNS policy table is full' in json.dumps(res[1]) if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: add_one_more_policy should fail!!")

    def test_04_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify the Edit buttons of DNS Policy work.
class TestSettings_1521085(Test):
    uuid = "SOSAIOT-TC-51466"
    description = show_testcase_info(TESTPLAN, '1521085', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521085')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy(self):
        rc = dnsRule_api.add_dns_rule(**dns_filter_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_02_edit_dns_policy(self):
        edit = {
            "name": CParam.Name, 'new-name': 'Edit', "priority": {"manual": 1},
            "enable": False, "action": {'proxy': True},
            "comment": 'test', "schedule": {"name": "Work Hours"},
            "ticket": {'tag1': '1', 'tag2': '2', 'tag3': '3'},
            "source": {'address': {'name': 'X0 Subnet'}},
            "from": "DMZ", "service": {"name": "DNS (Name Service) TCP"},
            "max_connections": 90, "connection_limit": {"source": {"enable": True, "threshold": {"value": 100}}},
            "proxy_mode": "ipv4-ipv6"}
        rc = dnsRule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: edit_dns_policy failed!!")

    def test_03_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify the Max length of DNS Policy Name is 39 chars
class TestBoundary_1521086(Test):
    uuid = "SOSAIOT-TC-51467"
    description = show_testcase_info(TESTPLAN, '1521086', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521086')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy_with_name_max_length(self):
        max_name = copy.deepcopy(dns_filter_dict)
        max_name["dns_policies"][0]["name"] = '123456789012_Here_are_thirty_nine_words'
        rc = dnsRule_api.add_dns_rule(**max_name)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_with_name_max_length failed!!")

    def test_02_add_dns_policy_with_name_over_max_length_failed(self):
        invalid_name = copy.deepcopy(dns_filter_dict)
        invalid_name["dns_policies"][0]["name"] = '1234_Here_are_thirty_nine_plus_one_words'
        res = dnsRule_api.add_dns_rule(msg=True, **invalid_name)
        rc = 'Value or string length(40) out of bounds (min = 1, max = 39)' in json.dumps(
            res[1]) if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_with_name_over_max_length should be failed!!")

    def test_03_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify the default status of DNS Policy switch is enabled in GUI and CLI.
class TestSettings_1521093(Test):
    uuid = "SOSAIOT-TC-51473"
    description = show_testcase_info(TESTPLAN, '1521093', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521093')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_dns_policy_enable_api(self):
        enable = copy.deepcopy(dns_filter_dict)
        enable["dns_policies"][0].pop("enable")
        rc_add = dnsRule_api.add_dns_rule(**enable)
        logger.info(f'Add dns policy via api result...... {rc_add}')
        res = dnsRule_api.get_dns_rule_by_name(name=enable["dns_policies"][0]["name"])
        rc = res["dns_policies"][0].get("enable") if res and res.get("dns_policies") else False
        Assertion.assert_equal(rc, True, "ERR: check_dns_policy_enable_api failed!!")

    def test_02_check_dns_policy_enable_cli(self):
        rc_add = dnsPolicy_cli.add_dns_policy(**{'name': 'cli'})
        logger.info(f'Add dns policy via cli result...... {rc_add}')
        res = dnsPolicy_cli.show_dns_policy(name='cli')
        rc = 'no enable' not in res if res else False
        Assertion.assert_equal(rc, True, "ERR: check_dns_policy_enable_cli failed!!")

    def test_03_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify Enable the DNS Policy.
class TestSettings_1521094(Test):
    uuid = "SOSAIOT-TC-51474"
    description = show_testcase_info(TESTPLAN, '1521094', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521094')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy(self):
        policy = copy.deepcopy(dns_filter_dict)
        policy["dns_policies"][0]["enable"] = False
        rc = dnsRule_api.add_dns_rule(**policy)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_02_enable_dns_policy(self):
        edit = {"name": dns_filter_dict["dns_policies"][0]["name"], "enable": True}
        rc = dnsRule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: edit_dns_policy failed!!")

    def test_03_check_dns_policy_enable(self):
        res = dnsRule_api.get_dns_rule_by_name(name=dns_filter_dict["dns_policies"][0]["name"])
        rc = res["dns_policies"][0].get("enable") if res and res.get("dns_policies") else False
        Assertion.assert_equal(rc, True, "ERR: check_dns_policy_enable failed!!")

    def test_04_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify Disable the DNS Policy.
class TestSettings_1521095(Test):
    uuid = "SOSAIOT-TC-51475"
    description = show_testcase_info(TESTPLAN, '1521095', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521095')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy(self):
        rc = dnsRule_api.add_dns_rule(**dns_filter_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_02_disable_dns_policy(self):
        edit = {"name": dns_filter_dict["dns_policies"][0]["name"], "enable": False}
        rc = dnsRule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: edit_dns_policy failed!!")

    def test_03_check_dns_policy_disable(self):
        res = dnsRule_api.get_dns_rule_by_name(name=dns_filter_dict["dns_policies"][0]["name"])
        rc = res["dns_policies"][0].get("enable") is False if res and res.get("dns_policies") else False
        Assertion.assert_equal(rc, True, "ERR: check_dns_policy_disable failed!!")

    def test_04_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify the custom Schedule/Zone/Address Object bind to a DNS policy can not be deleted.
class TestError_1521098(Test):
    uuid = "SOSAIOT-TC-51477"
    description = show_testcase_info(TESTPLAN, '1521098', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521098')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_custom_zone(self):
        zone_api.delete_zone_object(name=custom_zone_dict["zones"][0]["name"])
        rc = zone_api.add_zone_object(**custom_zone_dict)
        Assertion.assert_equal(rc, True, "ERR: add_custom_zone failed!!")

    def test_02_add_custom_address_object(self):
        ao_api.del_ao_by_name(name=ao_dict["name"], version="ipv4")
        rc = ao_api.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, "ERR: add_custom_address_object failed!!")

    def test_03_add_custom_schedule(self):
        schedule_api.delete_schedule(name=schedule_dict["name"])
        rc = schedule_api.add_schedule(**schedule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_custom_schedule failed!!")

    def test_04_add_dns_policy(self):
        custom = {"from": custom_zone_dict["zones"][0]["name"],
                  "source": {"address": {"name": ao_dict["name"]}},
                  "schedule": {"name": schedule_dict["name"]}}
        policy = copy.deepcopy(dns_filter_dict)
        policy["dns_policies"][0].update(custom)
        rc = dnsRule_api.add_dns_rule(**policy)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_05_delete_custom_zone_failed(self):
        res = zone_api.delete_zone_object(name=custom_zone_dict["zones"][0]["name"], msg=True)
        rc = "This zone object is in used by a DNS policy" in json.dumps(
            res[1]) if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: delete_custom_zone should be failed!!")

    def test_06_delete_custom_address_object_failed(self):
        res = ao_api.del_ao_by_name(msg=True, name=ao_dict["name"], version="ipv4")
        rc = "This address object is in used by a DNS policy" in json.dumps(
            res[1]) if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: delete_custom_address_object should be failed!!")

    def test_07_delete_custom_schedule_failed(self):
        res = schedule_api.delete_schedule(name=schedule_dict["name"], msg=True)
        rc = "This schedule object is in used by a DNS policy" in json.dumps(
            res[1]) if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: delete_custom_schedule should be failed!!")

    def test_08_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify the Service drop-down box only support UDP protocol when Action is Filter.
class TestError_1521100(Test):
    uuid = "SOSAIOT-TC-51479"
    description = show_testcase_info(TESTPLAN, '1521100', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521100')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_filter_policy_with_invalid_service(self):
        rc = False
        policy = copy.deepcopy(dns_filter_dict)
        invalid_services = ({"name": "DNS (Name Service) TCP"}, {"group": "DNS (Name Service)"})
        for service in invalid_services:
            policy["dns_policies"][0]["name"] = str(service)
            policy["dns_policies"][0]["service"] = service
            res = dnsRule_api.add_dns_rule(msg=True, **policy)
            rc = "DNS policy service don't support" in json.dumps(
                res[1]) if res and len(res) >= 2 and not res[0] else False
            if not rc:
                logger.error(f'Config service <{str(service)}> to Filter Policy should be failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: add_filter_policy_with_invalid_service should be failed!!")

    def test_02_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify the connection thresholds settings.
class TestSettings_1521101(Test):
    uuid = "SOSAIOT-TC-51480"
    description = show_testcase_info(TESTPLAN, '1521101', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521101')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy_with_valid_connection_settings(self):
        connection_set = {
            "max_connections": 90,
            "connection_limit": {"source": {"enable": True, "threshold": {"value": 100}}}}
        policy = copy.deepcopy(dns_filter_dict)
        policy["dns_policies"][0].update(connection_set)
        rc = dnsRule_api.add_dns_rule(**policy)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_with_valid_connection_settings failed!!")

    def test_02_delete_added_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")


# Expected: [GUI] Verify Delete one DNS Policy.
class TestSettings_1521103(Test):
    uuid = "SOSAIOT-TC-51482"
    description = show_testcase_info(TESTPLAN, '1521103', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521103')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy(self):
        rc = dnsRule_api.add_dns_rule(**dns_filter_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_02_delete_dns_policy(self):
        rc = dnsRule_api.del_dns_rule_by_name(name=dns_filter_dict["dns_policies"][0]["name"])
        Assertion.assert_equal(rc, True, "ERR: delete_dns_policy failed!!")


# Expected: [GUI] Verify Delete Multiple DNS Policies.
class TestSettings_1521104(Test):
    uuid = "SOSAIOT-TC-51483"
    description = show_testcase_info(TESTPLAN, '1521104', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521104')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policies(self):
        rc = False
        policy = copy.deepcopy(dns_filter_dict)
        for count in range(3):
            policy["dns_policies"][0]["name"] = f'{CParam.Name}_{count}'
            rc = dnsRule_api.add_dns_rule(**policy)
            if not rc:
                logger.error(f'Add policy <{count}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: add_dns_policies failed!!")

    def test_02_delete_dns_policies(self):
        rc = False
        for count in range(3):
            rc = dnsRule_api.del_dns_rule_by_name(name=f'{CParam.Name}_{count}')
            if not rc:
                logger.error(f'Delete policy <{count}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: delete_dns_policies failed!!")


# Expected: [TSR] Verify DNS policies show correctly in TSR.
class TestSettings_1521110(Test):
    uuid = "SOSAIOT-TC-51488"
    description = show_testcase_info(TESTPLAN, '1521110', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521110')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy(self):
        rc = dnsRule_api.add_dns_rule(**dns_filter_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_02_check_tsr(self):
        out = diag_api.get_tsr_part(func='Firewall', lab1='DNS Policy Table')
        logger.info(f'TSR\n{out}')
        rc = dns_filter_dict["dns_policies"][0]["name"] in out
        Assertion.assert_equal(rc, True, "ERR: check_tsr failed!!")

    def test_03_delete_dns_policy(self):
        rc = dnsRule_api.del_dns_rule_by_name(name=dns_filter_dict["dns_policies"][0]["name"])
        Assertion.assert_equal(rc, True, "ERR: delete_dns_policy failed!!")


# Expected: [GUI] Verify the Default profile is provided with correct default status.
class TestSettings_1521022(Test):
    uuid = "SOSAIOT-TC-51489"
    description = show_testcase_info(TESTPLAN, '1521022', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521022')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_default_profile(self):
        res = dnsFilter_api.get_dns_filtering_profile_by_name(name=CParam.Profile)
        logger.info(f'Get Default Profile result...... {res}')
        rc = False
        try:
            action = json.loads(res['dns_security']['dns_filtering']['profile'][0]['actions']) if res else False
        except BaseException as e:
            logger.error(f'Get action dict failed!! \nerror msg :{e}')
        else:
            logger.info(f'Get action dict result...... {action}')
            default_profile_dict = {'1': 2, '2': 0, '3': 2, '4': 2, '5': 2, '6': 2, '7': 2, '8': 0, '9': 2,
                                    '10': 2, '11': 0, '12': 2, '13': 2, '14': 2, '15': 2, '16': 2, '17': 2, '18': 2, '19': 2}
            if action:
                for key, value in action.items():
                    rc = default_profile_dict.get(key) == value
                    if not rc:
                        logger.error(f'Check action <{key}:{value}> failed!!')
                        break
        Assertion.assert_equal(rc, True, "ERR: check_default_profile failed!!")


# Expected: [GUI] Verify the MAX number of profile entries is 1024.
class TestBoundary_1521127(Test):
    uuid = "SOSAIOT-TC-51499"
    description = show_testcase_info(TESTPLAN, '1521127', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521127')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_profiles_with_max_count(self):
        rc = False
        profile = copy.deepcopy(profile_dict)
        for count in range(1023):
            profile["dns_security"]["dns_filtering"]["profile"][0]["name"] = f"{CParam.Name}_{count}"
            rc = dnsFilter_api.add_dns_filtering_profile(**profile)
            if not rc:
                logger.error(f'Add profile <{count+1}> failed!!')
                break
            if not (count+1) % 100:
                time.sleep(2)
        Assertion.assert_equal(rc, True, "ERR: add_dns_profiles_with_max_count failed!!")

    def test_02_add_dns_profiles_over_max_count_failed(self):
        res = dnsFilter_api.add_dns_filtering_profile(msg=True, **profile_dict)
        rc = 'The DNS Filtering profiles reach max volume' in json.dumps(
            res[1]) if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: add_dns_profiles_over_max_count should be failed!!")

    def test_03_delete_added_dns_profiles(self):
        rc = dnsFilter_cli.delete_filtering_profile()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_profiles failed!!")


# Expected: [GUI] Verify the MAX length of profile name is 399, and the long name shows completely.
class TestBoundary_1521128(Test):
    uuid = "SOSAIOT-TC-51500"
    description = show_testcase_info(TESTPLAN, '1521128', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521128')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_profile_with_name_max_length(self):
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(399)]
        name = ''.join(str_list)
        profile = copy.deepcopy(profile_dict)
        profile["dns_security"]["dns_filtering"]["profile"][0]["name"] = name
        rc = dnsFilter_api.add_dns_filtering_profile(**profile)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_with_name_max_length failed!!")

    def test_02_add_dns_profile_with_name_over_max_length_failed(self):
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(400)]
        name = ''.join(str_list)
        profile = copy.deepcopy(profile_dict)
        profile["dns_security"]["dns_filtering"]["profile"][0]["name"] = name
        res = dnsFilter_api.add_dns_filtering_profile(msg=True, **profile)
        rc = 'Value or string length(400) out of bounds (max = 399)' in json.dumps(
            res[1]) if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_with_name_over_max_length should be failed!!")

    def test_03_delete_added_dns_profiles(self):
        rc = dnsFilter_cli.delete_filtering_profile()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_profiles failed!!")


# Expected: [GUI] Verify the Add button work on Profile.
class TestSettings_1521129(Test):
    uuid = "SOSAIOT-TC-51501"
    description = show_testcase_info(TESTPLAN, '1521129', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521129')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_profiles_name(self):
        profile = copy.deepcopy(profile_dict)
        profile["dns_security"]["dns_filtering"]["profile"][0]["name"] = 'NName_123!'
        rc = dnsFilter_api.add_dns_filtering_profile(**profile)
        Assertion.assert_equal(rc, True, "ERR: add_dns_profiles_name failed!!")

    def test_02_add_dns_profiles_action(self):
        action = "{\"1\":1,\"2\":0,\"3\":2,\"4\":3,\"5\":2,\"6\":3,\"7\":1,\"8\":0,\"9\":2,\"10\":1,\"11\":0,\"12\":3,\"13\":2,\"14\":0,\"15\":1,\"16\":1,\"17\":2,\"18\":0,\"19\":3}"
        profile = copy.deepcopy(profile_dict)
        profile["dns_security"]["dns_filtering"]["profile"][0]["action"] = action
        rc = dnsFilter_api.add_dns_filtering_profile(**profile)
        Assertion.assert_equal(rc, True, "ERR: add_dns_profiles_action failed!!")

    def test_03_delete_added_dns_profiles(self):
        rc = dnsFilter_cli.delete_filtering_profile()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_profiles failed!!")


# Expected: [GUI] Verify the Edit button work on Profile.
class TestSettings_1521130(Test):
    uuid = "SOSAIOT-TC-51502"
    description = show_testcase_info(TESTPLAN, '1521130', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521130')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_profiles(self):
        rc = dnsFilter_api.add_dns_filtering_profile(**profile_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_profiles failed!!")

    def test_02_edit_dns_profiles(self):
        profile = copy.deepcopy(profile_dict)
        edit = {
            "name": "Edit",
            "action": "{\"1\":1,\"2\":0,\"3\":2,\"4\":3,\"5\":2,\"6\":3,\"7\":1,\"8\":0,\"9\":2,\"10\":1,\"11\":0,\"12\":3,\"13\":2,\"14\":0,\"15\":1,\"16\":1,\"17\":2,\"18\":0,\"19\":3}"}
        profile["dns_security"]["dns_filtering"]["profile"][0].update(edit)
        rc = dnsFilter_api.edit_dns_profile_by_name(msg=False, name=CParam.Name, **profile)
        Assertion.assert_equal(rc, True, "ERR: add_dns_profiles_action failed!!")

    def test_03_delete_added_dns_profiles(self):
        rc = dnsFilter_cli.delete_filtering_profile()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_profiles failed!!")


# Expected: [GUI] Verify Add/Edit profile with duplicate name fail.
class TestError_1521131(Test):
    uuid = "SOSAIOT-TC-51503"
    description = show_testcase_info(TESTPLAN, '1521131', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521131')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_profile(self):
        rc = dnsFilter_api.add_dns_filtering_profile(**profile_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_profile failed!!")

    def test_02_add_duplicate_dns_profile_failed(self):
        res = dnsFilter_api.add_dns_filtering_profile(msg=True, **profile_dict)
        rc = 'already exist' in json.dumps(res[1]).lower() if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: add_duplicate_dns_profile should be failed!!")

    def test_03_edit_duplicate_dns_profile_failed(self):
        profile = copy.deepcopy(profile_dict)
        profile["dns_security"]["dns_filtering"]["profile"][0]["name"] = CParam.Profile
        res = dnsFilter_api.edit_dns_profile_by_name(msg=True, name=CParam.Name, **profile)
        rc = 'the profile default profile already exist' in json.dumps(
            res[1]).lower() if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: edit_duplicate_dns_profile should be failed!!")

    def test_04_delete_added_dns_profiles(self):
        rc = dnsFilter_cli.delete_filtering_profile()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_profiles failed!!")


# Expected: [GUI] Verify the Delete icon work on Profile.
class TestSettings_1521132(Test):
    uuid = "SOSAIOT-TC-51504"
    description = show_testcase_info(TESTPLAN, '1521132', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521132')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_profile(self):
        rc = dnsFilter_api.add_dns_filtering_profile(**profile_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_profile failed!!")

    def test_02_delete_added_dns_profile(self):
        rc = dnsFilter_api.del_dns_profile_by_name(name=CParam.Name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_profile failed!!")


# Expected: [GUI] Verify the Delete All button work on Profile.
class TestSettings_1521133(Test):
    uuid = "SOSAIOT-TC-51505"
    description = show_testcase_info(TESTPLAN, '1521133', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521133')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_profiles(self):
        rc = False
        profile = copy.deepcopy(profile_dict)
        for count in range(3):
            profile["dns_security"]["dns_filtering"]["profile"][0]["name"] = f'{CParam.Name}_{count}'
            rc = dnsFilter_api.add_dns_filtering_profile(**profile)
            if not rc:
                logger.error(f'Add policy <{count+1}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: add_dns_profiles failed!!")

    def test_02_delete_added_dns_profiles(self):
        rc = False
        for count in range(3):
            rc = dnsFilter_api.del_dns_profile_by_name(name=f'{CParam.Name}_{count}')
            if not rc:
                logger.error(f'Delete policy <{count+1}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_profiles failed!!")


# Expected: [GUI] Verify when a profile is binded to a DNS Policy, the profile can not be deleted.
class TestError_1521134(Test):
    uuid = "SOSAIOT-TC-51506"
    description = show_testcase_info(TESTPLAN, '1521134', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521134')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_profile(self):
        rc = dnsFilter_api.add_dns_filtering_profile(**profile_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_profile failed!!")

    def test_02_bind_dns_profile_to_policy(self):
        policy = copy.deepcopy(dns_filter_dict)
        policy["dns_policies"][0]["action"] = {"filter_profile": CParam.Name}
        rc = dnsRule_api.add_dns_rule(**policy)
        Assertion.assert_equal(rc, True, "ERR: bind_dns_profile_to_policy failed!!")

    def test_03_delete_bind_dns_profile(self):
        res = dnsFilter_api.del_dns_profile_by_name(name=CParam.Name, msg=True)
        rc = 'The target DNS Filtering Object test is in used by a DNS policy' in json.dumps(
            res[1]) if res and len(res) >= 2 and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: delete bind dns profile should be failed!!")

    def test_04_delete_dns_policy_and_profile(self):
        rc_policy = dnsRule_api.del_dns_rule_by_name(name=CParam.Name)
        logger.info(f'Delete dns policy result...... {rc_policy}')
        rc_profile = dnsFilter_api.del_dns_profile_by_name(name=CParam.Name)
        logger.info(f'Delete dns profile result...... {rc_profile}')
        rc = rc_policy and rc_profile
        Assertion.assert_equal(rc, True, "ERR: delete_dns_policy_and_profile should be failed!!")

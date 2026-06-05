from definition.settings import *


class Test_acl_auto_added(Test):
    uuid = "SOSAIOT-TC-51428"
    description = show_testcase_info(TESTPLAN, '1521080', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521080')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_dns_policies(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: clear all dns policies failed")

    def test_02_add_dns_filter_policy(self):
        rc = dnsRule_api.add_dns_rule(**filter_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_rule failed")

    def test_03_check_auto_added_acl(self):
        rc_check = acl_api.is_accessrule_exists(**check_acl_keys_dict)
        logger.info(f"Check auto added access rule ......{rc_check}")
        msg = ''
        if rc_check:
            _, msg = acl_api.delete_accessrule_by_json(msg=True, **check_acl_keys_dict)
        logger.info(msg)
        Assertion.assert_regular(str(msg), "Read only", "ERR: Not Allow to Delete auto added access rule!!")

    def test_04_clear_all_dns_policies(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: clear all dns policies failed")

    def test_05_add_dns_proxy_policy(self):
        rc = dnsRule_api.add_dns_rule(**proxy_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_proxy_rule failed")

    def test_06_check_auto_added_acl(self):
        rc_check = acl_api.is_accessrule_exists(**check_acl_keys_dict)
        logger.info(f"Check auto added access rule...... {rc_check}")
        msg = ''
        if rc_check:
            _, msg = acl_api.delete_accessrule_by_json(msg=True, **check_acl_keys_dict)
        logger.info(msg)
        Assertion.assert_regular(str(msg), "Read only", "ERR: Not Allow to Delete auto added access rule!!")


class Test_acl_not_changed(Test):
    uuid = "SOSAIOT-TC-51429"
    description = show_testcase_info(TESTPLAN, '1521081', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521081')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_dns_policies(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: clear all dns policies failed")

    def test_02_add_dns_filter_policy(self):
        rc = dnsRule_api.add_dns_rule(**filter_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_rule failed")

    def test_03_check_auto_added_acl(self):
        CParams.UUIDs = acl_api.get_access_rules_uuid_by_json(version="ipv4", **check_acl_keys_dict)
        Assertion.assert_equal(bool(CParams.UUIDs), True, "ERR: Check auto added access rule failed!!")

    def test_04_edit_dns_filter_policy(self):
        rc_action = dnsRule_api.edit_dns_rule(**edit_rule_dict)
        logger.info(f"Edit dns rule action result...... {rc_action}")
        rc_name = dnsRule_api.edit_dns_rule_name(name='Filter', new_name='Proxy')
        logger.info(f"Edit dns rule name result...... {rc_name}")
        Assertion.assert_equal(rc_action & rc_name, True, "ERR: edit_dns_filter_policy failed")

    def test_05_check_no_new_auto_added_acl(self):
        out = acl_api.get_access_rules_uuid_by_json(version="ipv4", **{"comment": "Auto rule for DNS policy"})
        rc = len(out) == len(CParams.UUIDs) if out else False
        Assertion.assert_equal(rc, True, "ERR: check_no_new_auto_added_acl failed!!")


class Test_acl_disable_enable(Test):
    uuid = "SOSAIOT-TC-51430"
    description = show_testcase_info(TESTPLAN, '1521082', description=True)['title']
    dns_rule_name = filter_rule_dict["dns_policies"][0]["name"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521082')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_dns_policies(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: clear all dns policies failed")

    def test_02_add_dns_filter_policy(self):
        rc = dnsRule_api.add_dns_rule(**filter_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_rule failed")

    def test_03_check_auto_added_acl(self):
        CParams.UUIDs = acl_api.get_access_rules_uuid_by_json(version="ipv4", **check_acl_keys_dict)
        Assertion.assert_equal(bool(CParams.UUIDs), True, "ERR: Check auto added access rule failed!!")

    def test_04_check_auto_added_acl_disabled(self):
        rc = False
        if CParams.UUIDs:
            disable = {
                "name": self.dns_rule_name,
                "enable": False
            }
            rc_disable = dnsRule_api.edit_dns_rule(**disable)
            logger.info(f"Disable dns rule result...... {rc_disable}")
            rc = acl_api.is_accessrule_exists(**{"uuid": CParams.UUIDs[0], "enable": False})
        Assertion.assert_equal(rc, True, "ERR: Check auto added access rule disable failed!!")

    def test_05_add_new_enabled_dns_policy_and_check_acl_enabled(self):
        rc = False
        if CParams.UUIDs:
            rc_add_enable = dnsRule_api.add_dns_rule(**proxy_rule_dict)
            logger.info(f"Add enabled dns proxy rule result...... {rc_add_enable}")
            rc = acl_api.is_accessrule_exists(**{"uuid": CParams.UUIDs[0], "enable": True})
        Assertion.assert_equal(rc, True, "ERR: add_new_enabled_dns_proxy_policy_and_check_acl_enabled failed")

    def test_06_disable_dns_proxy_policy_and_check(self):
        self.dns_rule_name = proxy_rule_dict["dns_policies"][0]["name"]
        self.test_04_check_auto_added_acl_disabled()


class Test_acl_deleted(Test):
    uuid = "SOSAIOT-TC-51431"
    description = show_testcase_info(TESTPLAN, '1521083', description=True)['title']
    dns_rule_name = filter_rule_dict["dns_policies"][0]["name"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521083')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_dns_policies(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: clear all dns policies failed")

    def test_02_add_dns_filter_policy(self):
        rc = dnsRule_api.add_dns_rule(**filter_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_rule failed")

    def test_03_check_auto_added_acl(self):
        rc = acl_api.is_accessrule_exists(**check_acl_keys_dict)
        Assertion.assert_equal(rc, True, "ERR: Check auto added access rule failed!!")

    def test_04_check_auto_added_acl_deleted(self):
        rc_delete = dnsRule_api.del_dns_rule_by_name(name=self.dns_rule_name)
        logger.info(f"Delete dns rule result...... {rc_delete}")
        rc = not acl_api.is_accessrule_exists(**check_acl_keys_dict)
        Assertion.assert_equal(rc, True, "ERR: Check auto added access rule deleted failed!!")

    def test_05_add_new_dns_policies_and_check_acl(self):
        rc_filter = dnsRule_api.add_dns_rule(**filter_rule_dict)
        logger.info(f"Add dns filter rule result...... {rc_filter}")
        rc_proxy = dnsRule_api.add_dns_rule(**proxy_rule_dict)
        logger.info(f"Add dns proxy rule result...... {rc_proxy}")
        self.test_03_check_auto_added_acl()

    def test_06_delete_dns_filter_policy_and_check_acl_displayed(self):
        rc_delete = dnsRule_api.del_dns_rule_by_name(name=self.dns_rule_name)
        logger.info(f"Delete dns rule result...... {rc_delete}")
        rc = acl_api.is_accessrule_exists(**check_acl_keys_dict)
        Assertion.assert_equal(rc, True, "ERR: Check auto added access rule displayed failed!!")

    def test_07_delete_dns_proxy_policy_and_check_acl_deleted(self):
        self.dns_rule_name = proxy_rule_dict["dns_policies"][0]["name"]
        self.test_04_check_auto_added_acl_deleted()


class Test_acl_changes(Test):
    uuid = "SOSAIOT-TC-51432"
    description = show_testcase_info(TESTPLAN, '1521084', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521084')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_dns_policies(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: clear all dns policies failed")

    def test_02_add_dns_filter_policy(self):
        rc = dnsRule_api.add_dns_rule(**filter_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_rule failed")

    def test_03_add_dns_proxy_policy(self):
        rc = dnsRule_api.add_dns_rule(**proxy_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_proxy_rule failed")

    def test_04_check_auto_added_acl(self):
        rc = acl_api.find_access_rules_by_json(**{"comment": "Auto rule for DNS policy"})
        Assertion.assert_equal(len(rc), 1, "ERR: Check auto added access rule failed!!")

    def test_05_edit_dns_proxy_policy_and_check_new_added_acl(self):
        edit = {
            "name": proxy_rule_dict["dns_policies"][0]["name"],
            "from": "DMZ",
            "source": {"address": {"name": "X2 Subnet"}}
        }
        rc_edit = dnsRule_api.edit_dns_rule(**edit)
        logger.info(f"Edit dns rule result...... {rc_edit}")
        rc = acl_api.find_access_rules_by_json(**{"comment": "Auto rule for DNS policy"})
        Assertion.assert_equal(len(rc), 2, "ERR: Check new auto added access rule failed!!")

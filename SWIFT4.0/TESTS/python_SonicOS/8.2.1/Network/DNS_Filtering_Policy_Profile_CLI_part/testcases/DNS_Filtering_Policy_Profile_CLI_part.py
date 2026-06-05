from definition.settings import *


# Expected: When the profile name is a duplicate name, the Edit action failed via CLI Commends
class Test_duplicate_profile(Test):
    uuid = "SOSAIOT-TC-51442"
    # uuid = '68333034-8641-11EB-826C-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521138', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521138')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_a_profile(self):
        rc = dnsFilter_cli.add_filtering_profile(**{'name': CParam.Profile_Name})
        Assertion.assert_equal(rc, True, "ERR: Add_profile_use_CLI failed!")

    def test_02_duplicate_name_check(self):
        rc = dnsFilter_cli.edit_filtering_profile(
            tag=1, **{'name': CParam.Profile_Name, 'name-new': 'Default Profile'})[1]
        Assertion.assert_regular(str(rc), 'Error: The profile Default Profile already existed',
                                 "ERR: Should not to use duplicate profile name!")

    def test_03_delete_the_added_profile(self):
        rc = dnsFilter_cli.delete_filtering_profile(name=CParam.Profile_Name)
        Assertion.assert_equal(rc, True, "ERR: delete_the_added_profile failed!")


class Test_show_profiles(Test):
    uuid = "SOSAIOT-TC-51445"
    # uuid = 'FCC64D6E-863F-11EB-8339-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521141', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521141')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_a_profile(self):
        rc = dnsFilter_cli.add_filtering_profile(**{'name': CParam.Before_Name})
        Assertion.assert_equal(rc, True, "ERR: Add_profile_use_CLI failed!")

    def test_02_edit_the_profile(self):
        editP = {
            'name': CParam.Before_Name,
            'name-new': CParam.Profile_Name,
            'category': ['1.\ Adult forge-ip-reply']
        }
        rc = dnsFilter_cli.edit_filtering_profile(**editP)
        Assertion.assert_equal(rc, True, "ERR: Edit_profile_use_CLI failed.")

    def test_03_show_the_profile_by_name(self):
        out = dnsFilter_cli.show_filtering_profile(name=CParam.Profile_Name)
        logger.info(out)
        ekey = (f'name {CParam.Profile_Name}', 'category "1. Adult" forge-ip-reply')
        rc = [x in str(out) for x in ekey]
        logger.info(f'founded in show result [name, category] : {rc}')
        Assertion.assert_equal(all(rc), True, "ERR: show_the_profile_by_name failed.")

    def test_04_delete_the_added_profile(self):
        rc = dnsFilter_cli.delete_filtering_profile(name=CParam.Profile_Name)
        Assertion.assert_equal(rc, True, "ERR: delete_the_added_profile failed!")

    def test_05_show_the_profiles(self):
        out = dnsFilter_cli.show_filtering_profile()
        logger.info(out)
        rc = 'Default Profile' in str(out) and f'name {CParam.Before_Name}' not in str(out)
        Assertion.assert_equal(rc, True, "ERR: show_the_profiles failed.")


class Test_add_dns_proxy_policy(Test):
    uuid = "SOSAIOT-TC-51447"
    # uuid = 'B6615294-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521111', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521111')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_proxy_policy(self):
        proxy = {
            'name': CParam.Proxy_Name,
            'action': 'proxy',
            'proxy-mode': 'ipv4-ipv6',
            'from': 'LAN',
            'comment': 'TestProxy'
        }
        rc = dnsPolicy_cli.add_dns_policy(**proxy)
        Assertion.assert_equal(rc, True, "ERR: add_dns_proxy_policy failed!")


class Test_add_dns_filter_policy(Test):
    uuid = "SOSAIOT-TC-51448"
    # uuid = 'B663A1C0-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521112', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521112')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_filter_policy(self):
        filtering = {
            'name': CParam.Filter_Name,
            'action': 'filter-profile "Default Profile"',
            'priority': 'manual 1',
            'source': 'address name "X0 Subnet"',
            'service': 'name "DNS (Name Service) UDP"',
            'ticket': 'tag1 forfiltering'
        }
        rc = dnsPolicy_cli.add_dns_policy(**filtering)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_policy failed!")


class Test_edit_dns_policy(Test):
    uuid = "SOSAIOT-TC-51449"
    # uuid = 'B6679424-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521114', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521114')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_policy(self):
        rc = dnsPolicy_cli.add_dns_policy(**{'name': CParam.Before_Name})
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_policy failed!")

    def test_02_edit_dns_policy(self):
        edit = {
            'name': CParam.Before_Name,
            'name-new': CParam.Edit_Name,
            'schedule': 'name "Work Hours"',
            'priority': 'end',
        }
        rc = dnsPolicy_cli.edit_dns_policy(**edit)
        Assertion.assert_equal(rc, True, "ERR: edit_dns_policy failed!")


class Test_disable_dns_policy(Test):
    uuid = "SOSAIOT-TC-51451"
    # uuid = 'B66B631A-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521116', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521116')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_dns_policy(self):
        disable = {
            'name': CParam.Filter_Name,
            'enable': False
        }
        rc = dnsPolicy_cli.edit_dns_policy(**disable)
        Assertion.assert_equal(rc, True, "ERR: disable_dns_policy failed!")

    def test_02_check_disable(self):
        rc = dnsPolicy_cli.show_dns_policy(name=CParam.Filter_Name)
        logger.info(rc)
        Assertion.assert_regular(str(rc), 'no enable', "ERR: check_disable result failed!")


class Test_enable_dns_policy(Test):
    uuid = "SOSAIOT-TC-51450"
    # uuid = 'B6696BBE-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521115', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521115')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_dns_policy(self):
        enable = {
            'name': CParam.Filter_Name,
            'enable': True
        }
        rc = dnsPolicy_cli.edit_dns_policy(**enable)
        Assertion.assert_equal(rc, True, "ERR: enable_dns_policy failed!")

    def test_02_check_enable_result(self):
        rc = dnsPolicy_cli.show_dns_policy(name=CParam.Filter_Name)
        logger.info(rc)
        Assertion.assert_not_regular(str(rc), 'no enable', "ERR: check_enable result failed!")


class Test_config_conn_limit_and_max_conn(Test):
    uuid = "SOSAIOT-TC-51454"
    # uuid = 'B671D560-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521119', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521119')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_policy(self):
        conn = {
            'name': CParam.Conn_Name,
            'connection-limit-enable': True,
            'connection-limit-threshold': '999',
            'max-connections': '50'
        }
        rc = dnsPolicy_cli.add_dns_policy(**conn)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_policy failed!")

    def test_02_check_edit_result(self):
        out = dnsPolicy_cli.show_dns_policy(name=CParam.Conn_Name)
        ekey = ('max-connections 50', 'connection-limit source enable', 'connection-limit source threshold 999')
        rc = [x in out for x in ekey]
        logger.info(f'founded in show result [max, enable, threshold] : {rc}')
        Assertion.assert_equal(all(rc), True, "ERR: check_edit_result failed!")


class Test_clone_policy(Test):
    uuid = "SOSAIOT-TC-51455"
    # uuid = 'B67410FA-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521120', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521120')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_and_clone_dns_policy(self):
        rc = dnsPolicy_cli.add_dns_policy(**{'name': CParam.Before_Name})
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_policy failed!")

    def test_02_clone_dns_policy(self):
        clone = {
            'name': CParam.Before_Name,
            'new-name': CParam.Clone_Name,
            'location': 'before'
        }
        rc = dnsPolicy_cli.clone_dns_policy(**clone)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_policy failed!")


class Test_show_dns_policy(Test):
    uuid = "SOSAIOT-TC-51456"
    # uuid = 'B6760568-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521121', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521121')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_one_dns_policy(self):
        rc = dnsPolicy_cli.show_dns_policy(name=CParam.Filter_Name)
        Assertion.assert_regular(str(rc), f'name {CParam.Filter_Name}', "ERR: show_one_dns_policy failed!")

    def test_02_show_multiple_dns_policies(self):
        out = dnsPolicy_cli.show_dns_policy()
        ekey = (CParam.Proxy_Name, CParam.Filter_Name, CParam.Edit_Name, CParam.Conn_Name, CParam.Clone_Name)
        rc = [x in str(out) for x in ekey]
        logger.info(f'founded in show result [Proxy, Filter, Edit, Conn, Clone] : {rc}')
        Assertion.assert_equal(all(rc), True, "ERR: show_multiple_dns_policies failed!")


class Test_delete_one_dns_policy(Test):
    uuid = "SOSAIOT-TC-51452"
    # uuid = 'B66D5F30-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521117', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521117')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_one_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy(name=CParam.Filter_Name)
        Assertion.assert_equal(rc, True, "ERR: delete_one_dns_policy failed!")

    def test_02_check_delete_result(self):
        rc = dnsPolicy_cli.show_dns_policy(name=CParam.Filter_Name)
        Assertion.assert_regular(str(rc), 'No matching command found', "ERR: check_delete_result failed!")


class Test_delete_all_dns_policy(Test):
    uuid = "SOSAIOT-TC-51453"
    # uuid = 'B66FE804-4CFD-11EC-8A9D-A562918F55E4'
    description = show_testcase_info(TESTPLAN, '1521118', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521118')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_all_dns_policy(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_all_dns_policy failed!")

    def test_02_check_delete_result(self):
        out = dnsPolicy_cli.show_dns_policy()
        ekey = (CParam.Proxy_Name, CParam.Edit_Name, CParam.Conn_Name, CParam.Clone_Name)
        rc = [x not in str(out) for x in ekey]
        logger.info(f'founded in show result [Proxy, Edit, Conn, Clone] : {rc}')
        Assertion.assert_equal(all(rc), True, "ERR: check_delete_result failed!")

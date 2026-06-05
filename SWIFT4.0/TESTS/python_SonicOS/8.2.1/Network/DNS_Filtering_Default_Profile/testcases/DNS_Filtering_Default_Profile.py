from definition.settings import *


class TestDNS_Filtering_Default_Profile_03(Test):
    uuid = "SOSAIOT-TC-51491"
    description= show_testcase_info(Parameter.TESTPLAN, '003', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '003')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Edit_the_category_actions_in_Default_profile(self):
        rc = dns_filtering_obj.config_dns_filtering_profile(**edit_file)
        Assertion.assert_equal(rc, True, "ERR: Edit_the_category_actions_in_Default_profile failed")


class TestDNS_Filtering_Default_Profile_04(Test):
    uuid = "SOSAIOT-TC-51492"
    description= show_testcase_info(Parameter.TESTPLAN, '004', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '004')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Edit_the_name_of_Default_profile(self):
        rc = dns_filtering_obj.edit_dns_profile_by_name('Default Profile', msg=True, **edit_file_04)
        Assertion.assert_regular(str(rc), 'True', "ERR: Cannot Edit_the_category_actions_in_Default_profile.")


class TestDNS_Filtering_Default_Profile_05(Test):
    uuid = "SOSAIOT-TC-51493"
    description= show_testcase_info(Parameter.TESTPLAN, '005', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '004')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_Default_profile(self):
        rc = dns_filtering_obj.del_dns_profile_by_name('Default Profile', msg=True)
        logger.info(rc)
        out = rc[1]['status']['info'][0]['message']
        logger.info(out)
        Assertion.assert_regular(out, 'The target DNS Filtering Object Default Profile is not allowed to change name or delete', "ERR: Cannot Edit_the_category_actions_in_Default_profile.")


class TestDNS_Filtering_Default_Profile_06(Test):
    uuid = "SOSAIOT-TC-51437"
    description= show_testcase_info(Parameter.TESTPLAN, '006', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '006')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Edit_the_category_actions_in_Default_profile_use_CLI(self):
        rc = fw_cli.do_cli_commands(cmds_06)
        Assertion.assert_equal(rc, True, "ERR: Edit_the_category_actions_in_Default_profile use CLI failed")


class TestDNS_Filtering_Default_Profile_07(Test):
    uuid = "SOSAIOT-TC-51438"
    description= show_testcase_info(Parameter.TESTPLAN, '007', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '007')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Edit_the_name_of_Default_profile_use_CLI(self):
        rc = fw_cli.do_cli_commands(cmds_07, tag=1)
        logger.info(rc)
        Assertion.assert_regular(str(rc), 'Error: Read only', "ERR: Cannot Edit_the_name_of_Default_profile use CLI.")  


class TestDNS_Filtering_Default_Profile_08(Test):
    uuid = "SOSAIOT-TC-51439"
    description= show_testcase_info(Parameter.TESTPLAN, '008', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '008')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Del_Default_profile_use_cli(self):
        rc = fw_cli.do_cli_commands(cmds_08, tag=1)
        logger.info(rc)
        Assertion.assert_regular(str(rc), r'The target DNS Filtering Object Default Profile is not allowed to.*?change name or delete', "ERR: Cannot Del_Default_profile_use_cli.")





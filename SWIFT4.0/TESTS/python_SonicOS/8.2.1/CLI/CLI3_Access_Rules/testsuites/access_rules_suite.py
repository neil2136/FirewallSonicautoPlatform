import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Access_Rules')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Access_Rules/definition')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Access_Rules/testcases')


def suite():
    testcases_list = [
        # 'config.init_testbed.TestRestoreDUT',
        # 'config.init_testbed.TestUploadFirmware',
        # 'conf_fw',
        # 'access_rules.Test_ACLUUIDTests',
        'access_rules.Test_17_access_rule_comment_check',
        # 'access_rules.Test_02_access_rule_uuid_check',
        # 'access_rules.Test_01_access_rule_from_check',
        # 'access_rules.Test_05_access_rule_to_check',
        # 'access_rules.Test_07_access_rule_source_check',
        # 'access_rules.Test_08_access_rule_destination_check',
        # 'access_rules.Test_09_access_rule_service_check',
        # 'access_rules.Test_10_access_rule_action_check',
        # 'access_rules.Test_11_access_rule_user_check',
        # 'access_rules.Test_ACLNonUUIDTests',
        # 'access_rules.Test_18_access_rule_enable_check',
        # 'access_rules.Test_04_access_rule_modify_check',
        # 'access_rules.Test_13_access_rule_flow_report_check',
        # 'access_rules.Test_15_access_rule_botnet_filter_check',
        # 'access_rules.Test_06_access_rule_priority_check',
        # 'access_rules.Test_03_access_rule_restore_defaults_check'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    # author name
    to_users = 'lezhang@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()

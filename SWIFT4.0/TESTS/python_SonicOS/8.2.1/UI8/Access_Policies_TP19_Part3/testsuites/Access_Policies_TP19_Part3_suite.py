# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/UI8')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/UI8/Access_Policies_TP19_Part3')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'bin.init_resource.FWConfigure',
        'definition.init_fw_configure.TestConfigFW',
        # 'definition.init_fw_configure.TestConfigFW.test_02_get_default_policy_uuid', # debug
        # 'definition.init_fw_configure.TestConfigFW.test_03_get_default_policy_name', # debug
        'testcases.Access_Policies_TP19_Part3.TestACL_1520972',
        'testcases.Access_Policies_TP19_Part3.TestACL_1526085',
        'testcases.Access_Policies_TP19_Part3.Test_access_rule_details',
        'testcases.Access_Policies_TP19_Part3.TestAccess_rule_details_001',
        'testcases.Access_Policies_TP19_Part3.TestAccess_rule_details_002',
        'testcases.Access_Policies_TP19_Part3.TestAccess_rule_details_003',
        'testcases.Access_Policies_TP19_Part3.TestACL_1526088',
        'testcases.Access_Policies_TP19_Part3.Test_top_bar_buttons',
        'testcases.Access_Policies_TP19_Part3.TestTop_bar_buttons_001',
        'testcases.Access_Policies_TP19_Part3.TestTop_bar_buttons_002',
        'testcases.Access_Policies_TP19_Part3.TestTop_bar_buttons_003',
        'testcases.Access_Policies_TP19_Part3.TestACL_1552687',
        'testcases.Access_Policies_TP19_Part3.TestACL_1526099',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

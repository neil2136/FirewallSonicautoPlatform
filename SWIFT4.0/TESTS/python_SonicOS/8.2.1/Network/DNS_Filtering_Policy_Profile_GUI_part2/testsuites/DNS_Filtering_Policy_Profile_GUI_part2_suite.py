# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Policy_Profile_GUI_part2')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_configure.TestConfigFW',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_1521109',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.Test_Policy_Page',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_Page_001',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_Page_002',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_Page_003',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_Page_004',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestInit',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_1521088',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_1521092',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_1521097',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_1521099',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_1521105',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_1521107',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestPolicy_1521108',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.Test_Profile_Page',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestProfile_Page_001',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestProfile_Page_002',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestProfile_Page_003',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestProfile_Page_004',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestProfile_Page_005',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part2.TestProfile_1521124',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

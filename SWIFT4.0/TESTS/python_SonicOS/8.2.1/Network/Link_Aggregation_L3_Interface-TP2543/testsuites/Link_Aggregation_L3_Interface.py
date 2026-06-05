import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Network/Link_Aggregation_L3_Interface-TP2543")

'''
 ****add single test case to test suite****
 ****add test cases by module ****
'''
def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUTByUI',
        'config.init_testbed.TestUploadFirmware',
        'testcases.Link_Aggregation_L3_Interface.Test_1_Configure_Link_Aggregation',
        'testcases.Link_Aggregation_L3_Interface.Test_3_Management_on_LAG_Interface',
        'testcases.Link_Aggregation_L3_Interface.Test_11_Traffic_Across_Aggregation_LAN',
        'testcases.Link_Aggregation_L3_Interface.Test_12_Traffic_Across_Aggregation_WAN'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'sgao@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()


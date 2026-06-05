import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Network/Multicast_283")

'''
 ****add single test case to test suite****
 ****add test cases by module ****
'''
def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUTByUI',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_env.TestInitConfig',
        'testcases.Multicast_283.Test_12_Multicast_IGMP_State_Table_Timeout_Working_Properly',
        'testcases.Multicast_283.Test_16_Disable_Multicast_at_Multicast_Page_Disable_All_Multicast_Data_Reception',
        'testcases.Multicast_283.Test_17_Disable_Multicast_on_Interface_Disable_Multicast_Reception_on_Interface'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'sgao@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()


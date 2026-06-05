import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Invalidate_Local_User_Passwords')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Invalidate_Local_User_Passwords/testcases')
print(sys.path)

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',

        'invalidated_user_tc.TC01_Invalidated_User',
        'invalidated_user_tc.TC02_Invalidated_User',
        'invalidated_user_tc.TC03_Invalidated_User',
        'invalidated_user_tc.TC04_Invalidated_User',
        'invalidated_user_tc.TC05_Invalidated_User',
        'invalidated_user_tc.TC06_Invalidated_User',
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Lockout_User_Accounts')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_01',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_02',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_03',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_04',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_05',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_06',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_07',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_08',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_09',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_10',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_11',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_12',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_13',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_14',
        'testcases.Lockout_User_Accounts_tc.Test_Lockout_User_Accounts_15',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

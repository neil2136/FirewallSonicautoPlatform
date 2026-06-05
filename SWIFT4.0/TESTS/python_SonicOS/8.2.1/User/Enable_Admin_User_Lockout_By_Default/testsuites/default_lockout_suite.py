# __author__ = Rohit Sahu
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Enable_Admin_User_Lockout_By_Default')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Enable_Admin_User_Lockout_By_Default/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigTB',
        'default_lockout.TC01_Lockout_Enabled_By_Default',
        'default_lockout.TC02_Disable_Lockout_Warning',
        'default_lockout.TC03_Warning_When_Lockout_disabled',
        'default_lockout.TC04_User_lockout_funtionality',
        'default_lockout.TC05_Max_Login_Attempts_Using_CLI',
        'default_lockout.TC06_other_Admin_Users_Lockout',
        'default_lockout.TC07_Import_Configuration_File'

        
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
# __author__ = Rohit Sahu
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Stronger_Password_Requirement_By_Default')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Stronger_Password_Requirement_By_Default/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigTB',
        'testcases.TC_01_Enforce_Psw_Complexity_By_Default',
        'testcases.TC_02_Import_Configuration_File',
        'testcases.TC_03_All_Admin_Users_Creation',
        'testcases.TC_04_All_Users_login'
        
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
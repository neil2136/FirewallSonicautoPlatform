import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Combinations')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Auth_Combinations/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
         'config.init_testbed.TestRestoreDUT',
         'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigFW',
        'auth_combinations.TC01_Auth_combinations',
        'auth_combinations.TC02_Auth_combinations',
        'auth_combinations.TC03_Auth_combinations',
        'auth_combinations.TC04_Auth_combinations',
        'auth_combinations.TC05_Auth_combinations',
        'auth_combinations.TC06_Auth_combinations',
        'auth_combinations.TC07_Auth_combinations',
        'auth_combinations.TC08_Auth_combinations',
        'auth_combinations.TC09_Auth_combinations',
        'auth_combinations.TC10_Auth_combinations',
        'auth_combinations.TC11_Auth_combinations',
        'auth_combinations.TC12_Auth_combinations',
        'auth_combinations.TC13_Auth_combinations',
        'auth_combinations.TC14_Auth_combinations',
        'auth_combinations.TC15_Auth_combinations',
        'auth_combinations.TC16_Auth_combinations',
        'auth_combinations.TC17_Auth_combinations',
        'auth_combinations.TC18_Auth_combinations',
        'auth_combinations.TC19_Auth_combinations',
        'auth_combinations.TC20_Auth_combinations',
        'auth_combinations.TC21_Auth_combinations',
        'auth_combinations.TC22_Auth_combinations',
        'auth_combinations.TC23_Auth_combinations',
        'auth_combinations.TC24_Auth_combinations',
        'auth_combinations.TC25_Auth_combinations',
        'auth_combinations.TC26_Auth_combinations',
        'auth_combinations.TC27_Auth_combinations',
        'auth_combinations.TC28_Auth_combinations'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites



if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()


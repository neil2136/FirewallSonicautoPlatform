import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Combinations')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Combinations/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigFW',
        'auth_combinations_2.NonTC_installnx',
        'auth_combinations_2.TC29_Auth_combinations',
        'auth_combinations_2.TC30_Auth_combinations',
        'auth_combinations_2.TC31_Auth_combinations',
        'auth_combinations_2.TC32_Auth_combinations',
        'auth_combinations_2.TC33_Auth_combinations',
        'auth_combinations_2.TC34_Auth_combinations',
        'auth_combinations_2.TC35_Auth_combinations',
        'auth_combinations_2.TC36_Auth_combinations',
        'auth_combinations_2.TC37_Auth_combinations',
        'auth_combinations_2.TC38_Auth_combinations',
        'auth_combinations_2.TC39_Auth_combinations',
        'auth_combinations_2.TC40_Auth_combinations',
        'auth_combinations_2.TC41_Auth_combinations',
        'auth_combinations_2.TC42_Auth_combinations'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'sthaticherla@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()

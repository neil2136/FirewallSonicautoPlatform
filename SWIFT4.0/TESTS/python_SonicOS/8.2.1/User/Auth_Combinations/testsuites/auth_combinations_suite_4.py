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
        'auth_combinations_4.NonTC_installnx',
        'auth_combinations_4.TC057_Auth_combinations',
        'auth_combinations_4.TC058_Auth_combinations',
        'auth_combinations_4.TC059_Auth_combinations',
        'auth_combinations_4.TC060_Auth_combinations',
        'auth_combinations_4.TC061_Auth_combinations',
        'auth_combinations_4.TC062_Auth_combinations',
        'auth_combinations_4.TC063_Auth_combinations',
        'auth_combinations_4.TC064_Auth_combinations',
        'auth_combinations_4.TC065_Auth_combinations',
        'auth_combinations_4.TC066_Auth_combinations',
        'auth_combinations_4.TC067_Auth_combinations',
        'auth_combinations_4.TC068_Auth_combinations',
        'auth_combinations_4.TC069_Auth_combinations',
        'auth_combinations_4.TC070_Auth_combinations',
        'auth_combinations_4.TC071_Auth_combinations',
        'auth_combinations_4.TC072_Auth_combinations',
        'auth_combinations_4.TC073_Auth_combinations',
        'auth_combinations_4.TC074_Auth_combinations'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'sthaticherla@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()
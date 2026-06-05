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
        'auth_combinations_3.TC001_Ula_Auth_combinations',
        'auth_combinations_3.TC043_Auth_combinations',
        'auth_combinations_3.TC044_Auth_combinations',
        'auth_combinations_3.TC045_Auth_combinations',
        'auth_combinations_3.TC046_Auth_combinations',
        'auth_combinations_3.TC047_Auth_combinations',
        'auth_combinations_3.TC048_Auth_combinations',
        'auth_combinations_3.TC049_Auth_combinations',
        'auth_combinations_3.TC050_Auth_combinations',
        'auth_combinations_3.TC051_Auth_combinations',
        'auth_combinations_3.TC052_Auth_combinations',
        'auth_combinations_3.TC053_Auth_combinations',
        'auth_combinations_3.TC054_Auth_combinations',
        'auth_combinations_3.TC055_Auth_combinations',
        'auth_combinations_3.TC056_Auth_combinations'

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites



if __name__ == '__main__':
    to_users = 'sthaticherla@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()


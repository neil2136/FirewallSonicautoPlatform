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
        'auth_combinations_5.TC001_Ula_Auth_combinations',
        'auth_combinations_5.TC075_Auth_combinations',
        'auth_combinations_5.TC076_Auth_combinations',
        'auth_combinations_5.TC077_Auth_combinations',
        'auth_combinations_5.TC078_Auth_combinations',
        'auth_combinations_5.TC079_Auth_combinations',
        'auth_combinations_5.TC080_Auth_combinations'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites



if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()


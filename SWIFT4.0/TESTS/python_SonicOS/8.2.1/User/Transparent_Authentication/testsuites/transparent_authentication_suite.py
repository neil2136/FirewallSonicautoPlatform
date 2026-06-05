import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Transparent_Authentication')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Transparent_Authentication/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'transparent_authentication.TC_01_transparent_authentication',
        'transparent_authentication.TC_02_transparent_authentication',
        'transparent_authentication.TC_03_transparent_authentication',
        'transparent_authentication.TC_04_transparent_authentication',
        'transparent_authentication.TC_05_transparent_authentication',
        'transparent_authentication.TC_06_transparent_authentication',
        'transparent_authentication.TC_07_transparent_authentication',
        'transparent_authentication.TC_08_transparent_authentication',
        'transparent_authentication.TC_09_transparent_authentication',
        'transparent_authentication.TC_10_transparent_authentication',
        'transparent_authentication.TC_11_transparent_authentication',
        'transparent_authentication.TC_12_transparent_authentication',
        'transparent_authentication.TC_13_transparent_authentication',
        'transparent_authentication.TC_14_transparent_authentication',
        # 'transparent_authentication.TC_15_transparent_authentication',
        'transparent_authentication.TC_16_transparent_authentication',
        'transparent_authentication.TC_17_transparent_authentication',
        # 'transparent_authentication.TC_18_transparent_authentication',
        'transparent_authentication.TC_19_transparent_authentication',
        'transparent_authentication.TC_20_transparent_authentication',
        'transparent_authentication.TC_21_transparent_authentication',
        'transparent_authentication.TC_22_transparent_authentication',
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

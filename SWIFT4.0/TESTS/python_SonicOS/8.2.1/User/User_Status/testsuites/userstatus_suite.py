import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/User_Status')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/User_Status/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',

        'userstatus.TC01_GET_User_Management',
        'userstatus.TC02_PUT_User_Management'
     
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()


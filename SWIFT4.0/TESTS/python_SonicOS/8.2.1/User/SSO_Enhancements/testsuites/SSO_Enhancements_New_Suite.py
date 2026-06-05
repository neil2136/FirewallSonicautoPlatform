import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/SSO_Enhancements')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.SSO_Enhancements_cases.Test_SSO_Enhancements_1',
        'testcases.SSO_Enhancements_cases.Test_SSO_Enhancements_2',
        'testcases.SSO_Enhancements_cases.Test_SSO_Enhancements_3',
        'testcases.SSO_Enhancements_cases.Test_SSO_Enhancements_4',
        'testcases.SSO_Enhancements_cases.Test_SSO_Enhancements_5',
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

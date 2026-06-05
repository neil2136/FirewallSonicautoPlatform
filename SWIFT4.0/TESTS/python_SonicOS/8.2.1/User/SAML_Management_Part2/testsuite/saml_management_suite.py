# Author: cyuan
import os
import sys
import unittest

from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_Management_Part2')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.saml_management.Test_Saml_Management_TC01',
        'testcases.saml_management.Test_Saml_Management_TC02',
        'testcases.saml_management.Test_Saml_Management_TC03',
        'testcases.saml_management.Test_Saml_Management_TC04',
        'testcases.saml_management.Test_Saml_Management_TC05',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

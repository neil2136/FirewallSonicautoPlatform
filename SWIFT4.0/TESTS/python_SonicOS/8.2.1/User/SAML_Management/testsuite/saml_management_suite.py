# Author: cyuan
import os
import sys
import unittest

from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_Management')
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
        'testcases.saml_management.Test_Saml_Management_TC06',
        'testcases.saml_management.Test_Saml_Management_TC07',
        'testcases.saml_management.Test_Saml_Management_TC08',
        'testcases.saml_management.Test_Saml_Management_TC09',
        'testcases.saml_management.Test_Saml_Management_TC10',
        'testcases.saml_management.Test_Saml_Management_TC11',
        'testcases.saml_management.Test_Saml_Management_TC12',
        'testcases.saml_management.Test_Saml_Management_TC13',
        'testcases.saml_management.Test_Saml_Management_TC14',
        'testcases.saml_management.Test_Saml_Management_TC15',
        'testcases.saml_management.Test_Saml_Management_TC16',
        'testcases.saml_management.Test_Saml_Management_TC17',
        'testcases.saml_management.Test_Saml_Management_TC18',
        'testcases.saml_management.Test_Saml_Management_TC19',
        'testcases.saml_management.Test_Saml_Management_TC20',
        'testcases.saml_management.Test_Saml_Management_TC21',
        'testcases.saml_management.Test_Saml_Management_TC22',
        'testcases.saml_management.Test_Saml_Management_TC24',
        'testcases.saml_management.Test_Saml_Management_TC25',
        'testcases.saml_management.Test_Saml_Management_TC26',
        'testcases.saml_management.Test_Saml_Management_TC27',
        # 'testcases.saml_management.Test_Saml_Management_TC23',
        'testcases.saml_management.Test_Saml_Management_TC28'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

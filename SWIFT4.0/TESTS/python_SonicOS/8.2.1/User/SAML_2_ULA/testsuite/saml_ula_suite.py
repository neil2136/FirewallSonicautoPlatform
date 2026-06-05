# Author: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_2_ULA')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw.TestConfig_FW',
        'definition.init_config_pc.Test_Config_PC',
        'definition.init_config_fw.Test_PreSettings',
        'testcases.saml_ula.Test_TC27',
        'testcases.saml_ula.Test_TC25',
        'testcases.saml_ula.Test_TC26',
        'testcases.saml_ula.Test_TC01',
        'testcases.saml_ula.Test_TC02',
        'testcases.saml_ula.Test_TC03',
        'testcases.saml_ula.Test_TC04',
        'testcases.saml_ula.Test_TC05',
        'testcases.saml_ula.Test_TC06',
        'testcases.saml_ula.Test_TC07',
        'testcases.saml_ula.Test_TC08',
        'testcases.saml_ula.Test_TC09',
        'testcases.saml_ula.Test_TC10',
        'testcases.saml_ula.Test_TC11',
        'testcases.saml_ula.Test_TC12',
        'testcases.saml_ula.Test_TC13',
        'testcases.saml_ula.Test_TC14',
        'testcases.saml_ula.Test_TC15',
        'testcases.saml_ula.Test_TC16',
        'testcases.saml_ula.Test_TC17',
        'testcases.saml_ula.Test_TC18',
        'testcases.saml_ula.Test_TC19',
        'testcases.saml_ula.Test_TC20',
        'testcases.saml_ula.Test_TC21',
        'testcases.saml_ula.Test_TC22',
        'testcases.saml_ula.Test_TC23',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

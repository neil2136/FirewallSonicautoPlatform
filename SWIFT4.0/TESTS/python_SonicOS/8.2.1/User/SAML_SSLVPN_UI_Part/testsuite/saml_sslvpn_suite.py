# Author: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_SSLVPN_UI_Part')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.saml_sslvpn.Test_TC01',
        'testcases.saml_sslvpn.Test_TC02',
        'testcases.saml_sslvpn.Test_TC03',
        'testcases.saml_sslvpn.Test_TC04',
        'testcases.saml_sslvpn.Test_TC05',
        'testcases.saml_sslvpn.Test_TC06',
        'testcases.saml_sslvpn.Test_TC07',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_for_Terminal_Services')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_for_Terminal_Services/testcases/')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'sso_for_terminal_services.TC01_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC02_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC03_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC04_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC05_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC06_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC07_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC08_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC09_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC10_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC11_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC12_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC13_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC14_SSO_for_Terminal_Services',
        'sso_for_terminal_services.TC15_SSO_for_Terminal_Services'
        ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()


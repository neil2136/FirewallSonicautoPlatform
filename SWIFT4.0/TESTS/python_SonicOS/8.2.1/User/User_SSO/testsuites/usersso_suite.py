import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/User_SSO')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/User_SSO/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',

        'usersso.TC01_PUT_SSO_User_Settings',
        'usersso.TC02_POST_SSO_User_Agent',
        'usersso.TC03_PUT_SSO_User_Agent',
        'usersso.TC04_POST_SSO_User_Terminal_Service_Agent',
        'usersso.TC05_PUT_SSO_User_Terminal_Service_Agent',
        'usersso.TC06_POST_SSO_User_Radius_Accounting_Client',
        'usersso.TC07_PUT_SSO_User_Radius_Accounting_Client',
        'usersso.TC08_PUT_Non_Existing_SSO_User_Agent'

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    to_users = 'sbkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()


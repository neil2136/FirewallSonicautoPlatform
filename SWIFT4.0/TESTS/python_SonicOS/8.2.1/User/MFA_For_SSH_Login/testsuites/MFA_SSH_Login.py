import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/MFA_For_SSH_Login/')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'definition.setup_mail_server',
        'testcases.MFA_SSH_Login.sslvpn_config',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_1',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_2',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_3',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_4',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_5',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_6',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_7',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_8',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_9',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_10',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_11',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_12',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_13',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_14',
        'testcases.MFA_SSH_Login.MFA_SSH_Login_15'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    # to_users='rvijayaragavan@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()
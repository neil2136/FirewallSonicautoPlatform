import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/Encryption_Username_and_Password')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/Encryption_Username_and_Password/definition')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/Encryption_Username_and_Password/testcases')



def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_fw.TestConfigTB',

        'encrypt_username_password_3.TC_01_For_Sonicpoint_Administrator_Sensitive_Keys_Excluded',
        'encrypt_username_password_3.TC_02_For_Sonicpoint_Administrator_Sensitive_Keys_Included',
        'encrypt_username_password_3.TC_03_L3_SSLVPN_UserName_Sensitive_Keys_Excluded',
        'encrypt_username_password_3.TC_04_L3_SSLVPN_UserName_Included_And_Sensitive_Keys_Excluded',
        'encrypt_username_password_3.TC_05_L3_SSLVPN_UserName_Excluded_And_Sensitive_Keys_Included',
        'encrypt_username_password_3.TC_06_L3_SSLVPN_UserName_Sensitive_Keys_Included',
        'encrypt_username_password_3.TC_07_L2TP_Server_UserName_Sensitive_Keys_Excluded',
        'encrypt_username_password_3.TC_08_L2TP_Server_UserName_Included_And_Sensitive_Keys_Excluded',
        'encrypt_username_password_3.TC_09_L2TP_Server_UserName_Sensitive_Keys_Included',
        'encrypt_username_password_3.TC_10_PPTP_Server_UserName_Sensitive_Keys_Excluded',
        'encrypt_username_password_3.TC_11_PPTP_Server_UserName_Included_And_Sensitive_Keys_Excluded',
        'encrypt_username_password_3.TC_12_PPTP_SSLVPN_UserName_Excluded_And_Sensitive_Keys_Included',
        'encrypt_username_password_3.TC_13_PPTP_Server_UserName_Sensitive_Keys_Included'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

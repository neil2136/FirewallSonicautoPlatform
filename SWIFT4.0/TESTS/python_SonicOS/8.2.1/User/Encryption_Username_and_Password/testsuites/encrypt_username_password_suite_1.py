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
        'encrypt_username_password_1.nontc_config',

        'encrypt_username_password_1.Check_Encrypt_Local_Username_Present_TSR',
        'encrypt_username_password_1.Check_Unencrypt_Local_Username_Present_TSR',
        'encrypt_username_password_1.Check_FTP_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_FTP_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_FTP_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_FTP_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_Encrypt_Guest_Username_Present_TSR',
        'encrypt_username_password_1.Check_Unencrypt_Guest_Username_Present_TSR',
        'encrypt_username_password_1.Check_SMTP_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_SMTP_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_SMTP_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_PPPoE_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_PPPoE_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_PPPoE_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_PPPoE_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_DDNS_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_DDNS_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_DDNS_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_1.Check_DDNS_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

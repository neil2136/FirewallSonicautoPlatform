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
        'encrypt_username_password_2.nontc_config',

        'encrypt_username_password_2.Check_GMSserver_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_2.Check_GMSserver_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_2.Check_GMSserver_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_2.Check_GMSserver_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_2.Check_Encrypt_External_Guest_Auth_Shared_Secret_Present_TSR',
        'encrypt_username_password_2.Check_Unencrypt_External_Guest_Auth_Shared_Secret_Present_TSR',
        'encrypt_username_password_2.Check_Dynamic_External_Objects_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_2.Check_Dynamic_External_Objects_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_2.Check_Dynamic_External_Objects_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_2.Check_Dynamic_External_Objects_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR',
        'encrypt_username_password_2.Check_Encrypt_NTP_Password_Present_TSR',
        'encrypt_username_password_2.Check_Unencrypt_NTP_Password_Present_TSR',
        'encrypt_username_password_2.Check_Encrypt_RIP_Password_Present_TSR',
        'encrypt_username_password_2.Check_Unencrypt_RIP_Password_Present_TSR',
        'encrypt_username_password_2.Check_Encrypt_OSPF_Password_Present_TSR',
        'encrypt_username_password_2.Check_Unencrypt_OSPF_Password_Present_TSR',
        'encrypt_username_password_2.Check_Encrypt_VPN_Tunnel_Not_Present_TSR',
        'encrypt_username_password_2.Check_Unencrypt_VPN_Tunnel_Present_TSR',
        'encrypt_username_password_2.Check_EXP_Contains_Encrypted_Username_Password',
        'encrypt_username_password_2.Import_EXP_Supported_Firmware_Displays_Previous_Config'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

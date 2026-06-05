# This suite is not supported for nsv branches, hence removed the support from Sonicauto for nsv branches

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
        'encrypt_username_password_5.nontc_config',

        'encrypt_username_password_5.Check_Encrypt_WLAN_RADIUS_Client_Password_Present_TSR',
        'encrypt_username_password_5.Check_Unencrypt_WLAN_RADIUS_Client_Password_Present_TSR',
        'encrypt_username_password_5.Check_Encrypt_WLAN_LDAP_Password_Present_TSR'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

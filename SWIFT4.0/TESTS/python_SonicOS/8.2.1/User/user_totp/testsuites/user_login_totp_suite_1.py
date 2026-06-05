
import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/testcases')


def suite():
    testcases_list = [
        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw_totp.TestConfigTB',
        'user_totp_feature_test_1.sslvpn_config',
        'user_totp_feature_test_1.Totp_01',                
        'user_totp_feature_test_1.Totp_02',
        'user_totp_feature_test_1.Totp_03',
        'user_totp_feature_test_1.Totp_04',
        'user_totp_feature_test_1.Totp_05',
        'user_totp_feature_test_1.Totp_06',
        'user_totp_feature_test_1.Totp_07',
        'user_totp_feature_test_1.Totp_08',
        'user_totp_feature_test_1.Totp_09',
        'user_totp_feature_test_1.Totp_10',
        'user_totp_feature_test_1.Totp_11',
        'user_totp_feature_test_1.Totp_12',
        'user_totp_feature_test_1.Totp_13',
        'user_totp_feature_test_1.Totp_14',
        'user_totp_feature_test_1.Totp_15',
        'user_totp_feature_test_1.Totp_16',
        'user_totp_feature_test_1.Totp_17',
        'user_totp_feature_test_1.Totp_18',
        'user_totp_feature_test_1.Totp_19',
        'user_totp_feature_test_1.Totp_20',
        'user_totp_feature_test_1.Totp_21',

        
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites   


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

   

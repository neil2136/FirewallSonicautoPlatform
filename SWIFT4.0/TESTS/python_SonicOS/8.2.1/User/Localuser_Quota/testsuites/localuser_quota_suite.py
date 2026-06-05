import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Localuser_Quota/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Localuser_Quota/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'localuser_quota.Local_UserConfig',
        'localuser_quota.TC01_verify_Quota_configuration_for_localusers',
        'localuser_quota.TC08_verify_Quota_setting_of_sessionLifetime',
        'localuser_quota.TC20_verify_maximum_value_receive_limit',
        'localuser_quota.TC21_verify_minimum_value_receive_limit',
        'localuser_quota.TC22_verify_maximum_value_transmit_limit',
        'localuser_quota.TC23_verify_minimum_value_transmit_limit',
        'localuser_quota.TC24_verify_minimum_value_for_sessionLifetime',
        'localuser_quota.TC25_verify_maximum_value_Sessionlifetime',
        'localuser_quota.TC26_verify_invalid_value_for_receiveLimit',
        'localuser_quota.TC27_verify_invalid_value_for_transmitLimit',
        'localuser_quota.TC28_verify_invalid_value_for_sessionLifetime',
        'localuser_quota.TC37_Check_LocalUser_config_in_TSR',
        'localuser_quota.TC_delete_Localuser',
     

        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ujkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()


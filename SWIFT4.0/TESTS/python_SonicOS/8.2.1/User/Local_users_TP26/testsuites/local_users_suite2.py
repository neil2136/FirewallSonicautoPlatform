import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Local_users_TP26/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Local_users_TP26/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
         'config.init_testbed.TestRestoreDUT',
         'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
	    'localusers.Local_UserConfig',
         'localusers.TC37_AccountLifetime_BoundaryCheck',
         'localusers.TC38_AccountLifetime_NegativeCheck',
         'localusers.TC41_Check_Account_lifetime_of_different_groups',
         'localusers.TC42_Check_RemainingTime',
         'localusers.TC43_Edit_RemainingLifetime',
         'localusers.TC48_Check_LocalUser_config_in_TSR',
         'localusers.TC49_Check_LocalUser_logs',
         'localusers.TC39_Login_with_expired_not_pruned_user',
         'localusers.TC40_Login_with_expired_and_pruned_user',
         'localusers.TC51_Check_PrunedAndExpired_user_removed',
        #'localusers.TC52_Restart_firewall_and_check_remaining_time'
         'localusers.TC45_delete_Localuser'







        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ftahreen@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()


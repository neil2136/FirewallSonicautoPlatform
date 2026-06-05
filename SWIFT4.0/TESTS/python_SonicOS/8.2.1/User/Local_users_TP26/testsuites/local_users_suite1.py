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
         'localusers.TC27_Disable_prune_expired_user_Accounts',
         'localusers.TC26_Enable_prune_expired_user_Accounts',
         'localusers.TC28_Enable_Apply_Password_constraints',
         'localusers.TC29_Disable_Apply_Password_constraints',
         'localusers.TC30_AccountLifetime_never_expires',
         'localusers.TC31_AccountLifetime_byMinutes_pruneAccountUnchecked',
         'localusers.TC32_AccountLifetime_byMinutes_pruneAccountChecked',
         'localusers.TC33_AccountLifetime_byHours_pruneAccountUnChecked',
         'localusers.TC34_AccountLifetime_byHours_pruneAccountChecked',
         'localusers.TC35_AccountLifetime_byDays_pruneAccountUnChecked',
         'localusers.TC36_AccountLifetime_byDays_pruneAccountChecked',
         'localusers.TC45_delete_Localuser'



        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ftahreen@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()


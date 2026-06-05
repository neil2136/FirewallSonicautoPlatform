import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Cyclic_Quota_For_Guest_User_Group/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Cyclic_Quota_For_Guest_User_Group/testcases')




def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
         'cyclic_quota_guest_user_group_UI.TC001_Cyclic_quota',
         'cyclic_quota_guest_user_group_UI.TC002_Cyclic_quota',
         'cyclic_quota_guest_user_group_UI.TC003_Cyclic_quota',
         'cyclic_quota_guest_user_group_UI.TC004_Cyclic_quota',
          'cyclic_quota_guest_user_group_UI.TC005_Cyclic_quota',
          'cyclic_quota_guest_user_group_UI.TC006_Cyclic_quota',
        'cyclic_quota_guest_user_group_UI.TC007_Cyclic_quota',
        'cyclic_quota_guest_user_group_UI.TC008_Cyclic_quota',
        'cyclic_quota_guest_user_group_UI.TC009_Cyclic_quota',

    ]




    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'sthaticherla@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()



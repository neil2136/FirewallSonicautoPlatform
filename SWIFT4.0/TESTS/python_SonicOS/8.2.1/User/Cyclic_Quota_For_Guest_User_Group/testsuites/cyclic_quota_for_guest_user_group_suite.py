import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Cyclic_Quota_For_Guest_User_Group/testcases')




def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestInitConfig',
        'cyclic_quota_for_guest_user_group.NonTC_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC001_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC002_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC003_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC004_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC005_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC006_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC007_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC008_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC009_GuestUsers',
        #'cyclic_quota_for_guest_user_group.TC010_GuestUsers',   #time modification is not supported
        'cyclic_quota_for_guest_user_group.TC011_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC012_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC013_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC014_GuestUsers',
        'cyclic_quota_for_guest_user_group.TC015_GuestUsers'

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'sthaticherla@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()



import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Cyclic_Quota_For_Local_User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Cyclic_Quota_For_Local_User/testcases')




def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_env.TestInitConfig',
        'cyclic_quota_for_local_user.TC001_LocalUsers',
        'cyclic_quota_for_local_user.TC002_LocalUsers',
        'cyclic_quota_for_local_user.TC003_LocalUsers',
        'cyclic_quota_for_local_user.TC004_LocalUsers',
        'cyclic_quota_for_local_user.TC005_LocalUsers',
        'cyclic_quota_for_local_user.TC006_LocalUsers',
        'cyclic_quota_for_local_user.TC007_LocalUsers',
        'cyclic_quota_for_local_user.TC008_LocalUsers',
        'cyclic_quota_for_local_user.TC009_LocalUsers',
        'cyclic_quota_for_local_user.TC010_LocalUsers',
        'cyclic_quota_for_local_user.TC011_LocalUsers',
        'cyclic_quota_for_local_user.TC012_LocalUsers',
        'cyclic_quota_for_local_user.TC013_LocalUsers',
        'cyclic_quota_for_local_user.TC014_LocalUsers'

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    to_users = 'sthaticherla@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()



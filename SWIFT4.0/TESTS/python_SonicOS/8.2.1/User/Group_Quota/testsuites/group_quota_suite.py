import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Group_Quota/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Group_Quota/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'group_quota.TC01_default_group_quota',
        'group_quota.TC02_delete_group_quota',
        'group_quota.TC03_edit_group_quota',
        'group_quota.TC08_custom_quota',
        'group_quota.TC26_check_user_status',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'janania@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()


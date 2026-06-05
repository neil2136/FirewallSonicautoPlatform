import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Radius_Users_api/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Radius_Users_api')


def suite():
  testcases_list = [
    'config.init_testbed.TestRestoreDUT',
    'config.init_testbed.TestUploadFirmware',
    'definition.conf_fw.TestConfigTB',
    'Radius_user_api.TC001_Radius_users',
    'Radius_user_api.TC002_Radius_users',
    'Radius_user_api.TC003_Radius_users',
    'Radius_user_api.TC004_Radius_users',
    'Radius_user_api.TC005_Radius_users',
    'Radius_user_api.TC006_Radius_users',
    'Radius_user_api.TC007_Radius_users',
    'Radius_user_api.TC008_Radius_users',
    'Radius_user_api.TC009_Radius_users',
    'Radius_user_api.TC010_Radius_users',
    'Radius_user_api.TC011_Radius_users',
    'Radius_user_api.TC012_Radius_users',
    'Radius_user_api.TC013_Radius_users',
    'Radius_user_api.TC014_Radius_users'

    
  ]

  suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
  return suites


if __name__ == '__main__':
    to_users = 'sjogalekar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()




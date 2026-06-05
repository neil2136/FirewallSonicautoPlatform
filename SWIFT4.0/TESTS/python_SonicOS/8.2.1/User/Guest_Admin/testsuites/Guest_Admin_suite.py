import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin')


def suite():
  testcases_list = [
    'config.init_testbed.TestRestoreDUT',
    'config.init_testbed.TestUploadFirmware',
    'definition.conf_fw.TestConfigTB',
    'Guest_admin.Guest_admin_01',
    'Guest_admin.Guest_admin_02',
    'Guest_admin.Guest_admin_03',
    'Guest_admin.Guest_admin_04',
    'Guest_admin.Guest_admin_05',
    'Guest_admin.Guest_admin_06',
    'Guest_admin.Guest_admin_07',
    'Guest_admin.Guest_admin_09',
    'Guest_admin.Guest_admin_10',
    'Guest_admin.Guest_admin_12',
    'Guest_admin.Guest_admin_13',
    'Guest_admin.Guest_admin_11',
    'Guest_admin.Guest_admin_08'
   
    
    

    
  ]

  suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
  return suites


if __name__ == '__main__':
    to_users = 'sjogalekar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()




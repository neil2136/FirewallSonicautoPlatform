import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Force_password_change_on_First_Login/testcases')
sys.path.append(os.environ['PYTHON_SONICOS_HOME']+ '/User/Force_password_change_on_First_Login')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login/lib')

def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',
      'force_password_change_on_first_login.TC01_Local_User',
      'force_password_change_on_first_login.TC02_Local_User',     
]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'lgn@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()

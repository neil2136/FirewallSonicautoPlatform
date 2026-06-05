import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Force_password_change_on_First_Login_2/testcases')
sys.path.append(os.environ['PYTHON_SONICOS_HOME']+ '/User/Force_password_change_on_First_Login_2')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login_2/lib')

def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',
      'force_password_change_on_first_login.TC00_SSLVPN_config',
      'force_password_change_on_first_login.Admin_NonTC',
      'force_password_change_on_first_login.TC01_Local_User',
      'force_password_change_on_first_login.TC02_Local_User',  
      'force_password_change_on_first_login.TC03_Local_User',     
      'force_password_change_on_first_login.TC04_Local_User',     
      'force_password_change_on_first_login.TC05_Local_User',    
      'force_password_change_on_first_login.TC06_Local_User',     
      'force_password_change_on_first_login.TC07_Local_User',     
      'force_password_change_on_first_login.TC08_Local_User'      
]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Guest_Users_api/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Guest_Users_api')

def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',
      'Guestusers_api2.TC05_GuestUsers',
      'Guestusers_api2.TC09_GuestUsers',
      'Guestusers_api2.TC21_GuestUsers',
      'Guestusers_api2.TC22_GuestUsers', 
      'Guestusers_api2.TC11_GuestUsers',
      'Guestusers_api2.TC12_GuestUsers'   
 
 
]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'sbkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users, cc_users)
    st.run()




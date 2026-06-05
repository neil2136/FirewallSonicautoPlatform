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
      'Guestusers_api.TC01_GuestUsers',
      'Guestusers_api.TC02_GuestUsers',
      'Guestusers_api.TC04_GuestUsers',
      'Guestusers_api.TC06_GuestUsers', 
      'Guestusers_api.TC10_GuestUsers',
      'Guestusers_api.TC17_GuestUsers',    
      'Guestusers_api.TC18_GuestUsers',     
 
]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'sbkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users, cc_users)
    st.run()




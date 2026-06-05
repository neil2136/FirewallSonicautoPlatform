import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/CLDR-Feature/CLDR_Local_User_Password/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/CLDR-Feature/CLDR_Local_User_Password')

def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',
       'localuser_api.NonTC_1',
      'localuser_api.TC001_LocalUsers_Admin',
      'localuser_api.TC002_LocalUsers_SSLVPN',
      'localuser_api.TC003_LocalUsers_NX',
        'localuser_api.NonTC_2',
      'localuser_api.TC004_LocalUsers_Admin_enabled',
      'localuser_api.TC005_LocalUsers_SSLVPN_enabled',
      'localuser_api.TC006_LocalUsers_NX_enabled',
      'localuser_api.TC007_LocalUser_Admin_CL',


]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

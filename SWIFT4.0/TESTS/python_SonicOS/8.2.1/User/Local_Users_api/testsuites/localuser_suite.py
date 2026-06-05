import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Local_Users_api/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Local_Users_api')

def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',
      'localuser_api.TC001_LocalUsers',
      'localuser_api.TC004_LocalUsers',
      'localuser_api.TC005_LocalUsers',
      'localuser_api.TC011_LocalUsers',
      'localuser_api.TC012_LocalUsers',
      'localuser_api.TC013_LocalUsers',
      'localuser_api.TC017_LocalUsers',
      'localuser_api.TC018_LocalUsers',
      'localuser_api.TC019_LocalUsers',
      'localuser_api.TC020_LocalUsers',
      'localuser_api.TC022_LocalUsers',
      'localuser_api.TC024_LocalUsers',
      'localuser_api.TC026_LocalUsers',
      'localuser_api.TC029_LocalUsers',
      'localuser_api.TC030_LocalUsers',
      'localuser_api.TC031_LocalUsers', 
      'localuser_api.TC032_LocalUsers',          
      'localuser_api.TC015_LocalUsers',
      'localuser_api.TC016_LocalUsers',
      'localuser_api.TC034_LocalUsers',
      'localuser_api.TC033_LocalUsers',
      'localuser_api.TC02_LocalUsers',
      'localuser_api.TC05_LocalUsers',
      'localuser_api.TC06_LocalUsers',
      'localuser_api.TC07_LocalUsers',
      'localuser_api.TC08_LocalUsers',
      'localuser_api.TC20_LocalUsers',
      'localuser_api.TC22_LocalUsers',
      'localuser_api.TC13_LocalUsers',
      'localuser_api.TC26_LocalUsers',
      'localuser_api.TC27_LocalUsers',
      'localuser_api.TC09_LocalUsers',
      'localuser_api.TC24_LocalUsers'

      

]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

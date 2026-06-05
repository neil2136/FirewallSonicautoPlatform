import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/CLDR-Feature/Quick_Smoke/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/CLDR-Feature/Quick_Smoke')

def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',
      'localuser_api.TC01_disable_CLDR',
      'localuser_api.TC02_enable_CLDR',

]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

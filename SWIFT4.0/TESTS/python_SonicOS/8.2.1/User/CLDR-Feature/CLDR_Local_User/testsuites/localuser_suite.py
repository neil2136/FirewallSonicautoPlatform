import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/CLDR-Feature/CLDR_Local_User/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/CLDR-Feature/CLDR_Local_User')

def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',
       'localuser_api.sslvpn_config',
       'localuser_api.NonTC_1',
      'localuser_api.TC001_LocalUsers',
      'localuser_api.TC002_LocalUsers',
      'localuser_api.TC003_LocalUsers',
      'localuser_api.TC004_LocalUsers',
      'localuser_api.TC005_LocalUsers',
        'localuser_api.NonTC_2',
      'localuser_api.TC006_LocalUsers',
      'localuser_api.TC007_LocalUsers',
      'localuser_api.TC008_LocalUsers',
      'localuser_api.TC009_LocalUsers',
      'localuser_api.TC010_LocalUsers',
        'localuser_api.NonTC_3',
      'localuser_api.TC011_LocalUsers',
      'localuser_api.TC012_LocalUsers',
      'localuser_api.TC013_LocalUsers',
      'localuser_api.TC014_LocalUsers',
      'localuser_api.TC015_LocalUsers',
        'localuser_api.NonTC_4',
      'localuser_api.TC016_LocalUsers',
      'localuser_api.TC017_LocalUsers',
      'localuser_api.TC018_LocalUsers',
      'localuser_api.TC019_LocalUsers',
      'localuser_api.TC020_LocalUsers',


]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

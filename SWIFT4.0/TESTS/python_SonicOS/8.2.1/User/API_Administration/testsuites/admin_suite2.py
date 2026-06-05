import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/API_Administration/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/API_Administration')

def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',

      'api_admin.Admin_102',
      'api_admin.Admin_103',
      'api_admin.Admin_104',
      'api_admin.Admin_105',
      'api_admin.Admin_106',
      'api_admin.Admin_107',
      'api_admin.Admin_108',
      'api_admin.Admin_109',
      'api_admin.Admin_110',
      'api_admin.Admin_111',
      'api_admin.Admin_112',
      'api_admin.Admin_113',
      'api_admin.Admin_114',
      'api_admin.Admin_115',
      'api_admin.Admin_116',
      'api_admin.Admin_117',
      'api_admin.Admin_118',
      'api_admin.Admin_119',
      'api_admin.Admin_120',
      'api_admin.Admin_121',
      'api_admin.Admin_123',
      'api_admin.Admin_124',
      'api_admin.Admin_125',
      'api_admin.Admin_126',
      'api_admin.Admin_127',
      'api_admin.Admin_129',
      'api_admin.Admin_130',
      'api_admin.Admin_131',
      'api_admin.Admin_132',
      'api_admin.Admin_133',
      'api_admin.Admin_136',
      'api_admin.Admin_137',
      'config.init_testbed.TestRestoreDUT',
    ]

    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
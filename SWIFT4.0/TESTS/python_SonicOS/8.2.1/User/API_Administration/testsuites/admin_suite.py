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

      'api_admin.Configure_WAN_AND_LAN',
      'api_admin.Admin_001',
      # 'api_admin.Admin_097', #not supported
      'api_admin.Admin_05',
      'api_admin.Admin_07',
      'api_admin.Admin_027',
      'api_admin.Admin_034',
      'api_admin.Admin_049',
      'api_admin.Admin_055',
      'api_admin.Admin_059',
      # 'api_admin.Admin_073', #not supported
      'api_admin.Admin_089',
      'api_admin.Admin_135',
      'api_admin.Admin_138',
      'api_admin.Admin_134',

      'api_admin.Admin_002',
      'api_admin.Admin_003',
      'api_admin.Admin_004',
      'api_admin.Admin_006',
      'api_admin.Admin_008',
      'api_admin.Admin_009',
      'api_admin.Admin_010',
      'api_admin.Configure_WAN_AND_LAN',
      'api_admin.Admin_011',
      'api_admin.Configure_WAN_AND_LAN',
      'api_admin.Admin_012',
      'api_admin.Configure_WAN_AND_LAN',
      'api_admin.Admin_013',
      'api_admin.Admin_014',
      'api_admin.Configure_WAN_AND_LAN',
      'api_admin.Admin_015',
      'api_admin.Configure_WAN_AND_LAN',
      'api_admin.Admin_017',
      'api_admin.Admin_024',
      'api_admin.Admin_025',
      'api_admin.Admin_026',
      'api_admin.Admin_028',
      'api_admin.Admin_029',
      'api_admin.Admin_030',
      'api_admin.Admin_031',
      'api_admin.Admin_032',
      'api_admin.Admin_033',
      'api_admin.Admin_036',
      'api_admin.Admin_037',
      'api_admin.Admin_048',
      'api_admin.Admin_050',
      'api_admin.Admin_051',
      'api_admin.Admin_052',
      'api_admin.Admin_053',
      'api_admin.Admin_054',
      'api_admin.Admin_056',
      'api_admin.Admin_057',
      'api_admin.Admin_058',
      'api_admin.Admin_060',
      'api_admin.Admin_061',
      'api_admin.Admin_062',
      'api_admin.Admin_063',
      'api_admin.Admin_064',
      'api_admin.Admin_065',
      'api_admin.Admin_066',
      'api_admin.Admin_067',
      
      'api_admin.Admin_068',
      'api_admin.Admin_069',
      'api_admin.Admin_070',
      'api_admin.Admin_071',
      # 'api_admin.Admin_072', #not supported
      'api_admin.Admin_074',
      'api_admin.Configure_WAN_AND_LAN',
      'api_admin.Admin_075',
      'api_admin.Admin_076',
      'api_admin.Admin_077',
      'api_admin.Admin_078',
      'api_admin.Admin_079',
      'api_admin.Admin_080',
      'api_admin.Admin_081',
      'api_admin.Admin_082',
      'api_admin.Admin_083',

      'api_admin.Admin_084',
      'api_admin.Admin_085',
      'api_admin.Admin_086',
      'api_admin.Admin_087',
      'api_admin.Admin_088',
      'api_admin.Admin_090',
      'api_admin.Admin_091',
      'api_admin.Admin_092',
      'api_admin.Admin_093',
      'api_admin.Admin_094',
      'api_admin.Admin_095',
      'api_admin.Admin_096',
      'api_admin.Admin_098',
      'api_admin.Admin_099',
      'api_admin.Admin_100',
      'config.init_testbed.TestRestoreDUT'

    ]

    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
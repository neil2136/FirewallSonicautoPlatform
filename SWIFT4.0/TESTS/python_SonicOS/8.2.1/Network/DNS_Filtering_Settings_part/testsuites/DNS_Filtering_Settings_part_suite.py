# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Settings_part')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC.test_01_config_PC1_route',
        'definition.init_fw_configure.TestConfigFW',
        'definition.init_pc_configure.TestConfigPC.test_02_check_dns_server',
        'testcases.DNS_Filtering_Settings_part.TestError_1521003',
        'testcases.DNS_Filtering_Settings_part.TestFunc_1521018',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521004',
        'testcases.DNS_Filtering_Settings_part.TestError_1521005',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521006',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521009',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521007',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521010',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521011',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521012',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521014',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521013',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521039',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521040',
        'testcases.DNS_Filtering_Settings_part.TestError_1521041',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521044',
        'testcases.DNS_Filtering_Settings_part.TestError_1521046',
        'testcases.DNS_Filtering_Settings_part.TestSettings_1521047',
        'testcases.DNS_Filtering_Settings_part.TestFunc_1521179',
        'testcases.DNS_Filtering_Settings_part.TestFunc_1521180',
        'testcases.DNS_Filtering_Settings_part.TestFunc_1521181'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

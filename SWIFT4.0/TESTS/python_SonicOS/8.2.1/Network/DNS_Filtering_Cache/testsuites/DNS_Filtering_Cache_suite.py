# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Cache')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC.test_01_config_PC1_route',
        'definition.init_fw_configure.TestConfigFW',
        'definition.init_pc_configure.TestConfigPC.test_02_check_dns_server',
        'testcases.DNS_Filtering_Cache.TestCombine_Cache',
        'testcases.DNS_Filtering_Cache.TestSettings_1520984',
        'testcases.DNS_Filtering_Cache.TestSettings_1520985',
        'testcases.DNS_Filtering_Cache.TestSettings_1520986',
        'testcases.DNS_Filtering_Cache.TestSettings_1520987',
        'testcases.DNS_Filtering_Cache.TestSettings_1520988',
        'testcases.DNS_Filtering_Cache.TestSettings_1520989',
        'testcases.DNS_Filtering_Cache.TestSettings_1520990',
        'testcases.DNS_Filtering_Cache.TestSettings_1520991',
        'testcases.DNS_Filtering_Cache.TestSettings_1520992',
        'testcases.DNS_Filtering_Cache.TestSettings_1520993',
        'testcases.DNS_Filtering_Cache.TestSettings_1520994',
        'testcases.DNS_Filtering_Cache.TestSettings_1520995',
        'testcases.DNS_Filtering_Cache.TestSettings_1520996',
        'testcases.DNS_Filtering_Cache.TestSettings_1520997',
        'testcases.DNS_Filtering_Cache.TestSettings_1520998',
        'testcases.DNS_Filtering_Cache.TestSettings_1520999',
        'testcases.DNS_Filtering_Cache.TestSettings_1521000',
        'testcases.DNS_Filtering_Cache.TestSettings_2045123'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

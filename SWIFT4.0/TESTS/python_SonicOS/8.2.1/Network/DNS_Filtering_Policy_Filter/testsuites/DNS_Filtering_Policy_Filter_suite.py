# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Policy_Filter')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC',
        'definition.init_fw_configure.TestConfigFW',
        'testcases.DNS_Filtering_Policy_Filter.TestCheck_and_change_dns_server',
        'testcases.DNS_Filtering_Policy_Filter.TestSettings_01',
        'testcases.DNS_Filtering_Policy_Filter.TestSettings_02',
        'testcases.DNS_Filtering_Policy_Filter.TestSettings_03',
        'testcases.DNS_Filtering_Policy_Filter.TestBaseFun_04',
        'testcases.DNS_Filtering_Policy_Filter.TestSettings_11',
        'testcases.DNS_Filtering_Policy_Filter.TestSettings_12',
        'testcases.DNS_Filtering_Policy_Filter.TestSettings_13'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

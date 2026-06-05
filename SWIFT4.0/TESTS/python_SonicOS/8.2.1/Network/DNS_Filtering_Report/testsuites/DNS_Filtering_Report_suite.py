# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Report')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC',
        'definition.init_fw_configure.TestConfigFW',
        'definition.init_pc_configure.TestTraffic',
        'testcases.DNS_Filtering_Report.TestSettings_1521169',
        'testcases.DNS_Filtering_Report.TestSettings_1521170',
        'testcases.DNS_Filtering_Report.TestReboot_1521172'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

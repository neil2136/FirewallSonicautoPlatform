# __author__:cyuan

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] +
                '/Network/DMZ_on_NAT_TP124')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.dmz_on_nat.TestDMZNAT_TC34',
        'testcases.dmz_on_nat.TestDMZNAT_TC35',
        'testcases.dmz_on_nat.TestDMZNAT_TC37',
        'testcases.dmz_on_nat.TestDMZNAT_TC40',
        'testcases.dmz_on_nat.TestDMZNAT_TC41',
        'testcases.dmz_on_nat.TestDMZNAT_TC44',
        'testcases.dmz_on_nat.TestDMZNAT_TC47',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

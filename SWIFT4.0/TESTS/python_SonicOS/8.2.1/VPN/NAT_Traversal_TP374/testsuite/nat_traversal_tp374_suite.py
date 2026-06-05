# __author__: cyuan


import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/VPN/NAT_Traversal_TP374')


def suite():
    testcase_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC11",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC17",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC23",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC12",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC18",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC2",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC3",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC15",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC37",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC39",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC42",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC43",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC47",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC49",
        "testcases.nat_traversal_tp374.TestNAT_Traversal_TC52",

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcase_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Advanced_Routing_TP294_With_3_DUTs')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',   
        'definition.init_conf_fw',
        'config.init_testbed.TestUploadFirmware',   
        'testcases.AdvanceRoutingSmokePart2.TestRip_TC78',
        'testcases.AdvanceRoutingSmokePart2.TestRip_TC57',
        'testcases.AdvanceRoutingSmokePart2.TestOspf_TC117',
        'testcases.AdvanceRoutingSmokePart2.TestOspf_TC116',
        'testcases.AdvanceRoutingSmokePart2.TestRip_TC67',
        'testcases.AdvanceRoutingSmokePart2.TestOspf_TC120',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

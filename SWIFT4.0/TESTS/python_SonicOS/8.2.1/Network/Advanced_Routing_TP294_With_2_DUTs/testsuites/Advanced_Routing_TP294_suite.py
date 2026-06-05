# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Advanced_Routing_TP294_With_2_DUTs')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'testcases.AdvanceRoutingSmoke.TestRip_TC61',
        'testcases.AdvanceRoutingSmoke.TestRip_TC81',
        'testcases.AdvanceRoutingSmoke.TestRip_TC82',
        'testcases.AdvanceRoutingSmoke.TestRip_TC85',
        'testcases.AdvanceRoutingSmoke.TestRip_TC63',
        'testcases.AdvanceRoutingSmoke.TestRip_TC59',
        'testcases.AdvanceRoutingSmoke.TestRip_TC76',
        'testcases.AdvanceRoutingSmoke.TestRip_TC46',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC111',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC103',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC143',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC110',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC113',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC114',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC112',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC105',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC104',
        'testcases.AdvanceRoutingSmoke.TestOspf_TC142',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

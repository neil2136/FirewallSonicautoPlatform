# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/IPv6_NDP_TP2485")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUTByUI',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'testcases.ipv6_ndp_tp2485.TestBaseFun_TC1',
        'testcases.ipv6_ndp_tp2485.TestBaseFun_TC9',
        'testcases.ipv6_ndp_tp2485.TestBaseFun_TC11',
        'testcases.ipv6_ndp_tp2485.TestBaseFun_TC13',
        'testcases.ipv6_ndp_tp2485.TestBaseFun_TC16',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()




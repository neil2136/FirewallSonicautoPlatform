# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/IPv6_OSPFv3")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'testcases.ipv6_ospfv3.TestBaseFun_TC1',
        'testcases.ipv6_ospfv3.TestBaseFun_TC11',
        'testcases.ipv6_ospfv3.TestBaseFun_TC12',
        'testcases.ipv6_ospfv3.TestBaseFun_TC46',
        'testcases.ipv6_ospfv3.TestBaseFun_TC13',
        'testcases.ipv6_ospfv3.TestBaseFun_TC14',
        'testcases.ipv6_ospfv3.TestBaseFun_TC143',
        'testcases.ipv6_ospfv3.TestBaseFun_TC33',
        'testcases.ipv6_ospfv3.TestBaseFun_TC16',
        'testcases.ipv6_ospfv3.TestBaseFun_TC23',
        'testcases.ipv6_ospfv3.TestBaseFun_TC36',
        'testcases.ipv6_ospfv3.TestBaseFun_TC37',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

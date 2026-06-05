# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/IPv6_PBR_TP2518")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC1',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC6',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC7',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC8',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC11',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC24',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC25',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC19',
        'testcases.ipv6_pbr_tp2518.TestBaseFun_TC28',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
